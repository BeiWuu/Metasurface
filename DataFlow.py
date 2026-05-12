import torch
from AS import ASM_propagate
from parameters import kwargs
import torch.nn as nn
from FrontNetwork import FrontEnd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

folder_path = kwargs.get("folder_path")

class MetaOptim(nn.Module):
    def __init__(self, task, frequencies):
        super(MetaOptim, self).__init__()
        self.task = task
        self.frequencies = sorted(frequencies) # 从小到大
        self.phase = nn.Parameter(torch.randn(kwargs["N"], kwargs["N"]))
        self.frontNet = FrontEnd(task)

    def forward(self):
        input = self.frontNet() # batch, channel (frequencies), N, N
        distances = torch.load(folder_path + f"/{self.task}/distance.pt").squeeze(1) # batch
        outputs = torch.Tensor([])
        for i in range(input.shape[0]):  # Image iteration
            output = torch.Tensor([])
            for c in range(len(self.frequencies)):  # frequencies
                freeProp = ASM_propagate(self.frequencies[c], int(distances[i]))

                with open(folder_path+f"/MetaAtom/func_{self.frequencies[c]}.txt", "r") as file:
                    phase = eval(file.read().replace("Phase480","self.phase"))

                out = freeProp(torch.mul(input[i][c], torch.exp(1j * phase)))
                output = torch.cat((output, out.unsqueeze(0)), dim=0)
            outputs = torch.cat((outputs, output.unsqueeze(0)), dim=0)
        return outputs # batch, channel, N, N