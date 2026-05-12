# Optoelectronic Hybrid Neural Network for Image Style Transfer - Part 2: Code Analysis

## 1. FrontNetwork.py - Front Neural Network Module

The `FrontEnd` class acts as the interface between the electronic and optical domains.

### Structure:
```python
class FrontEnd(nn.Module):
    def __init__(self, task):
        # For "Generator" task, creates an EncoderNet via the Coder agent
        # EncoderNet transforms: [batch, 3, 512, 512] -> [batch, 3, 32, 32]
```

### Generator Method Flow:
1. **Load content image**: Loads `contentImg.pt` (shape: [1, 3, 512, 512])
2. **Encode**: Pass through `self.encoder()` to produce [1, 3, 32, 32] amplitude map
3. **Upsample**: Apply Kronecker product with ones matrix of size `zip x zip = 16x16` to expand from 32x32 back to 512x512
4. **Pad**: Zero-pad to 1024x1024 (full metasurface size) for diffraction calculation

### Key Design Choices:
- The encoder uses **no BatchNorm layers** (as specified)
- Lightweight architecture with ~1.4M parameters
- Downsampling factor of 16x (512/32 = 16), upsampled back via Kronecker product
- The padding operation adds zeros on both sides: half on top/bottom, double on left/right (due to previous half-padding)

## 2. AS.py - Angular Spectrum Propagation Module

Implements the physical wave propagation from metasurface to the focal plane.

### Class: `ASM_propagate`
```python
class ASM_propagate(nn.Module):
    def __init__(self, freq, z, refidx=1):
```

### Key Components:

1. **Wavelength Calculation**: `lamda = 3E-4 / freq` (converts THz to wavelength in meters)
   - 480 THz -> λ = 625 nm
   - 560 THz -> λ = 536 nm  
   - 640 THz -> λ = 469 nm

2. **Frequency Grid**: Creates spatial frequency coordinates `(Fvv, Fhh)` using meshgrid

3. **Propagation Transfer Function (PropGeneral)**:
   ```
   H(fx, fy) = exp(j * 2π * z/λ * sqrt(1 - (λ*fx)^2 - (λ*fy)^2))
   ```
   - Limited by diffraction limit: filters out evanescent waves where `(λ*fx)^2 + (λ*fy)^2 >= 1`
   - This ensures only propagating modes are considered

4. **Band-Limit Filter (BandLimitTransferFunction)**:
   - Additional filtering to prevent aliasing in the discrete Fourier transform
   - Based on pixel size and propagation distance

5. **Forward Pass**:
   ```
   wave -> FFT -> multiply by H -> apply freqmask -> IFFT -> |output|^2
   ```
   - Returns intensity (amplitude squared) on the focal plane

### Frequency-Dependent Behavior:
Each frequency has a separate ASM propagator with:
- Different wavelength → different transfer function
- Same propagation distance (50 μm)
- Same pixel size (160 nm)

## 3. DataFlow.py - Main Optimization Pipeline

### Class: `MetaOptim`
```python
class MetaOptim(nn.Module):
    def __init__(self, task, frequencies):
        self.phase = nn.Parameter(torch.randn(N, N))  # Learnable phase array
        self.frontNet = FrontEnd(task)
```

### Forward Pass Logic:
```
For each image in batch:
    For each frequency in [480, 560, 640]:
        1. Get amplitude from frontNet: amplitude[i][c]
        2. Read phase relationship file for this frequency
        3. Compute modulated wave: amplitude * exp(j * phase_mapped)
        4. Propagate via ASM to focal plane
```

### Phase Mapping Mechanism:
```python
with open(f"MetaAtom/func_{freq}.txt", "r") as file:
    phase = eval(file.read().replace("Phase480", "self.phase"))
```
- For 480 THz: reads just `Phase480` → no transformation
- For 560 THz: reads `1.2022*Phase480 - 2.2877` → linear mapping
- For 640 THz: reads `1.4321*Phase480 - 4.7134` → linear mapping

This allows a **single learnable phase array** to control all three frequencies simultaneously, with appropriate dispersion compensation.

## 4. LossFunction.py - Loss Computation

### Class: `OptimLoss`

### Generator Task Loss Flow:

1. **Target Generation** (executed once during first initialization):
   - Uses VGG-19 based neural style transfer (`styleCode.py`)
   - Content image + Style image → Style-transferred target image
   - Saved as `target.pt` for reuse

2. **Loss Computation**:
   ```python
   def Generator(self, output):
       # Crop to Meta_N x Meta_N center region
       output = output[:, :, N/4:3N/4, N/4:3N/4]
       # Load pre-computed target
       target = torch.load("Generator/target.pt")
       # MSELoss between output and target
       loss = nn.MSELoss()(output.double(), target.double())
   ```

### Style Transfer (`styleCode.py`):
- Uses **pretrained VGG-19** as feature extractor
- **Content Loss**: MSE between `conv_4` activations
- **Style Loss**: MSE between Gram matrices of `conv_1` through `conv_5` activations
- **Optimization**: L-BFGS optimizer, 300 iterations
- **Weights**: style_weight = 1e6, content_weight = 1

### Encoder Code Generation:
The `Coder.py` module uses a **programmer agent** (powered by LLM) to auto-generate the encoder neural network code based on a template query specifying input/output dimensions.

## 5. StyleLoss.py - Performance Evaluation Module

The `func_loss` function computes:
- **Content Score**: Per-sample MSE between feature maps of style-transferred output and content image
- **Style Score**: Per-sample MSE between Gram matrices of style-transferred output and style image

