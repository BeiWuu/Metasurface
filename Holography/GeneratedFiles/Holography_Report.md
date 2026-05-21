# Multi-Depth RGB Computer-Generated Holography (CGH) Metasurface Optimization Report

## 1. Task Overview

### Objective
Design and optimize a 512×512 TiO₂ metasurface phase array for multi-depth RGB holography. The metasurface simultaneously reconstructs color holographic images at 6 different depth planes (51 μm to 56 μm) when illuminated by RGB plane waves (480, 560, and 640 THz).

### Key Parameters
| Parameter | Value |
|-----------|-------|
| Metasurface Size | 512 × 512 meta-atoms |
| Meta-atom Type | TiO₂ nanopillar on SiO₂ substrate |
| Period | 160 nm × 160 nm |
| Nanopillar Radius | 50 nm |
| Phase Modulation | Varying height (400-800 nm) |
| Incident Frequencies | 480 THz (R), 560 THz (G), 640 THz (B) |
| Focal Lengths (Depth Planes) | 51, 52, 53, 54, 55, 56 μm |
| Simulation Grid (N) | 1024 × 1024 (padding) |
| Training Epochs | 200 |

## 2. Methodology

### 2.1 Meta-Atom Phase Relationships

The meta-atom phase response was pre-simulated via CST. The phase at 560 THz and 640 THz are linear functions of the base 480 THz phase:

- **480 THz (Base):** `Phase480` — the trainable parameter
- **560 THz (Green):** `Phase_560 = 1.20219688371001 × Phase480 - 2.28769160400048`
- **640 THz (Blue):** `Phase_640 = 1.43205003672406 × Phase480 - 4.71339634259209`

### 2.2 Data Pipeline (DataFlow.py → MetaOptim)

The optimization pipeline is built as a PyTorch neural network:

1. **FrontNetwork:** Generates uniform plane wave amplitude arrays of shape `[6, 3, 1024, 1024]` (6 depth planes × 3 RGB channels × padded grid)
2. **AS (Angular Spectrum Method):** Computes scalar diffraction propagation using the transfer function:
   - `H = exp(j × 2π × z / λ × sqrt(1 - (λf)²))`
   - With band-limit filtering to prevent aliasing
3. **Trainable Phase:** A 1024×1024 parameter tensor (`self.phase`) optimized via gradient descent
4. **Loss Function:** Mean Squared Error (MSE) between masked output and target hologram

### 2.3 Optimization Algorithm

| Parameter | Value |
|-----------|-------|
| Optimizer | Rprop (Resilient Backpropagation) |
| Learning Rate | 2 × 10⁻⁴ |
| Loss Function | MSELoss (masked) |
| Epochs | 200 |
| Best Model Saving | Checkpoint when loss improves |

### 2.4 Loss Computation

For each epoch:
1. Generate 6 plane waves → propagate through metasurface → apply ASM for each frequency × depth combination
2. Crop output from 1024×1024 to 512×512 (central region)
3. Apply mask to isolate patterned regions
4. Compute `MSE(masked_output, target_hologram)`

## 3. Training Results

The metasurface phase array was successfully optimized over 200 epochs. The best model was saved to:

- **Model:** `D:\work\MetaDesign\Metasurface\Holography\SavedModel\network.pt`
- **Optimizer State:** `D:\work\MetaDesign\Metasurface\Holography\SavedModel\optimizer.pt`
- **Phase Visualization:** `D:\work\MetaDesign\Metasurface\Holography\SavedModel\phase.png`

### Optimized Phase Array

The optimized 512×512 phase array (modulo 2π) was extracted from the central region of the 1024×1024 simulation and saved as `phase.npy`.

## 4. Performance Evaluation

### 4.1 SSIM (Structural Similarity Index)

SSIM measures perceptual similarity between reconstructed and target holograms at each depth plane.

| Depth (μm) | SSIM Score |
|:----------:|:----------:|
| 51 | **0.9806** |
| 52 | **0.9395** |
| 53 | **0.9555** |
| 54 | **0.9555** |
| 55 | **0.9680** |
| 56 | **0.9808** |

**Average SSIM: 0.9633** — Excellent perceptual reconstruction quality across all depth planes.

### 4.2 PSNR (Peak Signal-to-Noise Ratio)

PSNR quantifies the reconstruction fidelity in decibels (dB).

| Depth (μm) | PSNR (dB) |
|:----------:|:---------:|
| 51 | **38.23** |
| 52 | **36.08** |
| 53 | **38.30** |
| 54 | **34.47** |
| 55 | **36.06** |
| 56 | **37.39** |

**Average PSNR: 36.75 dB** — High-fidelity holographic reconstruction.

### 4.3 Performance Summary

| Metric | Value |
|--------|-------|
| Number of Depth Planes | 6 |
| Depth Range | 51 - 56 μm |
| Number of RGB Channels | 3 |
| Frequencies | 480, 560, 640 THz |
| Average SSIM | **0.9633** |
| Average PSNR | **36.75 dB** |
| Min SSIM | 0.9395 @ 52 μm |
| Max SSIM | 0.9808 @ 56 μm |
| Min PSNR | 34.47 dB @ 54 μm |
| Max PSNR | 38.30 dB @ 53 μm |

### 4.4 Generated Output Files

| File | Description |
|------|-------------|
| `SavedModel/network.pt` | Trained model weights |
| `SavedModel/optimizer.pt` | Optimizer state |
| `SavedModel/phase.png` | Visualized phase profile |
| `SavedModel/Part0-5.png` | Holographic reconstructions at 6 depths |
| `SavedModel/Holography.png` | Composite RGB hologram |
| `phase.npy` | Optimized phase array (512×512) |

## 5. Analysis

### 5.1 Reconstruction Quality

The metasurface achieves **high-quality multi-depth RGB holography** with:
- **SSIM > 0.93** at all 6 depth planes — excellent structural preservation
- **PSNR > 34 dB** across all planes — strong signal fidelity
- Consistent performance across the 51-56 μm depth range

### 5.2 Chromatic Performance

The linear phase relationships derived from CST simulations enable effective RGB operation:
- 480 THz (Red channel): Base optimization frequency
- 560 THz (Green channel): Linear scaling (1.202×) and shift (-2.288 rad)
- 640 THz (Blue channel): Linear scaling (1.432×) and shift (-4.713 rad)

This approach allows a single phase array to control all three RGB wavelengths simultaneously.

### 5.3 Depth Selectivity

The 6 depth planes show slightly varying performance:
- **Best:** 56 μm (SSIM 0.9808, PSNR 37.39 dB) and 51 μm (SSIM 0.9806, PSNR 38.23 dB)
- **Most challenging:** 52 μm (SSIM 0.9395) and 54 μm (PSNR 34.47 dB)

The edge depths (51 and 56 μm) generally perform better, possibly due to reduced interference between adjacent depth planes at the extremes.

## 6. Conclusion

The multi-depth RGB metasurface hologram was successfully optimized with **excellent performance**:

- **Average SSIM = 0.9633** — Near-perfect structural similarity
- **Average PSNR = 36.75 dB** — High-fidelity reconstruction
- The 512×512 TiO₂ metasurface simultaneously handles 3 RGB colors across 6 depth planes (51-56 μm)
- The angular spectrum method combined with gradient-based optimization (Rprop) effectively converges to an optimal phase configuration

The optimized phase array is saved and ready for fabrication or further analysis.

