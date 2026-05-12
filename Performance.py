from dotenv import load_dotenv
import torch
import torch.nn as nn
from FrontNetwork import FrontEnd
from pathlib import Path
from parameters import kwargs
from Coder import Coding

load_dotenv()
folder_path = kwargs.get("folder_path")

FWHM_QUERY = f"""Write a function that calculates the full width at half maximum (FWHM) of a waveform.
Input: A one-dimensional waveform array.
Output: The FWHM value, in nanometers.

Please ensure:

1. The spacing between adjacent points in the input waveform array is 160 nm. Therefore, the computed FWHM should be multiplied by 160 nm to obtain the result in nanometers.
2. Define the file name of the code as FWHM.py.
3. Define the function name as func_FWHM."""

SSIM_QUERY = f"""Write a function that measures the similarity between two images using the SSIM (Structural Similarity Index) metric.
Inputs:
1. An image with dimensions **[{kwargs["Meta_N"]},{kwargs["Meta_N"]},3]**.
2. Another image with the same dimensions **[{kwargs["Meta_N"]},{kwargs["Meta_N"]},3]**.
Output:
The SSIM value (a scalar).

Please ensure:

1. Define the file name of the code as SSIM.py.
2. Define the function name as func_SSIM.
3. Do not include any specific symbols (e.g., ✓, →, ★) or emoji/emoticons."""

PSNR_QUERY = f"""Write a function that measures the similarity between two images using the PSNR (peak signal-to-noise ratio) metric.
Inputs:
1. An image with dimensions **[{kwargs["Meta_N"]},{kwargs["Meta_N"]},3]**.
2. Another image with the same dimensions **[{kwargs["Meta_N"]},{kwargs["Meta_N"]},3]**.
Output:
The PSNR value (a scalar with unit in dB).

Please ensure:

1. Define the file name of the code as PSNR.py.
2. Define the function name as func_PSNR.
3. Do not include any specific symbols (e.g., ✓, →, ★) or emoji/emoticons."""

def read_file(file_name):
    file_name = Path(r"D:\work\MetaDesign\Metasurface") / file_name
    with open(file_name, 'r', encoding='utf-8') as f:
        code_content = f.read()
    return code_content

GENERATOR_QUERY = """Write a function that calculates the content loss between input_img and content_img, and the style_loss between input_img and style_img.
Inputs:
- input_img: The style_transferred images with dimensions of [batch, 3, {Meta_N}, {Meta_N}].
- content_img: The content images with dimensions of [batch, 3, {Meta_N}, {Meta_N}].
- style_img: The style images with dimensions of [batch, 3, {Meta_N}, {Meta_N}].
Output:
- content_score: Content loss value with dimensions of [batch].
- style_score: Style loss value with dimensions of [batch].

The reference code:
```Python
{code}
```

Please ensure:
1. Preserve the content of the reference code as much as possible.
2. Only return the content loss value and the style loss value. Do not optimize any parameters.
3. Define the file name of the code as StyleLoss.py.
4. Define the main function as **func_loss**."""

class Evaluate(nn.Module):
    def __init__(self, task, output):
        super(Evaluate, self).__init__()
        self.task = task
        self.frontNet = FrontEnd(task)
        self.output = output

    def Focus(self):
        input = self.frontNet()
        in_intensity = input[0][0].sum().detach()
        efficiency = []
        FWHM = []
        Coding('FWHM', FWHM_QUERY)
        from FWHM import func_FWHM
        for i in range(3):
            idx = torch.argmax(self.output[0,i])  # 展平后的索引
            x, y = torch.unravel_index(idx, self.output[0,i].shape)  # 转换为二维坐标
            efficiency.append((100*self.output[0,i,x-10:x+11,y-10:y+11].sum()/in_intensity).item())
            FWHM.append(func_FWHM(self.output[0,i,:,y].detach().numpy()).item())
        return f'At the red/green/blue lights, the efficiency of the designed metalens (defined as output intensity divided by input intensity) are {efficiency}%, and the FWHM are {FWHM} nm, respectively.'

    def Holography(self):
        output = self.output
        output = output[:, :, output.shape[2]//4: 3*output.shape[2]//4, output.shape[3]//4: 3*output.shape[3]//4] # batch, 3, Meta_N, Meta_N
        target = torch.load(folder_path + "/Holography/trainData.pt")
        img_arr1 = target.permute(0, 2, 3, 1).detach().numpy()
        img_arr2 = output.permute(0, 2, 3, 1).detach().numpy()
        Coding('SSIM', SSIM_QUERY)
        Coding('PSNR', PSNR_QUERY)
        from SSIM import func_SSIM
        from PSNR import func_PSNR
        SSIM_arr=[]
        PSNR_arr=[]
        for i in range(len(img_arr1)):
            SSIM_arr.append(func_SSIM(img_arr1[i], img_arr2[i]).tolist())
            PSNR_arr.append(func_PSNR(img_arr1[i], img_arr2[i]).tolist())
        return f'The SSIM scores between the holography images and the target images at {len(img_arr1)} focal lengths are {SSIM_arr}.\nThe PSNR scores between the holography images and the target images at {len(img_arr1)} focal lengths are {PSNR_arr}.'

    def Generator(self):
        Coding('StyleLoss', GENERATOR_QUERY.format(Meta_N=kwargs["Meta_N"],code=read_file('styleCode.py')))
        from StyleLoss import func_loss
        batch, channel, x, y = self.output.shape
        content_img = torch.load(folder_path + "/Generator/contentImg.pt")
        style_img = torch.load(folder_path + "/Generator/styleImg.pt")
        output = torch.load(folder_path + "/Generator/target.pt")
        content_score, style_score = func_loss(output, content_img, style_img)
        return f'For the content image, {batch} style-transferred images are generated. Their content loss values with respect to the content image are {content_score}, and their style_loss with respect to the style image are {style_score}, respectively.'

    def forward(self):
        if self.task == "Focus":
            return self.Focus()
        elif self.task == "Holography":
            return self.Holography()
        elif self.task == "Generator":
            return self.Generator()
        else:
            return f"The task {self.task} is not implemented."