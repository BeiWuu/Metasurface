import OpenEXR
import Imath
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import torch
from Metasurface.parameters import kwargs
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
def func(distance_min, distance_max):
    """
    Input:
        distance_min: The shortest focal length from the holography to the metasurface, in micrometer.
        distance_max: The longest focal length from the holography to the metasurface, in micrometer.
    """
    file = OpenEXR.InputFile(current_dir+"/image.exr")
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    imageG = [Image.frombytes("F", size, file.channel(c, pt)) for c in "G"]
    imageB = [Image.frombytes("F", size, file.channel(c, pt)) for c in "B"]
    imageR = [Image.frombytes("F", size, file.channel(c, pt)) for c in "R"]
    image = np.concatenate((imageR, imageG, imageB),0).transpose(1, 2, 0)
    # print('Image shape: ',image.shape)
    plt.imshow(image)
    plt.axis("off")
    plt.savefig(current_dir + f"/pic.png", dpi=500, bbox_inches='tight', pad_inches=0)
    plt.show()

    file = OpenEXR.InputFile(current_dir+"/depth.exr")
    pt = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)
    depth = np.array([Image.frombytes("F", size, file.channel(c, pt)) for c in "G"])[0]
    depth = np.where(depth > 7, 7, depth)
    depth = depth/depth.max()*(distance_max-distance_min)
    discrete_depth = np.round(depth) + distance_min
    # print(np.unique(discrete_depth).shape[0],discrete_depth.min(), discrete_depth.max())
    plt.imshow(discrete_depth,'gray')
    plt.axis("off")
    plt.colorbar()
    plt.savefig(current_dir + f"/depth.png", dpi=500, bbox_inches='tight', pad_inches=0)
    plt.show()

    trainData = torch.Tensor([])
    distances = torch.Tensor([])
    masks = torch.Tensor([])
    for depth in np.unique(discrete_depth):
        bool_mask = (discrete_depth == depth)
        bool_mask = np.repeat(bool_mask[:,:, np.newaxis], 3, axis=-1)
        img_mask = image*bool_mask
        img_mask = img_mask[::int(img_mask.shape[0]/kwargs["Meta_N"]), ::int(img_mask.shape[0]/kwargs["Meta_N"])]
        bool_mask = bool_mask[::int(bool_mask.shape[0]/kwargs["Meta_N"]), ::int(bool_mask.shape[0]/kwargs["Meta_N"])]
        plt.imshow(img_mask)
        plt.axis("off")
        plt.savefig(current_dir + f"/HoloPart{int(depth)}.png", dpi=500, bbox_inches='tight', pad_inches=0)
        plt.show()
        trainData = torch.cat((trainData, torch.Tensor(img_mask.transpose(2, 0, 1)).unsqueeze(0)),0)
        distances = torch.cat((distances, torch.Tensor([[depth]])),0)
        masks = torch.cat((masks, torch.Tensor(bool_mask.transpose(2, 0, 1)).unsqueeze(0)),0)

    # print(trainData.shape)
    # print(distances.shape)
    # print(masks.shape)
    torch.save(trainData, current_dir+'/trainData.pt')
    torch.save(distances, current_dir+'/distance.pt')
    torch.save(masks, current_dir+'/masks.pt')
    return f"The dataset has been created. It contains three files:\n1. The target 3D hologram with dimensions {trainData.shape}. It is saved to the file path {current_dir}\\trainData.pt.\n2. The focal length array with dimensions {distances.shape}, which represents the distance from each imaging plane to the metasurface. It is saved to the file path {current_dir}\distance.pt.\n3. The mask with dimensions {masks.shape}, corresponding to the target 3D hologram. In this mask, regions with pattern are set to 1, and regions without pattern are set to 0. It is saved to the file path {current_dir}\masks.pt."
