# Coding Assessment

Welcome. The purpose of this assessment is **not** to get the correct answer as quickly as possible. We're interested in how you approach the problem, how well you can explain your thought process, and how well you work with others. We don't necessarily expect you to finish all parts. Ask questions, search whatever you need, and think out loud.

---

## ⚠️ Before you start — IDE / agent setup

If you use **VS Code, Cursor, Copilot, or any IDE that loads a folder as workspace context:**
**`open folder` on `working_directory/` only.** Do not open the parent repo as your workspace.

If you use a **CLI agent (Claude Code, Aider, Codex CLI, etc.):**
**`cd working_directory/` first, then start the agent there.**

Why: this document contains the question text, and we want to see _you_ think — not your agent reading the question off disk.

---

## Setup

You should be able to do this in a terminal. We'll watch over your shoulder; if any step gets stuck on your environment, just say so.

### Notes for Windows users

- The commands below are identical on Windows; run them in **PowerShell**, **cmd**, or **Git Bash**.
- If you don't have Python yet, install **Python 3.11+** from <https://www.python.org/downloads/>. During the installer, check **"Add python.exe to PATH"**.
- If `pip install uv` fails, try `python -m pip install uv` instead.
- Don't unzip the OneDrive download yourself — let `verify_data.py` handle it (see step 4).

### 1. Clone

```bash
git clone https://github.com/Cattleya517/acrocyte_coding_assessment.git
cd acrocyte_coding_assessment
```

### 2. Install uv (if you don't have it)

```bash
pip install uv
```

Or, if you prefer Astral's standalone installer:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

If `pip install uv` is blocked at your company, the fallback is plain pip — see the bottom of this document.

### 3. Install dependencies

```bash
cd working_directory
uv sync
```

### 4. Download the data

1. Open this OneDrive link:
   <https://acrocyte-my.sharepoint.com/:f:/p/adam_wang/IgCXUmqzRV_LSLsSd-3Sk4vxAcgxz7Wjbdi__ONE4YsWgvk?e=YVHkx9>
2. When prompted for a password, ask the interviewer.
3. Click **Download** at the top — SharePoint will package the folder as a single zip (~600 MB). Takes a couple of minutes.
4. Move (or copy) the downloaded zip into `working_directory/` (next to `verify_data.py`). Don't unzip it yourself.
5. Run:
   ```bash
   uv run python verify_data.py
   ```
   This unzips everything into `data/`, flattens any wrapper folders, and verifies. You should see `Data OK (13 files in ...)`. After it succeeds, you can delete the OneDrive zip.

---

## Part 1 — Warmup

In a terminal (still inside `working_directory/`), run:

```bash
uv run python warmup.py
```

It will print a LeetCode URL. Solve it on leetcode.com.

**Rules for Part 1:**

- You may google syntax or look up error messages.
- Searching for the solution directly is not allowed.
- **AI / coding agents are not allowed for Part 1.**

---

## Part 2 — Microscope image analysis

### Open Jupyter

Open `notebook.ipynb`.

### Background

Grayscale images are stored as 2D matrices. Pixel value = intensity; higher value = brighter pixel. Most images are 8-bit (max 255), but the ones here are 12-bit (new scope, max 4095) and 16-bit (old scope, max 65535).

Immunofluorescence (IF) staining lets us see protein markers on cell surfaces. A molecule binds to a target protein and emits light when scanned by a fluorescence microscope. Each slide is stained with four colors:

- **Blue** — nucleus
- **Red** — protein X
- **Green** — protein Y
- **Yellow** — protein Z

You don't need to memorize which color targets which protein — there are simply four channels.

We scanned the same slide with two microscopes:

- **Old microscope** — 16-bit images
- **New microscope** — 12-bit images

So we have 4 channels × 2 scans = 8 images. Plus a "mask" file per scan (10 total). The mask labels every cell with a unique integer; pixels with value 0 are background.

The data layout (after `verify_data.py`) is:

```
working_directory/data/
├── leetcode_pool.txt
├── old microscope/
│   ├── old blue.tif
│   ├── old green.tif
│   ├── old red.tif
│   ├── old yellow.tif
│   └── old mask.tif
├── new microscope/
│   ├── new blue.tif
│   ├── new green.tif
│   ├── new red.tif
│   ├── new yellow.tif
│   └── new mask.tif
└── cells csv/
    ├── old cells.csv
    └── new cells.csv
```

**Note on autofluorescence.** Even without staining, cells fluoresce a bit. So "does this cell express protein X?" is not just "is its red intensity nonzero?". Raw intensity values have no units — they only mean something _relative to other intensities measured under the same conditions_.

### Part 2 rules

- AI agents allowed.
- Open `notebook.ipynb` in Jupyter and use the scaffolded sections.
- For each sub-question, write your **approach** in the markdown cell first, then implement.
- Talk through your thinking out loud — that's the main thing we care about.

### Part 2.1 — Mean intensity of one cell

A standard way to measure protein expression level is the mean intensity of a cell in the relevant channel. Compute the mean intensity of **cell 100** (in the old microscope's red channel).

### Part 2.2 — Mean intensity of all cells

Compute the mean intensity of every cell.

### Part 2.3 — Old → new microscope translation (open-ended discussion)

We use intensity thresholds (set from old microscope data) to decide whether a cell expresses a given protein. E.g., "if mean red intensity > 5000, the cell is protein X positive."

We're switching to the new microscope. Old is 16-bit (max 65,535), new is 12-bit (max 4,095) — absolute intensity values necessarily differ.

**How would you make old and new microscope data comparable?** How would you "translate" thresholds from one to the other? Use the data we provided to motivate your answer.

This part is mostly a discussion. Pseudo-code is fine; full implementation is optional.

---

## (Optional) Inspecting the .tif files

[ImageJ](https://imagej.net/ij/download.html) is the easiest way. macOS Preview / Windows Photos won't auto-scale 12/16-bit images so they look black — that doesn't mean the file is broken. In ImageJ, after opening: Image → Adjust → Brightness/Contrast → Auto.

---

## Fallback: if `uv` is blocked

```bash
cd working_directory
pip install -r requirements.txt
python verify_data.py
python warmup.py
jupyter lab
```

If your company also blocks PyPI / OneDrive entirely, let us know — we'll bring the data on a USB drive.
