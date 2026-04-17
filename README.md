# Linear Algebra Image Tools

A Tkinter desktop application that demonstrates core linear algebra ideas through interactive image transformations.

## Overview

This project lets you load an image, apply mathematically meaningful operations, and compare the original and transformed outputs side by side.

It also displays a small math dashboard that explains the active transformation using matrix forms, determinants, eigenvalues, and SVD details.

## Features

- Load images (`.png`, `.jpg`, `.jpeg`)
- Save transformed output (`.png`, `.jpg`)
- Side-by-side preview panels
- Clean, minimalist Tkinter UI
- Four operations:
  - Rotation
  - Scaling (zoom in/out)
  - Reflection (horizontal, vertical, both)
  - SVD compression (rank-k approximation)

## Tech Stack

- Python 3.9+
- NumPy
- SciPy
- Pillow
- Tkinter (usually included with standard Python installs)

## Project Structure

- `la_mini.py` - Main application file (GUI + all transformation logic)
- `README.md` - Project documentation

## Installation

1. Open a terminal in the project folder.
2. Install dependencies:

```bash
pip install numpy scipy pillow
```

## Run

```bash
python la_mini.py
```

## How To Use

1. Click **Load Image**.
2. Choose one operation from the left panel:
   - Rotation
   - Scaling (Zoom)
   - Reflection
   - SVD Compression
3. Adjust parameters.
4. Click **Apply Transformation**.
5. Click **Save Output** to export the result.

## Math Behind Each Operation

### Rotation

Uses the 2D rotation matrix:

$$
R = \begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
$$

### Scaling

Uses the diagonal scaling matrix:

$$
S = \begin{bmatrix}
s_x & 0 \\
0 & s_y
\end{bmatrix}
$$

### Reflection

Uses reflection matrices such as:

$$
\begin{bmatrix}
-1 & 0 \\
0 & 1
\end{bmatrix},
\begin{bmatrix}
1 & 0 \\
0 & -1
\end{bmatrix}
$$

### SVD Compression

Approximates the image matrix using rank-k reconstruction:

$$
A \approx U_k \Sigma_k V_k^T
$$

Keeping fewer singular values reduces storage while preserving most visual energy.

## Notes

- Transformations are applied around image center using affine mapping.
- For color images, grayscale space is used for SVD and then recolored.
- Very large images may take longer for SVD compression.

## Troubleshooting

- If dependencies are missing:

```bash
pip install --upgrade numpy scipy pillow
```

- If Tkinter is unavailable, install a Python distribution that includes Tk support.

## Context

Educational mini project for learning and demonstrating linear algebra through image processing.
