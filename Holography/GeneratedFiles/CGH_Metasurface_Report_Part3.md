# Computer-Generated Holography (CGH) with Metasurfaces — Technical Report

## Part 3: Multi-Plane Holography & RGB Color Handling

---

### 5. Multi-Plane Holography Techniques

Multi-plane holography aims to reconstruct different images at multiple depth planes (z₁, z₂, ..., z_N) from a single metasurface.

#### 5.1 Layer-Based CGH

The standard approach decomposes the 3D scene into N discrete depth layers.

**Forward model:** The total field at the metasurface plane is the sum of back-propagated fields from each target plane:

```
Given target images I₁, I₂, ..., I_N at depths z₁, z₂, ..., z_N:

For optimization, the reconstruction error is:
ℒ = Σₙ wₙ × MSE( |Propagate(exp(iφ), zₙ)|² , Iₙ )
```

**Key algorithms:**

**(a) Multi-plane GS (MP-GS):**
```
Initialize φ randomly
for iteration k:
    for each plane n = 1 to N:
        Propagate to plane n
        Apply amplitude constraint with Iₙ
        Back-propagate to hologram plane
    Average all N back-propagated fields
    Extract phase φₖ₊₁
```

**Limitation:** Speckle noise accumulates, and crosstalk between planes is hard to suppress.

**(b) Gradient descent for multi-plane (recommended):**
```
Minimize: ℒ(φ) = Σₙ wₙ × ℒ_n( |Propagate(exp(iφ), zₙ)|² , Iₙ )
```
Optimize with Adam directly — the gradient naturally accounts for all planes.

**(c) Point-cloud CGH:**
For sparse 3D scenes where the target is a set of 3D points:
```
U_hologram(x,y) = Σ_j A_j / r_j × exp(i × (2π/λ) × r_j)

where r_j = √[(x - x_j)² + (y - y_j)² + z_j²]
```
The phase is then extracted: φ = angle(U_hologram).

#### 5.2 Depth-Division Multiplexing for Metasurfaces

A technique specifically for metasurfaces where different wavelengths are assigned to different depths:

```
For RGB colors at depths z_R, z_G, z_B:
    φ_R(x,y) = CGH(I_R, λ_R, z_R)   # Phase for red channel at depth z_R
    φ_G(x,y) = CGH(I_G, λ_G, z_G)   # Phase for green channel at depth z_G
    φ_B(x,y) = CGH(I_B, λ_B, z_B)   # Phase for blue channel at depth z_B
    
    Combined: φ_total = angle(Σ exp(i × φ_c))
    Or: encode separate RGB holograms in spatial interleaving
```

#### 5.3 Angular Spectrum Layer-Oriented Method

```
For each depth layer n:
    1. Compute complex field: Uₙ = Aₙ × exp(i × φ_random)
    2. Propagate to hologram plane: U_hologram_n = Propagate(Uₙ, -zₙ, λ)
Total hologram field: U_total = Σ U_hologram_n
Phase: φ = angle(U_total)
```

Then optimize to minimize total reconstruction error.

---

### 6. RGB Color Handling in Metasurface Holography

Three primary approaches exist for full-color metasurface holography:

#### 6.1 Approach 1: Spatial Multiplexing / Interleaving

**Concept:** Partition the metasurface into sub-arrays, each responsible for one color channel.

```
Metasurface layout:
R | G | B | R | G | B | ...
G | B | R | G | B | R | ...
B | R | G | B | R | G | ...
(Each sub-pixel corresponds to one wavelength channel)
```

**Advantages:** Simple design, each sub-array optimized for one wavelength.

**Disadvantages:**
- **Resolution penalty:** Only 1/3 of pixels used per color → 3× lower pixel density
- **Inter-channel crosstalk** from diffraction between sub-pixels
- Strict alignment required

**Example from literature:** RGB interleaved unit cells, each pre-designed for λ = 450, 532, 633 nm respectively.

#### 6.2 Approach 2: 3D-Integrated Tandem Metasurfaces

**Concept (Hu et al. 2019, Light: Science & Applications):** Vertically stack a color-filter microarray on top of a hologram metasurface layer.

```
Layer 1 (top):    Fabry-Pérot cavity color filters (R, G, B pixels)
Layer 2:          Spacer layer
Layer 3 (bottom): TiO₂ nanofin hologram metasurface
```

**Operating principle:**
1. White light (or separate RGB lasers) illuminates the top color filter array
2. Each filter transmits only one wavelength band
3. The transmitted light reaches the bottom hologram metasurface
4. The metasurface encodes three independent CGH phase patterns

**Advantages:**
- Each filter acts as a wavelength-selective aperture, naturally separating colors
- Can work with white light illumination
- Compact integrated device

**Disadvantages:**
- Complex multi-layer fabrication (alignment between layers)
- Absorption loss in filters
- Limited by filter spectral bandwidth

#### 6.3 Approach 3: Single-Celled Metasurface with Wavelength-Decoupled Phase Control (Recommended)

**Concept (Yoon et al., 2019; Zhang et al., 2024; Ouyang et al., 2025):** Design each unit cell (single nanostructure) to simultaneously provide independent phase shifts at R, G, and B wavelengths.

**Wavelength-decoupled phase principle:**
The total phase response of a rectangular dielectric nanopillar is:

```
φ_total(λ) = φ_geometric(λ) + φ_propagation(λ)
            = 2σθ + (2π/λ) × n_eff(W, L, λ) × H
```

For three wavelengths, we need to satisfy:
```
φ_R = 2σθ + (2π/λ_R) × n_eff(W, L, λ_R) × H  (given θ)
φ_G = 2σθ + (2π/λ_G) × n_eff(W, L, λ_G) × H
φ_B = 2σθ + (2π/λ_B) × n_eff(W, L, λ_B) × H
```

The design degrees of freedom:
- **θ (rotation):** Controls geometric phase (same shift for all λ)
- **W, L (width, length):** Controls propagation phase (different shift for each λ)
- **H (height):** Fixed globally

For three-target phase control, typically a **cross-shaped nanopillar** design is used:

```
Cross-shaped SiN nanopillar:
- Arm widths: W₁, W₂ (two independent parameters)
- Arm lengths: L₁, L₂ (two independent parameters)  
- Height: H (fixed)
- Material: SiN (transparent at R, G, B)
```

**Key design insight from Ouyang et al. (2025):**
Using a **single polarization-independent cross-shaped SiN nanopillar**, each unit cell achieves independent phase control for R, G, and B simultaneously:

1. The cross shape provides shape birefringence → different n_eff for different polarizations and wavelengths
2. No spatial interleaving needed → full pixel density for each color
3. Polarization-independent → works with unpolarized or linearly polarized light
4. **Single meta-atom** serves R, G, B simultaneously — the "Holy Grail" of color metasurface holography

**Design workflow:**
```
Step 1: Compute CGH phases for R, G, B independently (using Adam optimizer)
Step 2: Build a meta-atom library (cross-shaped nanopillars with varying W₁, W₂, L₁, L₂)
Step 3: For each pixel position (x,y):
    - Lookup meta-atom that simultaneously satisfies φ_R(x,y), φ_G(x,y), φ_B(x,y)
    - This is a 3D matching problem solved by nearest-neighbor search in the library
Step 4: Generate final metasurface layout
```

**Performance comparison of RGB approaches:**

| Method | Pixel Density | Efficiency | Fabrication Complexity | Color Purity |
|--------|--------------|------------|----------------------|--------------|
| Spatial interleaving | Low (1/3) | Medium | Simple | Good |
| 3D tandem (stacked) | Full | Medium | Complex (multi-layer) | Best |
| Wavelength-decoupled single-cell | **Full** | **High** | Single-layer | Good |
| Cross-shaped single-cell | **Full** | **High** | Single-layer | Good |

#### 6.4 Complete RGB Workflow Summary

**Recommended end-to-end pipeline:**

1. **CGH computation:**
   ```
   For each wavelength λ ∈ {R=633nm, G=532nm, B=473nm}:
       φₗ(x,y) = AdamOptimizer( I_target_luminance(λ), λ, propagation_distance )
   ```

2. **Meta-atom library design:**
   ```
   For each (W, L) geometry pair:
       Simulate φ_R(W,L), φ_G(W,L), φ_B(W,L) via FDTD/RCWA
       Store in HDF5 database
   ```

3. **Phase-to-structure mapping:**
   ```
   For each pixel (x,y):
       Find (W*, L*) such that:
           φ_R_sim(W*,L*) ≈ φ_R_CGH(x,y)
           φ_G_sim(W*,L*) ≈ φ_G_CGH(x,y)
           φ_B_sim(W*,L*) ≈ φ_B_CGH(x,y)
   ```

4. **Fabrication:**
   - E-beam lithography or deep-UV stepper lithography
   - ICP-RIE etching of SiN/TiO₂
   - Result: Single-layer metasurface producing full-color 3D holographic reconstruction

---

### 7. Key Open Challenges and Future Directions

1. **Chromatic aberration correction** — Dispersion of meta-atoms across RGB bandwidth
2. **Large-area fabrication** — Wafer-scale metasurface patterning with high yield
3. **Dynamic metasurfaces** — Tunable/active materials (phase-change, liquid crystal) for real-time CGH
4. **Deep learning integration** — Neural network-based CGH solvers trained end-to-end with metasurface physics
5. **Camera-in-the-loop optimization** — Closed-loop calibration of metasurface hologram quality
6. **Speckle suppression** — Random phase optimization and temporal averaging techniques

---

### References

1. Yoon, G. et al. "Wavelength-decoupled geometric metasurfaces by arbitrary dispersion control." *Communications Physics* 2, 129 (2019).
2. Hu, Y. et al. "3D-Integrated metasurfaces for full-colour holography." *Light: Science & Applications* 8, 86 (2019).
3. Jiang, Q., Jin, G. & Cao, L. "When metasurface meets hologram: principle and advances." *Advances in Optics and Photonics* 11(3), 518 (2019).
4. Huang, L., Zhang, S. & Zentgraf, T. "Metasurface holography: from fundamentals to applications." *Nanophotonics* 7(6), 1169-1190 (2018).
5. Peng, Y. et al. "Neural holography with camera-in-the-loop training." *ACM Transactions on Graphics (SIGGRAPH Asia)* (2020).
6. Ouyang, G. et al. "Wavelength- and angle-multiplexed full-color 3D metasurface hologram." *Nanophotonics* 14(4), 4665 (2025).
7. Zheng, H. et al. "Non-iterative phase-only hologram generation via stochastic gradient descent optimization." *Photonics* 12(5), 500 (2025).
8. Zhang, X. et al. "Single-celled metasurface full-color holography by independent phase control at RGB wavelengths." *SPIE Proc.* 13283 (2024).
9. Chen, W. T. et al. "A broadband achromatic metalens for focusing and imaging in the visible." *Nature Nanotechnology* 13, 220-226 (2018).
10. Chen, C. et al. "Metasurface color holography." *Opto-Electronic Advances* 5(8), 210088 (2022).

