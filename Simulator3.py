import numpy as np
from parameters import kwargs
import os
from cst.interface import DesignEnvironment

# 画出超构透镜的三维模型图

folder_path = kwargs.get("folder_path")

with open(os.path.join(folder_path, "MetaAtom", "freq_480.txt"), "r") as file:
    heightFile = file.read()

phase = np.load(folder_path + f"/phase.npy")
height = eval(heightFile.replace(f"Phase480", "phase"))

line_break = '\n'
de = DesignEnvironment.new()

mws = de.open_project(kwargs["cst_lens_path"])
modeler = mws.modeler
meta_arr = np.array(height).round()

num = 0
for i in range(int(meta_arr.shape[0])):
    for j in range(int(meta_arr.shape[1])):
        num += 1
        Str_Name = "meta%s" % num
        Str_Material = 'Copper (annealed)'
        Str_Component = "component%s" % num
        sCommand = ['With Cylinder',
                    '   .Reset',
                    '   .Name "%s"' % Str_Name,
                    '   .Component "component1"',
                    '   .Material "%s"' % Str_Material,
                    '   .OuterRadius "50"',
                    '   .InnerRadius "0"',
                    '   .Axis "z"',
                    '   .Zrange "0", "%s"' % meta_arr[j, i],
                    '   .Xcenter "period*%s"' % i,
                    '   .Ycenter "-period*%s"' % j,
                    '   .Segments "0"',
                    '   .Create',
                    'End With']
        sCommand = line_break.join(sCommand)
        modeler.add_to_history('define cylinder: %s:%s' % (Str_Component, Str_Name,), sCommand)
mws.save(kwargs["cst_lens_path"])
mws.close()
