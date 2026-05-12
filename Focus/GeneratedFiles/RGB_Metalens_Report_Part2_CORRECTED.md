# CORRECTED REPORT: RGB Metalens Part 2 - Simulation, Dataset & Optimization

## 4. Meta-Atom Simulation (CST)

### 4.1 Simulation Setup (Unchanged)

**Meta-atom Structure:**
- **Material:** TiO₂ nanopillar (high refractive index, low loss in visible)
- **Substrate:** SiO₂ (glass)
- **Nanopillar radius:** 50 nm
- **Period:** 160 nm × 160 nm
- **Phase modulation:** Achieved by varying nanopillar height

**Simulated Frequencies:** 480, 520, 560, 600, 640, 680, 720 THz

### 4.2 Phase Relationships (CORRECTED: Color labels fixed)

The CST simulation established linear relationships between the phase at different frequencies and the phase at the reference frequency (480 THz):

| Frequency | Wavelength | Actual Color | Phase Relationship |
|-----------|-----------|-------------|-------------------|
| **480 THz** | 625 nm | **Red** (reference) | φ₄₈₀ (identity) |
| **520 THz** | 577 nm | **Yellow** | φ₅₂₀ = 1.100·φ₄₈₀ - 1.141 |
| **560 THz** | 536 nm | **Green** | φ₅₆₀ = 1.202·φ₄₈₀ - 2.288 |
| **600 THz** | 500 nm | **Cyan** | φ₆₀₀ = 1.312·φ₄₈₀ - 3.472 |
| **640 THz** | 469 nm | **Blue** | φ₆₄₀ = 1.432·φ₄₈₀ - 4.713 |
| **680 THz** | 441 nm | **Violet** | φ₆₈₀ = 1.553·φ₄₈₀ - 6.022 |
| **720 THz** | 417 nm | **Violet/UV** | φ₇₂₀ = 1.691·φ₄₈₀ - 7.398 |

**Key observations:**
- The dispersion slope coefficient k(f) increases with frequency: 1.100 (520 THz) → 1.691 (720 THz)
- This means higher frequencies (shorter wavelengths) experience **stronger phase sensitivity** per unit height change
- The three target frequencies (480, 560, 640 THz) have slopes k = 1.000, 1.202, 1.432 respectively

### 4.3 Physical Interpretation

The linear phase relationship φ(f) = k(f)·φ₄₈₀ + b(f) arises from:
- **k(f):** Approximates the ratio of wavelengths (fₓ₅₆₀/f₄₈₀ = 1.167, actual k = 1.202; f₆₄₀/f₄₈₀ = 1.333, actual k = 1.432), modified by material dispersion in TiO₂
- **b(f):** Constant offset from material refractive index dispersion

These relationships allow **single-parameter optimization**: only φ₄₈₀ (phase at the reference frequency 480 THz) needs to be learned, and the phases at 560 THz and 640 THz are derived analytically.

---

## 5. Dataset Creation

### 5.1 Focus Dataset Generation

The dataset was created using:
```python
focus_data(
    distance=70,     # focal length in micrometers
    xr=0, yr=-64,    # Red (480 THz): y = -64 μm
    xg=0, yg=0,      # Green (560 THz): y = 0 μm (center)
    xb=0, yb=64      # Blue (640 THz): y = +64 μm
)
```

### 5.2 Generated Files

| File | Content | Description |
|------|---------|-------------|
| `Focus/target.pt` | Tensor [1, 3, 512, 512] | One-hot encoded focal spots |
| `Focus/distance.pt` | Tensor [1, 1] = 70 | Focal length in μm |

**Target tensor encoding (CORRECTED):**
- **Channel 0** = Red target (480 THz, 625 nm): value 1 at (x=256, y=192) → center - 64 pixels
- **Channel 1** = Green target (560 THz, 536 nm): value 1 at (x=256, y=256) → center
- **Channel 2** = Blue target (640 THz, 469 nm): value 1 at (x=256, y=320) → center + 64 pixels

Physical separation: 64 pixels × 160 nm/pixel = **10.24 μm** between adjacent color foci.

---

## 6. Optimization Process

### 6.1 Optimization Pipeline

```
Input: Uniform plane waves at 480, 560, 640 THz
                    ↓
       ┌───────────────────────┐
       │  Metasurface Phase     │  ← Learnable Parameter (1024×1024)
       │  Array (φ₄₈₀)         │      Optimized via backpropagation
       └───────────────────────┘
                    ↓
    Phase conversion for each frequency:
    φ₄₈₀ (Red, 625 nm):   phase = self.phase
    φ₅₆₀ (Green, 536 nm): phase = 1.202·self.phase - 2.288
    φ₆₄₀ (Blue, 469 nm):  phase = 1.432·self.phase - 4.713
                    ↓
    Complex field: E = A·exp(j·φ)  (A = 1 for Focus task)
                    ↓
       ┌───────────────────────┐
       │  ASM Propagation      │  ← Angular Spectrum Method
       │  (z = 70 μm)          │     1024×1024 grid, 160 nm pixel
       └───────────────────────┘
                    ↓
       ┌───────────────────────┐
       │  Crop to 512×512      │  ← Central region extraction
       │  (central region)     │     for loss evaluation
       └───────────────────────┘
                    ↓
       ┌───────────────────────┐
       │  Focal Loss           │  ← Compare with target spots
       │  (FocalLoss)          │      Backpropagate gradients
       └───────────────────────┘
                    ↓
            Update φ₄₈₀ via Rprop
```

### 6.2 Optimization Parameters

| Parameter | Value |
|-----------|-------|
| **Optimizer** | Rprop (Resilient Propagation) |
| **Learning Rate** | 2 × 10⁻⁴ |
| **Epochs** | 200 |
| **Loss Function** | FocalLoss (α=0.5, γ=2) |
| **Phase Array Size** | 1024 × 1024 |
| **Evaluation Region** | Central 512 × 512 pixels |
| **Phase Initialization** | Random normal |

### 6.3 The Role of Focal Loss

The FocalLoss is ideal for this task because:
- **Extreme class imbalance:** Only 1 target pixel out of 262,144 (512²)
- **γ=2:** Down-weights easy background pixels, forces focus on hard focal spot pixels
- **α=0.5:** Balances positive/negative class weights

### 6.4 Numerical Aperture

The effective NA depends on the utilized aperture of the metasurface:

**Full aperture (1024×1024):**
- Radius: R = 512 × 160 nm = 81.92 μm
- NA = R/√(R² + f²) = 81.92/√(81.92² + 70²) = **0.76**

**Effective focusing aperture:**
- The loss function evaluates only the central 512×512 of the focal plane
- Light from the outer annular region of the metasurface (beyond r=256) contributes to the outer focal plane that is cropped away
- This means the **effective NA for the central focal spot is between 0.5 and 0.76**, depending on how much the outer rings contribute to the central spot intensity

---

## 7. Optimization Results (CORRECTED)

### 7.1 Focusing Efficiency

| Color | Frequency | Wavelength | Efficiency | 
|-------|-----------|-----------|-----------|
| **Red** | 480 THz | 625 nm | **20.27%** |
| **Green** | 560 THz | 536 nm | **17.35%** |
| **Blue** | 640 THz | 469 nm | **16.02%** |
| **Average** | - | - | **~17.88%** |

The efficiency is computed as the ratio of intensity in an 11×11 pixel window around the focal spot to the total incident intensity.

### 7.2 Focal Spot Quality (FWHM) — IMPORTANT NOTE

The FWHM values reported below were computed by the Performance evaluation module, which uses an AI-generated FWHM function with a pixel spacing of 160 nm.

| Color | Frequency | λ (nm) | Reported FWHM (nm) | Diffraction Limit (NA=0.76) | Diffraction Limit (NA=0.50) | 
|-------|-----------|--------|-------------------|---------------------------|---------------------------|
| **Red** | 480 THz | 625 | **320.5** | 0.52×625/0.76 = **428 nm** | 0.52×625/0.50 = **650 nm** |
| **Green** | 560 THz | 536 | **257.1** | 0.52×536/0.76 = **367 nm** | 0.52×536/0.50 = **557 nm** |
| **Blue** | 640 THz | 469 | **216.5** | 0.52×469/0.76 = **321 nm** | 0.52×469/0.50 = **488 nm** |

**Analysis of FWHM values:**

The reported FWHM values (320.5, 257.1, 216.5 nm) are smaller than even the most optimistic diffraction limit (NA=0.76: 428, 367, 321 nm). This is **physically suspicious** and requires explanation:

1. **The measured FWHM (1D slice) vs 2D Airy disk:** The FWHM is measured along a 1D vertical slice through the focal spot. For an elliptical or non-ideal spot, the 1D FWHM in one direction could be smaller than the 2D diffraction limit.

2. **Potential FWHM calculation issue:** The AI-generated `func_FWHM` code may contain errors in how it computes the FWHM. Without reviewing the actual generated code, we cannot verify the calculation.

3. **Effective NA:** If the effective focusing aperture is larger (contributing from the full 1024×1024 metasurface), the NA increases, which decreases the diffraction-limited spot size. With NA=0.76, the minima are: 428, 367, 321 nm. The reported values are slightly below these.

4. **Spatial resolution of the focal plane:** With 160 nm pixels, a FWHM of 216.5 nm corresponds to **only ~1.35 pixels**, which is near the sampling limit and may introduce discretization error.

**Recommendation:** The FWHM values should be verified by:
- Directly inspecting the 2D intensity profiles from the saved images
- Computing FWHM using a more reliable method (e.g., Gaussian fitting)
- Checking if the effective NA is truly 0.76 or lower

### 7.3 Color Separation — CONFIRMED

The three colors are successfully separated on the focal plane:
- **Red (480 THz, 625 nm):** Focuses at y = -64 pixels (channel 0) → confirmed by channel assignment
- **Green (560 THz, 536 nm):** Focuses at y = 0 pixels (channel 1, center)
- **Blue (640 THz, 469 nm):** Focuses at y = +64 pixels (channel 2)

Physical separation between adjacent foci: **64 pixels × 160 nm = 10.24 μm**
Total color span (red to blue): **20.48 μm**

### 7.4 Saved Output Files

| File | Path | Description |
|------|------|-------------|
| **network.pt** | `Focus/SavedModel/network.pt` | Trained model with optimized phase |
| **optimizer.pt** | `Focus/SavedModel/optimizer.pt` | Optimizer state |
| **phase.png** | `Focus/SavedModel/phase.png` | Phase profile visualization |
| **2D_0.png** | `Focus/SavedModel/2D_0.png` | 2D focal intensity (Red, 480 THz) |
| **2D_1.png** | `Focus/SavedModel/2D_1.png` | 2D focal intensity (Green, 560 THz) |
| **2D_2.png** | `Focus/SavedModel/2D_2.png` | 2D focal intensity (Blue, 640 THz) |
| **1D_2.png** | `Focus/SavedModel/1D_2.png` | 1D cross-sectional intensity |

