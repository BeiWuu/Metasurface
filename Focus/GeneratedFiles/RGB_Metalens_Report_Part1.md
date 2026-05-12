# Comprehensive RGB Metalens Design Report - Part 1: Background & Project Analysis

## 1. Executive Summary

This report documents the complete design, optimization, and analysis of an **RGB metalens** that focuses red (640 THz), green (560 THz), and blue (480 THz) light at distinct positions on the focal plane. The metalens has a focal length of 70 μm and separates the colors by ±64 μm along the y-axis on the focal plane.

**Design Specifications:**
| Parameter | Value |
|-----------|-------|
| **Task Type** | RGB Metalens (Focus) |
| **Focal Length** | 70 μm |
| **Operating Frequencies** | 480 THz (Blue), 560 THz (Green), 640 THz (Red) |
| **Corresponding Wavelengths** | 625 nm (Red), 535.7 nm (Green), 468.75 nm (Blue) |
| **Red Focus (640 THz)** | (x=0, y=-64 μm) |
| **Green Focus (560 THz)** | (x=0, y=0 μm) - Center |
| **Blue Focus (480 THz)** | (x=0, y=+64 μm) |
| **Metasurface Grid** | 1024 × 1024 (512 × 512 active) |
| **Meta-atom Period** | 160 nm × 160 nm |
| **Meta-atom Material** | TiO₂ nanopillar on SiO₂ substrate |
| **Phase Modulation** | Nanopillar height tuning (radius = 50 nm) |

---

## 2. Academic Research and Theoretical Background

### 2.1 RGB Metalens Principles

An **RGB metalens** is an ultra-thin planar optical device based on a metasurface — an array of subwavelength nanostructures (meta-atoms) — engineered to control red, green, and blue light simultaneously. The central challenge is chromatic aberration: conventional metalenses focus different wavelengths at different focal lengths because the required phase profile scales as 1/λ.

**Key Physical Principles:**

1. **Generalized Snell's Law:** The phase gradient dφ/dx across the metasurface determines the wavefront bending angle via:
   ```
   sin(θt)·nt - sin(θi)·ni = (λ/2π)·dφ/dx
   ```

2. **Hyperbolic Phase Profile for Focusing:** To focus an incident plane wave to a point (xf, yf, f):
   ```
   φ(x,y;λ) = -(2π/λ)·(√((x-xf)² + (y-yf)² + f²) - f)
   ```
   This converts the planar wavefront into a converging spherical wavefront.

3. **Propagation Phase Control:** When light passes through TiO₂ nanopillars, the effective wavelength inside the material is reduced, introducing a phase delay:
   ```
   φ_prop(x,y) = (2π/λ₀)·h·n_eff(x,y)
   ```
   where h is the pillar height and n_eff depends on the cross-sectional geometry.

4. **Phase Dispersion Engineering:** Different frequencies experience different phase shifts due to dispersion in the meta-atom's effective index. This dispersion can be exploited to simultaneously satisfy phase conditions at multiple wavelengths.

### 2.2 Design Strategy for This Project

This project uses a **single-layer metasurface** with propagation phase control, where the phase at each meta-atom position is optimized via gradient descent. The key innovation is that:

- The metasurface phase array is a **learnable parameter** optimized through backpropagation
- The Angular Spectrum Method (ASM) models wave propagation from metasurface to focal plane
- A Focal Loss function drives the optimization toward the desired focal spots
- The phase relationships between different frequencies (determined via CST simulation) couple the RGB responses

### 2.3 Relevant References

1. Z. Li et al., "Meta-optics achieves RGB-achromatic focusing for virtual reality," *Science Advances* 7, eabe4458 (2021).
2. J. Zhang et al., "RGB Achromatic Metalens Doublet for Digital Imaging," *Nano Letters* 22, 3969-3975 (2022).
3. W. T. Chen et al., "A broadband achromatic metalens for focusing and imaging in the visible," *Nature Nanotechnology* 13, 220-226 (2018).
4. M. Khorasaninejad et al., "Achromatic Metalens over 60 nm Bandwidth in the Visible," *Nano Letters* 17, 1819-1824 (2017).
5. S. Wang et al., "Broadband achromatic optical metasurface devices," *Nature Communications* 8, 187 (2017).

---

## 3. Project Codebase Analysis

### 3.1 File Architecture

The project is organized as follows (base: `D:\work\MetaDesign\Metasurface\`):

| File | Purpose |
|------|---------|
| **main.py** | Orchestrator: manages solver, verifier, and correction agents |
| **parameters.py** | Global configuration: N=1024, Meta_N=512, meta_atom_size=160nm |
| **AS.py** | Angular Spectrum Method propagation module |
| **DataFlow.py** | Main optimization pipeline (MetaOptim class) |
| **FrontNetwork.py** | Front-end network: Focus (uniform), Holography, Generator |
| **LossFunction.py** | Loss functions: FocalLoss, OptimLoss |
| **Coder.py** | Code generation agent for neural networks |
| **Optimizer.py** | Optimization agent |
| **Researcher.py** | Research agent |
| **Performance.py** | Performance evaluation |
| **Simulator.py/.pyc** | CST simulation interface |
| **DatasetManager.py** | Dataset creation tools |
| **FileManager.py** | File I/O management |
| **Visualization.py** | Visualization utilities |
| **Focus/** | Focus task data and saved models |
| **Holography/** | Holography task data |
| **Generator/** | Generator task data (content/style images) |
| **MetaAtom/** | Meta-atom simulation data and phase functions |

### 3.2 Key Module: AS.py - Angular Spectrum Method

The `ASM_propagate` class implements diffraction-limited wave propagation:

```python
class ASM_propagate(nn.Module):
    def __init__(self, freq, z, refidx=1):
        # self.H: propagation transfer function in frequency domain
        # self.freqmask: band-limit filter to prevent aliasing
    
    def forward(self, waves, use_freqmask=True):
        spectrum = torch.fft.fftshift(torch.fft.fft2(waves))
        spectrum_z = spectrum * self.H
        spectrum_z = spectrum_z * self.freqmask  # anti-aliasing
        wave_z = torch.fft.ifft2(torch.fft.ifftshift(spectrum_z))
        return |wave_z|²  # Intensity
```

The transfer function is:
```
H(fx, fy) = exp(j·2π·z·√((n/λ)² - fx² - fy²))
```

### 3.3 Key Module: DataFlow.py - Optimization Pipeline

The `MetaOptim` class orchestrates the entire optimization:

1. **Phase Parameter:** A learnable 1024×1024 phase array (center 512×512 active)
2. **Front Network:** For Focus task, generates uniform amplitude (ones) for all frequencies
3. **Propagation:** For each frequency, applies ASM propagation to focal plane
4. **Multi-frequency Loop:** Iterates over all RGB frequencies, loading appropriate phase models

### 3.4 Key Module: LossFunction.py - Training Objective

For the **Focus** task, `FocalLoss` is used:
```python
def FocalLoss(self, alpha=0.5, gamma=2):
    # Modified focal loss for precise single-pixel focal spots
    BCE_loss = binary_cross_entropy(output/30000, target)
    pt = exp(-BCE_loss)
    F_loss = alpha·(1-pt)^gamma·BCE_loss
```

The Focal Loss emphasizes hard-to-classify pixels, sharpening the focal spots.

### 3.5 Key Module: FrontNetwork.py - Input Generation

For the **Focus** task, the front-end generates uniform plane wave illumination:
```python
def Focus(self):
    return torch.ones(1, 3, kwargs["N"], kwargs["N"])
```

This simulates a uniform plane wave incident on the metasurface, with equal amplitude for all three RGB frequencies.

