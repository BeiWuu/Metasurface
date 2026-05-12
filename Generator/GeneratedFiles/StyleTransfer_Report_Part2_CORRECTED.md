# Optoelectronic Hybrid Neural Network for Image Style Transfer - Part 2: Code Analysis (REVISED)

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

### Padding Operation Details:
```python
def padding(self, x):
    batch, channels, height, width = x.size()
    # height and width are captured at function entry (both 512)
    x1 = torch.cat((zeros(b,c,height//2,w), x, zeros(b,c,height//2,w)), 2)  # dim=2: height
    x2 = torch.cat((zeros(b,c,height*2, w//2), x1, zeros(b,c,height*2, w//2)), 3)  # dim=3: width
    return x2
```
- Step 1 (height padding): Pads 256 zeros on top + 256 zeros on bottom → 512+256+256 = **1024 height**
- Step 2 (width padding): Pads 256 zeros on left + 256 zeros on right → 512+256+256 = **1024 width**
- Final output: [batch, 3, **1024, 1024**]

Note: `height*2` in the second concat uses the **original** height value (512), not the padded height. So `height*2 = 1024` is used as the first dimension of the zero tensors (matching 1024 height from step 1), while `width//2 = 256` is used for the padding amount.

### Key Design Choices:
- The encoder uses **no BatchNorm layers** (as specified)
- Lightweight architecture with **~398K parameters** (not ~1.4M as previously stated)
- Downsampling factor of 16x (512/32 = 16), upsampled back via Kronecker product

## 2. AS.py - Angular Spectrum Propagation Module

Implements the physical wave propagation from metasurface to the focal plane.

### Class: `ASM_propagate`
```python
class ASM_propagate(nn.Module):
    def __init__(self, freq, z, refidx=1):
```

### Key Components:

1. **Wavelength Calculation**: `lamda = 3E-4 / freq` (converts THz to wavelength in meters)
   - 480 THz -> λ = 625 nm (Red)
   - 560 THz -> λ = 536 nm (Green)  
   - 640 THz -> λ = 469 nm (Blue)

2. **Frequency Grid**: Creates spatial frequency coordinates `(Fvv, Fhh)` using meshgrid with sampling frequency Fs = 1/pixelsize

3. **Propagation Transfer Function (PropGeneral)**:
   ```
   H(fx, fy) = exp(j * 2π * z/λ * sqrt(1 - (λ*fx)^2 - (λ*fy)^2))
   ```
   - Limited by diffraction limit: filters out evanescent waves where `(λ*fx)^2 + (λ*fy)^2 >= 1`

4. **Band-Limit Filter (BandLimitTransferFunction)**:
   - Additional filtering to prevent aliasing in the discrete Fourier transform
   - Based on pixel size and propagation distance

5. **Forward Pass**:
   ```
   wave -> FFTshift -> FFT2 -> multiply by H -> apply freqmask -> IFFT2 -> IFFTshift -> |output|^2
   ```
   - Returns intensity (amplitude squared) on the focal plane

### Frequency-Dependent Behavior:
Each frequency has a separate ASM propagator with different wavelength → different transfer function, same propagation distance (50 μm), same pixel size (160 nm).

## 3. DataFlow.py - Main Optimization Pipeline

### Class: `MetaOptim`
```python
class MetaOptim(nn.Module):
    def __init__(self, task, frequencies):
        self.phase = nn.Parameter(torch.randn(N, N))  # Learnable phase array, 1024x1024
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
- For 480 THz (Red): reads just `Phase480` → identity (no transformation)
- For 560 THz (Green): reads `1.2022*Phase480 - 2.2877` → linear mapping
- For 640 THz (Blue): reads `1.4321*Phase480 - 4.7134` → linear mapping

This allows a **single learnable phase array** to control all three frequencies simultaneously through dispersion engineering.

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
       # Crop to Meta_N x Meta_N center region (512x512)
       output = output[:, :, N/4:3N/4, N/4:3N/4]
       # Load pre-computed style-transferred target
       target = torch.load("Generator/target.pt")
       # MSELoss between optically propagated output and target
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
- **Content Score**: Per-sample MSE between feature maps (conv_4) of input image and content image
- **Style Score**: Per-sample MSE between Gram matrices (conv_1-5) of input image and style image

Note: In the `Evaluate.Generator()` function, these are called on the **pre-computed style transfer target** (target.pt), not the metasurface optical output. The target's content and style losses reflect the quality of the VGG-19 style transfer process itself.

