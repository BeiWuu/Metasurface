import torch
import torch.nn as nn
import torch.nn.functional as F
from dotenv import load_dotenv
from parameters import kwargs
import numpy as np
from Coder import Coding

load_dotenv()
folder_path = kwargs.get("folder_path")

CODING_QUERY = f"""Write PyTorch code to implement image style transfer.
Define the main function as **run_style_transfer**, which accepts two input tensors:
- **content**: shape [batch, 3, {kwargs["Meta_N"]}, {kwargs["Meta_N"]}]
- **style**: shape [batch, 3, {kwargs["Meta_N"]}, {kwargs["Meta_N"]}]

For each content-style pair (treated as individual images with batch dimension 1), generate a style-transferred image of shape [1, 3, {kwargs["Meta_N"]}, {kwargs["Meta_N"]}].
Concatenate all generated images along the batch dimension and return a tensor of shape [batch, 3, {kwargs["Meta_N"]}, {kwargs["Meta_N"]}].

Please ensure:
1. Preserve the style of the retrievable code as much as possible.
2. The style_weight is **1e6**, content_weight is **1**, and optimize for 300 epochs.
3. Save the code in a file named styleCode.py. The code file should not have any parent folder; that is, the file path should be directly styleCode.py, not x/styleCode.py."""

class FocalLoss(nn.Module):
    def __init__(self,alpha=0.5,gamma=2,logits=False,reduce=True):
        super(FocalLoss,self).__init__()
        self.alpha=alpha
        self.gamma=gamma
        self.logits=logits
        self.reduce=reduce

    def forward(self,inputs,targets):
        if self.logits:
            BCE_loss=F.binary_cross_entropy_with_logits(inputs,targets,reduce=False)
        else:
            BCE_loss=F.binary_cross_entropy(inputs,targets,reduce=False)
        pt=torch.exp(-BCE_loss)
        F_loss=self.alpha*(1-pt)**self.gamma*BCE_loss

        if self.reduce:
            return torch.mean(F_loss)
        else:
            return F_loss

class OptimLoss(nn.Module):
    def __init__(self, task):
        super(OptimLoss, self).__init__()
        self.task = task
        if self.task == "Generator":
            try:
                self.transfer_target = torch.load(folder_path + "/Generator/target.pt")
                print('=' * 20, " Load style-transferred images ", "=" * 20)
            except:
                Coding('styleCode', CODING_QUERY)
                from styleCode import run_style_transfer
                content_img = torch.load(folder_path + "/Generator/contentImg.pt")
                style_img = torch.load(folder_path + "/Generator/styleImg.pt")
                print('Transferring image style, this may take some time for large images...')
                self.transfer_target = run_style_transfer(content_img, style_img)
                torch.save(self.transfer_target, folder_path + "/Generator/target.pt")

    def Focus(self, output):
        output = output[:, :, output.shape[2] // 4: 3 * output.shape[2] // 4, output.shape[3] // 4: 3 * output.shape[3] // 4]  # batch, 3, Meta_N, Meta_N
        target = torch.load(folder_path + "/Focus/target.pt")
        loss = FocalLoss()(output/30000, target)
        return loss

    def Holography(self, output):
        output = output[:, :, output.shape[2] // 4: 3 * output.shape[2] // 4, output.shape[3] // 4: 3 * output.shape[3] // 4]  # batch, 3, Meta_N, Meta_N
        target = torch.load(folder_path + "/Holography/trainData.pt") # batch, 3, Meta_N, Meta_N
        mask = torch.load(folder_path + "/Holography/masks.pt") # batch, 3, Meta_N, Meta_N
        output = torch.mul(output, mask)
        loss = nn.MSELoss()(output.double(), target.double())
        return loss

    def Generator(self, output):
        output = output[:, :, output.shape[2] // 4: 3 * output.shape[2] // 4, output.shape[3] // 4: 3 * output.shape[3] // 4]  # batch, 3, Meta_N, Meta_N
        loss = nn.MSELoss()(output.double(), self.transfer_target.double())
        return loss

    def forward(self,output):
        if self.task == "Focus":
            return self.Focus(output)
        elif self.task == "Holography":
            return self.Holography(output)
        elif self.task == "Generator":
            return self.Generator(output)
        else:
            return f"The task {self.task} is not implemented."
