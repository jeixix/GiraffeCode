# 🦒 GiraffeCode / SavannaCode 🐆

**SavannaCode** (formerly GiraffeCode) is an educational programming game designed to introduce children (ages 5–9) to computational thinking and coding principles through a playful, visual experience.

Players can choose their favorite animal hero—a hungry **Giraffe** or a speedy **Cheetah**—and navigate them across a savanna grid by sequencing directional commands (`FORWARD`, `LEFT`, `RIGHT`) to reach their goal (Acacia Leaves or a Gazelle) while avoiding obstacles like rocks and rivers.

---

## 🌟 Features

- **Choose Your Hero:** Interactive character selection screen. Play as the Giraffe to reach acacia leaves, or play as the Cheetah to catch the gazelle!
- **High-Quality Emoji Graphics:** The game uses bundled high-resolution Twemoji graphics for characters, targets, and UI icons, guaranteeing consistent, vibrant visuals across all operating systems without relying on missing system fonts.
- **200 Solvable Levels:** 200 thoughtfully designed and procedurally generated levels ranging from gentle straight lines to complex maze puzzles. All 200 levels are mathematically verified to be 100% solvable!
- **Real-Time Code Execution Highlighter:** Just like Scratch and Blockly, the command queue is rendered as visual code pills that glow golden in real time as the animal executes each step!
- **Undo (⌫) & Emergency Stop (⏹):** Made a typo? Click **UNDO** or press `Backspace` to delete just the last command without wiping your whole queue. If you see a crash coming, click **STOP** to halt execution instantly.
- **Progress Tracking & Stars (⭐):** Your completed levels are saved automatically! Completed levels earn a gold star in the level select menu, tracking your journey to 200/200 stars.
- **Natural Biome Terrain:** Coherent savanna environment with lush grass, sun-baked dry savanna patches, natural clustered watering holes, and muddy riverbanks.
- **Dynamic Resolution & Display Modes:** Built for both Fullscreen and Windowed mode (`F11`), with dynamic grid scaling ensuring the entire grid and all bottom tiles are 100% visible on all monitor sizes. Fully crash-proof display toggling!
- **Animated Walk Cycles:** Procedural running and walking simulations with dynamic leg shearing, wobbling, and vertical bobbing.

---

## 🎮 How to Play & Controls

### Objective
Plan a sequence of instructions to guide your animal to the goal tile without crashing into rocks, water hazards, or stepping out of bounds!

### 🖱️ Mouse Controls
- **FORWARD:** Moves your hero 1 tile forward in the direction they are facing.
- **LEFT:** Rotates your hero 90° counter-clockwise.
- **RIGHT:** Rotates your hero 90° clockwise.
- **UNDO ⌫:** Removes the last added command from the queue.
- **CLEAR 🗑:** Clears the entire queue and resets the hero to start.
- **RUN ▶ / STOP ⏹:** Starts executing your code, or stops execution immediately.

### ⌨️ Keyboard Shortcuts
| Key | Action |
| :--- | :--- |
| **`W` or `↑ Up Arrow`** | Add `FORWARD` command |
| **`A` or `← Left Arrow`** | Add `LEFT` command |
| **`D` or `→ Right Arrow`** | Add `RIGHT` command |
| **`Backspace`** | `UNDO` last command (⌫) |
| **`C`** | `CLEAR` entire command queue |
| **`Enter`** | `RUN` / `STOP` execution |
| **`SPACE`** | Advance to Next Level (after winning) or Retry (after crashing) |
| **`ESC`** | Return to Main Menu |
| **`F11`** | Toggle Fullscreen / Windowed Mode |

---

## 🚀 Running from Source

### Prerequisites
- Python 3.10 or higher
- `pip` package manager

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone git@github.com:jeixix/GiraffeCode.git
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
   pyinstaller -y --onefile --noconsole --icon=assets/icon.png --add-data "assets/*:assets" --name GiraffeCode src/main.py
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
   pyinstaller -y --onefile --noconsole --icon=assets/icon.png --add-data "assets/*;assets" --name GiraffeCode src/main.py
   ```

6. Your standalone Windows executable will be available at:
   ```cmd
   dist\GiraffeCode.exe
   ```
   You can distribute this single `.exe` file to any Windows computer without needing Python!

---

## 📂 Project Structure

Following modern Python packaging standards, all execution logic resides cleanly within the `src/` module:

```text
GiraffeCode/
├── assets/             # Game graphics (PNG sprites, walk cycle frames & JPG backgrounds)
├── src/
│   ├── main.py         # Entry point and launcher script
│   ├── game.py         # Main loop, menus, dynamic scaling & terrain generation
│   ├── executor.py     # Command execution engine, step timing & state sync
│   ├── game_state.py   # Grid state, directional movement & collision detection
│   ├── giraffe.py      # Player entity, smooth sub-pixel interpolation & walk animations
│   ├── levels.py       # 200 verified solvable level definitions
│   ├── ui.py           # Buttons, visual code pills, highlighter & UI rendering
│   └── scripts/        # Asset generation & walk cycle utility scripts
├── requirements.txt    # Python dependencies (pygame-ce, Pillow)
├── .gitignore          # Git exclusion rules
└── README.md           # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
