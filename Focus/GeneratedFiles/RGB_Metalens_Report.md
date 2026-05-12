# Comprehensive Report: RGB Metalens — Principles, Design, and Physics

## 1. Introduction

An **RGB metalens** is an ultra-thin, planar optical device based on a metasurface — an array of subwavelength nanostructures (meta-atoms) — that is engineered to focus red (~630–650 nm), green (~520–550 nm), and blue (~450–470 nm) light simultaneously, with chromatic aberration correction. Unlike conventional refractive lenses or diffractive Fresnel zone plates, RGB metalenses achieve multi-wavelength focusing through **precise phase control** at each wavelength using dispersion-engineered meta-atoms.

The central challenge: a conventional singlet metalens exhibits strong **chromatic aberration** — different wavelengths focus at different positions along the optical axis, because the phase shift imparted by a simple nanostructure scales with wavelength (∝ 1/λ). RGB achromatic metalenses overcome this by engineering the **phase dispersion** (wavelength-dependence of the phase response) of each meta-atom to simultaneously fulfill the desired phase profiles for red, green, and blue light.

### Key Applications
- Compact full-color imaging systems (digital cameras, endoscopes)
- Augmented/Virtual Reality (AR/VR) near-eye displays
- Fluorescence microscopy and spectroscopy
- Laser-based projection systems

---

## 2. Metasurface Phase Control Mechanisms

There are two primary mechanisms for controlling the phase of transmitted light using nanostructures:

### 2.1 Propagation Phase

The **propagation phase** exploits the optical path length difference as light travels through a dielectric nanostructure (e.g., TiO₂, Si, GaN nanopillar). When light enters a high-index nanostructure, the effective wavelength is reduced, introducing a phase delay:

$$\phi_{\text{prop}}(x,y) = \frac{2\pi}{\lambda_0} \cdot h \cdot n_{\text{eff}}(x,y)$$

Where:
- $h$ = height of the nanopillar (constant across the metasurface)
- $n_{\text{eff}}(x,y)$ = effective refractive index of the guided mode in the nanostructure, which depends on the cross-sectional geometry (diameter, width, length)
- $\lambda_0$ = free-space wavelength

By varying the diameter (or width/length for rectangular pillars) of nanopillars at each position, the effective index $n_{\text{eff}}$ changes, producing a continuous phase shift from 0 to $2\pi$.

**Key characteristics:**
- Polarization-independent (for symmetric cross-sections like cylinders)
- Broadband operation possible
- Simple single-parameter control (e.g., diameter)
- Phase response is inherently dispersive (wavelength-dependent)

### 2.2 Geometric Phase (Pancharatnam–Berry Phase)

The **geometric phase** (also called Pancharatnam–Berry or PB phase) arises from the spin-orbit interaction of light. When circularly polarized light passes through an anisotropic nanostructure (nanofin) rotated by an angle $\theta$, the transmitted cross-circular polarized component acquires a phase equal to twice the rotation angle:

$$\phi_{\text{PB}} = 2\sigma\theta$$

Where:
- $\sigma = \pm 1$ for left/right circular polarization (LCP/RCP)
- $\theta$ = in-plane rotation angle of the nanofin

**Key characteristics:**
- Wavelength-independent (achromatic) phase response in principle — the phase is purely geometric
- Requires circular polarization; works for opposite handedness with opposite sign
- High polarization conversion efficiency requires resonant nanostructures
- Provides full $2\pi$ phase coverage with just rotation control
- Often combined with propagation phase for dispersion engineering

### 2.3 Combined Phase Control for RGB Achromatic Design

For RGB achromatic metalenses, both mechanisms are typically combined because:
- **Propagation phase** provides wavelength-dependent phase control (dispersive)
- **Geometric phase** provides wavelength-independent phase offset (non-dispersive)

By engineering both the dimensions (for propagation phase) and the rotation angle (for geometric phase) of each meta-atom, independent phase control at multiple wavelengths becomes possible:

$$\phi_{\text{total}}(\lambda) = \phi_{\text{prop}}(\lambda) + \phi_{\text{PB}}(\lambda)$$

Where $\phi_{\text{prop}}(\lambda)$ varies with both geometry and wavelength, while $\phi_{\text{PB}}$ depends only on rotation angle.

---

## 3. Mathematical Formulation: Phase Profile for Focusing

### 3.1 Hyperbolic Phase Profile (Diffraction-Limited Focusing)

A metalens focuses an incident plane wave to a point on the optical axis by imposing a spatially-varying phase profile that converts the planar wavefront into a spherical wavefront converging to the focal point. The required phase profile at the metasurface plane ($z=0$) is:

$$\phi_{\text{lens}}(r; \lambda) = -\frac{2\pi}{\lambda} \left( \sqrt{r^2 + f^2} - f \right) + \phi_0$$

Where:
- $r = \sqrt{x^2 + y^2}$ = radial distance from the lens center
- $f$ = focal length
- $\lambda$ = operating wavelength
- $\phi_0$ = constant reference phase

This is known as the **hyperbolic phase profile** (not a simple quadratic/parabolic approximation). The term $\sqrt{r^2 + f^2} - f$ represents the optical path difference (OPD) between the lens center and a point at radius $r$.

### 3.2 For Off-Axis Focusing (Arbitrary Focal Spot Position)

For focusing at a point $(x_f, y_f, f)$ on the focal plane (not necessarily on-axis):

$$\phi(x,y;\lambda) = -\frac{2\pi}{\lambda} \left( \sqrt{(x-x_f)^2 + (y-y_f)^2 + f^2} - f \right)$$

This is the general form where different wavelengths can be directed to different focal positions $(x_f(\lambda), y_f(\lambda))$ on the same focal plane.

### 3.3 Multi-Wavelength Phase Requirement

For an RGB achromatic metalens operating at three discrete wavelengths $\lambda_R, \lambda_G, \lambda_B$, the metasurface must simultaneously satisfy:

$$\phi(x,y;\lambda_R) = -\frac{2\pi}{\lambda_R} \left( \sqrt{r^2 + f^2} - f \right)$$
$$\phi(x,y;\lambda_G) = -\frac{2\pi}{\lambda_G} \left( \sqrt{r^2 + f^2} - f \right)$$
$$\phi(x,y;\lambda_B) = -\frac{2\pi}{\lambda_B} \left( \sqrt{r^2 + f^2} - f \right)$$

Since $1/\lambda$ is different for each color, the phase profiles for R, G, B are **different** at the same position $(x,y)$. The meta-atom at each position must independently provide the correct phase for all three wavelengths simultaneously — this is the core difficulty of RGB achromatic metalens design.

---

## 4. Chromatic Aberration and Dispersion Engineering

### 4.1 Origin of Chromatic Aberration in Metalenses

A conventional diffractive lens (Fresnel zone plate) has a focal length that scales as $f(\lambda) \propto 1/\lambda$, meaning blue light focuses closer than red light. A simple metasurface following the hyperbolic phase profile at a single design wavelength $\lambda_0$ will also exhibit this behavior:

$$f(\lambda) = \frac{\lambda_0}{\lambda} f_0$$

This results in **longitudinal chromatic aberration** (focal spot shift along the optical axis) and **transverse chromatic aberration** (spot shift in the focal plane).

### 4.2 Phase Compensation Principle

To achieve the same focal length $f$ for all RGB wavelengths, the phase at each position $(x,y)$ must deviate from the single-wavelength hyperbolic profile. The required phase compensation $\Delta\phi(x,y;\lambda)$ at wavelength $\lambda$ relative to a reference wavelength $\lambda_0$ is:

$$\Delta\phi(r;\lambda) = \phi(r;\lambda) - \phi(r;\lambda_0) = -\frac{2\pi}{\lambda} \left( \sqrt{r^2 + f^2} - f \right) + \frac{2\pi}{\lambda_0} \left( \sqrt{r^2 + f^2} - f \right)$$

$$= -2\pi \left( \sqrt{r^2 + f^2} - f \right) \left( \frac{1}{\lambda} - \frac{1}{\lambda_0} \right)$$

This compensation increases with radial distance $r$ and the wavelength difference from $\lambda_0$.

### 4.3 Group Delay and Group Delay Dispersion

For broadband achromatic operation, the phase response of each meta-atom must satisfy conditions on:

**Group delay (GD):**
$$\text{GD}(r) = \frac{\partial \phi(r,\omega)}{\partial \omega} = -\frac{2\pi}{c} \left( \sqrt{r^2 + f^2} - f \right)$$

**Group delay dispersion (GDD):**
$$\text{GDD}(r) = \frac{\partial^2 \phi(r,\omega)}{\partial \omega^2}$$

The group delay increases linearly with radial distance from the lens center. Meta-atoms at the edge of the lens must provide larger group delays than those at the center. The **group delay range** ($\Delta\text{GD}$) sets the fundamental bandwidth limit:

$$\Delta\text{GD} = \text{GD}(r_{\max}) - \text{GD}(0) = \frac{2\pi}{c} \left( \sqrt{R^2 + f^2} - f \right)$$

For an RGB metalens operating at discrete wavelengths (not continuous broadband), the phase at exactly $\lambda_R, \lambda_G, \lambda_B$ must be satisfied, with relaxed requirements between them.

---

## 5. RGB Achromatic Metalens Design Strategies

### 5.1 Strategy 1: Dispersion-Engineered Single-Layer Metasurface

**Approach:** Design a library of meta-atoms (e.g., TiO₂ or Si nanopillars/nanofins with varying dimensions and rotation angles) that provide independent phase control at R, G, B wavelengths. Each meta-atom is characterized by a multi-dimensional parameter space (diameter, width, length, rotation angle) and its phase response at all three target wavelengths is computed via FDTD/RCWA simulations.

**Key reference work:** Li et al., "Meta-optics achieves RGB-achromatic focusing for virtual reality," *Science Advances* 7, eabe4458 (2021).

- **Material:** TiO₂ nanofins on glass substrate
- **Wavelengths:** 633 nm (R), 532 nm (G), 488 nm (B) — or 450/532/633 nm
- **Method:** Simultaneous engineering of propagation phase (via nanofin dimensions) and geometric phase (via nanofin rotation) to achieve independent phase control at three wavelengths
- **Performance:** Diffraction-limited focusing, NA up to ~0.7, millimeter-scale diameter
- The nanofin acts as a truncated waveguide, and both the effective index (propagation phase) and form birefringence (geometric phase) are tuned

### 5.2 Strategy 2: Bilayer/Stacked Metasurface

**Approach:** Use two layers of metasurfaces separated by a spacer layer. The first layer provides partial phase compensation, and the second layer provides the remaining correction. This increases the degrees of freedom for phase control.

**Key reference work:** "Design of a Bilayer Metalens for Red, Green, and Blue-Achromatic Imaging with Wide Field of View," *Advanced Photonics Research* (2025).

- Two independently designed metasurface layers
- Each layer uses a different set of meta-atom geometries
- Combined effect satisfies RGB phase profiles simultaneously
- Enables wider field of view (up to ~80°) and higher NA (up to ~0.65)

**Phase design equations:**

Layer 1: $\phi_1(r;\lambda) = \alpha(\lambda) \cdot \phi_{\text{target}}(r;\lambda)$
Layer 2: $\phi_2(r;\lambda) = (1-\alpha(\lambda)) \cdot \phi_{\text{target}}(r;\lambda)$

Where $\alpha(\lambda)$ is a wavelength-dependent splitting ratio optimized for dispersion matching.

### 5.3 Strategy 3: Metalens Doublet

**Approach:** Two cascaded metasurfaces separated by a distance, acting as a compound lens. The first metasurface (aperture metasurface) redistributes the wavefront, and the second (focusing metasurface) completes the focusing.

**Key reference work:** Zhang et al., "RGB Achromatic Metalens Doublet for Digital Imaging," *Nano Letters* (2022).

- **Diameter:** 1 mm
- **NA:** 0.8
- **Operation:** RGB simultaneously with shared aperture
- Combined Strehl ratio > 0.8 for all R, G, B wavelengths
- Demonstrated in a full digital imaging system
- Solves the fundamental trade-off between NA and diameter faced by single-layer designs

**Phase distribution:**

Metalens 1 (correction layer): $\phi_1(x,y;\lambda) = -\frac{2\pi}{\lambda} \left( \sqrt{x^2 + y^2 + d^2} - d \right)$
Metalens 2 (focusing layer): $\phi_2(x,y;\lambda) = -\frac{2\pi}{\lambda} \left( \sqrt{x^2 + y^2 + f^2} - \sqrt{x^2 + y^2 + d^2} \right)$

Where $d$ is the separation between the two metalenses, and $f$ is the back focal length.

### 5.4 Strategy 4: Stepwise Phase Dispersion Compensation (SPDC)

**Approach:** Divide the metasurface into concentric zones. Within each zone, meta-atoms are designed to provide a specific **linear phase dispersion** (i.e., group delay) that matches the required compensation at that radial position.

**Key reference work:** "Broadband achromatic metalens for high-resolution imaging" and "High-performance achromatic flat lens by multiplexing meta-atoms on stepwise phase dispersion compensation layer."

- The metasurface is segmented into annular zones
- Each zone uses meta-atoms with a specific phase dispersion slope (group delay)
- The discrete group delay steps approximate the continuous group delay requirement
- Enables very large bandwidths (full visible 400–700 nm) and high NA

---

## 6. Diffraction-Limited Focusing

### 6.1 Definition

A metalens achieves **diffraction-limited focusing** when the focal spot size is determined only by diffraction due to the finite aperture, not by aberrations. The criterion is typically:

- **Strehl ratio** $S \geq 0.8$ (ratio of peak intensity to ideal diffraction-limited peak)
- **Full width at half maximum (FWHM)** of focal spot $\leq 1.22 \lambda / (2\text{NA})$ for incoherent light
- For RGB: the **Airy disk radius** $= 0.61\lambda/\text{NA}$ should be close to the theoretical minimum for each wavelength

### 6.2 Numerical Aperture (NA)

$$\text{NA} = n \sin\theta = n \frac{R}{\sqrt{R^2 + f^2}}$$

Where:
- $R$ = lens radius (half the diameter $D$)
- $f$ = focal length
- $n$ = refractive index of the medium
- $\theta$ = maximum half-angle of collected light

For RGB: the same NA applies to all three wavelengths, but the resolution (Airy disk radius) is slightly different: blue achieves better resolution than red.

### 6.3 Focusing Efficiency

The focusing efficiency is defined as the ratio of optical power within a specified region around the focal spot to the total power incident on the metalens. RGB achromatic metalenses typically achieve:

- Single-layer designs: 40–70% average across RGB
- Bilayer/doublet designs: 60–86% 
- Trade-off exists between efficiency, bandwidth, and NA

---

## 7. Design Methodology — Step-by-Step

### Step 1: Define Target Specifications
- Focal length $f$, diameter $D$, NA
- Target wavelengths: e.g., $\lambda_R = 633$ nm, $\lambda_G = 532$ nm, $\lambda_B = 450$ nm
- Substrate material (e.g., SiO₂, glass)

### Step 2: Compute Required Phase Profiles
For each wavelength, compute:
$$\phi_{\text{target}}(r;\lambda) = -\frac{2\pi}{\lambda} \left( \sqrt{r^2 + f^2} - f \right) \quad \text{mod } 2\pi$$

### Step 3: Build Meta-Atom Library
- Material selection: TiO₂ (high index, low loss in visible), GaN, Si₃N₄, or Si
- Parameter sweeps using FDTD or RCWA: vary dimensions (diameter, width, length, height) and rotation
- For each meta-atom geometry, record phase response $(\phi_R, \phi_G, \phi_B)$ and transmission amplitude $(T_R, T_G, T_B)$

### Step 4: Match Meta-Atoms to Required Phases
For each position $(x,y)$ with target $(\phi_R, \phi_G, \phi_B)$, select the meta-atom from the library that minimizes:

$$\text{Cost} = \sum_{\lambda \in \{R,G,B\}} w_\lambda \left| e^{i\phi_{\text{meta}}(\lambda)} - e^{i\phi_{\text{target}}(\lambda)} \right|^2$$

Where $w_\lambda$ are weighting factors. This is typically done with a **nearest-neighbor search** in the 3D phase space or via **particle swarm optimization** / **genetic algorithms**.

### Step 5: Full-Wave Simulation and Validation
- Simulate the full metasurface using FDTD
- Analyze focal spots at each wavelength
- Compute Strehl ratio, FWHM, focusing efficiency

---

## 8. Advanced Topics

### 8.1 Polarization-Multiplexed RGB Metalenses

By designing meta-atoms with different phase responses for orthogonal polarizations (e.g., LCP vs RCP), the same metalens can switch between different RGB focusing behaviors based on the incident polarization state. This enables:

- Varifocal RGB metalenses
- Switchable color channels
- Enhanced degrees of freedom for phase control

### 8.2 Inverse Design and Topology Optimization

Advanced approaches use adjoint-based optimization to simultaneously optimize all geometric parameters of the metasurface for the required multi-wavelength performance. The optimization solves:

$$\min_{\mathbf{p}} \sum_{\lambda} \left\| \mathbf{E}_{\text{calc}}(\mathbf{p}; \lambda) - \mathbf{E}_{\text{target}}(\lambda) \right\|^2$$

Where $\mathbf{p}$ represents all geometric design parameters of the nanostructures, and $\mathbf{E}$ is the electromagnetic field.

### 8.3 Computational Aberration Correction

Post-processing with deep neural networks (Vision Transformers, CNNs) can computationally correct residual chromatic aberrations in metalens-captured images, relaxing the stringent requirements on the hardware design.

---

## 9. Key Physical Principles Summary

| Principle | Description | Relevance to RGB |
|-----------|-------------|------------------|
| **Generalized Snell's Law** | $\sin\theta_t n_t - \sin\theta_i n_i = \frac{\lambda}{2\pi}\frac{d\phi}{dx}$ | Defines how phase gradient controls wavefront |
| **Hyperbolic Phase Profile** | $\phi(r) = -\frac{2\pi}{\lambda}(\sqrt{r^2+f^2}-f)$ | Required phase for diffraction-limited focusing |
| **Propagation Phase** | $\phi_{\text{prop}} = \frac{2\pi}{\lambda} h \cdot n_{\text{eff}}$ | Wavelength-dependent phase via waveguide effect |
| **Geometric Phase** | $\phi_{\text{PB}} = 2\sigma\theta$ | Wavelength-independent geometric phase via rotation |
| **Phase Dispersion** | $\frac{\partial\phi}{\partial\lambda}$ | Determines chromatic behavior; must be engineered |
| **Group Delay** | $\text{GD} = \partial\phi/\partial\omega$ | Key parameter for broadband achromatic bandwidth |
| **Diffraction Limit** | $\text{FWHM} = 0.51\lambda/\text{NA}$ | Minimum achievable focal spot size |

---

## 10. References

1. Z. Li et al., "Meta-optics achieves RGB-achromatic focusing for virtual reality," *Science Advances* 7, eabe4458 (2021).
2. J. Zhang et al., "RGB Achromatic Metalens Doublet for Digital Imaging," *Nano Letters* 22, 3969–3975 (2022).
3. S. Baek et al., "High numerical aperture RGB achromatic metalens in the visible," *Photonics Research* 10, B30–B40 (2022).
4. M. Khorasaninejad et al., "Achromatic Metalens over 60 nm Bandwidth in the Visible and Metalens with Reverse Chromatic Dispersion," *Nano Letters* 17, 1819–1824 (2017).
5. L. Hou et al., "High-efficiency broadband achromatic metalens in the visible," *Applied Physics Letters* 126, 101704 (2025).
6. "Design of a Bilayer Metalens for Red, Green, and Blue-Achromatic Imaging with Wide Field of View," *Advanced Photonics Research* (2025).
7. W. T. Chen et al., "A broadband achromatic metalens for focusing and imaging in the visible," *Nature Nanotechnology* 13, 220–226 (2018).
8. "Achromatic metalenses for full visible spectrum with extended group delay control via dispersion-matched layers," *Nature Communications* 15, 53701 (2024).
9. F. Ding et al., "Gradient metasurfaces: a review of fundamentals and applications," *Reports on Progress in Physics* 81, 026401 (2017).
10. S. Wang et al., "Broadband achromatic optical metasurface devices," *Nature Communications* 8, 187 (2017).

