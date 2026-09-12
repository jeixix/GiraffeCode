# 🦒 GiraffeCode / SavannaCode 🐆

**SavannaCode** (formerly GiraffeCode) is an educational programming game designed to introduce children (ages 5–9) to computational thinking and coding principles through a playful, visual experience.

Players can choose their favorite animal hero—a hungry **Giraffe** or a speedy **Cheetah**—and navigate them across a savanna grid by sequencing directional commands (`FORWARD`, `LEFT`, `RIGHT`) to reach their goal (Acacia Leaves or a Gazelle) while avoiding obstacles like rocks and rivers.

---

## 🌟 Features

- **Choose Your Hero:** Interactive character selection screen. Play as the Giraffe to eat acacia leaves, or play as the Cheetah to catch the gazelle!
- **100 Engaging Levels:** From simple straight paths to complex maze-like puzzles. Level names dynamically adapt depending on the hero you play!
- **Visual Command Queue:** Click buttons to compose code blocks and watch your hero execute the sequence step-by-step.
- **Dynamic Savanna Environments:** Features multiple terrain textures (lush grass, dry savanna patches, mud tracks), rocky hazards, water obstacles (rivers & lakes), and transparent cartoon sprites.
- **Fluid Progression:** Clear a level and press `SPACE` to immediately jump into the next challenge. Switch heroes anytime from the main menu!

---

## 🎮 How to Play

1. **Pick your Hero:** Click the character card to select the Giraffe or the Cheetah.
2. **Plan Your Route:** Look at the grid and find the path from your hero to their goal.
3. **Add Commands:**
   - **FORWARD:** Moves your hero 1 tile forward in the direction they are currently facing.
   - **LEFT:** Rotates your hero 90° counter-clockwise.
   - **RIGHT:** Rotates your hero 90° clockwise.
4. **Run the Code:** Click **RUN!** to watch your hero execute your instructions.
5. **Clear & Retry:** If you hit an obstacle or step out of bounds, click **CLEAR** or press `SPACE` to reset.
6. **Next Level:** Once you reach your target, press `SPACE` to advance to the next level!
7. **Return to Menu:** Press `ESC` at any time to return to the level selection menu.

---

## 🚀 Running from Source

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jeixix/GiraffeCode.git
   cd GiraffeCode
   ```

2. **Create and activate a virtual environment:**
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - **Windows (Command Prompt):**
     ```cmd
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the game:**
   ```bash
   python src/main.py
   ```

---

## 📦 Compiling Standalone Executables

You can compile the game into a single, standalone executable that bundles Python, all dependencies, and all image assets. Users will not need Python installed to play!

### Compiling on Linux

1. Make sure your virtual environment is active and dependencies are installed:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt pyinstaller
   ```

2. Run PyInstaller (note the colon `:` used to separate paths on Linux):
   ```bash
   pyinstaller -y --onefile --noconsole --add-data "assets/*:assets" --name GiraffeCode src/main.py
   ```

3. Your standalone Linux binary will be ready in the `dist/` directory:
   ```bash
   ./dist/GiraffeCode
   ```

---

### Compiling on Windows

> **Note:** PyInstaller creates executables for the operating system it is run on. To generate a `.exe` for Windows, run these commands on a Windows machine.

1. Clone or copy the project folder to your Windows PC.
2. Open **Command Prompt** (`cmd.exe`) in the project directory.
3. Create and activate a virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install the requirements and PyInstaller:
   ```cmd
   pip install -r requirements.txt pyinstaller
   ```

5. Run PyInstaller (note the semicolon `;` used to separate paths on Windows):
   ```cmd
   pyinstaller -y --onefile --noconsole --add-data "assets/*;assets" --name GiraffeCode src/main.py
   ```

6. Your standalone Windows executable will be available at:
   ```cmd
   dist\GiraffeCode.exe
   ```
   You can distribute this single `.exe` file to any Windows computer without needing Python!

---

## 📂 Project Structure

```text
GiraffeCode/
├── assets/             # Game graphics (PNG sprites & JPG backgrounds)
├── src/
│   ├── game.py         # Main game loop, menus, and application logic
│   ├── executor.py     # Command execution engine & timing
│   ├── game_state.py   # Grid state, movement logic, collision detection
│   ├── giraffe.py      # Player entity, rotation & rendering
│   ├── levels.py       # 100 level definitions with obstacles & goals
│   └── ui.py           # Buttons, command queue, and UI rendering
│   └── main.py         # Lightweight launcher script
├── requirements.txt    # Python package dependencies
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
