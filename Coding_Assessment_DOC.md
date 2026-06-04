# Coding Assessment

Welcome. The purpose of this assessment is **not** to get the correct answer as quickly as possible. We're interested in how you approach the problem, how well you can explain your thought process, and how well you work with others. We don't necessarily expect you to finish all parts. Ask questions, search whatever you need, and think out loud.

---

## How to run — everything is in Google Colab

This assessment runs **entirely in your browser via Google Colab**. There is nothing to install and no data to download by hand.

1. Open the notebook — click the **Open in Colab** badge in [`README.md`](README.md), or open
   `working_directory/notebook_colab.ipynb` in Colab.
2. Run the **Setup** cell (installs `tifffile`, `pyzipper`, `tqdm`).
3. Run the **Unlock** cell and enter the **data password** — *ask your interviewer*. You enter it
   **once**; the same password unlocks the Part 2 image data later in the notebook.
4. **Part 1** draws your warmup problem right away.
5. When you reach **Part 2**, run the download cell (~1 GB, a couple of minutes — you'll see a
   progress bar), then work through the scaffolded sections.

> If Colab is blocked for you, or the data won't download, just tell your interviewer and we'll sort it out.

---

## Part 1 — Warmup

Run the **Part 1** cell in the notebook. It prints — and links — a LeetCode problem. Solve it on [leetcode.com](https://leetcode.com).

**Rules for Part 1:**

- You may google syntax or look up error messages.
- Searching for the solution directly is not allowed.
- **AI / coding agents are not allowed for Part 1.**

---

## Part 2 — Microscope image analysis

Run the **Part 2** download cell in the notebook, then use the scaffolded sections. Before the questions, the notebook includes a short `vmin`/`vmax` display demo and a zoomed-in look at the mask, so the display conventions are clear.

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

The data layout (after the download cell) is:

```
data/
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
- For each sub-question, write your **approach** in the markdown cell first, then implement.
- Talk through your thinking out loud — that's the main thing we care about.

### Part 2.1 — How many cells are in this image?

Use the mask file to figure out how many cells the image contains.

### Part 2.2 — Mean intensity of one cell

A standard way to measure protein expression level is the mean intensity of a cell in the relevant channel. Compute the mean intensity of **cell 100** (in the old microscope's red channel).

### Part 2.3 — Mean intensity of all cells

Compute the mean intensity of every cell.

### Part 2.4 — Old → new microscope translation (open-ended discussion)

We use intensity thresholds (set from old microscope data) to decide whether a cell expresses a given protein. E.g., "if mean red intensity > 5000, the cell is protein X positive."

We're switching to the new microscope. Old is 16-bit (max 65,535), new is 12-bit (max 4,095) — absolute intensity values necessarily differ.

**How would you make old and new microscope data comparable?** How would you "translate" thresholds from one to the other? Use the data we provided to motivate your answer.

This part is mostly a discussion. Pseudo-code is fine; full implementation is optional.

---

## (Optional) Inspecting the .tif files

[ImageJ](https://imagej.net/ij/download.html) is the easiest way. macOS Preview / Windows Photos won't auto-scale 12/16-bit images so they look black — that doesn't mean the file is broken. In ImageJ, after opening: Image → Adjust → Brightness/Contrast → Auto.
