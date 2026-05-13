import numpy as np
import torch
import torch.nn as nn
from dotenv import load_dotenv
from parameters import kwargs
from Coder import Coding

load_dotenv()
folder_path = kwargs.get("folder_path")

ENCODER_QUERY = """Write PyTorch code for a neural network.
The input with dimension of **{input_dimension1}**.
The output with dimension of **{output_dimension}**.

Please ensure:
1. Define the file name of the code as Encoder.py.
2. Define the class name of the network as EncoderNet.
3. Use a lightweight architecture."""

class FrontEnd(nn.Module):
    def __init__(self, task):
        super(FrontEnd, self).__init__()
        self.task = task
        if task == "Generator":
            Coding('Encoder', ENCODER_QUERY.format(input_dimension1=f'[batch, 3, {kwargs["Meta_N"]}, {kwargs["Meta_N"]}]', output_dimension=f'[batch, 3, {kwargs["Meta_N"] // kwargs["zip"]}, {kwargs["Meta_N"] // kwargs["zip"]}]'))
            from Encoder import EncoderNet
            self.encoder = EncoderNet()

    def Focus(self):
        return torch.ones(1,3,kwargs["N"],kwargs["N"])

    def Holography(self):
        return torch.ones(6,3,kwargs["N"],kwargs["N"])

    def padding(self, x):
        batch, channels, height, width = x.size()
        x1 = torch.cat((torch.zeros(batch, channels, height//2, width), x, torch.zeros(batch, channels, height//2, width)),2) # batch, 3, N, Meta_N
        x2 = torch.cat((torch.zeros(batch, channels, height*2, width//2), x1, torch.zeros(batch, channels, height*2, width//2)), 3) # batch, 3, N, N
        return x2

    def Generator(self):
        x1 = torch.load(folder_path + "/Generator/contentImg.pt") # batch, 3, Meta_N, Meta_N
        out = torch.kron(abs(self.encoder(x1)), torch.ones(kwargs["zip"], kwargs["zip"])) # batch, 3, Meta_N, Meta_N
        out = self.padding(out) # batch, 3, N, N
        return out

    def forward(self):
        if self.task == "Focus":
            return self.Focus()
        elif self.task == "Holography":
            return self.Holography()
        elif self.task == "Generator":
            return self.Generator()
        else:
            return f"The task {self.task} is not implemented."
