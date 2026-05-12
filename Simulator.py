import numpy as np
import os
from parameters import kwargs
from dotenv import load_dotenv
from skimage.restoration import unwrap_phase
import matplotlib.pyplot as plt
from sympy import symbols,solve,simplify
from langchain.tools import tool

load_dotenv()
folder_path = kwargs.get("folder_path")

try:
    os.makedirs(folder_path + f"/MetaAtom")
except:
    pass

@tool
def simulation()->str:
    """Simulate the phase relationship between different frequencies in the meta-atom.

    Returns:
        Phase relationships."""

    freq_arr = sorted(list(set([480, 520, 560, 600, 640, 680, 720]))) # 频率从小到大
    height_arr = np.load(folder_path + f"/MetaAtom/train_x.npy")[:,0]

    phase = unwrap_phase(np.load(folder_path + f"/MetaAtom/train_y.npy"))
    plt.plot(phase[:,0],label='0')
    plt.plot(phase[:,1],label='1')
    plt.plot(phase[:,2],label='2')
    plt.plot(phase[:,3],label='3')
    plt.plot(phase[:,4],label='4')
    plt.plot(phase[:,5],label='5')
    plt.plot(phase[:,6],label='6')
    plt.legend()
    plt.show()

    # 超表面单元的相位和纳米柱高度之间的关系
    for i in range(len(freq_arr)):
        # print(phase[-1,i]-phase[0,i])
        k = (phase[-1,i]-phase[0,i])/(height_arr[-1]-height_arr[0])
        b = phase[0,i] - k * height_arr[0]
        with open(os.path.join(folder_path, "MetaAtom", f"freq_{freq_arr[i]}.txt"), "w") as file:
            file.write(f'(Phase{freq_arr[i]} - {b})/{k}')
        # print(k,b)

    # 不同入射频率下超表面单元的相位关系
    equation_arr = []
    for freq in freq_arr:
        with open(os.path.join(folder_path, "MetaAtom", f"freq_{freq}.txt"), "r") as file:
            equation_arr.append(file.read())

    outText=f"The phase relationships between different frequencies are saved in the folder {folder_path}\MetaAtom. Specifically:\n"
    with open(os.path.join(folder_path, "MetaAtom", f"func_480.txt"), "w") as file:
        file.write('Phase480')
    for i in range(1, len(freq_arr)):
        func = simplify(equation_arr[i] + "-" + equation_arr[0])
        s = solve(func, symbols(f'Phase{freq_arr[i]}'))
        phase = str(s[0])
        with open(os.path.join(folder_path, "MetaAtom", f"func_{freq_arr[i]}.txt"), "w") as file:
            file.write(f'{phase}')
        outText+=f'For frequency {freq_arr[i]} THz, the relationship of the phase change with respect to the phase at 480 THz is: {phase}\n'
    return outText