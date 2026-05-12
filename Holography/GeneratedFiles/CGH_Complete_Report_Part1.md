# Computer-Generated Holography with Metasurface — Complete Project Report (Part 1)

## Overview of the Complete Workflow

This report documents the full pipeline for designing and optimizing a phase-modulated metasurface for computer-generated holography (CGH) with RGB illumination at 480 THz, 560 THz, and 640 THz, reconstructing a 3D holographic image across 6 depth planes from 51 to 56 μm.

---

## Stage 1: Academic Research & Technical Background

### 1.1 Fundamentals of Computer-Generated Holography (CGH) with Metasurfaces

**What is CGH with Metasurfaces?**
Computer-Generated Holography (CGH) with metasurfaces combines algorithmic computation of holographic phase patterns with subwavelength-thin nanostructured surfaces (metasurfaces) that physically encode and reconstruct these patterns. Unlike traditional spatial light modulators (SLMs) with micron-scale pixels, metasurfaces achieve subwavelength resolution, offering:
- Wider field-of-view
- Higher diffraction efficiency
- Multi-functional wavefront control
- Compact form factor

### 1.2 Phase Modulation Mechanisms

Three primary mechanisms exist for phase modulation in metasurfaces:

**1. Propagation Phase (Dynamic Phase):**
When light propagates through a dielectric nanopillar of height H, the accumulated phase is:
```
φ_prop(λ) = (2π/λ) × n_eff(λ) × H
```
- Phase tuned by varying nanopillar width/length
- Height fixed to achieve 2π coverage
- Material: TiO₂ (n ≈ 2.4-2.6 at visible)

**2. Geometric Phase (Pancharatnam-Berry Phase):**
```
φ_PB = 2σθ
```
- σ = ±1 for circular polarization handedness
- θ = in-plane rotation angle
- Wavelength-independent geometric phase

**3. Combined Propagation + Geometric Phase:**
The key insight for RGB holography: combining both mechanisms enables independent phase control at different wavelengths:
```
φ_total(λ) = 2σθ + (2π/λ) × n_eff(W, L, λ) × H
```

### 1.3 CGH Optimization Algorithms

**Angular Spectrum Method (ASM)** — Most accurate propagation model:
```
U(x,y;z) = ℱ⁻¹{ ℱ{ U₀(x,y) } × H(fx, fy; z) }
where H(fx, fy; z) = exp(i × 2π/λ × z × √(1 - (λfx)² - (λfy)²))
```

**Gradient Descent (Adam Optimizer)** — The recommended approach:
- Formulate CGH as inverse optimization
- Minimize reconstruction loss (MSE, SSIM)
- Directly handles multi-plane and multi-wavelength objectives
- Uses automatic differentiation in PyTorch

### 1.4 Multi-Plane Holography

For multi-plane reconstruction, the total loss is:
```
ℒ(φ) = Σₙ wₙ × ℒₙ( |Propagate(exp(iφ), zₙ)|² , Iₙ )
```
where n indexes the depth planes and ℒₙ is the reconstruction error per plane.

### 1.5 RGB Color Handling

Three approaches for full-color metasurface holography:
1. **Spatial multiplexing** — Partition metasurface into color sub-arrays (1/3 pixel density per color)
2. **3D-integrated tandem metasurfaces** — Color filter array on top of hologram metasurface
3. **Single-celled wavelength-decoupled control** — Each cell independently controls R, G, B phases (full pixel density, recommended)

---

## Stage 2: Project Code Architecture Analysis

### 2.1 Overall Design Framework

The project implements an end-to-end differentiable pipeline in PyTorch for metasurface optimization. The key modules are:

```
main.py (Entry point with LLM Agent orchestration)
├── parameters.py (Configuration)
├── FrontNetwork.py (Amplitude generation)
├── AS.py (Angular Spectrum propagation)
├── DataFlow.py (Data processing pipeline)
├── LossFunction.py (Loss computation)
├── Optimizer.py (Optimization agent)
├── DatasetManager.py (Dataset management)
└── Simulator.py (CST simulation interface)
```

### 2.2 FrontNetwork.py — Amplitude Front-End

**Purpose:** Generates amplitude arrays at the metasurface plane for each incident frequency.

```python
class FrontEnd(nn.Module):
    def __init__(self, task):
        # For Holography: returns torch.ones(6, 3, N, N)
        # 6 = batch (depth planes), 3 = RGB channels, N×N = metasurface size
```

**Key insight for Holography task:** Since the metasurface is illuminated by plane waves (uniform amplitude), FrontNetwork returns all-ones arrays. The 6×3×N×N output means:
- 6 different depth planes (51-56 μm)
- Each evaluated at 3 RGB frequencies
- Uniform amplitude = plane wave illumination

### 2.3 AS.py — Angular Spectrum Method Propagator

**Purpose:** Implements scalar diffraction theory for light propagation from metasurface to focal plane.

```python
class ASM_propagate(nn.Module):
    def __init__(self, freq, z, refidx=1):
        # freq: incident frequency (THz)
        # z: propagation distance (μm)
        # Computes wavelength: λ = 3E-4/freq (m)
        #   where 3E-4 = c × 10⁻¹² (c=3×10⁸ m/s, and freq is in THz)
        #   e.g., 480 THz → λ = 3E-4/480 = 6.25×10⁻⁷ m = 625 nm
        # Builds transfer function H(fx, fy) in frequency domain
```

**Key parameters:**
- Meta-atom size: 160 nm (period)
- Grid size: 1024 × 1024 (N)
- Transfer function includes band-limiting to prevent aliasing

**Propagation equation:**
```
H(fx, fy; z) = exp(i × 2π/λ × z × √(1 - (λfx)² - (λfy)²))
```

**Forward pass:**
1. FFT of input field → frequency domain
2. Multiply by transfer function H
3. Band-limit mask application
4. Inverse FFT → output intensity |U|²

### 2.4 DataFlow.py — End-to-End Pipeline

**Purpose:** Wraps the entire optimization loop into a PyTorch Module for automatic differentiation.

```python
class MetaOptim(nn.Module):
    def __init__(self, task, frequencies):
        self.phase = nn.Parameter(torch.randn(N, N))  # Learnable phase
        self.frontNet = FrontEnd(task)
    
    def forward(self):
        # 1. Get amplitude input from FrontNetwork
        input = self.frontNet()  # [6, 3, 1024, 1024]
        
        # 2. For each depth plane and frequency:
        #    - Read phase-frequency relationship from simulation files
        #    - Apply phase to illumination amplitude
        #    - Propagate using ASM
        #    - Concatenate results
```

**Critical detail — Phase-frequency mapping:**
The meta-atom simulation provides relationships linking phase at different frequencies:
- φ_480 = Phase480 (base variable)
- φ_560 = 1.202 × Phase480 - 2.288
- φ_640 = 1.432 × Phase480 - 4.713

These linear relationships come from the CST simulation of the TiO₂ nanopillar (radius=50nm) on SiO₂ substrate with period 160nm.

### 2.5 LossFunction.py — Optimization Loss

**Purpose:** Computes the loss between reconstructed and target holograms.

**For Holography task:**
```python
def Holography(self, output):
    # Crop to central region (Meta_N × Meta_N = 512×512)
    output = crop(output)
    
    # Load target and mask
    target = trainData.pt  # Ground truth hologram slices
    mask = masks.pt        # Region mask
    
    # Apply mask and compute MSE loss
    output = output × mask
    loss = nn.MSELoss()(output, target)
```

**Key features:**
- **MSE Loss** — Direct pixel-wise comparison
- **Masking** — Only evaluates loss in regions with pattern content
- **Cropping** — Extracts central 512×512 region (Meta_N) from 1024×1024 full grid

---

## Stage 3: Meta-Atom Simulation

### 3.1 Simulation Setup

Before optimization, CST software simulated the TiO₂ nanopillar meta-atom:
- **Structure:** Cylindrical nanopillar
- **Radius:** 50 nm
- **Material:** TiO₂ (high index, low loss in visible)
- **Substrate:** SiO₂
- **Period:** 160 nm × 160 nm
- **Phase modulation:** By varying nanopillar height

### 3.2 Simulation Results

The simulation established linear phase relationships with respect to Phase480:

| Frequency (THz) | Wavelength (nm) | Phase Relationship |
|:---------------:|:---------------:|:------------------:|
| 480 | 625 | Phase480 (base) |
| 520 | 577 | 1.100 × Phase480 - 1.141 |
| 560 | 536 | 1.202 × Phase480 - 2.288 |
| 600 | 500 | 1.312 × Phase480 - 3.472 |
| 640 | 469 | 1.432 × Phase480 - 4.713 |
| 680 | 441 | 1.553 × Phase480 - 6.022 |
| 720 | 417 | 1.691 × Phase480 - 7.398 |

For the RGB CGH task, we use **480 THz (R)**, **560 THz (G)**, and **640 THz (B)** — spanning the visible spectrum from red to blue.

### 3.3 Physical Interpretation

The linear phase relationship has two components:
1. **Slope > 1** (1.202, 1.432): Represents dispersive propagation phase — higher frequencies (shorter λ) experience more phase change per unit height change
2. **Intercept** (-2.288, -4.713): Represents the initial phase offset at zero height, capturing material dispersion and geometric effects

This dispersion is essential for wavelength-multiplexed holography: the same metasurface encodes different phase patterns for different colors.

