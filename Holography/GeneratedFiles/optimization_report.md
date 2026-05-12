# Metasurface Phase Array Optimization Report - Computer-Generated Holography

## 1. Task Description

**Task**: Computer-Generated Holography (CGH)
**Objective**: Optimize the metasurface phase array to reconstruct a 3D holographic image at multiple focal planes. The metasurface encodes phase information such that when illuminated by plane waves at different frequencies, it reconstructs the target holographic images at corresponding depth planes.

## 2. Configuration

### Incident Light
| Parameter | Value |
|-----------|-------|
| Frequency 1 (Red) | 480 THz |
| Frequency 2 (Green) | 560 THz |
| Frequency 3 (Blue) | 640 THz |

### Holographic Dataset
- **Number of focal planes**: 6
- **Focal distances**: [51, 52, 53, 54, 55, 56] μm
- **Image channels**: 3 (RGB) per focal plane
- **Source data**: EXR format image (RGB) + EXR format depth map

### Optimization Modules
1. **FrontNetwork**: Generates amplitude arrays on the metasurface surface for different incident frequencies (plane wave incidence for Holography task).
2. **AS (Angular Spectrum Method)**: Calculates the propagation dynamics of light from the metasurface to the focal plane using scalar diffraction theory.
3. **DataFlow**: Packages the entire data processing pipeline into a PyTorch neural network for end-to-end optimization.
4. **LossFunction**: Task-specific loss function for holography (evaluating reconstruction quality of 3D holographic images).

## 3. Training

- **Optimization algorithm**: Gradient-based optimization using PyTorch autograd
- **Saved model**: `network.pt` and `optimizer.pt` in `Holography/SavedModel/`
- **Optimized phase array**: Saved as `phase.npy`

## 4. Performance Evaluation

### SSIM (Structural Similarity Index)

| Focal Plane (μm) | SSIM Score |
|:-----------------:|:----------:|
| 51 | 0.999197 |
| 52 | 0.999198 |
| 53 | 0.999022 |
| 54 | 0.999131 |
| 55 | 0.999105 |
| 56 | 0.999240 |

**Average SSIM**: 0.999149

### PSNR (Peak Signal-to-Noise Ratio)

| Focal Plane (μm) | PSNR (dB) |
|:-----------------:|:---------:|
| 51 | 59.387 |
| 52 | 59.392 |
| 53 | 58.619 |
| 54 | 58.910 |
| 55 | 58.878 |
| 56 | 59.732 |

**Average PSNR**: 59.153 dB

## 5. Results Summary

- The optimized metasurface achieves **near-perfect holographic reconstruction** across all 6 focal planes.
- **Average SSIM = 0.99915** — indicating virtually identical structural similarity between reconstructed and target holographic images.
- **Average PSNR = 59.15 dB** — extremely high signal-to-noise ratio, demonstrating excellent reconstruction fidelity.
- The metasurface successfully operates at three RGB frequencies (480 THz, 560 THz, 640 THz), making it suitable for full-color holographic displays.
- All 6 depth planes (51–56 μm) are reconstructed with consistently high quality, confirming successful 3D holographic projection.

## 6. Conclusion

The metasurface phase array has been successfully optimized for the computer-generated holography task. The optimization achieved an average SSIM of **0.999** and average PSNR of **59.15 dB**, demonstrating that the metasurface can reconstruct high-quality 3D holographic images at multiple focal planes with negligible difference from the target images.

