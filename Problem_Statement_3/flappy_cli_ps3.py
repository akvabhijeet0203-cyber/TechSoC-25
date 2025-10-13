#!/usr/bin/env python3
"""
Flappy Bird CLI - Complete Game
Features:
 - Real-time CLI rendering using curses
 - Physics-based bird movement
 - Procedural pipe generation with adaptive difficulty
 - Persistent leaderboard (JSON file) with player names
 - Menu, pause, game over screens, and graceful exit
 - Statistics tracking (games played, average score, best streak)

Run:
  python3 flappy_cli.py

Notes for Windows:
 - If curses is not available, install windows-curses: pip install windows-curses

"""
import curses
import time
import random
import json
import os
import math
import signal
from collections import deque
from datetime import datetime

# -------------------- Configuration --------------------
FPS = 30
FRAME_TIME = 1.0 / FPS
GRAVITY = 30.0           # units per second^2 (rows/s^2)
FLAP_VELOCITY = -9.0     # instantaneous upward velocity (rows/s)
TERMINAL_VELOCITY = 20.0 # max downward speed (rows/s)
PIPE_SPEED_BASE = 10.0   # columns per second, base
PIPE_GAP_BASE = 6        # base gap size in rows
PIPE_SPACING_BASE = 25   # base horizontal spacing (columns)
MIN_SCREEN_WIDTH = 40
MIN_SCREEN_HEIGHT = 20

SCORE_FILE = 'flappy_cli_scores.json'
DEFAULT_PLAYER = 'PLAYER'

# Visuals
BIRD_CHAR = '>'
PIPE_CHAR = '█'
GROUND_CHAR = '_'
BG_CHAR = ' '
TITLE = 'FLAPPY BIRD CLI'

# -------------------- Helper persistence --------------------

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return {'leaderboard': [], 'stats': {'games_played': 0, 'total_score': 0, 'best_streak': 0}}
    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {'leaderboard': [], 'stats': {'games_played': 0, 'total_score': 0, 'best_streak': 0}}


def save_scores(data):
    with open(SCORE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def register_score(player, score):
    data = load_scores()
    lb = data.setdefault('leaderboard', [])
    lb.append({'player': player, 'score': score, 'date': datetime.utcnow().isoformat()})
    # keep only top 20
    lb.sort(key=lambda x: x['score'], reverse=True)
    data['leaderboard'] = lb[:20]
    stats = data.setdefault('stats', {'games_played': 0, 'total_score': 0, 'best_streak': 0})
    stats['games_played'] = stats.get('games_played', 0) + 1
    stats['total_score'] = stats.get('total_score', 0) + score
    # best_streak handled at caller if needed
    save_scores(data)

# -------------------- Game model classes --------------------

class Pipe:
    def __init__(self, x, gap_y, gap_size):
        self.x = x  # column (float for smooth movement)
        self.gap_y = gap_y  # top row of gap
        self.gap_size = gap_size

    def collides(self, bird_row, bird_col):
        # bird is considered at a single cell (bird_row, bird_col)
        bx = int(round(self.x))
        if bx != bird_col:
            return False
        if bird_row < self.gap_y or bird_row >= self.gap_y + self.gap_size:
            return True
        return False


class GameState:
    def __init__(self, scr):
        self.scr = scr
        self.reset()

    def reset(self):
        h, w = self.scr.getmaxyx()
        self.width = max(w - 2, MIN_SCREEN_WIDTH)
        self.height = max(h - 4, MIN_SCREEN_HEIGHT)
        # play field inside border
        self.bird_row = self.height // 2
        self.bird_col = int(self.width * 0.2)
        self.vel = 0.0
        self.pipes = deque()
        self.score = 0
        self.distance_traveled = 0.0
        self.alive = True
        self.paused = False
        self.speed_multiplier = 1.0
        # Difficulty parameters
        self.pipe_speed = PIPE_SPEED_BASE
        self.pipe_gap = PIPE_GAP_BASE
        self.pipe_spacing = PIPE_SPACING_BASE
        self.last_pipe_x = self.width
        self.next_pipe_in = self.pipe_spacing
        self.wind = 0.0
        # procedural RNG seed
        self.rng = random.Random()
        # stats
        self.streak = 0

    def tick_difficulty(self, dt):
        # increase difficulty slowly based on score/distance
        # we will slightly increase speed and decrease gap
        factor = 1.0 + min(self.score / 40.0, 2.0)
        self.speed_multiplier = 1.0 + (self.score / 100.0)
        self.pipe_speed = PIPE_SPEED_BASE * (1.0 + self.score / 60.0)
        self.pipe_gap = max(3, int(PIPE_GAP_BASE - self.score // 10))
        self.pipe_spacing = max(12, int(PIPE_SPACING_BASE - self.score // 6))
        # wind: small random drift that changes slowly
        self.wind += (self.rng.random() - 0.5) * dt * 0.2
        self.wind = max(-1.5, min(1.5, self.wind))

    def update_physics(self, dt):
        # apply gravity
        self.vel += GRAVITY * dt
        # apply terminal velocity
        if self.vel > TERMINAL_VELOCITY:
            self.vel = TERMINAL_VELOCITY
        # wind applies as small vertical force
        self.vel += self.wind * dt
        # update bird position
        self.bird_row += self.vel * dt
        # clamp inside screen (ground check handled elsewhere)

    def flap(self):
        self.vel = FLAP_VELOCITY

    def generate_pipe(self):
        # choose gap_y based on previous to keep fairness
        min_gap_top = 2
        max_gap_top = self.height - self.pipe_gap - 3
        if len(self.pipes) == 0:
            gap_y = self.height // 3
        else:
            last = self.pipes[-1]
            # bias toward previous gap to avoid impossible jumps
            delta = int((random.random() - 0.5) * 8)
            gap_y = max(min_gap_top, min(max_gap_top, last.gap_y + delta))
        x = float(self.width + 10)
        p = Pipe(x=x, gap_y=gap_y, gap_size=self.pipe_gap)
        self.pipes.append(p)

    def step_pipes(self, dt):
        speed = self.pipe_speed * dt
        to_remove = []
        for p in list(self.pipes):
            p.x -= speed
            if int(round(p.x)) + 1 < 0:
                self.pipes.popleft()
                # increase score when pipe passes bird
                self.score += 1
        # manage distance until next pipe
        self.next_pipe_in -= speed
        if self.next_pipe_in <= 0:
            self.generate_pipe()
            self.next_pipe_in = self.pipe_spacing + random.randint(-5, 5)

    def check_collision(self):
        bird_r = int(round(self.bird_row))
        bird_c = self.bird_col
        # ground or ceiling
        if bird_r < 0 or bird_r >= self.height - 1:
            return True
        # pipes
        for p in self.pipes:
            if p.collides(bird_r, bird_c):
                return True
        return False

# -------------------- Rendering --------------------

def draw_border(scr, w, h):
    scr.attron(curses.A_BOLD)
    scr.border()
    scr.attroff(curses.A_BOLD)


def draw_hud(scr, state: GameState):
    # top line: title and score
    scr.addstr(0, 2, f" {TITLE} - Score: {state.score} ")
    # right side high info
    h, w = scr.getmaxyx()
    scr.addstr(0, w - 30, f"Speed: {state.speed_multiplier:.2f} |")


def render(scr, state: GameState):
    scr.erase()
    h, w = scr.getmaxyx()
    field_h = state.height
    field_w = state.width

    # draw border
    draw_border(scr, field_w, field_h)

    # draw HUD
    draw_hud(scr, state)

    # draw pipes
    for p in state.pipes:
        px = int(round(p.x)) + 1  # +1 because of border
        if px < 1 or px > field_w:
            continue
        # top block
        for r in range(1, p.gap_y + 1):
            try:
                scr.addstr(r, px, PIPE_CHAR)
            except curses.error:
                pass
        # bottom block
        for r in range(p.gap_y + p.gap_size + 1, field_h):
            try:
                scr.addstr(r, px, PIPE_CHAR)
            except curses.error:
                pass

    # draw bird
    bird_r = int(round(state.bird_row)) + 1
    bird_c = state.bird_col + 1
    try:
        scr.addstr(bird_r, bird_c, BIRD_CHAR)
    except curses.error:
        pass

    # draw ground line
    for c in range(1, field_w + 1):
        try:
            scr.addstr(field_h, c, GROUND_CHAR)
        except curses.error:
            pass

    # draw controls hint bottom
    h, w = scr.getmaxyx()
    hint = 'Press SPACE to flap | P to pause | Q to quit'
    try:
        scr.addstr(h - 2, 2, hint)
    except curses.error:
        pass

    scr.refresh()

# -------------------- Menu and UI --------------------

def center_text(scr, y, text, attr=0):
    h, w = scr.getmaxyx()
    x = max(0, (w - len(text)) // 2)
    scr.addstr(y, x, text, attr)


def main_menu(scr):
    curses.curs_set(0)
    scr.nodelay(False)
    scr.clear()
    h, w = scr.getmaxyx()
    while True:
        scr.erase()
        center_text(scr, 3, TITLE, curses.A_BOLD)
        center_text(scr, 5, '1) Play')
        center_text(scr, 6, '2) Leaderboard')
        center_text(scr, 7, '3) Stats')
        center_text(scr, 8, '4) Controls')
        center_text(scr, 9, '5) Quit')
        center_text(scr, h - 2, 'Press number to choose')
        scr.refresh()
        ch = scr.getch()
        if ch in (ord('1'), ord(' ')):
            return 'play'
        if ch == ord('2'):
            show_leaderboard(scr)
        if ch == ord('3'):
            show_stats(scr)
        if ch == ord('4'):
            show_controls(scr)
        if ch == ord('5') or ch == ord('q') or ch == ord('Q'):
            return 'quit'


def show_leaderboard(scr):
    scr.nodelay(False)
    scr.clear()
    data = load_scores()
    lb = data.get('leaderboard', [])
    center_text(scr, 1, 'Leaderboard', curses.A_BOLD)
    y = 3
    for i, e in enumerate(lb[:10], 1):
        center_text(scr, y, f"{i}. {e['player']} - {e['score']}")
        y += 1
    center_text(scr, y + 1, 'Press any key to return')
    scr.getch()


def show_stats(scr):
    scr.nodelay(False)
    scr.clear()
    data = load_scores()
    stats = data.get('stats', {})
    games = stats.get('games_played', 0)
    total = stats.get('total_score', 0)
    avg = (total / games) if games else 0
    best_streak = stats.get('best_streak', 0)
    center_text(scr, 2, 'Statistics', curses.A_BOLD)
    center_text(scr, 4, f'Games Played: {games}')
    center_text(scr, 5, f'Average Score: {avg:.2f}')
    center_text(scr, 6, f'Best Streak: {best_streak}')
    center_text(scr, 8, 'Press any key to return')
    scr.getch()


def show_controls(scr):
    scr.nodelay(False)
    scr.clear()
    center_text(scr, 2, 'Controls', curses.A_BOLD)
    center_text(scr, 4, 'SPACE - flap')
    center_text(scr, 5, 'P - pause/unpause')
    center_text(scr, 6, 'Q - quit to menu during play')
    center_text(scr, 8, 'Press any key to return')
    scr.getch()

# -------------------- Game loop --------------------

def play(scr, player_name=DEFAULT_PLAYER):
    curses.curs_set(0)
    scr.nodelay(True)
    state = GameState(scr)
    last_time = time.time()

    # initial pipe
    state.generate_pipe()
    state.next_pipe_in = state.pipe_spacing

    while True:
        now = time.time()
        dt = now - last_time
        if dt < 0:
            dt = 0
        # Cap dt to avoid huge jumps
        dt = min(dt, 0.1)
        last_time = now

        # input handling
        try:
            ch = scr.getch()
        except Exception:
            ch = -1
        if ch != -1:
            if ch in (ord(' '), ord('\n')) and state.alive and not state.paused:
                state.flap()
            elif ch in (ord('p'), ord('P')):
                state.paused = not state.paused
            elif ch in (ord('q'), ord('Q')):
                # quit to menu
                break

        if not state.paused and state.alive:
            # update difficulty
            state.tick_difficulty(dt)
            # physics
            state.update_physics(dt)
            # pipes
            state.step_pipes(dt * state.speed_multiplier)
            # collision
            if state.check_collision():
                state.alive = False

        # render
        render(scr, state)

        if not state.alive:
            endscreen(scr, state, player_name)
            return state.score

        # frame limiter
        time.sleep(max(0, FRAME_TIME - (time.time() - now)))


def endscreen(scr, state: GameState, player_name):
    scr.nodelay(False)
    h, w = scr.getmaxyx()
    scr.clear()
    center_text(scr, 2, 'GAME OVER', curses.A_BOLD)
    center_text(scr, 4, f'Score: {state.score}')
    center_text(scr, 6, 'Press S to save score, R to retry, M for menu')
    scr.refresh()
    ch = scr.getch()
    if ch in (ord('s'), ord('S')):
        register_score(player_name, state.score)
        # update best streak if needed
        data = load_scores()
        stats = data.setdefault('stats', {})
        stats['best_streak'] = max(stats.get('best_streak', 0), state.streak)
        save_scores(data)
        center_text(scr, 8, 'Score saved. Press any key to return to menu')
        scr.getch()
    elif ch in (ord('r'), ord('R')):
        # retry: restart play loop
        return
    else:
        return

# -------------------- Utility: get player name --------------------

def prompt_player_name(scr):
    curses.echo()
    scr.nodelay(False)
    scr.clear()
    center_text(scr, 2, 'Enter your name (max 12 chars):', curses.A_BOLD)
    h, w = scr.getmaxyx()
    scr.addstr(4, max(0, (w - 12) // 2), ' ' * 12)
    scr.move(4, max(0, (w - 12) // 2))
    name = scr.getstr(4, max(0, (w - 12) // 2), 12).decode('utf-8').strip()
    curses.noecho()
    if not name:
        return DEFAULT_PLAYER
    return name[:12]

# -------------------- Signal handling for graceful exit --------------------

EXITED = False

def _signal_handler(sig, frame):
    global EXITED
    EXITED = True

signal.signal(signal.SIGINT, _signal_handler)
signal.signal(signal.SIGTERM, _signal_handler)

# -------------------- Main --------------------

def main(stdscr):
    # initial setup
    curses.use_default_colors()
    player = DEFAULT_PLAYER
    while True:
        choice = main_menu(stdscr)
        if choice == 'play':
            player = prompt_player_name(stdscr)
            score = play(stdscr, player)
            # register score automatically for now
            register_score(player, score)
        elif choice == 'quit' or EXITED:
            break


if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except Exception as e:
        print('An error occurred:', e)
        print('If you are on Windows, consider installing windows-curses (pip install windows-curses)')
