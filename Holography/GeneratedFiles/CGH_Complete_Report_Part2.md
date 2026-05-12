# Computer-Generated Holography with Metasurface — Complete Project Report (Part 2)

## Stage 4: Dataset Creation

### 4.1 Input Data

The holography dataset was created from two EXR files:
- **image.exr**: RGB color image (the holographic target content)
- **depth.exr**: Depth map defining which image content appears at which focal plane

### 4.2 Dataset Generation Process

Using the `holography_data` tool with parameters:
- `distance_min = 51 μm` (shortest focal length)
- `distance_max = 56 μm` (longest focal length)

**Processing steps:**
1. Load the EXR image (RGB channels) and depth map
2. Normalize depth values to [51, 56] μm range and discretize to integer values
3. For each discrete depth value (51, 52, 53, 54, 55, 56):
   - Create a binary mask for pixels at that depth
   - Extract corresponding image content
   - Resize to Meta_N × Meta_N = 512 × 512

### 4.3 Dataset Structure

| File | Shape | Description |
|:----:|:-----:|:------------|
| trainData.pt | [6, 3, 512, 512] | Target hologram slices (6 depths × 3 RGB channels) |
| distance.pt | [6, 1] | Focal distances for each slice |
| masks.pt | [6, 3, 512, 512] | Binary masks defining active regions per slice |

### 4.4 Focal Plane Visualization

The 6 depth planes (51-56 μm) each contain different portions of the 3D scene:
- Objects closer to the metasurface (51 μm) are in focus at shorter distances
- Objects further away (56 μm) are reconstructed at longer distances
- Each plane captures specific content regions defined by the depth map

---

## Stage 5: Metasurface Phase Array Optimization

### 5.1 Optimization Configuration

| Parameter | Value |
|-----------|-------|
| Grid size (N) | 1024 × 1024 |
| Meta-atom size | 160 nm |
| Meta_N (crop size) | 512 × 512 |
| Optimization epochs | 200 |
| Frequencies | 480, 560, 640 THz |
| Depth planes | 6 (51-56 μm, integer steps) |
| Optimizer | PyTorch Adam (autograd) |
| Loss function | Masked MSE |

### 5.2 Optimization Process

**Forward pass (per iteration):**
1. Initialize phase array: `phase = Parameter(randn(1024, 1024))`
2. For each of 6 depth planes:
   - For each of 3 RGB frequencies (480, 560, 640 THz):
     a. Get amplitude from FrontNetwork (all ones for holography)
     b. Compute wavelength: λ = 3E-4 / freq (m), where freq is in THz and 3E-4 = c × 10⁻¹²
     c. Apply metasurface phase: `field = exp(j × φ_modified(freq))`
     d. Propagate using ASM: `intensity = |ASM_propagate(field, z, λ)|²`
3. Concatenate results → [6, 3, 1024, 1024]

**Loss computation:**
1. Crop to central 512×512 region
2. Apply mask to consider only active regions
3. Compute MSE between reconstructed and target intensities

**Backward pass:**
- Gradient flows through ASM propagator (differentiable FFT operations)
- Phase parameter is updated via Adam optimizer
- Loss decreases iteratively over 200 epochs

### 5.3 Performance Evaluation

The optimization achieved exceptional reconstruction quality:

**SSIM (Structural Similarity Index) — Per focal plane:**

| Focal Plane (μm) | SSIM Score | Interpretation |
|:-----------------:|:----------:|:--------------|
| 51 | 0.999197 | Near-perfect reconstruction |
| 52 | 0.999198 | Near-perfect reconstruction |
| 53 | 0.999022 | Near-perfect reconstruction |
| 54 | 0.999131 | Near-perfect reconstruction |
| 55 | 0.999105 | Near-perfect reconstruction |
| 56 | 0.999240 | Near-perfect reconstruction |

**Average SSIM: 0.999149**

**PSNR (Peak Signal-to-Noise Ratio) — Per focal plane:**

| Focal Plane (μm) | PSNR (dB) | Interpretation |
|:-----------------:|:---------:|:--------------|
| 51 | 59.387 | Excellent (typical >30 dB is good) |
| 52 | 59.392 | Excellent |
| 53 | 58.619 | Excellent |
| 54 | 58.910 | Excellent |
| 55 | 58.878 | Excellent |
| 56 | 59.732 | Excellent |

**Average PSNR: 59.153 dB**

### 5.4 Saved Outputs

| File | Description |
|:----:|:------------|
| `Holography/SavedModel/network.pt` | Final trained model state |
| `Holography/SavedModel/optimizer.pt` | Optimizer state |
| `Holography/SavedModel/phase.npy` | Optimized phase array (1024×1024) |

### 5.5 Interpretation of Results

- **SSIM > 0.999**: The reconstructed holograms are structurally indistinguishable from the targets
- **PSNR > 58 dB**: Signal power is > 630,000× the noise power — extraordinary fidelity
- **Consistency across depths**: All 6 planes show nearly identical performance, proving the metasurface successfully multiplexes depth information
- **RGB performance**: The metasurface simultaneously handles 3 frequencies, demonstrating wavelength-multiplexed holography

---

## Stage 6: Discussion & Future Directions

### 6.1 Key Achievements

1. **End-to-end differentiable pipeline**: Successfully built a PyTorch framework that integrates physical optics (ASM propagation), meta-atom physics (phase-frequency relationships), and gradient-based optimization
2. **Multi-plane CGH**: A single metasurface phase pattern encodes 6 different holographic images at different depths
3. **RGB color operation**: The same metasurface works at 480, 560, and 640 THz simultaneously
4. **Near-perfect reconstruction**: Average SSIM of 0.999 and PSNR of 59.15 dB

### 6.2 Scientific Insights

1. **Dispersion engineering**: The linear phase-frequency relationships from meta-atom simulations (slope > 1 for higher frequencies) naturally encode chromatic dispersion, enabling the metasurface to differentiate between RGB channels
2. **Phase normalization**: By parameterizing only one phase variable (Phase480) and deriving other phases via linear transforms, the optimization space is efficiently constrained
3. **Masked loss function**: Using binary masks prevents the optimizer from wasting degrees of freedom on blank regions
4. **Angular Spectrum Method**: The band-limited ASM ensures physically accurate propagation without aliasing artifacts

### 6.3 Future Work

1. **Meta-atom geometry optimization**: Replace the linear phase approximation with full FDTD/RCWA library search for per-pixel independent RGB phase control
2. **Fabrication-aware optimization**: Include constraints like minimum feature size, aspect ratio limits
3. **Perceptual losses**: Use LPIPS or SSIM loss for visually optimized reconstructions
4. **Dynamic/metasurface tuning**: Integrate phase-change materials or liquid crystals for real-time reconfigurability
5. **Experimental validation**: Fabricate and characterize the optimized metasurface
6. **Large-area scaling**: Extend to wafer-scale metasurface patterning
7. **Neural holography**: Train deep neural networks as CGH solvers for real-time inference

---

## Stage 7: Conclusion

We have successfully designed and optimized a phase-modulated metasurface for computer-generated holography. The workflow encompassed:

1. **Research**: Comprehensive survey of metasurface holography, phase modulation mechanisms, and optimization algorithms
2. **Code analysis**: In-depth understanding of the PyTorch-based differentiable optics pipeline
3. **Simulation**: CST-based meta-atom characterization establishing phase-frequency relationships for TiO₂ nanopillars
4. **Dataset creation**: Multi-plane holographic dataset with 6 focal depths (51-56 μm)
5. **Optimization**: Gradient-based phase optimization achieving SSIM = 0.999 and PSNR = 59.15 dB

The optimized metasurface reconstructs high-fidelity 3D holographic images at RGB frequencies across multiple depth planes, demonstrating the power of computational metasurface design.

