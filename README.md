# Aim Paradigm

Aim Paradigm is a Python/Pygame reflex game where players test their reaction speed and accuracy by clicking timed targets before they disappear.

The name connects the gameplay concept of aiming with the Programming Paradigms course where the project was created. This enhanced version keeps the project simple enough for a class assignment while improving the user interface, gameplay polish, menu flow, scoring system, and replay value.

## Project Overview

The goal of Aim Paradigm is to click glowing targets as quickly and accurately as possible. Each target appears in a random position with a timer ring around it. The player earns points for clicking targets, builds combos for bonus points, and loses lives depending on the selected game mode.

The program opens directly into a **Select Gamemode** screen. After choosing a mode, the player sees a clean vertical setup screen: game title, mode description and rules, a prominent Start Game button, three difficulty buttons, a wide Custom Difficulty button, and a Quit button.

## Features

- Opens with a dedicated Select Gamemode screen
- Clean vertical game setup screen
- Game title shown above the selected mode
- Selected gamemode title, description, and rules
- Larger gamemode/rules panel for readability
- Rules text contained inside its panel
- Dropdown menu to change gamemode
- Three main difficulty presets: Casual, Standard, and Tryhard
- Standard difficulty selected by default
- Large standout Start Game button
- Wide Custom Difficulty button
- Custom Difficulty screen with one setting per row
- Custom lives, target size, target lifetime, and round time
- Reset button for custom difficulty
- Quit confirmation screen
- Resizable window using the normal window borders
- Fullscreen support with F11
- Polished rounded buttons
- Larger readable UI labels with restored descriptions
- Wrapped subtitles and descriptions
- Animated neon-style background
- Hearts for lives
- Timer bar with visual urgency
- Combo system
- Time Attack score penalties for missed clicks and expired targets
- Accuracy tracking
- Best reaction time tracking
- High score saving by mode and difficulty
- Particle effects when targets are clicked
- Bonus targets
- Game-over statistics screen
- Escape key support
- Built with Python and Pygame

## Game Modes

### Classic

Balanced mode with hearts, scoring, combos, and penalties.

### Time Attack

No hearts, but mistakes subtract points. Wrong clicks subtract 75 points, expired targets subtract 50 points, and both break the combo.

### Sudden Death

One heart. One mistake ends the run.

### Zen

Relaxed practice with no punishment for mistakes.

## Difficulty Options

Aim Paradigm includes these main difficulty buttons:

- Casual
- Standard
- Tryhard

It also includes a Custom Difficulty screen where the player can adjust:

- Number of lives
- Target size
- Target lifetime
- Round time

## Technologies Used

- Python
- Pygame Community Edition (`pygame-ce`)

## Repository Structure

```text
aim-paradigm/
├── README.md
├── game.py
├── requirements.txt
├── run.bash
└── .gitignore
```

## How to Execute the Game

### 1. Install Python

Make sure Python 3 is installed.

Check your version:

```powershell
py --version
```

or:

```powershell
python --version
```

### 2. Open the Project Folder

In PowerShell, go to the project folder:

```powershell
cd C:\Users\remer\OneDrive\github\aim-paradigm
```

### 3. Install the Required Dependency

```powershell
py -m pip install -r requirements.txt
```

If `py` does not work, use:

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the Game

```powershell
py game.py
```

If `py` does not work, use:

```powershell
python game.py
```

On macOS or Linux, use:

```bash
python3 game.py
```

You can also run it with the included Bash script on compatible systems:

```bash
bash run.bash
```

## Controls

- Left mouse click: select menu buttons or click targets
- Escape: go back, quit from mode select, or end the current round during gameplay
- Space: start or retry the game
- F11: toggle fullscreen
- Drag window edges: resize the game window

## Important Dependency Note

This project uses `pygame-ce` because it supports newer Python versions better than some older `pygame` releases.

It is installed as:

```text
pygame-ce
```

but the Python code still imports it normally:

```python
import pygame
```

## What I Learned

This project helped me practice:

- Python program structure
- Pygame setup
- Game loops
- Event handling
- Mouse input
- Collision detection
- Random target generation
- Game state management
- UI design inside a game window
- Score and lives systems
- Timers and countdown logic
- File-based high score saving
- Building a complete interactive project

## Future Improvements

Possible future improvements include:

- Sound effects
- More target types
- Animated menu transitions
- Online leaderboard
- Packaged executable version
- More advanced accuracy analytics
- Custom color themes

## Project Status

This project is complete as an enhanced Programming Paradigms final project and is ready to be uploaded to GitHub as a portfolio project.
