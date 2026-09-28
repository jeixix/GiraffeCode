# 🦒 GiraffeCode / SavannaCode 🐆

**SavannaCode** (formerly GiraffeCode) is an educational programming game designed to introduce children (ages 5–9) to computational thinking and coding principles through a playful, visual experience.

Players can choose their favorite animal hero—a hungry **Giraffe** or a speedy **Cheetah**—and navigate them across a savanna grid by sequencing directional commands (`FORWARD`, `LEFT`, `RIGHT`) to reach their goal (Acacia Leaves or a Gazelle) while avoiding obstacles like rocks and rivers.

---

## 🌟 Features

- **Choose Your Hero:** Interactive character selection screen. Play as the Giraffe to reach acacia leaves, or play as the Cheetah to catch the gazelle!
- **Step-by-Step Debugger (`STEP ⏭️`):** Essential educational tool allowing young coders to execute their code one command at a time, seeing their hero move while the corresponding code pill glows golden.
- **Adjustable Execution Speed (🐢 Normal / ⚡ Turbo):** Toggle between gentle 600ms step pacing for beginners and rapid 250ms turbo speed for testing long solutions.
- **10-Chapter Paginated Level Selector (🗺️):** All 200 levels are cleanly organized across 10 themed savanna biomes (20 levels per chapter in an intuitive 5x4 grid) with quick-jump world pills and arrow navigation.
- **Bilingual English 🇬🇧 / Spanish 🇪🇸 Localization:** One-click language switching (`L` or top-right button) instantly translates all commands, code pills, tutorials, dialogue overlays, and all 200 level titles dynamically across both Giraffe and Cheetah heroes!
- **Global Sound Mute Toggle (🔊 / 🔇):** Easily mute all sound effects with a single click or keyboard shortcut (`M`), perfect for classroom and quiet settings.
- **Visual "Juice" & Particle Effects (✨):** Cheerful, lightweight particle bursts: fluttering leaves when the giraffe reaches the acacia tree, sparkle stars when the cheetah catches the gazelle, running dust clouds under animal paws, water splashes, and victory confetti.
- **Built-in Level Editor (🛠️):** Design and save custom savanna puzzles! Adjust grid dimensions, place obstacles, water, start, and goals. Features a mandatory BFS mathematical solvability checker that ensures custom levels are 100% solvable before allowing players to test and play them!
- **Playful Audio Engine (🎵):** Immersive sound effects for movement steps, turn chirps, UI button pops, crash thuds, and joyful victory jingles with graceful device fallback.
- **High-Quality Emoji Graphics:** The game uses bundled high-resolution Twemoji graphics for characters, targets, and UI icons, guaranteeing consistent, vibrant visuals across all operating systems without relying on missing system fonts.
- **Educational "Loops" (`REPEAT`):** Teaches computational thinking and loop constructs, allowing players to repeat sequences cleanly.
- **200 Solvable Levels:** 200 thoughtfully designed and procedurally generated levels ranging from gentle straight lines to complex maze puzzles. All 200 levels are mathematically verified to be 100% solvable, with dynamic bilingual titles in English and Spanish for both animal heroes!
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
- **REPEAT 🔁:** Repeats the sequence of instructions in the queue (loops up to 2 extra times).
- **UNDO ⌫:** Removes the last added command from the queue.
- **CLEAR 🗑:** Clears the entire queue and resets the hero to start.
- **STEP ⏭️:** Single-step debugger: executes exactly one command and pauses.
- **RUN ▶ / STOP ⏹:** Starts executing your code, or stops execution immediately.
- **Speed Toggle (1x / 2x):** Switch between Normal and Turbo execution speed.
- **Mute Toggle (Sound ON/OFF):** Silences or unmutes sound effects.
- **Language Toggle (EN / ES):** Switches interface between English and Spanish.

### ⌨️ Keyboard Shortcuts
| Key | Action |
| :--- | :--- |
| **`W` or `↑ Up Arrow`** | Add `FORWARD` command |
| **`A` or `← Left Arrow`** | Add `LEFT` command |
| **`D` or `→ Right Arrow`** | Add `RIGHT` command |
| **`R`** | Add `REPEAT` loop command (🔁) |
| **`Backspace`** | `UNDO` last command (⌫) |
| **`C`** | `CLEAR` entire command queue |
| **`S`** | `STEP` (Single-step debugger) |
| **`Enter`** | `RUN` / `STOP` execution |
| **`T`** | Toggle Speed (`Normal` / `Turbo`) |
| **`M`** | Toggle Sound Mute (`ON` / `OFF`) |
| **`L`** | Toggle Language (`EN` / `ES`) |
| **`←` / `→` or `PgUp` / `PgDn`** | Previous / Next Chapter in Level Select |
| **`SPACE`** | Advance to Next Level (after winning) or Retry (after crashing) |
| **`ESC`** | Return to Main Menu / Editor |
| **`F11`** | Toggle Fullscreen / Windowed Mode |

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
     > **💡 Note on Windows PowerShell Execution Policy:**
     > By default, Windows sets its execution policy to `Restricted` to prevent unverified scripts from running, which may cause PowerShell to block `Activate.ps1` with the error: *`File ... cannot be loaded because running scripts is disabled on this system`*.
     >
     > You can safely allow activation scripts **only for your current terminal session** (without altering any permanent system-wide security settings) by running:
     > ```powershell
     > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     > .\venv\Scripts\Activate.ps1
     > ```
     > *(Alternatively, you can simply use the standard Windows **Command Prompt (`cmd.exe`)**, which does not have this restriction.)*

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

2. Run PyInstaller using the included specification file:
   ```bash
   pyinstaller GiraffeCode.spec --noconfirm
   ```
   *(Or alternatively build directly with custom flags: `pyinstaller -y --onefile --noconsole --icon=assets/icon.ico --add-data "assets/*:assets" --name GiraffeCode src/main.py`)*

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

5. Run PyInstaller using the included specification file:
   ```cmd
   pyinstaller GiraffeCode.spec --noconfirm
   ```
   *(Or alternatively build directly with custom flags, noting the `.ico` icon and semicolon `;` path separator on Windows)*:
   ```cmd
   pyinstaller -y --onefile --noconsole --icon=assets\icon.ico --add-data "assets/*;assets" --name GiraffeCode src\main.py
   ```

6. Your standalone Windows executable will be available at:
   ```cmd
   dist\GiraffeCode.exe
   ```
   You can distribute this single `.exe` file to any Windows computer without needing Python!

---

### 💿 Creating a Windows Setup Installer (`.exe`)

You can package the game into a single setup wizard (`SavannaCode-Setup-v1.0.exe`) that includes:
- Bilingual installation wizard (English 🇬🇧 & Spanish 🇪🇸).
- Automatic Desktop and Start Menu shortcut creation with game icon.
- Full uninstaller registered in Windows Settings / Control Panel (which completely purges all game files, settings, and saves upon removal).
- Read-only protection: game data automatically saves to `%APPDATA%\SavannaCode` if installed into `Program Files`.

#### Option A: Automatic Cloud Build (GitHub Actions — 100% Free)
1. Go to your repository on GitHub and click the **Actions** tab.
2. Select **Build Windows Installer** from the left sidebar.
3. Click **Run workflow** -> **Run workflow**.
4. Once completed (~2 minutes), download the ready-to-distribute `SavannaCode-Windows-Installer` artifact from the run summary!
*(Pushing a version tag like `git tag v1.0.0 && git push origin v1.0.0` will automatically publish a GitHub Release with the installer attached).*

#### Option B: Building Locally on Windows (Inno Setup)
1. Install [Inno Setup 6](https://jrsoftware.org/isdl.php) (free & open source, or via `winget install JRSoftware.InnoSetup`).
2. Build the PyInstaller executable first:
   ```cmd
   pyinstaller GiraffeCode.spec --noconfirm
   ```
3. Compile the installer:
   - **Via Command Line**:
     ```cmd
     "C:\Program Files (x86)\Inno Setup 6\iscc.exe" installer.iss
     ```
   - **Or via GUI**: Right-click `installer.iss` in File Explorer and click **Compile**.
4. Your setup wizard will be created in the `installer_output\` directory:
   ```cmd
   installer_output\SavannaCode-Setup-v1.0.exe
   ```

---

## 📂 Project Structure

Following modern Python packaging standards, all execution logic resides cleanly within the `src/` module:

```text
GiraffeCode/
├── assets/             # Game graphics (PNG sprites, walk cycle frames, JPG backgrounds & icon.ico)
├── src/
│   ├── main.py         # Entry point and launcher script
│   ├── game.py         # Main loop, menus, dynamic scaling & terrain generation
│   ├── executor.py     # Command execution engine, step debugger & speed controls
│   ├── game_state.py   # Grid state, directional movement & collision detection
│   ├── giraffe.py      # Player entity, smooth sub-pixel interpolation & walk animations
│   ├── levels.py       # 200 verified solvable levels with dynamic bilingual (EN/ES) names
│   ├── editor.py       # Level editor with BFS mathematical solvability verification
│   ├── sound.py        # Audio manager, mute toggle & procedural SFX playback engine
│   ├── ui.py           # Buttons, visual code pills, highlighter & UI rendering
│   ├── i18n.py         # Bilingual localization engine (English 🇬🇧 / Spanish 🇪🇸)
│   ├── particles.py    # Visual particle engine (leaf munch, sparkles, dust, confetti)
│   └── scripts/        # Asset generation & walk cycle utility scripts
├── .github/
│   └── workflows/      # Automated GitHub Actions cloud CI/CD workflows
├── requirements.txt    # Python dependencies (pygame-ce)
├── GiraffeCode.spec    # Standalone PyInstaller build specification
├── installer.iss       # Inno Setup Windows installer script (EN/ES)
├── .gitignore          # Git exclusion rules
├── LICENSE             # MIT License
└── README.md           # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
