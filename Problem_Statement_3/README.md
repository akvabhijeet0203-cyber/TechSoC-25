# PS3: Flappy Bird CLI - Real-Time Game Development Challenge

## Goal
You're tasked with creating a fully functional Flappy Bird game that runs entirely in the command line interface! This isn't just a simple program - you'll build a real-time game with physics simulation, procedural terrain generation, persistent high scores, and smooth gameplay. This challenge will test your skills in game development, real-time programming, and advanced software architecture.

## What You'll Build
A complete game featuring:
- Real-time CLI graphics with smooth animation
- Physics-based bird movement and collision detection
- Procedurally generated pipe obstacles
- Dynamic difficulty scaling
- Persistent leaderboard system with player names
- Graceful game termination (no Ctrl+C dependency)

## Your Tasks

### Level 1: Core Game Engine & Physics
**The Challenge:** Build the fundamental game engine with real-time rendering and realistic physics simulation.

**Requirements:**
- **Game Loop:** Implement a continuous game loop that runs at consistent frame rate
- **Physics Engine:** Gravity affects the bird, flapping provides upward velocity
- **Real-time Input:** Detect spacebar/enter presses without blocking game execution
- **CLI Rendering:** Draw the game field, bird, and obstacles using ASCII characters
- **Collision Detection:** Accurate detection between bird and pipes/ground

> [!TIP]
> **Think About:**
> How do you handle real-time input in a CLI environment? What makes physics feel realistic vs. artificial?

### Level 2: Procedural Generation & Dynamic Difficulty
**The Challenge:** Create an intelligent system that generates infinite, varied gameplay with progressively increasing challenge.

**The Problem:** Implement:
- **Procedural Pipes:** Randomly generate pipe gaps and heights using mathematical algorithms
- **Adaptive Difficulty:** Gradually increase pipe frequency, reduce gap sizes, or increase speed
- **Terrain Variation:** Create different pipe patterns and obstacle types
- **Score System:** Points based on pipes passed, with bonus multipliers for difficulty

> [!TIP]
> **Think About:
> ** How do you balance randomness with fairness? What makes difficulty progression feel natural rather than frustrating?

### Level 3: Advanced Features & Data Persistence
**The Challenge:** Transform your game into a polished experience with persistent data and advanced gameplay features.

**The Problem:** Implement:
- **Leaderboard System:** Store player names and high scores in local files
- **Game States:** Menu system, pause functionality, game over screens
- **Advanced Physics:** Wind effects, different bird types with unique physics
- **Statistics Tracking:** Games played, average score, best streak
- **Graceful Exit:** Proper game termination without relying on Ctrl+C

> [!TIP]
> **Think About:** 
> How do you design a user experience that feels professional? What data structures best represent persistent game state?


## Sample Game Output:
```
╔══════════════════════════════════════════════════════════════╗
║  FLAPPY BIRD CLI - Score: 15  High: 42  Speed: 1.2x          ║
╠══════════════════════════════════════════════════════════════╣
║                                    ██                        ║
║                                    ██                        ║
║                                    ██                        ║
║                      🐦            ██                        ║
║                                    ██                        ║
║                                                              ║
║                                                              ║
║                                                              ║
║                                    ██                        ║
║                                    ██                        ║
║                                    ██                        ║
║                                    ██                        ║
╚══════════════════════════════════════════════════════════════╝
Press SPACE to flap | P to pause | Q to quit
```



