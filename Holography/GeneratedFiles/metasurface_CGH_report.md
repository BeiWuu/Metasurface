# State-of-the-Art in Metasurface Computer-Generated Holography (CGH)
## Comprehensive Research Report: 2024–2025

---

## 1. NATURE/SCIENCE-LEVEL PAPERS ON METASURFACE HOLOGRAPHY

### 1.1 Full-colour 3D Holographic AR Displays with Metasurface Waveguides
- **Publication:** *Nature* **629**, 791–797 (2024)
- **Authors:** M. Gopakumar, G.-Y. Lee, S. Choi, B. Chao, Y. Peng, J. Kim, G. Wetzstein (Stanford Computational Imaging Lab)
- **Key Innovation:** First demonstration of a **glasses-like AR headset** combining:
  - Inverse-designed **full-colour metasurface gratings** for waveguide coupling
  - **Dispersion-compensating waveguide geometry** eliminating bulky collimation optics
  - **AI-driven holography algorithms** (camera-in-the-loop trained neural networks)
  - Full-color 3D moving images overlaid on the real world through ordinary-looking lenses
- **Impact:** The total optical stack is dramatically thinner than conventional AR systems. Co-design of nanophotonic metasurface waveguides with AI holography algorithms represents a paradigm shift.
- **arXiv:** Available via Nature and Stanford Computational Imaging Lab

### 1.2 Synthetic Aperture Waveguide Holography for Compact MR Displays
- **Publication:** *Nature Photonics* (2025) — DOI: 10.1038/s41566-025-01718-w
- **Authors:** Meta Display Systems Research (D. Lanman) × Stanford (G. Wetzstein)
- **Key Innovation:** 
  - **"Synthetic Aperture Holography" (SAH)** — builds on the "Holocake" concept
  - Total optical stack thickness **< 3 mm**
  - Large **étendue** (supports wide FOV over large eye box)
  - Custom-designed waveguide holography + AI algorithmic framework combining implicit large-étendue waveguide models, efficient wave propagation for partially coherent mutual intensity, and novel CGH framework
- **Impact:** VR glasses form factor that delivers full-color 3D holographic images; key enabler for Meta's next-gen VR/mixed reality roadmap

### 1.3 Single-Layer Waveguide Displays using Achromatic Metagratings
- **Publication:** *Nature Nanotechnology* (April 2025) — DOI: 10.1038/s41565-025-01887-3
- **Authors:** Moon, Kim, et al.
- **Key Innovation:**
  - **500-µm-thick single-layer waveguide** substrate with **achromatic metagratings**
  - Dispersion-free couplers enabling true full-color AR
  - Substantially reduces device form factor while boosting brightness and color uniformity
- **Impact:** Solves the chromatic aberration problem that has plagued waveguide-based AR displays, enabling ultra-compact AR headsets

### 1.4 An Achromatic Metasurface Waveguide for AR Displays
- **Publication:** *Light: Science & Applications (Nature)* (2025) — DOI: 10.1038/s41377-025-01761-w
- **Key Innovation:** Inverse-designed metasurface couplers combined with high-refractive-index waveguide achieving true achromatic behavior and superior color accuracy
- **Impact:** Opens new direction for AR display technology by resolving chromatic aberration at the metasurface level

### 1.5 OLED-Illuminated Metasurfaces for Holographic Image Projection
- **Publication:** *Light: Science & Applications (Nature)* (2025) — DOI: 10.1038/s41377-025-01912-z
- **Key Innovation:** Combining organic semiconductors (OLEDs) with holographic metasurfaces for compact projection
- **Impact:** Eliminates need for external laser illumination; potential for self-emissive holographic displays

---

## 2. DEEP LEARNING FOR METASURFACE DESIGN

### 2.1 On-Demand Design of Holographic Metasurfaces using Deep Learning
- **Publication:** *Materials & Design* (2024)
- **Key Innovation:** Deep learning method achieving MAE of 0.04 for on-demand metasurface design. End-to-end network maps target holographic patterns directly to physical meta-atom geometries.

### 2.2 Advances in Deep Learning-Driven Metasurface Design
- **Publication:** *Photonics* (MDPI, 2024)
- **Coverage:** Comprehensive review of DL integration with metasurface holographic imaging, propelling optical imaging and display development.

### 2.3 3D Holographic Metasurface Design by Deep Learning with Physical Prior
- **Publication:** *Photonics Research* (Optica, 2024)
- **Key Innovation:** Incorporation of physical priors (EM wave physics) into neural network training to ensure physically realizable designs with high fidelity.

### 2.4 Deep-Learning-Empowered Holographic Metasurface
- **Publication:** *ACS Applied Materials & Interfaces* 
- **Key Innovation:** Inverse design of meta-atoms simultaneously and independently controlling phase AND amplitude of transmitted waves. Dual-polarization capability.

### 2.5 Tensor Holography (MIT)
- **Publication:** *Nature* **592**, 80–85 (2021); **V2** (2024)
- **Authors:** L. Shi, B. Li, C. Kim, P. Kellnhofer, W. Matusik (MIT CSAIL)
- **Key Innovation:** First deep learning-based CGH pipeline for photorealistic color 3D holograms from a single RGB-D image in real time using CNNs. Created MIT-CGH-4K dataset (4,000 image-hologram pairs).
- **V2 Improvements:** End-to-end synthesis of 3D phase-only holograms with deep double phase encoding.

### 2.6 Deep Learning for Computer-Generated Holography - Comprehensive Review
- **Publication:** *iScience* (Cell Press, 2025)
- **Coverage:** Comprehensive review examining DL-based CGH (DLCGH) development, from fundamentals to cutting-edge applications, including metasurface design integration.

---

## 3. END-TO-END OPTIMIZATION FRAMEWORKS

### 3.1 End-to-End Design of High-Dimensional Multiplexed Metasurfaces
- **Publication:** *Laser & Photonics Reviews* (2025) — DOI: 10.1002/lpor.202502573
- **Key Innovation:** Fully differentiable end-to-end framework enabling efficient polarization, wavelength, and angular multiplexing. Co-optimizes metasurface physical structures with target optical performance.

### 3.2 End-to-End Metasurface Inverse Design for Single-Shot Multi-Channel Imaging
- **Publication:** *Optics Express* (2022, MIT)
- **Key Innovation:** Large-area metasurface designs for multi-spectral imaging, depth-spectral imaging, and all-optical processing. Adjoint-based optimization nested within end-to-end pipeline.

### 3.3 End-to-End Design of Metasurface-Based Complex-Amplitude Holograms
- **Publication:** *PMC / NIH* (2024)
- **Key Innovation:** Unsupervised physics-driven deep neural network for complex-amplitude hologram design using artificial meta-atom blocks. Simultaneous amplitude and phase control.

### 3.4 End-to-End Multichannel Holographic Metasurface Inverse Design
- **Publication:** *Optics Express* (2025) — DOI: 10.1364/OE.553142
- **Key Innovation:** Periodicity-aware modified gradient descent (MGD) combined with enhanced bidirectional neural network. Optimizes multichannel holographic performance simultaneously.

### 3.5 End-to-End Optimization of Metasurfaces for Imaging with Compressed Sensing
- **Publication:** arXiv:2201.12348 (2024 update)
- **Key Innovation:** Nests iterative compressed sensing reconstruction into end-to-end optimization pipeline. Demonstrates physically realizable metasurfaces approaching mathematical limits of compressed sensing.

### 3.6 Overcoming Information Sparsity in Metasurfaces for Full-Color Holography
- **Publication:** *Nano Letters* (ACS, 2025) — DOI: 10.1021/acs.nanolett.5c02573
- **Key Innovation:** E2E system for RGB meta-hologram generation determining optimal material and geometry. Addresses fundamental information capacity limits of metasurface pixels.

---

## 4. ACTIVE/TUNABLE METASURFACE HOLOGRAPHY

### 4.1 Tunable Holographic Metasurfaces for AR/VR
- **Publication:** *Nanophotonics* (De Gruyter, 2024) — DOI: 10.1515/nanoph-2024-0734
- **Key Innovation:** Comprehensive review of tunable metasurfaces as a platform for AR/VR devices, enabling precise light control at subwavelength scale.

### 4.2 Electrically Tunable Metasurface for Real-Time THz Holography
- **Publication:** *SPIE / phys.org* (Sept 2025)
- **Key Innovation:** "Microladder" metasurface with electrically controlled THz response. Enables real-time holographic imaging, stable low-power platform for fast THz optical modulation.

### 4.3 Dynamic 3D Metasurface Holography via Cascaded Polymer Dispersed Liquid Crystal (PDLC)
- **Publication:** *Microsystems & Nanoengineering* (Nature, 2024) — DOI: 10.1038/s41378-024-00855-6
- **Key Innovation:** Cascaded device with PDLC and broadband metasurface enabling dynamic 3D holography. Electrically switchable between multiple holographic patterns.

### 4.4 Liquid Crystal on Metasurfaces (LCoMs) Toward Dynamic Photonic Control
- **Publication:** *Advanced Functional Materials* (2025) — DOI: 10.1002/adfm.202529188
- **Key Innovation:** Review of emerging LCoM concept integrating soft-matter responsiveness with nanoscale photonic design for tunable holographic devices.

### 4.5 Vectorial Liquid-Crystal Holography
- **Publication:** *eLight* (Springer Nature, 2024) — DOI: 10.1186/s43593-024-00061-x
- **Key Innovation:** Pixelated single-layer LC displaying versatile and tunable vectorial holography. Independent control of polarization and amplitude.

### 4.6 Dynamic Vectorial Liquid-Crystal Metasurface
- **Coverage in Nature Index:** Pixelates LC layer atop static holographic substrate for arbitrary, independent amplitude and polarization control at each pixel.

### 4.7 Optically Addressed Metasurface Spatial Light Modulator (OA-MSLM)
- **Publication:** *Nature* (2025) — DOI: 10.1038/s41586-025-08729-1 (anticipated)
- **Key Innovation:** 
  - **Sub-micrometer pixel pitch** using optical addressing of independently tunable meta-atom supercells
  - Spatiotemporal product density: **2.3 × 10¹² pixels·s⁻¹·cm⁻²** (meets threshold for true holography)
  - Real-time complex-amplitude holography, 3D focusing, and beam steering over ±20.6° FOV in visible spectrum
- **Impact:** Revolutionary paradigm in wavefront control — bridges the gap between metasurface resolution and dynamic SLM functionality

### 4.8 Nonvolatile Phase-Only Transmissive Spatial Light Modulator
- **Publication:** *ACS Nano* (2024) — DOI: 10.1021/acsnano.4c00340
- **Key Innovation:** Sb₂Se₃ phase-change material (PCM) based SLM with nonvolatile operation — no power needed to hold static state. Enables energy-efficient holographic displays.

---

## 5. METASURFACE WAVEGUIDES FOR AR/VR HOLOGRAPHY (STANFORD/META)

### 5.1 Stanford Computational Imaging Lab (Prof. Gordon Wetzstein)
**Key people:** Gordon Wetzstein (PI), Suyeon Choi (PhD → Postdoc), Manu Gopakumar, Gun-Yeal Lee, Brian Chao, Yifan Peng, Jonghyun Kim

**Major Contributions:**
1. **Nature 2024** — Full-color 3D holographic AR with metasurface waveguides
2. **Nature Photonics 2025** — Synthetic aperture waveguide holography (with Meta)
3. **SIGGRAPH 2022** — Time-multiplexed neural holography
4. **SIGGRAPH 2022** — Holographic glasses for VR
5. **SIGGRAPH 2024** — Holographic parallax for improved 3D perceptual realism
6. **SIGGRAPH Asia 2024** — Large étendue 3D holographic display
7. **Gaussian Wave Splatting** — Novel CGH algorithm (SIGGRAPH 2025)

**Approach:** Co-design of nanophotonic metasurface waveguides + AI-driven holography algorithms + camera-in-the-loop optimization.

### 5.2 Meta Display Systems Research (Douglas Lanman)
**Key people:** Douglas Lanman (Director)

**Major Contributions:**
1. **Nature Photonics 2025** — Synthetic aperture waveguide holography (with Stanford)
2. **"Holocake"** — Previous generation compact VR optics
3. **Holographic VR glasses** — < 3mm optical stack targeting glasses-like VR

**Approach:** Waveguide holography combined with AI-based CGH, focusing on large étendue for practical MR systems.

### 5.3 Achromatic Metasurface Waveguide Technologies (2025)
- **Light: Science & Applications** — Achromatic metasurface waveguide
- **Nature Nanotechnology** — Single-layer waveguide with achromatic metagratings (500 µm substrate)
- **Optica** — Tandem achromatic metasurface for waveguide coupling in full-color AR

---

## 6. TIME-MULTIPLEXED NEURAL HOLOGRAPHY

### 6.1 Time-Multiplexed Neural Holography: A Flexible Framework
- **Publication:** *ACM SIGGRAPH 2022* (Updated 2024)
- **Authors:** S. Choi, M. Gopakumar, Y. Peng, J. Kim, G. Wetzstein
- **Key Innovation:**
  - Framework for holographic near-eye displays with **fast, heavily-quantized spatial light modulators**
  - **Camera-calibrated wave propagation models** for accurate physical modeling
  - Robust optimization of heavily quantized phase patterns
  - Supports 2D, 2.5D RGB-D, 3D focal stacks, and 4D light fields
- **Code:** Open source at github.com/computational-imaging/time-multiplexed-neural-holography

### 6.2 Time-Multiplexed Neural Network for Focal Cues
- **Publication:** *Optics & Laser Technology* (2025)
- **Key Innovation:** Neural network framework based on time multiplexing for obtaining 3D CGH with obvious focal cues and natural defocus blur from 2D input images.

### 6.3 Holographic Parallax
- **Publication:** *ACM SIGGRAPH 2024 Emerging Technologies*
- **Authors:** Kim, Nam, Choi, et al.
- **Key Innovation:** Time-multiplexed neural holography applied to improve 3D perceptual realism through enhanced parallax cues.

---

## 7. HOLOGRAPHIC GLASSES AND NEAR-EYE DISPLAYS

### 7.1 See-Through Conformable Holographic Metasurface Patches
- **Publication:** *Laser & Photonics Reviews* (2024)
- **Key Innovation:** Flexible holographic metasurface patches that can turn any pair of glasses into AR glasses. Conformable, low-cost approach.

### 7.2 Metasurfaces for Near-Eye Display Applications - Review
- **Publication:** *Opto-Electronic Science* (2023-2024)
- **Coverage:** Comprehensive review of three mainstream metasurface devices for NED:
  - **Metalenses** — replacing bulky objective lenses
  - **Metacouplers** — waveguide in/out-coupling with high efficiency
  - **Metaholograms** — direct holographic image generation

### 7.3 Stanford Metasurface Display for AR/VR (Brongersma Lab)
- **Key Innovation:** Non-repeating 2D pattern metasurface supporting high efficiencies and wide FOV. Dynamic contrast control enables switching between AR and VR modes. Polarization control for dimming environmental light.

---

## 8. RECENT BREAKTHROUGHS — FULL-COLOR 3D HOLOGRAPHIC AR

### 8.1 Stanford Computational Imaging + Meta — The Two Foundational Papers

| Paper | Journal | Year | Innovation |
|-------|---------|------|------------|
| Full-colour 3D holographic augmented-reality displays with metasurface waveguides | *Nature* | 2024 | First glasses-like AR headset with inverse-designed metasurface gratings + AI holography |
| Synthetic aperture waveguide holography for compact mixed-reality displays with large étendue | *Nature Photonics* | 2025 | < 3mm VR glasses with large étendue waveguide + novel CGH framework |

### 8.2 Gaussian Wave Splatting for CGH
- **Publication:** *ACM SIGGRAPH 2025*
- **Authors:** S. Choi, B. Chao, J. Yang, M. Gopakumar, G. Wetzstein
- **Key Innovation:** Novel algorithm converting optimized 2D Gaussians from 3D Gaussian Splatting into holograms. Bridges neural rendering (3DGS) with holographic display.

### 8.3 Holographic Multiplexing Metasurface with Twisted Diffractive Neural Network
- **Publication:** *Nature Communications* **15**, 9416 (2024)
- **Authors:** Fan, Qian, et al.
- **Key Innovation:** Introduces "meta-disk" concept to expand capacity limits of optical holographic storage. Physical twisted neural network describes optical behavior of the meta-disk. Multi-dimensional holographic multiplexing.

### 8.4 36-Channel Spin and Wavelength Co-Multiplexed Metasurface Holography
- **Publication:** *Advanced Science* (Wiley, 2025)
- **Key Innovation:** Single-cell metasurface multiplexing holographic images across 36 channels using spin and wavelength. Achieves massive information capacity.

### 8.5 Ultranarrow-Linewidth Wavelength-Vortex Metasurface Holography
- **Publication:** *Science Advances* (2024) — DOI: 10.1126/sciadv.adt9159
- **Key Innovation:** Harnesses multiple degrees of freedom (wavelength + orbital angular momentum) for enhanced information channel capacity.

### 8.6 Vectorial Holography — Ultrathin Metasurface
- **Publication:** *Light: Science & Applications* (2025)
- **Key Innovation:** High-efficiency vectorial holography enabling arbitrary polarization state control in reconstructed images.

---

## 9. LEADING RESEARCH GROUPS WORLDWIDE

### 9.1 Stanford University
- **Lab:** Computational Imaging Lab (Prof. Gordon Wetzstein)
- **Focus:** AI-driven CGH, metasurface waveguides, camera-in-the-loop optimization, neural holography
- **Key People:** Gordon Wetzstein, Suyeon Choi, Manu Gopakumar, Gun-Yeal Lee, Brian Chao
- **Flagship:** *Nature* 2024 AR glasses, *Nature Photonics* 2025 synthetic aperture waveguide

### 9.2 MIT CSAIL
- **Lab:** Computational Fabrication Group (Prof. Wojciech Matusik)
- **Focus:** Tensor holography, deep learning for CGH, 3D printing optics
- **Key People:** Wojciech Matusik, Liang Shi
- **Flagship:** *Nature* 2021 Tensor Holography, Tensor Holography V2

### 9.3 Meta Reality Labs / Display Systems Research
- **Focus:** Waveguide holography, VR glasses form factor, large étendue systems
- **Key People:** Douglas Lanman
- **Flagship:** *Nature Photonics* 2025 synthetic aperture holography

### 9.4 Seoul National University (SNU)
- **Lab:** Prof. Byoungho Lee's group
- **Focus:** Holographic displays, aberration correction, full-color AR near-eye displays, PB phase lenses
- **Key People:** Byoungho Lee, Dongyeon Kim

### 9.5 Caltech
- **Lab:** Atwater Research Group (Prof. Harry Atwater)
- **Focus:** Active metasurfaces in space and time, tunable nanophotonics
- **Flagship:** META 2024 plenary — "Active Metasurfaces in Space and Time"

### 9.6 Princeton University
- **Lab:** Computational Imaging Lab (Prof. Felix Heide)
- **Focus:** Meta-optics, hardware-in-the-loop, end-to-end optimization
- **Flagship:** Meta-optics computational imaging, end-to-end optimization of metasurfaces

### 9.7 Zhejiang University / Nanjing University (China)
- **Groups:** Various (Hongsheng Chen, Zuojia Wang, Chao Qian, et al.)
- **Focus:** Deep learning for metasurfaces, twisted diffractive neural networks, multiplexed holography
- **Flagship:** *Nature Communications* 2024 — twisted diffractive neural network metasurface

### 9.8 UNIST/POSTECH (Korea)
- **Lab:** Prof. Junsuk Rho (POSTECH) / MetAI Lab
- **Focus:** Inverse design, deep learning for metasurfaces, dual-functional metasurfaces for holography + color printing
- **Key People:** Junsuk Rho, Trevon Badloe, Sunae So

---

## 10. FUTURE DIRECTIONS

### 10.1 Metasurface + AI Co-Design
The biggest trend is **co-design of metasurface optics and AI-driven holographic algorithms**. Rather than treating optics and computation separately, the Stanford/Meta approach demonstrates that joint optimization achieves results neither could achieve alone. Expect this to become the dominant paradigm.

### 10.2 Ultra-Compact Form Factors
The push toward **true glasses-like form factors** (< 3mm optical stack) is accelerating. Key enablers:
- Achromatic metasurface waveguides (solving color dispersion at the component level)
- Lensless holographic light engines (eliminating collimation optics)
- Single-layer waveguide substrates (500 µm demonstrated)

### 10.3 Dynamic/Tunable Metasurfaces
The next frontier is **moving from static to dynamic metasurfaces**:
- LC-integrated metasurfaces (LCoMs) for electrical tunability
- Optically addressed metasurface SLMs with sub-micron pixel pitch
- Phase-change materials (PCMs) for nonvolatile operation
- Microladder/polymer-dispersed LC approaches for real-time switching

### 10.4 3D Neural Rendering + Holography Integration
**Gaussian Wave Splatting for CGH** represents a convergence of 3D neural scene representation (3DGS) with holographic display. This trend will likely accelerate, enabling photorealistic 3D holograms directly from neural scene representations.

### 10.5 Large Étendue Systems
The synthetic aperture approach from Stanford/Meta addresses the fundamental étendue challenge that has limited waveguide holography. Expect continued work on:
- Partial coherence modeling for large eye boxes
- Mutual intensity propagation in waveguides
- Extended eye-box designs without sacrificing FOV

### 10.6 High-Dimensional Multiplexing
Moving beyond conventional multiplexing:
- **36-channel spin/wavelength** multiplexing demonstrated
- **Twisted diffractive neural networks** for optical storage
- **OAM + wavelength + polarization** combined multiplexing
- Pushing toward hundreds of independent channels

### 10.7 True Holographic SLMs
The optically addressed metasurface SLM (sub-micron pixels, 2.3×10¹² pixels·s⁻¹·cm⁻²) finally meets the spatiotemporal product threshold for "true holography." This opens possibilities for:
- Full complex-amplitude modulation
- Wide-angle beam steering (> ±20°)
- Real-time 3D holographic video at visible wavelengths

### 10.8 Full-Color and Chromatic Correction
Multiple approaches to chromatic correction are converging:
- Achromatic metagratings (Nature Nanotech 2025)
- Inverse-designed dispersion-compensating waveguides (Nature 2024)
- Tandem achromatic metasurfaces (Optica 2025)
- PB phase-based dispersion engineering

### 10.9 Manufacturing and Scalability
Critical challenges remaining:
- Large-area fabrication of metasurfaces with nanometer precision
- Wafer-scale compatible processes for volume production
- Reducing sensitivity to fabrication tolerances through robust inverse design

---

## 11. KEY TAKEAWAYS SUMMARY

1. **2024-2025 is a transformative period** — two landmark *Nature*/*Nature Photonics* papers from Stanford/Meta have demonstrated that **metasurface waveguide + AI holography** is a viable path to true holographic AR/VR glasses.

2. **Deep learning has become integral to metasurface CGH**, enabling everything from inverse design of meta-atoms to real-time hologram synthesis to camera-in-the-loop calibration.

3. **End-to-end optimization** frameworks that simultaneously optimize meta-atom geometry, waveguide performance, and holographic algorithms represent the state of the art.

4. **Active/tunable metasurfaces** are progressing rapidly, with LC integration, PCMs, and optically addressed architectures enabling dynamic modulation at sub-micron scales.

5. **The convergence of 3D neural rendering (Gaussian Splatting) with holography** is an exciting new frontier for photorealistic 3D AR.

6. **Key challenges remain**: manufacturing scalability, wide FOV with large eye box, full-color achromatic operation, and computational efficiency for battery-powered wearables.

7. **The leading groups** are Stanford (Wetzstein), MIT (Matusik), Meta Reality Labs (Lanman), Caltech (Atwater), SNU (B. Lee), Princeton (Heide), and several Chinese/Korean groups making rapid advances.

---

*Report generated October 2025 based on web and database searches spanning Nature, Nature Photonics, Nature Nanotechnology, Nature Communications, Science Advances, Light: Science & Applications, ACM SIGGRAPH, Optica, ACS Nano, Nano Letters, and arXiv preprints.*

