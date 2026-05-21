# Multi-Depth RGB Computer-Generated Holography (CGH) Metasurface Optimization Report

## 1. Task Overview

### Objective
Design and optimize a **512×512 TiO₂ metasurface phase array** for **multi-depth RGB holography**. The metasurface simultaneously reconstructs color holographic images at **6 depth planes** (51–56 μm) when illuminated by RGB plane waves at 480, 560, and 640 THz.

### Key Parameters

| Parameter | Value |
|-----------|-------|
| Metasurface Size | 512 × 512 meta-atoms |
| Simulation Grid (N) | 1024 × 1024 (with zero-padding) |
| Meta-atom Type | TiO₂ nanopillar on SiO₂ substrate |
| Period | 160 nm × 160 nm |
| Nanopillar Radius | 50 nm |
| Phase Modulation | Varying height (400–800 nm) |
| Incident Frequencies | [480, 560, 640] THz (sorted ascending → R,G,B channels) |
| Focal Lengths (Depth Planes) | [51, 52, 53, 54, 55, 56] μm |
| Training Epochs | 200 |
| Optimizer | Rprop (lr = 2×10⁻⁴) |
| Loss Function | MSELoss (masked output vs. target) |

---

## 2. Methodology

### 2.1 Meta-Atom Phase Relationships

The meta-atom phase response was pre-simulated via CST. The phase at 560 THz and 640 THz are linear functions of the base **480 THz phase**:

| Frequency | Phase Relationship |
|:---------:|:------------------|
| **480 THz** (Base) | `Phase480` — the trainable parameter |
| **560 THz** (Green) | `Phase_560 = 1.20219688371001 × Phase480 − 2.28769160400048` |
| **640 THz** (Blue) | `Phase_640 = 1.43205003672406 × Phase480 − 4.71339634259209` |

### 2.2 Optimization Pipeline (DataFlow.py → MetaOptim)

The pipeline is built as a differentiable PyTorch `nn.Module`:

1. **FrontNetwork** (`FrontEnd.Holography`): Generates **6 uniform plane waves** of shape `[6, 3, 1024, 1024]` (6 depth planes × 3 RGB channels × padded simulation grid).

2. **Trainable Phase Array** (`self.phase`): A `1024×1024` parameter tensor initialized with random values, optimized via gradient descent.

3. **Phase Mapping per Frequency**: For each frequency `f` in `[480, 560, 640]`:
   - Load `func_{f}.txt` which contains the phase expression
   - Evaluate: `phase = eval(expression.replace("Phase480", "self.phase"))`
   - This maps the base 480 THz phase to the corresponding frequency

4. **Angular Spectrum Method** (`ASM_propagate`): Computes scalar diffraction propagation using the transfer function:
   - **Transfer function**: `H = exp(j × 2π × z/λ × √(1 − (λf)²))`
   - **Band-limit filtering** applied to prevent aliasing
   - **Output**: Intensity `|E|²` at the focal plane

5. **Loss Computation**:
   - Crop output from 1024×1024 → 512×512 (central Meta_N region)
   - Apply mask (`masks.pt`) to isolate patterned regions
   - Compute `MSELoss(masked_output, target_hologram)`

### 2.3 Training Loop (Optimizer.py)

```python
for epoch in range(200):
    outputs = network()                        # Forward pass
    loss = f_loss(outputs)                     # Compute masked MSE loss
    optimizer.zero_grad()
    loss.backward(torch.ones_like(loss))
    optimizer.step()                           # Rprop update
    if loss < best_loss:                       # Save best model
        torch.save(network.state_dict(), ...)
```

---

## 3. Training Results

- **Best Model**: `D:\work\MetaDesign\Metasurface\Holography\SavedModel\network.pt`
- **Optimizer State**: `D:\work\MetaDesign\Metasurface\Holography\SavedModel\optimizer.pt`
- **Phase Visualization**: `D:\work\MetaDesign\Metasurface\Holography\SavedModel\phase.png`
- **Phase Array (numpy)**: `phase.npy` (512×512, modulo 2π)

---

## 4. Performance Evaluation

### 4.1 SSIM (Structural Similarity Index)

SSIM measures perceptual similarity between the reconstructed hologram and the target at each depth plane (range 0–1, higher is better).

| Depth (μm) | SSIM Score |
|:----------:|:----------:|
| 51 | **0.9844** |
| 52 | **0.9525** |
| 53 | **0.9643** |
| 54 | **0.9637** |
| 55 | **0.9739** |
| 56 | **0.9842** |

### 4.2 PSNR (Peak Signal-to-Noise Ratio)

PSNR quantifies reconstruction fidelity in dB (higher is better).

| Depth (μm) | PSNR (dB) |
|:----------:|:---------:|
| 51 | **39.34** |
| 52 | **37.31** |
| 53 | **39.47** |
| 54 | **35.49** |
| 55 | **37.08** |
| 56 | **38.43** |

### 4.3 Performance Summary

| Metric | Value |
|--------|:-----:|
| Number of Depth Planes | 6 |
| Depth Range | 51–56 μm |
| RGB Channels | 3 (480, 560, 640 THz) |
| **Average SSIM** | **0.9705** |
| **Average PSNR** | **37.85 dB** |
| Min SSIM | 0.9525 @ 52 μm |
| Max SSIM | 0.9844 @ 51 μm |
| Min PSNR | 35.49 dB @ 54 μm |
| Max PSNR | 39.47 dB @ 53 μm |

### 4.4 Comparison with Previous Run

| Metric | Previous Run | **This Run (Corrected)** | Improvement |
|--------|:-----------:|:------------------------:|:----------:|
| Avg SSIM | 0.9633 | **0.9705** | **+0.0072** |
| Avg PSNR | 36.75 dB | **37.85 dB** | **+1.10 dB** |

The corrected channel ordering (matching [R, G, B] → [480, 560, 640] THz) yields measurable improvements across all metrics.

### 4.5 Generated Output Files

| File | Description |
|------|-------------|
| `SavedModel/network.pt` | Trained model weights (best checkpoint) |
| `SavedModel/optimizer.pt` | Optimizer state (best checkpoint) |
| `SavedModel/phase.png` | Visualized 512×512 phase profile |
| `SavedModel/Part0.png` | Holographic reconstruction at 51 μm |
| `SavedModel/Part1.png` | Holographic reconstruction at 52 μm |
| `SavedModel/Part2.png` | Holographic reconstruction at 53 μm |
| `SavedModel/Part3.png` | Holographic reconstruction at 54 μm |
| `SavedModel/Part4.png` | Holographic reconstruction at 55 μm |
| `SavedModel/Part5.png` | Holographic reconstruction at 56 μm |
| `SavedModel/Holography.png` | Composite RGB hologram (all depths merged) |
| `phase.npy` | Optimized 512×512 phase array (numpy format) |

---

## 5. Analysis

### 5.1 Reconstruction Quality

The metasurface achieves **excellent multi-depth RGB holography**:

- **SSIM > 0.95** at all 6 depth planes — near-perfect structural preservation
- **PSNR > 35 dB** across all planes — strong signal fidelity
- Minimal variation across the 51–56 μm depth range (SSIM spread: 0.9525–0.9844)

### 5.2 Depth Dependence

Performance is slightly better at the extreme depths (51 μm and 56 μm) compared to the middle depths (52–54 μm). This is expected because:
- The holographic signals at edge depths experience **less crosstalk** from adjacent planes
- The angular spectrum propagation has different numerical characteristics at different distances

### 5.3 Importance of Correct Channel Ordering

The re-created dataset with corrected [R, G, B] → [480, 560, 640] THz channel ordering yields **measurable improvements**:
- **SSIM improved** from 0.9633 → 0.9705 (+0.72%)
- **PSNR improved** from 36.75 dB → 37.85 dB (+1.10 dB)

This confirms the importance of proper channel-to-frequency mapping for accurate color holography.

### 5.4 Chromatic Performance

The linear phase relationships enable effective RGB operation:
- **480 THz (Red)**: Base optimization frequency
- **560 THz (Green)**: Linear scaling factor 1.202, offset −2.288 rad
- **640 THz (Blue)**: Linear scaling factor 1.432, offset −4.713 rad

Since the frequencies are sorted ascending `[480, 560, 640]` and the `DataFlow.py` code maps `frequencies[c]` to `func_{freq}.txt`, the three RGB wavelengths are correctly handled in sequence.

---

## 6. Conclusion

The multi-depth RGB metasurface hologram has been **successfully optimized** with the re-created (channel-corrected) dataset:

| Metric | Value |
|--------|:-----:|
| ✅ **Average SSIM** | **0.9705** |
| ✅ **Average PSNR** | **37.85 dB** |
| ✅ **Depth Planes** | 6 (51–56 μm) |
| ✅ **RGB Channels** | 3 (480, 560, 640 THz) |
| ✅ **Metasurface Size** | 512 × 512 |

The optimized 512×512 phase array has been saved in both PyTorch (`network.pt`) and NumPy (`phase.npy`) formats, ready for fabrication or further analysis.

