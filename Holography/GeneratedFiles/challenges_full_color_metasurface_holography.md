# Comprehensive Report: Challenges and Solutions for RGB/Full-Color Holography on a Single Metasurface

---

## 1. Introduction

Full-color metasurface holography aims to reconstruct three-dimensional images by independently controlling the wavefront of red (R), green (G), and blue (B) wavelengths using a single, ultrathin layer of subwavelength nanostructures (meta-atoms). While metasurfaces offer unprecedented control over light at the nanoscale, achieving faithful full-color holography on a **single layer** presents profound challenges. This report synthesizes findings from the latest research (2016-2025) across multiple dimensions of these challenges and the emerging solutions.

---

## 2. Fundamental Challenge #1: Chromatic Dispersion Issues

### Why Different Wavelengths Interact Differently with Nanostructures

The core difficulty stems from the **intrinsic material and structural dispersion** of meta-atoms:

- **Material Dispersion:** The refractive index of any dieletric material (Si, TiO₂, SiN, GaN) varies with wavelength. In the visible range, a single nanofin dimension that provides a phase shift of 2π for red light (λ ≈ 633 nm) will provide a completely different phase shift for blue light (λ ≈ 473 nm). This is because the effective mode index within a nanostructure depends on the ratio of its physical dimensions to the operating wavelength.

- **Resonance Dispersion:** Meta-atoms operate near their electromagnetic resonances. The Mie resonances (electric and magnetic dipolar resonances) occur at wavelength-dependent positions. A meta-atom designed to function as a half-wave plate at one wavelength may behave entirely differently at another wavelength.

- **Propagation Phase Wavelength Dependence:** The propagation phaseφ_prop = (2π/λ) × n_eff × h (where h is nanopillar height) is explicitly dependent on 1/λ, meaning that for a fixed height, the phase accumulation is inherently different for RGB wavelengths.

- **Geometric Phase Constraint:** The geometric (Pancharatnam-Berry) phase φ_PB = 2σθ (where σ = ±1 for circular polarization and θ is the rotation angle) is **theoretically achromatic** — the same rotation produces the same phase shift regardless of wavelength. However, this ideal behavior requires the meta-atom to behave as a perfect half-wave plate across all desired wavelengths, which is extremely difficult to achieve in practice due to dispersion of the waveplate behavior.

### Key Reference
- **Yoon et al. (2019), *Communications Physics*:** "Wavelength-decoupled geometric metasurfaces by arbitrary dispersion control" — This paper explicitly identified that conventional multicolor metaholograms suffer from fundamental limitations because each unit structure's functionality is confined to a single wavelength. They proposed wavelength-decoupled metasurfaces enabling independent chromatic phase control (0 to 2π) for each wavelength by combining propagation and geometric phases.

---

## 3. Fundamental Challenge #2: Cross-Talk Between Color Channels

### The Nature of Cross-Talk

When a single metasurface is illuminated simultaneously by RGB lasers (or a white light source), each meta-atom is designed to contribute a specific phase to each color channel. However, because the meta-atom simultaneously interacts with all wavelengths, the phase it imposes on one wavelength unavoidably affects the others. Cross-talk manifests in several ways:

- **Phase Cross-Talk:** The phase response at λ_R, λ_G, and λ_B from the same nanostructure are coupled. If you optimize the structure for a specific phase triplet (φ_R, φ_G, φ_B), the actual achieved triplet may deviate significantly.

- **Intensity Cross-Talk:** In addition to phase errors, the meta-atom's transmittance/reflectance amplitude varies with wavelength, creating uneven brightness across color channels.

- **Image Cross-Talk:** When reconstructing, the holographic image from one wavelength may appear as noise in the reconstruction of another wavelength, creating ghost images and color bleeding.

- **Spatial Cross-Talk in Multiplexed Designs:** In spatial-multiplexing approaches (interleaving pixels dedicated to different colors), there is cross-talk due to diffraction from neighboring sub-pixels and imperfect color filtering.

### Quantified Cross-Talk Levels

Research has shown that:
- Early approaches using spatial interleaving of RGB sub-pixels achieved **cross-talk of ~17-30%** between color channels.
- The **3D-integrated metasurface approach** (Nature Light, 2019) using Fabry-Pérot cavity-based color filters reduced channel cross-talk to lower than previously reported levels by carefully selecting RGB color filters.
- The **single-sized antenna approach** (Shan et al., *Optics Letters* 2021) claims "full-color holographic images **without cross talk**" by utilizing the conjugation property of two circularly polarized lights.

### Key References
- **Shan et al. (2021), *Optics Letters* 46(21):** 5417 — "Metasurfaces with single-sized antennas for reconstructing full-color holographic images without cross talk"
- **Omori & Iwami (2025), *Nanophotonics*:** "Wavelength- and angle-multiplexed full-color 3D metasurface hologram" — Uses deterministic separation of crosstalk by spatially dividing reconstructed 3D images while changing incident angles.

---

## 4. Fundamental Challenge #3: Limited Degrees of Freedom in a Single Meta-Atom

### The Design Constraint Problem

A typical meta-atom (e.g., a rectangular TiO₂ or SiN nanopillar) has very few geometric degrees of freedom (DOFs):
- **Length (L)** and **Width (W)** — control propagation phase along two axes
- **Rotation Angle (θ)** — controls geometric (PB) phase
- **Height (h)** — typically fixed during fabrication
- **Period (P)** — typically fixed

### The "One Structure → One Phase Per Wavelength" Problem

For a single-wavelength hologram, a nano-pillar with parameters (L, W, θ) can encode one phase value. For full-color RGB holography, each meta-atom simultaneously needs to provide:
- φ_R(λ_R), φ_G(λ_G), φ_B(λ_B) — **three independent phase values**

This is fundamentally underdetermined. With only 2-3 geometric DOFs (L, W, and possibly θ), it is impossible to independently specify 3 arbitrary phase values for 3 different wavelengths. This is the core **information bottleneck** of single-celled metasurfaces.

### The Consequence

As noted in the literature:
- "The limited capabilities and degree of freedoms in commonly used meta-atoms restrict the design flexibility to break the conventional trade-off" (*ACS Applied Materials & Interfaces*, 2022)
- "Achieving multiple holographic images using a single metasurface is still difficult due to the **capacity limit of a single meta-atom**" (*Advanced Materials*, 2023)

### Attempted Workarounds

1. **Interleaved sub-pixels:** Partition the metasurface into sublattices, each dedicated to one color. This triples the meta-atom count but **reduces resolution by 3×** and introduces cross-talk.

2. **Single-celled with combined phases:** Use the combination of geometric phase (for one color, typically G) and propagation phase differences (for R and B relative to G). This reduces the required DOFs from 3 to 2 (length + rotation). This approach was used by **Zhang et al. (2024, SPIE Proc.)** in "Single-celled metasurface full-color holography by independent phase control at RGB wavelengths."

3. **Multi-layer stacking:** Stack multiple metasurfaces vertically, each handling different DOFs.

---

## 5. Approach #1: Inverse Design and End-to-End Optimization

### The Paradigm Shift

Rather than manually designing meta-atom libraries and separately computing holograms, **inverse design** treats the metasurface as a differentiable system that can be optimized as a whole. This is the most transformative approach to emerge in recent years.

### Key Methods and Works

#### a) Gradient-Descent Inverse Design
- **So et al. (2023), *Advanced Materials* 35(18):** "Multicolor and 3D Holography Generated by Inverse-Designed Single-Cell Metasurfaces" — arXiv:2207.04778
  - Uses gradient-descent optimization to encode multiple pieces of holographic information into a single metasurface.
  - Demonstrated the **first experimental metasurface-generated 3D holograms with completely independent images in each plane**.
  - Simulated up to 10 wavelength-based hyperspectral polarization-dependent 3D holography with **60 distinct channels**.
  - Eliminates the need for complex meta-atom library design.

#### b) End-to-End Inverse Design Framework
- **Multi-Dimensional Multiplexed Metasurface Holography by Inverse Design** (2024, *Nature Light*)
  - Directly links metasurface parameters to reconstructed images via a loss function.
  - Demonstrated **12 channels** of multi-wavelength, multi-plane, and multi-polarization holography.
  - The hologram calculation step is completely bypassed — the metasurface is directly optimized.

#### c) 36-Channel Spin and Wavelength Co-Multiplexed Metasurface Holography
- **Park, Jeon et al. (2025), *Advanced Science* 12(28):**
  - Single-cell metasurface multiplexing across both spin states (LCP/RCP) and multiple wavelengths.
  - Uses **phase-gradient inverse design** with automatic differentiation to minimize loss between target and output images.
  - Covers visible to near-infrared wavelengths.

#### d) I-MGD Algorithm
- **Zhao et al. (2025), *JOSA B* 42(9):** "Efficient multi-channel holography with 3D multiplexed metasurfaces"
  - Integrated Modified Gradient Descent (I-MGD) algorithm.
  - Achieves 12-channel holographic metasurface designed in only **51 seconds**.

### Key Advantages
- Automatically handles cross-talk by minimizing it during optimization
- Makes full use of available DOFs
- Can incorporate fabrication constraints
- End-to-end approaches can co-optimize metasurface + algorithm

---

## 6. Approach #2: Combined Geometric and Propagation Phase

### The Hybrid Phase Strategy

One powerful technique to overcome the DOF limitation is to **simultaneously use geometric (PB) phase and propagation phase** within the same meta-atom:

- **Geometric Phase:** φ_g = 2σθ — controls phase for one chosen wavelength (typically G) through rotation angle θ. This is essentially achromatic in theory.
  
- **Propagation Phase:** The phase delay from light propagating through the nanostructure length L. Since the propagation phase Δφ_prop = (2π/λ) × Δn_eff × h depends on λ, the *difference* between phase at R and G (or B and G) can be tuned by adjusting the nanopillar dimensions.

### Implementation

- **Zhang, Li et al. (2024), SPIE Proc. 13283:** 
  - G-channel phase is set by geometric phase (via rotation).
  - Phase differences (φ_R - φ_G) and (φ_B - φ_G) are set by propagation phase (via nanopillar length/width).
  - This provides **independent phase control at 3 wavelengths using just 2 DOFs** (L and θ).
  - Eliminates the need for spatial multiplexing (no resolution loss).

- **Yoon et al. (2019), *Communications Physics* 2(1):**
  - Demonstrated "wavelength-decoupled geometric metasurfaces" by arbitrary dispersion control.
  - Used both propagation phase and geometric phase of rectangular dielectric nanostructures to embed a **dual phase response** into a single nanostructure.
  - Demonstrated noise-free multicolor metaholograms.

### Limitations
- The geometric phase approach works only for circularly polarized light, with a theoretical maximum efficiency of 50% (for PB phase only).
- The propagation phase engineering is constrained by the available aspect ratios in fabrication.
- True independence at three wavelengths is still an approximation — the phase relationships are not fully decoupled.

---

## 7. Approach #3: Multi-Layer (3D-Integrated) Metasurfaces

### The Stacked Approach

Multi-layer metasurfaces add additional DOFs by stacking multiple metasurface layers vertically, or by combining metasurfaces with other optical elements.

#### Major Work: 3D-Integrated Metasurfaces for Full-Colour Holography
- **Hu et al. (2019), *Light: Science & Applications* 8(1):**
  - Stacked a **hologram metasurface** on top of a **monolithic Fabry-Pérot cavity-based color filter microarray**.
  - The color filter layer selectively transmits RGB components with minimal cross-talk.
  - The hologram metasurface then imparts the correct phase profile for each color.
  - This separates the **color generation** function from the **phase modulation** function, allowing independent optimization.

#### Advantages
- **Reduced cross-talk:** Color filters provide physical wavelength selection.
- **Additional DOFs:** Each metasurface layer can add its own phase profile.
- **Compatible with standard fabrication:** Each layer can be optimized separately.

#### Disadvantages
- **Alignment complexity:** Vertical alignment between layers is critical.
- **Increased thickness:** The "ultrathin" advantage of metasurfaces is partially lost.
- **Limited scalability:** Difficult to stack more than 2-3 layers due to scattering losses.

#### More Recent Developments
- **Dispersion-engineered compact twisted metasurfaces** (2025) — using relative twist angles between layers for 3D holography and dispersion manipulation.
- **Single-cell bilayer design** in the terahertz regime — combining phase-change materials (VO₂) with bilayer structures for 6-channel simultaneous holograms.

---

## 8. Approach #4: Polarization Multiplexing for Color Holography

### Using Polarization as an Additional DOF

Polarization provides a powerful additional degree of freedom that can be exploited simultaneously with wavelength multiplexing:

#### Spin Multiplexing (Circular Polarization)
- The geometric (PB) phase naturally provides spin-dependent phase: φ_PB = 2σθ, where σ = +1 for LCP and σ = -1 for RCP.
- This means **two independent holograms** can be encoded for LCP and RCP in the same metasurface.
- **Broadband spin-multiplexed single-celled metasurface holograms** have been experimentally demonstrated (2024).

#### Combining Spin + Wavelength
- **36-Channel Spin and Wavelength Co-Multiplexed** (2025, *Advanced Science*): Multiplexes across 2 spin states × multiple wavelength channels using a single-cell metasurface.
- **Time-sequential color code division multiplexing (CDM)** (2023, *Opto-Electronic Advances*): 48 monochrome images reconstructed in dual polarization channels.

#### Depolarized Holography
- **Depolarized Holography with Polarization-Multiplexing Metasurface** (2024, *ACM Trans. Graphics*):
  - Uses polarization multiplexing to bring an additional DOF for CGH algorithms.
  - Creates **incoherent-like behavior** due to mutual incoherence of orthogonal polarization states.
  - Reduces speckle noise significantly.

#### Asymmetric Photon Spin Conversion
- **Polarization-multiplexed dynamic full-color holography using composite phase metasurfaces** (2025, *Physics Letters A*):
  - Uses asymmetric photon spin conversion mechanism.
  - Independent modulation of two orthogonal circular polarizations.
  - Dynamic color holography with time-sequential RGB illumination.

---

## 9. The Information Sparsity Problem

### What is Information Sparsity?

The **information sparsity problem** was formally identified and named in the research by **Noh, Kim, and Rho (2025)** at POSTECH. The term describes the following core challenge:

A metasurface is a **discrete sampling of the wavefront** with subwavelength-spaced meta-atoms. Each meta-atom can only encode a limited number of parameters (typically 1-3 real numbers: phase, possibly amplitude). For full-color holography, each meta-atom position must encode information about **three different wavelengths** simultaneously. The ratio of desired information to available encoding capacity is **information-dense → information-sparse** when the meta-atom lacks the DOFs to represent the full color information.

### Formal Statement of the Problem

1. For a metasurface with N × N meta-atoms, each providing M degrees of freedom (typically L, W, θ → M=3).
2. Total encoding capacity: N² × M.
3. For full-color 3D holography with K planes and P polarization channels, required information: N² × K × P × 3 (RGB).
4. When the required information exceeds the encoding capacity, **information sparsity** occurs — the metasurface cannot faithfully represent the desired full-color hologram.

### Proposed Solution: End-to-End Design

- **Noh, Kim, Rho (2025), *Nano Letters* 25(29), 11398–11405:**
  - Title: "Overcoming Information Sparsity in Metasurfaces for Full-Color Holography via End-to-End Design"
  - Proposes an **end-to-end (E2E) system** for RGB meta-hologram generation.
  - **Integrates:** metasurface modeling → transmission coefficient calculation → optical propagation → holographic image evaluation.
  - **Hybrid loss function** combining spectral fidelity and polarization accuracy.
  - Efficiently determines optimal material and geometry for target holograms.
  - The E2E approach **directly addresses information sparsity** by treating the whole system (metasurface + hologram) as jointly optimizable, rather than trying to independently assign phase values.

---

## 10. Key Papers Summary

| Paper (Year) | Authors | Journal | Key Contribution |
|---|---|---|---|
| "Full-Color Plasmonic Metasurface Holograms" (2016) | Wan et al. | *ACS Nano* | First full-color metasurface holograms with amplitude+phase modulation |
| "Visible-Frequency Dielectric Metasurfaces for Multiwavelength Holograms" (2016) | Wang et al. | *Nano Letters* | Si nanoblocks multiplexed for RGB wavefront manipulation |
| "Full-Colour Nanoprint-Hologram Synchronous Metasurface" (2019) | Bao et al. | *Light: Sci. & Appl.* | HSB color nanoprinting + full-color holography on single-layer |
| "3D-Integrated Metasurfaces for Full-Colour Holography" (2019) | Hu et al. | *Light: Sci. & Appl.* | Stacked color filter + hologram metasurface |
| "Wavelength-Decoupled Geometric Metasurfaces" (2019) | Yoon et al. | *Comm. Physics* | Dual phase response (propagation+geometry) in single nanostructure |
| "Metasurfaces with Single-Sized Antennas for Full-Color Holography Without Cross Talk" (2021) | Shan et al. | *Optics Letters* | Single-sized strategy using conjugation property of circular polarizations |
| "Multicolor and 3D Holography by Inverse-Designed Single-Cell Metasurfaces" (2023) | So et al. | *Adv. Materials* | Gradient-descent inverse design; 60-channel hyperspectral holography |
| "Time-Sequential Color CDM Holographic Display with Metasurface" (2023) | — | *Opto-Electronic Advances* | Code-division multiplexing for dynamic color video |
| "Multi-Dimensional Multiplexed Metasurface Holography by Inverse Design" (2024) | — | *Light: Sci. & Appl.* | 12-channel end-to-end inverse design |
| "Single-Celled Full-Color Holography by Independent Phase Control at RGB" (2024) | Zhang, Li et al. | *SPIE Proc.* | Geometric phase (G) + propagation phase differences (R-G, B-G) |
| "Overcoming Information Sparsity in Metasurfaces for Full-Color Holography" (2025) | Noh, Kim, Rho | *Nano Letters* | E2E system solving the information sparsity problem |
| "Wavelength- and Angle-Multiplexed Full-Color 3D Metasurface Hologram" (2025) | Omori & Iwami | *Nanophotonics* | Polarization-independent meta-atom (SiN cross-shape) with angle multiplexing |
| "36-Channel Spin and Wavelength Co-Multiplexed Holography" (2025) | Park, Jeon et al. | *Adv. Science* | Phase-gradient inverse design for 36-channel multiplexing |
| "Dynamic Polarization-Dependent Multicolor 3D Holography" (2025) | — | *Adv. Materials* | Gradient descent combining polarization in full-color 3D holography |

---

## 11. Summary of Challenges and Solutions

| Challenge | Key Difficulty | Current Best Solutions |
|---|---|---|
| **Chromatic Dispersion** | λ-dependent refractive index and resonance behavior | Wavelength-decoupled metasurfaces (Yoon 2019); combined geometric + propagation phase; inverse design optimization |
| **Color Channel Cross-Talk** | Phase/intensity coupling across wavelengths | Single-sized antennas (Shan 2021); angle-multiplexed spatial separation (Omori 2025); color filter stacking (Hu 2019) |
| **Limited Meta-Atom DOFs** | 2-3 geometric parameters cannot independently control 3 wavelengths | Combined geometric + propagation phase (Zhang 2024); inverse design with gradient descent (So 2023); multi-layer stacking |
| **Information Sparsity** | Encoding capacity < required holographic information | End-to-end optimization (Noh, Rho 2025); joint metasurface-hologram optimization |
| **Efficiency** | PB phase limited to 50% theoretical efficiency | Polarization-independent meta-atoms (cross-shaped SiN); multi-layer approaches |
| **Fabrication Complexity** | High aspect ratio nanostructures; alignment in multi-layer | Single-step lithography approaches; inverse design with fabrication constraints |

---

## 12. Conclusions and Future Directions

1. **No single "perfect" solution exists yet** — each approach involves trade-offs between resolution, efficiency, cross-talk, fabrication complexity, and color fidelity.

2. **Inverse design is the most promising trend.** Gradient-descent and end-to-end optimization methods are rapidly surpassing manual meta-atom library approaches. The ability to co-optimize metasurface geometry and hologram algorithms directly addresses both the DOF limitations and the information sparsity problem.

3. **Combined geometric + propagation phase** within single-celled meta-atoms offers a practical path to full-color holography without spatial multiplexing (resolution loss), but with polarization constraints.

4. **Multi-layer and 3D-integrated** approaches sacrifice the "single-layer" advantage but provide cleaner color separation.

5. **Angle multiplexing** (Omori & Iwami 2025) is an emerging technique that adds a new dimension — incident angle — as a DOF, enabling single polarization-independent meta-atoms to achieve full-color 3D holography.

6. **The field is rapidly advancing** — from 2016 (first plasmonic color holograms) to 2025 (36-channel spin/wavelength multiplexing, information sparsity solutions, and end-to-end inverse design). The combination of **machine learning + inverse design + nanofabrication advances** is likely to yield practical full-color metasurface holography in the near future.

---

*Report compiled from web searches of published literature (2016-2025) across Nature, ACS, Optica, SPIE, Wiley, AIP, and arXiv sources.*

