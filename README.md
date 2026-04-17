# Linear Algebra Image Tools

An interactive desktop app built with Tkinter that demonstrates core linear algebra concepts through image processing.

The app loads an image, applies one of 4 mathematically grounded transformations, and displays both the original and processed output side by side. Each step also shows an explanation panel with the underlying matrix concept.

## Features

- GUI built with Python Tkinter
- Image loading, processing, and saving (PNG/JPG)
- Side-by-side original and result previews
- 4 transformation modes linked to linear algebra topics:
  - Rotation
  - Scaling / Zoom
  - Reflection
  - SVD Compression

## Project Structure

- `la_mini.py`: Complete application code (math transformations + GUI)
- Sample image files for testing: `pic1.jpg`, `blurry_pic.jpg`

## Requirements

- Python 3.9+
- Packages:
  - numpy
  - scipy
  - pillow

Install dependencies:

```bash
pip install numpy scipy pillow
```

## How to Run

From the project folder:

```bash
python la_mini.py
```

The app opens a window where you can:

2. Choose a pipeline step from the left sidebar

## Pipeline Step Summary

<<<<<<< HEAD
### Rotation, Scaling, Reflection
### Step 1: Matrix Representation
>>>>>>> 1b1451455340fcdd6d07a9d1b5b29c434e974841

- Rotate using a 2x2 rotation matrix
- Scale using a diagonal matrix

SVD-domain filters:

- **Sharpen**: boost dominant singular values
- **Contrast**: scale all singular values
## Notes

- The app processes grayscale for many matrix operations and restores color where needed.
<<<<<<< HEAD
- The full image is kept in memory for processing; previews are scaled only for display.
=======
>>>>>>> 1b1451455340fcdd6d07a9d1b5b29c434e974841
- For large images, computations can be slower in steps involving decomposition.
- If a step fails due to numerical issues, the app uses safe fallbacks (for example, pseudo-inverse in some cases).

## Troubleshooting

- If import errors occur, re-check installed packages:

```bash
pip install --upgrade numpy scipy pillow
```

- If Tkinter is missing (uncommon on standard Python installs), install a Python distribution that includes Tk support.

## Author / Context

This project is structured as an educational mini project for demonstrating linear algebra concepts through practical image transformations.
