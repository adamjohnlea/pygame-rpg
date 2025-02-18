# Simple RPG Game

A simple RPG game built with Pygame featuring room transitions, quest system, inventory management, and shop interactions.

## Features
- Multiple interconnected rooms (Town, Shop, Dungeon)
- Basic quest system with objectives and rewards
- Inventory management
- Shop system for buying/selling items
- Animated HUD with health and gold display
- Smooth room transitions

## Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

## Installation
1. Clone the repository:
   ```bash
   git clone [your-repository-url]
   cd simple-rpg
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   .\venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
1. Ensure your virtual environment is activated
2. Run the game:
   ```bash
   python main.py
   ```

## Game Controls

### Movement
| Key | Action     |
|-----|------------|
| W   | Move up    |
| A   | Move left  |
| S   | Move down  |
| D   | Move right |

### Menu and Interface
| Key | Action            |
|-----|-------------------|
| ESC | Toggle main menu  |
| I   | Toggle inventory  |
| Q   | Toggle quest log  |
| J   | View quests      |
| R   | Reset game       |
| SPACE| Dismiss messages |

### Interaction
| Key   | Action                                    |
|-------|------------------------------------------|
| E     | Interact with shop (when near counter)    |
| ENTER | Accept quest or buy item                  |

### Shop Navigation
| Key   | Action              |
|-------|-------------------- |
| ↑     | Previous item      |
| ↓     | Next item          |
| ENTER | Buy selected item  |

### Room Navigation
Walk to the edges of rooms to transition between:
- Town → Shop (right exit)
- Town → Dungeon (left exit)
- Shop → Town (left exit)
- Dungeon → Town (right exit)

## Project Structure
```
simple-rpg/
├── assets/           # Game assets directory
├── data/             # Game data files (items, quests, saves)
├── game/             # Game source code
│   ├── combat.py     # Combat system
│   ├── game_state.py # Game state management
│   ├── hud.py        # Heads-up display
│   ├── inventory.py  # Inventory system
│   ├── menu.py       # Menu system
│   ├── player.py     # Player class and controls
│   ├── quest.py      # Quest system
│   ├── room.py       # Room management
│   └── shop.py       # Shop system
├── main.py           # Main game entry point
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Development
The game is currently using simple geometric shapes for visualization during development. Sprite support is planned for future updates.

### Current Features
- Basic movement and collision detection
- Room transition system with spawn points
- Quest system with objectives and rewards
- Animated HUD with health bar and gold counter
- Basic shop interface
- Inventory system

### Planned Features
- Custom sprite support
- Combat system implementation
- More quests and items
- Save/Load system

## Contributing
This is a development project. Feel free to fork and experiment!

## License
This project is open source and available under the MIT License. 