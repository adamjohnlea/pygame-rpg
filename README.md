<h1>Simple RPG Game</h1>

<p>A simple RPG game built with Pygame featuring room transitions, quest system, inventory management, and shop interactions.</p>

<h2>Features</h2>
<ul>
    <li>Multiple interconnected rooms (Town, Shop, Dungeon)</li>
    <li>Basic quest system with objectives and rewards</li>
    <li>Inventory management</li>
    <li>Shop system for buying/selling items</li>
    <li>Animated HUD with health and gold display</li>
    <li>Smooth room transitions</li>
</ul>

<h2>Prerequisites</h2>
<ul>
    <li>Python 3.11 or higher</li>
    <li>pip (Python package installer)</li>
</ul>

<h2>Installation</h2>
<ol>
    <li>Clone the repository:
        <pre><code>git clone [your-repository-url]
cd simple-rpg</code></pre>
    </li>
    <li>Create a virtual environment:
        <pre><code>python3 -m venv venv</code></pre>
    </li>
    <li>Activate the virtual environment:
        <pre><code>On macOS/Linux:
source venv/bin/activate</li>
<li><pre><code>
On Windows:
.\venv\Scripts\activate</code></pre>
    </li>
    <li>Install dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
</ol>

<h2>Running the Game</h2>
<ol>
    <li>Ensure your virtual environment is activated</li>
    <li>Run the game:
        <pre><code>python main.py</code></pre>
    </li>
</ol>

<h2>Game Controls</h2>

<h3>Movement</h3>
<table>
    <tr>
        <th>Key</th>
        <th>Action</th>
    </tr>
    <tr>
        <td>W</td>
        <td>Move up</td>
    </tr>
    <tr>
        <td>A</td>
        <td>Move left</td>
    </tr>
    <tr>
        <td>S</td>
        <td>Move down</td>
    </tr>
    <tr>
        <td>D</td>
        <td>Move right</td>
    </tr>
</table>

<h3>Menu and Interface</h3>
<table>
    <tr>
        <th>Key</th>
        <th>Action</th>
    </tr>
    <tr>
        <td>ESC</td>
        <td>Toggle main menu</td>
    </tr>
    <tr>
        <td>I</td>
        <td>Toggle inventory</td>
    </tr>
    <tr>
        <td>Q</td>
        <td>Toggle quest log</td>
    </tr>
    <tr>
        <td>J</td>
        <td>View available quests</td>
    </tr>
    <tr>
        <td>R</td>
        <td>Reset game</td>
    </tr>
</table>

<h3>Interaction</h3>
<table>
    <tr>
        <th>Key</th>
        <th>Action</th>
    </tr>
    <tr>
        <td>E</td>
        <td>Interact with shop (when near shop counter)</td>
    </tr>
    <tr>
        <td>ENTER</td>
        <td>Accept quest (in available quests menu) or Buy item (in shop)</td>
    </tr>
</table>

<h3>Shop Navigation</h3>
<table>
    <tr>
        <th>Key</th>
        <th>Action</th>
    </tr>
    <tr>
        <td>↑</td>
        <td>Select previous item</td>
    </tr>
    <tr>
        <td>↓</td>
        <td>Select next item</td>
    </tr>
    <tr>
        <td>ENTER</td>
        <td>Buy selected item</td>
    </tr>
</table>

<h3>Room Navigation</h3>
<p>Walk to the edges of rooms to transition between:</p>
<ul>
    <li>Town → Shop (right exit)</li>
    <li>Town → Dungeon (left exit)</li>
    <li>Shop → Town (left exit)</li>
    <li>Dungeon → Town (right exit)</li>
</ul>

<h2>Project Structure</h2>
<pre>
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
</pre>

<h2>Development</h2>
<p>The game is currently using simple geometric shapes for visualization during development. Sprite support is planned for future updates.</p>

<h3>Current Features</h3>
<ul>
    <li>Basic movement and collision detection</li>
    <li>Room transition system with spawn points</li>
    <li>Quest system with objectives and rewards</li>
    <li>Animated HUD with health bar and gold counter</li>
    <li>Basic shop interface</li>
    <li>Inventory system</li>
</ul>

<h3>Planned Features</h3>
<ul>
    <li>Custom sprite support</li>
    <li>Combat system implementation</li>
    <li>More quests and items</li>
    <li>Save/Load system</li>
</ul>

<h2>Contributing</h2>
<p>This is a development project. Feel free to fork and experiment!</p>

<h2>License</h2>
<p>This project is open source and available under the MIT License.</p> 