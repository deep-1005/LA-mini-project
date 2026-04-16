# Linear Algebra Image Pipeline

An interactive desktop app built with Tkinter that demonstrates core linear algebra concepts through image processing.

The app loads an image, applies one of 10 mathematically grounded transformations, and displays both the original and processed output side by side. Each step also shows an explanation panel with the underlying matrix concept.

## Features

- GUI built with Python Tkinter
- Image loading, processing, and saving (PNG/JPG)
- Side-by-side original and result previews
- 10 pipeline steps linked to linear algebra topics:
  - Step 1: Matrix Representation (Rotate / Scale / Flip)
  - Step 2: Matrix Simplification (RREF + LU)
  - Step 3: Rank and Nullity (SVD-based)
  - Step 4: Basis Selection (QR with pivoting)
  - Step 5: Gram-Schmidt Orthogonalization
  - Step 6: Orthogonal Projection
  - Step 7: Least Squares Polynomial Fit
  - Step 8: Eigenanalysis / PCA
  - Step 9: SVD Compression
  - Step 10: SVD-based Enhancement

## Project Structure

- `la_mini.py`: Complete application code (math pipeline + GUI)
- Sample image files (for testing): `pic1.jpg`, `blurry_pic.jpg`

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

1. Click **Load Image**
2. Choose a pipeline step from the left sidebar
3. Adjust parameters (sliders/radio options)
4. Click **Apply**
5. Optionally click **Save Result**

## Pipeline Step Summary

### Step 1: Matrix Representation

- Rotate using a 2x2 rotation matrix
- Scale using a diagonal matrix
- Flip using reflection matrices

### Step 2: Matrix Simplification

- Extracts a center patch
- Computes manual RREF (Gauss-Jordan)
- Performs LU decomposition and reconstruction check

### Step 3: Rank and Nullity

- Uses SVD singular values
- Demonstrates rank-nullity relation
- Reconstructs image using rank-k approximation

### Step 4: Basis Selection

- Uses QR decomposition with pivoting to select independent rows
- Reconstructs rows from selected basis vectors

### Step 5: Gram-Schmidt

- Orthogonalizes selected row vectors
- Projects image onto orthonormal basis

### Step 6: Projection

- Builds projection matrix P = Uk * Uk^T from top singular vectors
- Projects image onto dominant subspace

### Step 7: Least Squares

- Fits polynomial models column-wise using normal equations
- Reports RMSE of fit

### Step 8: Eigenanalysis / PCA

- Builds covariance matrix
- Uses eigenvectors with largest eigenvalues
- Reconstructs image from top principal components

### Step 9: SVD Compression

- Keeps top-k singular values
- Reports retained energy and compression ratio

### Step 10: Enhancement

SVD-domain filters:

- **Sharpen**: boost dominant singular values
- **Smooth**: suppress low singular values
- **Contrast**: scale all singular values

## Notes

- The app processes grayscale for many matrix operations and restores color where needed.
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
