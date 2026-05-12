# Computer-Generated Holography (CGH) with Metasurfaces — Technical Report

## Part 2: CGH Algorithms & Optimization Methods

---

### 4. CGH Optimization Algorithms for Metasurface Holography

The core problem: Given a target intensity image I_target(x, y) at the reconstruction plane, find a phase-only hologram φ(x, y) on the metasurface plane such that when light propagates from the metasurface to the reconstruction plane, the intensity matches I_target.

#### 4.1 Wave Propagation Models

**Angular Spectrum Method (ASM)** — The most accurate propagation model for metasurface CGH:

```
U(x,y;z) = ℱ⁻¹{ ℱ{ U₀(x,y) } × H(fx, fy; z) }

where transfer function:
H(fx, fy; z) = exp(i × 2π/λ × z × √(1 - (λfx)² - (λfy)²))

For propagation distance z:
- fx, fy = spatial frequencies
- λ = wavelength
```

**Fresnel Propagation** — Approximate for z >> λ:
```
H_Fresnel(fx, fy; z) = exp(-iπλz(fx² + fy²))
```

**Fraunhofer Propagation** — Far-field (z → ∞):
```
U(x,y) ∝ ℱ{ U₀(x,y) }
```

For metasurface holography, **Fresnel** and **Angular Spectrum** are most commonly used since the metasurface-to-image distance is typically in the mm-cm range.

#### 4.2 Gerchberg–Saxton (GS) Algorithm

The GS algorithm is an iterative phase retrieval method that alternates between two domains (hologram plane and image plane) with constraints:

**Algorithm steps:**
```
Input: Target amplitude A_target(x,y), initial guess φ₀(x,y) (random or constant)

for iteration k = 1 to K:
    Step 1. Construct complex field at metasurface plane:
        U_hologram(x,y) = A_illumination(x,y) × exp(i × φₖ(x,y))
    
    Step 2. Propagate to image plane (forward propagation):
        U_image(x',y') = Propagate{ U_hologram(x,y), z }
    
    Step 3. Apply image constraint (replace amplitude with target, keep phase):
        U'_image(x',y') = A_target(x',y') × exp(i × angle(U_image(x',y')))
    
    Step 4. Back-propagate to hologram plane:
        U'_hologram(x,y) = Propagate{ U'_image(x',y'), -z }
    
    Step 5. Apply hologram constraint (keep phase, set amplitude to 1):
        φₖ₊₁(x,y) = angle(U'_hologram(x,y))

Output: φ_optimized(x,y)
```

**Variants for improved performance:**

- **Weighted GS (WGS):** Apply adaptive weight W(x',y') to reduce errors in bright regions:
  ```
  U'_image(x',y') = [W(x',y') × A_target + (1-W(x',y')) × |U_image|] × exp(i × angle(U_image))
  ```
- **Fienup algorithm:** Uses hybrid input-output (HIO) approach for better convergence
- **Adaptive Weighted GS (AWGS):** Dynamically adjusts weights per iteration

**Limitations of GS:**
- Prone to local minima and speckle noise
- Only 2D (single-plane) reconstruction natively
- Poor convergence for complex amplitude targets
- No direct control over reconstruction quality metrics

#### 4.3 Gradient Descent Methods (First-Order Optimization)

Formulate CGH as an **inverse optimization problem**:

```
Minimize: ℒ(φ) = ℒ_recon( I_recon(φ), I_target ) + λ × ℒ_reg(φ)

Where:
- φ = phase pattern of hologram (pixel-wise variables)
- I_recon = |Propagate{ exp(iφ), z }|²
- ℒ_recon = reconstruction loss (MSE, SSIM, LPIPS, etc.)
- ℒ_reg = regularization term (smoothness, sparsity, etc.)
- λ = regularization weight
```

**Loss functions commonly used:**
```
MSE Loss:      ℒ_MSE = || √I_recon - √I_target ||²_F
SSIM Loss:     ℒ_SSIM = 1 - SSIM(I_recon, I_target)
Amplitude Loss: ℒ_amp = || |U_recon| - A_target ||²_F
Complex Loss:  ℒ_complex = || U_recon - A_target × exp(i×ψ) ||²_F
  (where ψ is the phase of U_recon — jointly optimized)
```

**SGD (Stochastic Gradient Descent):**
```
φₖ₊₁ = φₖ - η × ∇ℒ(φₖ)
where η = learning rate
```

**Adam Optimizer (Adaptive Moment Estimation):**
```
mₖ = β₁ × mₖ₋₁ + (1-β₁) × gₖ          (momentum/first moment)
vₖ = β₂ × vₖ₋₁ + (1-β₂) × gₖ²         (RMS/second moment)
φₖ₊₁ = φₖ - η × mₖ / (√vₖ + ε)        (bias-corrected update)
where gₖ = ∇ℒ(φₖ), β₁ = 0.9, β₂ = 0.999, ε = 1e-8
```

**Advantages over GS:**
- Directly optimizes perceptual metrics (SSIM, LPIPS)
- Can handle arbitrary differentiable models (multi-plane, multi-wavelength)
- Better noise suppression via explicit loss terms
- Flexible regularization

**Important implementation note:** The Adam optimizer for CGH is typically implemented using **automatic differentiation** in frameworks like PyTorch/TensorFlow:

```python
import torch
import torch.nn.functional as F

# Phase hologram to optimize (random initialization)
phase = torch.randn(H, W, requires_grad=True)
optimizer = torch.optim.Adam([phase], lr=0.01)

for i in range(num_iterations):
    optimizer.zero_grad()
    
    # Forward model: hologram plane → image plane
    hologram = torch.exp(1j * phase)
    recon_field = angular_spectrum_propagate(hologram, z, wavelength, pitch)
    recon_intensity = torch.abs(recon_field)**2
    
    # Loss computation
    loss = F.mse_loss(torch.sqrt(recon_intensity + 1e-10), torch.sqrt(target + 1e-10))
    
    # Backpropagation
    loss.backward()
    optimizer.step()
```

#### 4.4 Adjoint Optimization (Physics-Based Gradient)

For pixel-based metasurface inverse design where the meta-atom geometry itself is the optimization variable:

**Forward simulation:** Maxwell's equations solver → field at targets  
**Adjoint simulation:** Same solver with adjoint sources → sensitivity map

```
Gradient of objective w.r.t. geometry parameter p:
∂ℒ/∂p = 2 × Re{ ∫ E_forward · E_adjoint × (∂ε/∂p) dV }
```

This requires only **2 simulations per iteration** (forward + adjoint), regardless of the number of design parameters — the key efficiency advantage over finite-difference methods.

#### 4.5 Comparison of Optimization Methods

| Method | Type | Speed | Quality | Multi-plane | RGB | Complexity |
|--------|------|-------|---------|-------------|-----|------------|
| GS | Iterative, projection | Fast | Moderate | Requires extension | Per-channel | Low |
| WGS | Iterative, weighted projection | Fast | Good | Requires extension | Per-channel | Low |
| SGD | Gradient descent | Medium | Good | Natural | Sum loss | Medium |
| Adam | Adaptive GD | Medium | Best | Natural | Sum loss | Medium |
| Fienup | Hybrid I/O | Fast | Moderate | Requires extension | Per-channel | Low |
| CNN/DNN | Learned | Very fast (inference) | Best | If trained | Joint | High (training) |
| Adjoint | Physics GD | Slow | Best | Natural | Natural | Very high |

**Practical recommendation:**
- **For 2D holograms:** Use Adam with amplitude loss (50-200 iterations)
- **For multi-plane:** Use Adam with per-plane MSE loss summed
- **For RGB:** Use Adam with joint loss across R, G, B channels
- **For fabrication constraints:** Use either Adam with regularization or adjoint method

---

