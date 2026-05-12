# Computer-Generated Holography (CGH) with Metasurfaces — Comprehensive Technical Report

## Part 1: Fundamentals of Phase-Modulated Metasurfaces for Holography

---

### 1. Introduction

Computer-generated holography (CGH) with metasurfaces combines two powerful technologies: (1) algorithmic computation of holographic phase patterns, and (2) subwavelength-thin nanostructured surfaces (metasurfaces) that physically encode and reconstruct these phase patterns. Unlike traditional spatial light modulators (SLMs) which have pixel pitches on the order of microns, metasurfaces can achieve subwavelength resolution, offering wider field-of-view, higher diffraction efficiency, and multi-functional wavefront control.

This report covers how to design phase-modulated metasurfaces for RGB holography, the relationship between meta-atom geometry and optical response, multi-plane techniques, optimization algorithms, and RGB color handling.

---

### 2. Phase Modulation Mechanisms in Metasurfaces

There are three primary mechanisms for imparting phase shifts in metasurfaces:

#### 2.1 Propagation Phase (Dynamic Phase)

**Physical principle:** When light propagates through a dielectric nanopillar (or nanostructure) of height H and effective refractive index n_eff(λ), it accumulates a phase shift given by:

```
φ_prop(λ) = (2π / λ) × n_eff(λ) × H
```

Where:
- λ = free-space wavelength
- H = physical height of the nanopillar
- n_eff(λ) = effective refractive index of the waveguide mode supported by the pillar

**Design parameters:** For a given material, the phase is tuned by varying the **width (W)** and **length (L)** of the nanopillar while keeping the height H fixed. As W and L change, the modal confinement changes, altering n_eff.

- Typical materials: TiO₂ (n ~ 2.4-2.6 at visible), SiN (n ~ 2.0-2.2), a-Si (n ~ 3.5 at near-IR)
- Height H is typically chosen to achieve 2π phase coverage: H ≈ λ₀ / (n_max - n_min)
- For TiO₂ at λ = 532 nm: H ≈ 600-900 nm provides full 2π coverage

**Key equation for full-wave (RCWA/FDTD) design:**
```
Phase coverage condition:  Δφ = (2π/λ) × H × (n_eff_max - n_eff_min) ≥ 2π
```

#### 2.2 Geometric Phase (Pancharatnam–Berry / PB Phase)

**Physical principle:** When circularly polarized light passes through a half-wave plate-like nano-structure, the transmitted cross-circularly polarized component acquires a geometric phase equal to twice the rotation angle θ of the fast axis:

```
φ_PB = 2σθ
```

Where:
- σ = ±1 for LCP/RCP incident light
- θ = in-plane rotation angle of the meta-atom

**Advantages:**
- Phase is independent of wavelength (geometric, not dispersive)
- Simple design: only one structural parameter (θ) needed
- Continuous 0 to 2π phase control

**Limitations:**
- Requires circular polarization → polarization-dependent
- Theoretical maximum efficiency: 100% for ideal half-wave plate; practical: ~80-95%
- Same geometric phase for all wavelengths — cannot independently control RGB phases with PB phase alone

#### 2.3 Combined Propagation + Geometric Phase (Wavelength-Decoupled)

**Breakthrough concept (Yoon et al., 2019, Communications Physics):**
By combining both propagation phase and geometric phase in a single rectangular dielectric nanostructure, one can achieve **independent phase control at two different wavelengths**:

```
For a rectangular nanopillar with dimensions (W, L, H) and rotation θ:

Output field for incident wavelength λᵢ:
E_out ∝ exp[i × φ_PB(λᵢ) + i × φ_prop(λᵢ, W, L, H)]

Where:
- φ_PB(λᵢ) = 2σθ (same for all λ — geometric)
- φ_prop(λᵢ) = (2π/λᵢ) × n_eff(W, L, λᵢ) × H (wavelength-dependent)
```

The key insight: since the propagation phase φ_prop has different values at different wavelengths for the same nanostructure geometry, one can solve for (W, L, H, θ) that simultaneously satisfies two desired phase targets:

```
At λ₁: φ_target(λ₁) = 2σθ + (2π/λ₁) × n_eff(W, L, λ₁) × H
At λ₂: φ_target(λ₂) = 2σθ + (2π/λ₂) × n_eff(W, L, λ₂) × H
```

This is the foundation for single-celled **RGB** metasurface holography.

---

### 3. The Meta-Atom Library Design Workflow

The standard workflow for designing a metasurface hologram:

#### Step 1: Material Selection
| Material | Bandgap | n (visible) | Fabrication | Best for |
|----------|---------|-------------|-------------|----------|
| TiO₂ | 3.2 eV | ~2.4-2.6 | ALD + etching | Visible (high index, low loss) |
| SiN | 5.0 eV | ~2.0-2.2 | PECVD + etching | Visible (transparent) |
| a-Si | 1.7 eV | ~3.5-4.0 | Deposition + etching | Near-IR (absorbs in blue) |
| GaN | 3.4 eV | ~2.3-2.5 | Epitaxy + etching | Visible (blue/green LEDs) |

#### Step 2: FDTD/RCWA Simulation of Meta-Atom Library
Simulate a unit cell with periodic boundary conditions for each combination of geometry parameters:

```
For each (W_i, L_j) pair in the design space:
    For each wavelength λ_k in {R, G, B}:
        Compute complex transmission: t_ij(λ_k) = A_ij × exp(i × φ_ij)
    Store in HDF5 database
```

- Typical grid: W and L from 50 nm to 500 nm in steps of 5-10 nm
- Period P (pitch) is fixed (e.g., P = 300-400 nm for visible)
- Height H is fixed (e.g., 600 nm for TiO₂ at visible)
- Computational cost: ~10,000-50,000 individual FDTD simulations

#### Step 3: Phase Matching
For each meta-atom position (x, y) with desired phase φ_desired(λ):
```
Find (W, L, θ) in the library that minimizes:
    Error = Σ_k w_k × |exp(i × φ_sim(W, L, θ, λ_k)) - exp(i × φ_desired(λ_k))|²
```
Where w_k are wavelength weights.

#### Step 4: Layout Generation
Generate GDSII layout with the selected meta-atoms arranged at their positions with appropriate rotations.

---

