# Project Context: Zero Game

This document provides a general overview of the "Zero Game" project, intended to serve as context for the AI agent.

## Project Name

Zero Game

## Purpose

"Zero Game" is a game development project built using Python and the `pygame-community-edition` library. Its primary goal is to create a 2D game.

## Technology Stack

- **Language:** Python 3
- **Game Library:** `pygame-community-edition` (pygame-ce)

## Project Structure Overview

The project follows a structured directory layout to organize game components, resources, and development configurations.

- **`.gemini/`**: Contains configuration and context files for the AI agent.
- **`.git/`**: Git version control repository.
- **`.github/`**: GitHub-related configurations, including Copilot prompts.
- **`.ruff_cache/`**: Cache directory for Ruff linter.
- **`.vscode/`**: Visual Studio Code specific settings and launch configurations.
- **`build/`**: Contains build artifacts.
- **`saves/`**: Directory for game save files.
- **`src/`**: The core source code of the game. This is the main development directory and contains:
  - **`controllers/`**: Logic for managing game flow and interactions (e.g., `game_controller`, `spawn_controller`).
  - **`game/`**: Core game mechanics, including `camera`, `game` loop, `playground`, and `spawner`.
  - **`game/map_system/`**: Contains the `Map` and `MapRenderer` classes for handling polygon-based maps.
  - **`game/game_objects/`**: Definitions for various in-game entities such as `characters`, `equippables` (weapons), `inventory`, `npcs`, and `projectiles`.
  - **`resources/`**: Static assets and configurations like `colors` and `shape_png_factory`.
  - **`states/`**: Manages different game states (e.g., `game_over_state`, `game_state`, `main_menu_state`).
  - **`systems/`**: Handles cross-cutting concerns like `game_data_system`, `load_game_system`, and `save_game_system`.
  - **`ui/`**: User interface components and menus (e.g., `game_over_ui`, `main_menu_ui`, `pause_menu_ui`).
  - Other top-level modules like `main.py` (entry point), `screen.py` (screen management), `singleton.py`, `time_handler.py`, `events_dictionary.py`, and `states_enum.py`.
- **`zero_game_env/`**: Likely a Python virtual environment for the project.

## Key Game Concepts

The game appears to be structured around common game development patterns:

- **Game States:** Managing different phases of the game (menu, gameplay, game over).
- **Controllers:** Separating game logic from presentation.
- **Game Objects:** Hierarchical organization of in-game entities.
- **Systems:** Handling persistent data and cross-cutting concerns.
- **UI:** Dedicated components for user interaction.

This context should help AI agents understand the project's architecture and assist effectively with development tasks.
