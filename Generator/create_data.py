from PIL import Image
import torch
from torchvision import transforms
from Metasurface.parameters import kwargs
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def func(contimg, styleimg, distance):
    """
    Input:
        contimg: The filename of the content image.
        styleimg: The filename of the style image.
        distance: The focal length of the imaging plane to the metasurface, in micrometer.
    """
    transform = transforms.ToTensor()
    content = transform(Image.open(current_dir+'/'+contimg).resize((kwargs["Meta_N"], kwargs["Meta_N"])))[:3].unsqueeze(0)
    style = transform(Image.open(current_dir+'/'+styleimg).resize((kwargs["Meta_N"], kwargs["Meta_N"])))[:3].unsqueeze(0)
    distance = torch.ones(content.shape[0], 1)*distance
    torch.save(content, current_dir+"/contentImg.pt")
    torch.save(style, current_dir+"/styleImg.pt")
    torch.save(distance, current_dir+"/distance.pt")
    return f"The dataset has been created. It contains three files:\n1. The tensor of the content image with dimensions {content.shape}. It is saved to the file path {current_dir}\contentImg.pt.\n2. The tensor of the style image with dimensions {style.shape}. It is saved to the file path {current_dir}\styleImg.pt.\n3. The focal length of the imaging plane to the metasurface with dimensions {distance.shape}. It is saved to the file path {current_dir}\distance.pt."

func('cont.png','style.png',50)