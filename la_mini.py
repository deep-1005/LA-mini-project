import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
from scipy.ndimage import affine_transform
from PIL import Image, ImageTk
import os

# ── CLEAN MINIMALIST THEME ────────────────────────────────────
BG       = '#FFFFFF'
PANEL    = '#F8F9FA'
TEXT     = '#000000'
DIMTXT   = '#6C757D'
BORDER   = '#DEE2E6'
BTN_BG   = '#212529'
BTN_FG   = '#FFFFFF'
ACCENT   = '#E9ECEF' # Light gray for active states

# ── HELPERS ───────────────────────────────────────────────────
def to_gray(img):
    if img.ndim == 3:
        return (0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]).astype(float)
    return img.astype(float)

def gray_to_rgb(arr):
    g = np.clip(arr, 0, 255).astype(np.uint8)
    return np.stack([g, g, g], axis=2)

def apply_transform(img, M_fwd):
    # To zoom IN when scaling > 1, we must use the Inverse Matrix for the affine warp
    M_inv = np.linalg.inv(M_fwd)
    center = np.array(img.shape[:2]) / 2.0
    offset = center - M_inv @ center
    
    if img.ndim == 3:
        channels = [affine_transform(img[:, :, c], M_inv, offset=offset, cval=255) for c in range(3)]
        return np.stack(channels, axis=2).astype(np.uint8)
    return affine_transform(img, M_inv, offset=offset, cval=255).astype(np.uint8)

def recolor(original, gray_new, gray_old):
    if original.ndim == 3:
        ratio = gray_new / np.clip(gray_old, 1, None)
        return np.clip(original.astype(float) * ratio[:, :, np.newaxis], 0, 255).astype(np.uint8)
    return gray_to_rgb(gray_new)

# ── CORE LA OPERATIONS ────────────────────────────────────────
def do_rotate(img, angle):
    t = np.radians(angle)
    c, s = np.cos(t), np.sin(t)
    R = np.array([[c, -s], [s, c]])
    
    eigenvalues, _ = np.linalg.eig(R)
    
    info = (f"LINEAR TRANSFORMATION: ROTATION\n\n"
            f"Rotation matrix R =\n"
            f"  [ {c:.3f}  {-s:.3f} ]\n"
            f"  [ {s:.3f}   {c:.3f} ]\n\n"
            f"det(R) = {np.linalg.det(R):.1f} (Area Preserved)\n"
            f"Eigenvalues: {eigenvalues[0]:.2f}, {eigenvalues[1]:.2f}")
    return apply_transform(img, R), info

def do_scale(img, sx, sy):
    S = np.array([[sx, 0.0], [0.0, sy]])
    
    eigenvalues, _ = np.linalg.eig(S)
    
    info = (f"LINEAR TRANSFORMATION: SCALING\n\n"
            f"Scale matrix S =\n"
            f"  [ {sx:.2f}   0   ]\n"
            f"  [  0    {sy:.2f} ]\n\n"
            f"det(S) = {np.linalg.det(S):.3f} (Area Multiplier)\n"
            f"Eigenvalues: λ₁={eigenvalues[0]:.2f}, λ₂={eigenvalues[1]:.2f}")
    return apply_transform(img, S), info

def do_flip(img, direction):
    if direction == "Horizontal":
        result = np.fliplr(img)
        F = np.array([[-1, 0], [0, 1]])
    elif direction == "Vertical":
        result = np.flipud(img)
        F = np.array([[1, 0], [0, -1]])
    else:
        result = np.flipud(np.fliplr(img))
        F = np.array([[-1, 0], [0, -1]])
        
    eigenvalues, _ = np.linalg.eig(F)
        
    info = (f"LINEAR TRANSFORMATION: REFLECTION\n\n"
            f"Reflection Matrix F =\n"
            f"  [ {F[0,0]}   {F[0,1]} ]\n"
            f"  [ {F[1,0]}   {F[1,1]} ]\n\n"
            f"det(F) = {np.linalg.det(F):.1f}\n"
            f"Eigenvalues: λ₁={eigenvalues[0]:.1f}, λ₂={eigenvalues[1]:.1f}")
    return result.astype(np.uint8), info

def do_compress(img, k_percent):
    gray = to_gray(img)
    U, S, Vt = np.linalg.svd(gray, full_matrices=False)
    
    k = max(1, int(len(S) * (k_percent / 100.0)))
    S_mod = np.zeros_like(S)
    S_mod[:k] = S[:k]
    
    total_energy = np.sum(S**2)
    retained_energy = np.sum(S[:k]**2)
    energy_ratio = (retained_energy / total_energy) * 100

    compressed_gray = np.clip(U @ np.diag(S_mod) @ Vt, 0, 255)
    
    info = (f"SVD COMPRESSION (Rank-{k} Approximation)\n\n"
            f"Original Dimensions: {gray.shape[0]}x{gray.shape[1]}\n"
            f"Singular Values Kept (k): {k} of {len(S)}\n"
            f"Energy Retained: {energy_ratio:.2f}%\n"
            f"Storage Space Saved: ~{100 - k_percent:.0f}%\n\n"
            f"Math: A ≈ U_k · Σ_k · V_kᵀ")
            
    return recolor(img, compressed_gray, gray), info


# ── GUI ───────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LA Image Tools — UE24MA241B | PES University")
        self.configure(bg=BG)
        self.geometry('1250x800')
        
        self.original_image = None
        self.result_image   = None
        
        self.build_ui()

    def build_ui(self):
        # ── TOP BAR ──
        bar = tk.Frame(self, bg=BG)
        bar.pack(fill='x', padx=20, pady=15)
        tk.Label(bar, text="LINEAR ALGEBRA IMAGE TOOLS", font=('Helvetica', 16, 'bold'), fg=TEXT, bg=BG).pack(side='left')
        tk.Label(bar, text="UE24MA241B | PES University", font=('Helvetica', 10), fg=DIMTXT, bg=BG).pack(side='right')

        # ── MAIN LAYOUT ──
        main = tk.Frame(self, bg=BG)
        main.pack(fill='both', expand=True, padx=20, pady=5)
        
        # ── LEFT SIDEBAR (CONTROLS) ──
        sidebar = tk.Frame(main, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, width=320)
        sidebar.pack(side='left', fill='y', padx=(0, 10))
        sidebar.pack_propagate(False)

        tk.Button(sidebar, text="1. Load Image", command=self.load_image, bg=BTN_BG, fg=BTN_FG, font=('Helvetica', 10, 'bold'), pady=8).pack(fill='x', padx=20, pady=20)
        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', padx=10)

        tk.Label(sidebar, text="2. SELECT OPERATION", font=('Helvetica', 10, 'bold'), fg=TEXT, bg=PANEL).pack(pady=(15, 5))

        steps = [("Rotation", "Rotate"), ("Scaling (Zoom)", "Scale"),
                 ("Reflection", "Flip"), ("SVD Compression", "Compress")]
                 
        self.current_step = tk.StringVar(value="Rotate")
        self.step_btns = {}
        for label, key in steps:
            b = tk.Button(sidebar, text=label, font=('Helvetica', 10),
                          bg=BG, fg=TEXT, relief='flat', cursor='hand2',
                          pady=6, anchor='w', padx=15,
                          command=lambda k=key: self.switch_step(k))
            b.pack(fill='x', pady=2, padx=20)
            self.step_btns[key] = b

        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', padx=10, pady=15)
        tk.Label(sidebar, text="3. PARAMETERS", font=('Helvetica', 10, 'bold'), fg=TEXT, bg=PANEL).pack(anchor='w', padx=20, pady=(0, 5))
        
        self.param_frame = tk.Frame(sidebar, bg=PANEL)
        self.param_frame.pack(fill='x', padx=20)

        ttk.Separator(sidebar, orient='horizontal').pack(fill='x', padx=10, pady=15)
        
        self.apply_btn = tk.Button(sidebar, text="▶  Apply Transformation", command=self.apply_step,
                                   font=('Helvetica', 10, 'bold'), bg=BTN_BG, fg=BTN_FG,
                                   relief='flat', cursor='hand2', pady=8)
        self.apply_btn.pack(fill='x', padx=20, pady=5)
        
        self.save_btn = tk.Button(sidebar, text="Save Output (.png)", command=self.save_result,
                                  font=('Helvetica', 9), bg=BG, fg=TEXT,
                                  relief='flat', cursor='hand2', pady=5)
        self.save_btn.pack(fill='x', padx=20, pady=5)

        # ── RIGHT AREA (IMAGES & MATH DASHBOARD) ──
        right_col = tk.Frame(main, bg=BG)
        right_col.pack(side='right', fill='both', expand=True)

        # Images
        img_frame = tk.Frame(right_col, bg=BG)
        img_frame.pack(side='top', fill='both', expand=True)
        
        self.lbl_orig = self.create_image_panel(img_frame, "Original Matrix (A)", "left")
        self.lbl_res = self.create_image_panel(img_frame, "Result Matrix", "right")

        # Math Dashboard
        bot_frame = tk.Frame(right_col, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        bot_frame.pack(side='bottom', fill='x', pady=(15, 0))
        tk.Label(bot_frame, text="MATH CONCEPTS DASHBOARD", font=('Helvetica', 10, 'bold'), fg=TEXT, bg=PANEL).pack(anchor='w', padx=15, pady=(10, 0))
        
        self.stats_text = tk.Text(bot_frame, font=('Courier', 10), fg=TEXT, bg=PANEL, relief='flat', height=6)
        self.stats_text.pack(fill='both', expand=True, padx=15, pady=10)

        self.build_rotate_params()
        self.switch_step("Rotate")
        self.update_stats("Ready. Load an image to begin.")

    def create_image_panel(self, parent, title, side):
        f = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        f.pack(side=side, fill='both', expand=True, padx=5)
        tk.Label(f, text=title, font=('Helvetica', 9, 'bold'), fg=DIMTXT, bg=PANEL).pack(pady=10)
        lbl = tk.Label(f, bg=BORDER, text="No Image", fg=DIMTXT, font=('Helvetica', 10))
        lbl.pack(fill='both', expand=True, padx=5, pady=(0, 5))
        return lbl

    def clear_params(self):
        for w in self.param_frame.winfo_children(): w.destroy()

    def lbl(self, text):
        tk.Label(self.param_frame, text=text, font=('Helvetica', 9), fg=TEXT, bg=PANEL, anchor='w').pack(fill='x', pady=(5, 0))

    def slider(self, var, lo, hi, step, start):
        var.set(start)
        tk.Scale(self.param_frame, variable=var, from_=lo, to=hi, resolution=step, orient='horizontal',
                 bg=PANEL, fg=TEXT, troughcolor=BORDER, highlightthickness=0, activebackground=DIMTXT).pack(fill='x', pady=(0, 5))

    def build_rotate_params(self):
        self.lbl("Angle (degrees)")
        self.angle_var = tk.DoubleVar()
        self.slider(self.angle_var, -180, 180, 1, 45)

    def build_scale_params(self):
        self.lbl("Scale X (%) [Higher = Zoom In]")
        self.scale_x_var = tk.IntVar()
        self.slider(self.scale_x_var, 10, 500, 5, 150)
        self.lbl("Scale Y (%) [Higher = Zoom In]")
        self.scale_y_var = tk.IntVar()
        self.slider(self.scale_y_var, 10, 500, 5, 150)

    def build_flip_params(self):
        self.lbl("Direction")
        self.flip_var = tk.StringVar(value="Horizontal")
        for opt in ["Horizontal", "Vertical", "Both"]:
            tk.Radiobutton(self.param_frame, text=opt, variable=self.flip_var, value=opt,
                           font=('Helvetica', 9), fg=TEXT, bg=PANEL, selectcolor=BG, activebackground=PANEL).pack(anchor='w')

    def build_compress_params(self):
        self.lbl("k-Components to keep (%)")
        self.compress_var = tk.IntVar()
        self.slider(self.compress_var, 1, 100, 1, 15)

    def switch_step(self, key):
        self.current_step.set(key)
        for k, b in self.step_btns.items():
            b.configure(bg=ACCENT if k == key else BG, font=('Helvetica', 10, 'bold' if k == key else 'normal'))
        
        self.clear_params()
        {'Rotate': self.build_rotate_params, 
         'Scale': self.build_scale_params,
         'Flip': self.build_flip_params, 
         'Compress': self.build_compress_params}[key]()

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not path: return
        img = Image.open(path).convert('RGB')
        self.original_image = np.array(img)
        self.show_image(self.lbl_orig, self.original_image)
        self.lbl_res.configure(image='', text='Click Apply to process')
        self.result_image = None
        self.update_stats(f"Loaded: {os.path.basename(path)}")

    def apply_step(self):
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
            
        step = self.current_step.get()
        try:
            img = self.original_image
            if step == 'Rotate':
                result, info = do_rotate(img, self.angle_var.get())
            elif step == 'Scale':
                # Divide by 100 to convert percentage to scalar (e.g. 150 = 1.5x zoom)
                result, info = do_scale(img, self.scale_x_var.get() / 100.0, self.scale_y_var.get() / 100.0)
            elif step == 'Flip':
                result, info = do_flip(img, self.flip_var.get())
            elif step == 'Compress':
                result, info = do_compress(img, self.compress_var.get())
                
            self.result_image = result
            self.show_image(self.lbl_res, result)
            self.update_stats(info)
        except Exception as err:
            import traceback
            messagebox.showerror("Error", str(err) + "\n\n" + traceback.format_exc())

    def save_result(self):
        if self.result_image is None: return
        path = filedialog.asksaveasfilename(defaultextension=".png", 
                                            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")],
                                            initialfile="result.png")
        if path:
            Image.fromarray(self.result_image).save(path)
            self.update_stats(f"Successfully Saved: {path}")

    def show_image(self, widget, arr):
        pil = Image.fromarray(arr.astype(np.uint8))
        pil.thumbnail((500, 500), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil)
        widget.configure(image=tk_img, text='')
        widget.image = tk_img

    def update_stats(self, text):
        self.stats_text.configure(state='normal')
        self.stats_text.delete('1.0', tk.END)
        self.stats_text.insert(tk.END, text)
        self.stats_text.configure(state='disabled')

if __name__ == '__main__':
    app = App()
    app.mainloop()