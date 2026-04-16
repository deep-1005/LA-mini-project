Linear Algebra Image Pipeline
UE24MA241B — PES University

A desktop GUI application that demonstrates key linear algebra concepts through image processing. It applies techniques such as matrix transformations, SVD, eigenanalysis, and projections in an interactive and visual manner.

Requirements
Python 3.8 or higher
Required Python packages:
pip install numpy scipy pillow

tkinter is included with most Python installations. If it is missing on Linux:

sudo apt-get install python3-tk
Running the Application
python pipeline.py

The application opens in a resizable window (default size: 1280 × 740).

Usage
Click Load Image (top-right) and select an image (PNG, JPEG, BMP, or TIFF).
Choose a pipeline step from the left sidebar.
Adjust the available controls (sliders or options).
Click Apply to process the image.
View the result on the right panel.
Read the explanation in the info panel.
Click Save Result to export the processed image.
Pipeline Overview
Step	Name	Concept
1a	Rotate	Rotation matrix, determinant = 1
1b	Scale	Diagonal matrix, eigenvalues
1c	Flip	Reflection matrix
2	RREF + LU	Gaussian elimination, LU decomposition
3	Rank / Nullity	SVD, rank-nullity theorem
4	Basis Select	QR decomposition with pivoting
5	Gram-Schmidt	Orthonormal basis construction
6	Projection	Orthogonal projection
7	Least Squares	Polynomial fitting, normal equations
8	Eigenanalysis	Covariance matrix, PCA
9	SVD Compress	Rank-k approximation
10	Enhance	SVD-based image enhancement
Step Details
Step 1 — Matrix Transformations

Images are treated as coordinate grids where each pixel position is transformed using a 2×2 matrix.

Rotate: Uses a rotation matrix (area-preserving).
Scale: Uses a diagonal matrix; determinant reflects area scaling.
Flip: Uses reflection matrices to mirror the image.
Step 2 — Matrix Simplification

Operates on a small central patch of the image.

RREF: Custom Gaussian elimination implementation.
LU Decomposition: Uses SciPy to factor the matrix and verify reconstruction accuracy.
Step 3 — Rank and Nullity

Applies SVD to a grayscale image.

Demonstrates rank-k approximation.
Verifies the rank-nullity theorem numerically.
Displays retained image energy.
Step 4 — Basis Selection

Uses QR decomposition with column pivoting.

Identifies linearly independent rows.
Reconstructs remaining rows using linear combinations.
Step 5 — Gram-Schmidt

Constructs an orthonormal basis from selected vectors.

Validates orthogonality numerically.
Projects the image onto the computed subspace.
Step 6 — Projection

Builds a projection matrix using SVD components.

Ensures symmetry and idempotence properties.
Step 7 — Least Squares

Fits polynomial curves to image columns.

Uses Vandermonde matrices.
Solves using normal equations.
Reports fitting error (RMSE).
Step 8 — Eigenanalysis (PCA)

Performs Principal Component Analysis.

Computes covariance matrix.
Extracts principal components.
Displays explained variance.
Step 9 — SVD Compression

Performs image compression using truncated SVD.

Reduces storage requirements.
Displays compression ratio and retained energy.
Processes RGB channels independently.
Step 10 — Enhancement

Modifies singular values to adjust image characteristics.

Sharpen: Enhances dominant features.
Smooth: Reduces noise and texture.
Contrast: Scales overall intensity.
Code Structure
pipeline.py
├── Helper functions        (image conversion and transformations)
├── Step functions          (step1 → step10)
└── App class (tkinter GUI)
    ├── UI construction
    ├── Parameter controls
    ├── Image loading and display
    ├── Processing logic
    └── Save functionality
Notes
Images are resized to fit within 600 × 600 pixels while preserving aspect ratio.
Computationally intensive steps may take longer for large images.
The RREF step operates on a limited patch to maintain performance.
Color consistency is preserved by adjusting RGB channels based on grayscale transformations.
