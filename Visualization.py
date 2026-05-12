import torch
from parameters import kwargs
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

folder_path = kwargs.get("folder_path")

class Visual(nn.Module):
    def __init__(self, task):
        super(Visual, self).__init__()
        self.task = task

    def Focus(self, output):
        output = output[0, :, output.shape[2]//4: 3*output.shape[2]//4, output.shape[3]//4: 3*output.shape[3]//4] # batch, 3, Meta_N, Meta_N
        color = ['#FE0000', '#3EFF00', '#00B5FF']
        for i in range(output.shape[0]):
            plt.figure(figsize=(4, 4))
            out = output[i]
            idx = torch.argmax(out)  # 展平后的索引
            x, y = torch.unravel_index(idx, out.shape)  # 转换为二维坐标
            plt.imshow(out[x-10:x+11,y-10:y+11].detach().numpy(), cmap=LinearSegmentedColormap.from_list('custom_cmap', ['#000000', color[i]], N=100))
            plt.colorbar(fraction=0.046, pad=0.04)
            plt.axis('off')
            plt.savefig(folder_path + "/Focus/SavedModel/2D_"+str(i)+".png",dpi=500, bbox_inches='tight', pad_inches=0)
            plt.show()

        plt.figure(figsize=(4, 3))
        plt.xlim(0,512)
        for i in range(output.shape[0]):
            intensity = output[i,:,y].detach().numpy()
            plt.plot(intensity/intensity.max(), color = color[i])
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.savefig(folder_path + "/Focus/SavedModel/1D_"+str(i)+".png",dpi=500, bbox_inches='tight', pad_inches=0, transparent=True)
        plt.show()

    def Holography(self,output):
        output = output[:, :, output.shape[2]//4: 3*output.shape[2]//4, output.shape[3]//4: 3*output.shape[3]//4] # batch, 3, Meta_N, Meta_N
        out = output.permute(0, 2, 3, 1).squeeze(0).detach().numpy()

        for i in range(len(out)):
            plt.figure(figsize=(6, 6))
            plt.imshow(out[i])
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(folder_path + f"/Holography/SavedModel/Part{i}.png",dpi=500, bbox_inches='tight', pad_inches=0)
            plt.show()

        plt.figure(figsize=(6, 6))
        mask = torch.load(folder_path + "/Holography/masks.pt")
        output = torch.mul(output,mask).permute(0, 2, 3, 1).sum(0).detach().numpy()
        plt.imshow(output)
        plt.axis("off")
        plt.savefig(folder_path + "/Holography/SavedModel/Holography.png",dpi=500, bbox_inches='tight', pad_inches=0)
        plt.show()

    def Generator(self,output):
        out = output[:, :, output.shape[2]//4: 3*output.shape[2]//4, output.shape[3]//4: 3*output.shape[3]//4].permute(0, 2, 3, 1).detach().numpy() # batch, 3, Meta_N, Meta_N

        for i in range(out.shape[0]):
            plt.figure(figsize=(6, 6))
            plt.imshow(out[i])
            plt.axis("off")
            plt.savefig(folder_path + "/Generator/SavedModel/transferPic"+str(i)+".png",dpi=500, bbox_inches='tight', pad_inches=0)
            plt.show()

    def forward(self,output):
        if self.task == "Focus":
            return self.Focus(output)
        elif self.task == "Holography":
            return self.Holography(output)
        elif self.task == "Generator":
            return self.Generator(output)
        else:
            return f"The task {self.task} is not implemented."