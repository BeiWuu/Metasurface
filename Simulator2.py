import cst
import cst.results
from cst.interface import DesignEnvironment
import numpy as np
import cmath
import os
from dotenv import load_dotenv
from parameters import kwargs

# 仿真超表面单元的相位和纳米柱高度之间的关系；
# 仿真不同入射频率下超表面单元的相位关系。

load_dotenv()
folder_path = kwargs.get("folder_path")
height_arr = np.linspace(400, 800, 20)
freq_arr = sorted(list(set([480, 520, 560, 600, 640, 680, 720]))) # 频率从小到大

try:
    os.makedirs(folder_path + f"/MetaAtom")
except:
    pass

def AtomSimulation(frequencies):
    """Simulate the S-parameters of Meta-Atom at specified frequencies."""
    de = DesignEnvironment.new()
    mws = de.open_project(kwargs["cst_atom_path"])
    modeler = mws.modeler
    trainX = []
    trainY = []
    for h in height_arr:
        mws.model3d.StoreDoubleParameter("height", float(h))
        trainX.append([h])
        modeler.run_solver()
        project = cst.results.ProjectFile(kwargs["cst_atom_path"], allow_interactive=True)
        s11 = project.get_3d().get_result_item(r"1D Results\S-Parameters\SZmin(2),Zmax(2)")
        frequency = s11.get_xdata()
        index = [min(range(len(frequency)), key=lambda i: abs(frequency[i] - f*1e-3)) for f in frequencies]
        phase = [cmath.phase(i) for i in s11.get_ydata()]
        phase = [phase[i] for i in index]
        trainY.append(phase)
    mws.close()
    de.close()
    trainX = np.array(trainX)
    trainY = np.array(trainY)
    np.save(folder_path + f"/MetaAtom/train_x", trainX)
    np.save(folder_path + f"/MetaAtom/train_y", trainY)

AtomSimulation(freq_arr)
