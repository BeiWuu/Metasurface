import torch
import os
import matplotlib.pyplot as plt
from Metasurface.parameters import kwargs

current_dir = os.path.dirname(os.path.abspath(__file__))

def func(distance, xr, yr, xg, yg, xb, yb):
    """
    Input:
        distance: Focal length of the achromatic metalens, in micrometer.
        xr: The x-coordinate of the focal point for red light on the focal plane. In the focus is at the origin or the user does not specify, the value is 0.
        yr: The y-coordinate of the focal point for red light on the focal plane. In the focus is at the origin or the user does not specify, the value is 0.
        xg: The x-coordinate of the focal point for green light on the focal plane. In the focus is at the origin or the user does not specify, the value is 0.
        yg: The y-coordinate of the focal point for green light on the focal plane. In the focus is at the origin or the user does not specify, the value is 0.
        xb: The x-coordinate of the focal point for blue light on the focal plane. In the focus is at the origin or the user does not specify, the value is 0.
        yb: The y-coordinate of the focal point for blue light on the focal plane. In the focus is at the origin or the user does not specify, the value is 0.
    """
    target = torch.zeros((1,3,512,512))
    target[0, 0, kwargs['Meta_N']//2 + int(yr), kwargs['Meta_N']//2 + int(xr)] = 1
    target[0, 1, kwargs['Meta_N']//2 + int(yg), kwargs['Meta_N']//2 + int(xg)] = 1
    target[0, 2, kwargs['Meta_N']//2 + int(yb), kwargs['Meta_N']//2 + int(xb)] = 1
    torch.save(target,current_dir+"/target.pt")
    torch.save(torch.ones(1,1)*distance,current_dir+"/distance.pt")
    return f"The dataset has been created. It contains two files:\n1. The positions where different colors of light focus on the focal plane, with dimensions {target.shape}. It is saved to the path: {current_dir}\\target.pt.\n2. The focal length, with dimension of [1, 1]. It is saved to the path {current_dir}\distance.pt."
