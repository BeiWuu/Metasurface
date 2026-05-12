from langchain.tools import tool
from pathlib import Path
import os
from parameters import kwargs
import torch
import numpy as np

folder_path = kwargs.get("folder_path")
@tool
def read_file(file_name: str)->str:
    """Read the content of a local file.

    Input:
        file_name: the bare file name, such as x.py or x.md
            Do not include:
                - a leading slash (/x.py)
                - ./x.py
                - any directory path
                - any extra text
            If you want to read the contents of a file located in a subfolder, for example, D:\work\MetaDesign\Metasurface\Focus\distance.pt, you should specify the relative path as file_name='Focus/distance.pt'

    Returns:
        The plain text content from the file."""
    file_name = Path(r"D:\work\MetaDesign\Metasurface") / file_name
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            code_content = f.read()
        return code_content
    except:
        pass

    try:
        return torch.load(file_name)
    except:
        pass

    try:
        return np.load(file_name)
    except:
        pass

    return f"A error occurred. The reasons may be: 1. Cannot read images. 2. The requested file does not exist in the current folder.Available files are: {[name for name in os.listdir(folder_path)]}."

@tool
def read_folder(folder_name: str)->str:
    """Get all file names in a specified folder.

    The base directory is "D:\work\MetaDesign\Metasurface". When you receive a folder name as input, it always refers to a first-level subfolder directly under this base.
    For example:
    - To access content inside "D:\work\MetaDesign\Metasurface\Holography", the input should be Holography.
    - To access content deeper, such as "D:\work\MetaDesign\Metasurface\Holography\SavedModel", the input should still be Holography.

    Input:
        folder_name: The first-level subfolder.
            Do not include:
                - a leading slash (/x)
                - ./x
                - any directory path
                - any extra text

    Returns:
        The plain text content from the file."""
    filePath = Path(r"D:\work\MetaDesign\Metasurface") / folder_name
    file_name = []
    for i, j, k in os.walk(filePath):
        file_name.append(k)
    return f"The file names include {file_name}."
