import torch
import torch.nn as nn


class EncoderNet(nn.Module):
    """
    Lightweight encoder network that downsamples input from [batch, 3, 512, 512] to [batch, 3, 32, 32].
    This represents a 16x downsampling (512/32 = 16).
    """
    
    def __init__(self):
        super(EncoderNet, self).__init__()
        
        # Encoder blocks with progressive downsampling
        # Each block reduces spatial dimensions by 2x
        
        # Block 1: 512x512 -> 256x256
        self.block1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True)
        )
        
        # Block 2: 256x256 -> 128x128
        self.block2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True)
        )
        
        # Block 3: 128x128 -> 64x64
        self.block3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True)
        )
        
        # Block 4: 64x64 -> 32x32
        self.block4 = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, stride=2, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True)
        )
        
        # Final projection to 3 channels at 32x32
        self.output_conv = nn.Conv2d(64, 3, kernel_size=1, stride=1, padding=0)
    
    def forward(self, x):
        """
        Forward pass of the encoder network.
        
        Args:
            x: Input tensor of shape [batch, 3, 512, 512]
        
        Returns:
            Output tensor of shape [batch, 3, 32, 32]
        """
        # Progressive downsampling through encoder blocks
        x = self.block1(x)  # [batch, 32, 256, 256]
        x = self.block2(x)  # [batch, 64, 128, 128]
        x = self.block3(x)  # [batch, 128, 64, 64]
        x = self.block4(x)  # [batch, 64, 32, 32]
        x = self.output_conv(x)  # [batch, 3, 32, 32]
        
        return x


if __name__ == "__main__":
    # Test the network
    model = EncoderNet()
    
    # Create a random input tensor
    batch_size = 4
    input_tensor = torch.randn(batch_size, 3, 512, 512)
    
    # Forward pass
    output_tensor = model(input_tensor)
    
    # Print shapes
    print(f"Input shape: {input_tensor.shape}")
    print(f"Output shape: {output_tensor.shape}")
    
    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Total parameters: {total_params:,}")

