# CORRECTED REPORT: RGB Metalens Part 1 - Background & Project Analysis

## 1. Executive Summary (CORRECTED)

This report documents the complete design, optimization, and analysis of an **RGB metalens** that focuses red (480 THz), green (560 THz), and blue (640 THz) light at distinct positions on the focal plane. The metalens has a focal length of 70 μm and separates the colors by ±64 μm along the y-axis on the focal plane.

### CORRECTION NOTE: Color-Frequency Mapping

The frequencies in this design correspond to the following physical colors:
| Frequency | Wavelength (c/f) | Actual Color | User's Label |
|-----------|------------------|-------------|-------------|
| **480 THz** | 625 nm | **Red** | Requested "red" |
| **560 THz** | 536 nm | **Green** | Requested "green" |
| **640 THz** | 469 nm | **Blue** | Requested "blue" |

This was incorrectly reported in the initial version where 480 THz was called "blue" and 640 THz was called "red". The mapping is now corrected.

### Corrected Design Specifications

| Parameter | Value |
|-----------|-------|
| **Task Type** | RGB Metalens (Focus) |
| **Focal Length** | 70 μm |
| **Operating Frequencies** | 480 THz (Red), 560 THz (Green), 640 THz (Blue) |
| **Corresponding Wavelengths** | 625 nm (Red=480 THz), 536 nm (Green=560 THz), 469 nm (Blue=640 THz) |
| **Red Focus (480 THz)** | (x=0, y=-64 μm) |
| **Green Focus (560 THz)** | (x=0, y=0 μm) - Center |
| **Blue Focus (640 THz)** | (x=0, y=+64 μm) |
| **Metasurface Grid** | 1024 × 1024 (full aperture), central 512×512 evaluated |
| **Meta-atom Period** | 160 nm × 160 nm |
| **Physical Aperture** | 163.84 μm × 163.84 μm |
| **Numerical Aperture (NA)** | ~0.76 (full aperture: R=81.92 μm, f=70 μm) |
| **Meta-atom Material** | TiO₂ nanopillar on SiO₂ substrate |
| **Phase Modulation** | Nanopillar height tuning (radius = 50 nm) |

---

## 2. Academic Research and Theoretical Background (Unchanged - theory is correct)

[Content from original Part 1, Sections 2.1-2.3 remains valid as the physics principles are correct independent of color labeling.]

### Key Physical Principles (Reviewd and Confirmed)

1. **Generalized Snell's Law:** The phase gradient dφ/dx across the metasurface determines the wavefront bending angle.

2. **Hyperbolic Phase Profile for Focusing:** To focus an incident plane wave to a point (xf, yf, f):
   ```
   φ(x,y;λ) = -(2π/λ)·(√((x-xf)² + (y-yf)² + f²) - f)
   ```

3. **Propagation Phase Control:** φ_prop(x,y) = (2π/λ₀)·h·n_eff(x,y)

4. **Phase Dispersion Engineering:** Different frequencies experience different phase shifts due to dispersion.

---

## 3. Project Codebase Analysis (Updated with NA clarification)

### 3.1 File Architecture

[Same as original - no changes needed to file listing.]

### 3.2 Key Module: AS.py - Angular Spectrum Method

The `ASM_propagate` class implements diffraction-limited wave propagation:

```python
class ASM_propagate(nn.Module):
    def __init__(self, freq, z, refidx=1):
        self.input_size = [N, N]  # N = 1024
        self.z = z * 1e-6          # propagation distance in meters
        self.pixelsize = 160e-9    # 160 nm
        self.lamda = 3E-4/freq     # wavelength from frequency
        # self.H: propagation transfer function
        # self.freqmask: band-limit anti-aliasing filter
```

**Key insight about ASM resolution:** The output plane has the same pixel size (160 nm) and grid size (1024×1024) as the input plane. This means:
- Total output field of view: 1024 × 160 nm = 163.84 μm
- The central 512×512 region (cropped for loss evaluation) covers 81.92 μm × 81.92 μm

### 3.3 Key Module: DataFlow.py - Optimization Pipeline

The `MetaOptim` class orchestrates the optimization with these critical details:

**Frequency order matters:** `self.frequencies = sorted(frequencies)` → [480, 560, 640] THz
- c=0 → 480 THz (Red, 625 nm) → compared against target channel 0 (y=-64)
- c=1 → 560 THz (Green, 536 nm) → compared against target channel 1 (y=0)  
- c=2 → 640 THz (Blue, 469 nm) → compared against target channel 2 (y=+64)

**Phase coupling mechanism:**
```python
# For each frequency c, the phase is computed as:
with open(f"MetaAtom/func_{freq[c]}.txt", "r") as file:
    phase = eval(file.read().replace("Phase480", "self.phase"))
# This creates:
# For 480 THz: phase = self.phase (identity)
# For 560 THz: phase = 1.202*self.phase - 2.288
# For 640 THz: phase = 1.432*self.phase - 4.713
```

### 3.4 Key Module: LossFunction.py - Training Objective

The Focal Loss function is used:
```python
loss = FocalLoss()(output/30000, target)
```

The output (1024×1024) is cropped to the central 512×512 (Meta_N × Meta_N) before loss computation.

### 3.5 Key Module: Performance.py - FWHM Evaluation

The FWHM is computed from a 1D vertical slice through the focal spot peak:
```python
idx = torch.argmax(self.output[0,i])  # find peak position
x, y = torch.unravel_index(idx, self.output[0,i].shape)
FWHM.append(func_FWHM(self.output[0,i,:,y]))
```

The FWHM function (AI-generated via Coder agent) uses **160 nm pixel spacing** and returns FWHM in nanometers.

### 3.6 NA Clarification

The metasurface phase array is 1024×1024, corresponding to an active area of 163.84 μm × 163.84 μm. The **effective lens radius** is:
- R = 512 × 160 nm = 81.92 μm (from center to edge of the 1024 grid)
- f = 70 μm
- NA = R / √(R² + f²) = 81.92 / √(81.92² + 70²) = 81.92 / 107.75 ≈ **0.76**

**Important nuance:** The loss function only evaluates the central 512×512 region of the focal plane. However, the full 1024×1024 metasurface contributes to the diffraction pattern. The outer annulus (between radius 256 and 512 in the meta-atom grid) diffracts light to the outer regions of the focal plane that are cropped away — these regions are not directly optimized but still affect the focal spot through diffraction.

