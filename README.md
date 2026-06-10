# Panic Power Maze

> Working title. The final theme/name may change.
> Alternative names:
>
> - "Watt Now?"
> - "No Outlet"
> - "Low Battery Labyrinth"
> - "Power Panic"
> - "Path of Least Resistance"
>

A grid-based maze game where the player controls a robot trying to reach a charging station before its battery runs out.

The current prototype focuses on the core movement and maze logic: drawing a tile-based level, moving the robot through the maze, blocking movement through walls, and detecting when the robot reaches the charging station.

## Concept

The player controls a small robot navigating a maze-like environment. The goal is to reach a charging station before the robot loses power.

Future versions may include battery drain, battery pickups, multiple levels, hazards, and randomly generated mazes.

## Current Features

* Tile-based maze rendering
* Sprite-based floor, wall, charger, and robot visuals
* Robot movement using keyboard controls
* Wall collision / blocked movement
* Charging station win condition
* Restart after winning
* Scaled maze rendering inside a larger game window
* Basic modular project structure

## Planned Features

* Battery level system
* Battery pickups throughout the maze
* Lose condition when battery reaches zero
* Multiple levels
* Improved sprites and tile artwork
* Sound effects / visual feedback
* Random maze generation
* Optional fullscreen or monitor-sized window mode

## Tech Stack

* Python
* Pygame

## Controls

| Key           | Action                                      |
| ------------- | ------------------------------------------- |
| Arrow Keys    | Move robot                                  |
| W / A / S / D | Move robot                                  |
| R             | Restart after reaching the charging station |
| Esc           | Quit the game                               |

## Project Structure

```text
maze-game/
    main.py
    requirements.txt
    assets/
        robot.png
        charger.png
        ...
    game/
        __init__.py
        settings.py
        level.py
        robot.py
        tile.py
```

## Setup

Clone the repository:

```bash
git clone https://github.com/jasbot01/maze-game.git
cd maze-game
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux/WSL:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Running the Game

From the project root:

```bash
python main.py
```

## Development Notes

The game currently uses a hardcoded tile map while the core mechanics are being built.

Tile IDs are defined in `game/settings.py`, and the current level layout is defined in `game/level.py`.

The robot is represented by a `Robot` sprite, while maze tiles are represented by `Tile` sprites. The level is first rendered to an offscreen surface, then scaled to fit the game window.

## Current Gameplay Loop

```text
Start level
Move robot through maze
Prevent movement through walls
Reach charging station
Show win message
Press R to restart
```

## Roadmap

### Phase 1: Core Prototype

* [x] Draw tile-based maze
* [x] Add robot sprite
* [x] Add tile-by-tile movement
* [x] Block walls
* [x] Add charging station win condition

### Phase 2: Battery Mechanics

* [ ] Add battery level
* [ ] Drain battery when robot moves
* [ ] Add battery display
* [ ] Add battery pickups
* [ ] Add lose condition when battery reaches zero

### Phase 3: Level Expansion

* [ ] Add more hardcoded levels
* [ ] Add level reset
* [ ] Add level progression
* [ ] Add random maze generation

### Phase 4: Polish

* [ ] Improve placeholder sprites
* [ ] Add animations
* [ ] Add sound effects
* [ ] Add title screen
* [ ] Add fullscreen or monitor-sized window option

## Status

This project is currently an early prototype.
