# Aim Paradigm

Aim Paradigm is a Python/Pygame reflex game created as a Programming Paradigms final project. The game challenges players to click timed targets as quickly and accurately as possible while managing score, combos, lives, difficulty settings, and different gameplay rules.

The project started as a simple aim-clicking game and was expanded into a more complete interactive program with a structured menu flow, multiple game modes, custom difficulty options, score penalties, high score saving, and a polished game interface.

## Project Overview

The goal of Aim Paradigm is to click randomly appearing targets before they disappear. Each successful hit increases the player's score and combo. Misses, expired targets, and penalties behave differently depending on the selected game mode.

The program opens with a gamemode selection screen. After choosing a mode, the player can select a difficulty preset, customize the difficulty settings, or start the game. At the end of each round, the game displays performance statistics such as score, hits, misses, accuracy, max combo, and best reaction time.

## Programming Paradigms Concepts Applied

This project applies several programming concepts from a Programming Paradigms course in a visual and interactive way:

* Event-driven programming through keyboard, mouse, window, and game events
* State-based program flow for menus, gameplay, custom settings, confirmation screens, and game-over screens
* Object-oriented design using classes for buttons, targets, particles, and the main game controller
* Procedural decomposition through separate functions for drawing, updating, collision checking, scoring, and UI behavior
* Data-driven configuration using dictionaries for game modes and difficulty settings
* Conditional logic to support different rules for Classic, Time Attack, Sudden Death, and Zen modes
* File-based persistence using JSON to save high scores
* Real-time loops, timers, and frame-based updates through Pygame

## Game Modes

### Classic

Classic mode is the standard version of the game. The player has a limited number of lives, and mistakes reduce those lives. The round ends when the timer reaches zero or the player runs out of hearts.

### Time Attack

Time Attack is focused on scoring under pressure. The player does not have lives, but missed clicks and expired targets subtract points and break the combo.

### Sudden Death

Sudden Death is the most difficult mode. The player only has one life, so one missed click or expired target ends the round.

### Zen

Zen mode is a relaxed practice mode. There are no lives or penalties, allowing the player to focus on improving accuracy and reaction speed.

## Difficulty Options

Aim Paradigm includes three preset difficulty levels:

* Casual
* Standard
* Tryhard

The game also includes a custom difficulty editor where the player can adjust:

* Number of lives
* Target size
* Target lifetime
* Round duration

## Features

* Gamemode selection screen
* Difficulty selection screen
* Custom difficulty editor
* Timed target system
* Score and combo system
* Lives displayed as hearts
* Time Attack point penalties
* Bonus targets
* Game-over statistics screen
* High score saving with JSON
* Resizable game window
* Fullscreen support with F11
* Particle effects when targets are clicked
* Keyboard and mouse controls

## Technologies Used

* Python
* Pygame Community Edition (`pygame-ce`)
* JSON for local high score storage

## How to Run

Open the project folder:

```bash
cd aim-paradigm
```

Install the required dependency:

```bash
py -m pip install -r requirements.txt
```

Run the game:

```bash
py game.py
```

If `py` does not work, use:

```bash
python -m pip install -r requirements.txt
python game.py
```

On macOS or Linux, use:

```bash
python3 game.py
```

## Controls

* Left mouse click: select buttons or click targets
* Escape: go back or end the current round
* Space: start or retry
* F11: toggle fullscreen
* Drag window borders: resize the game window


## Project Status

Aim Paradigm is complete as a Programming Paradigms final project and GitHub portfolio project.
