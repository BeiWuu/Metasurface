from dotenv import load_dotenv
import os
import torch
from parameters import kwargs
from DataFlow import MetaOptim
from LossFunction import OptimLoss
from Visualization import Visual
import math
import matplotlib.pyplot as plt
import numpy as np
from deepagents import create_deep_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from Performance import Evaluate
from FileManager import read_file,read_folder
from Coder import internet_search
from Researcher import search_paper

load_dotenv()
checkpointer = InMemorySaver()
folder_path = kwargs.get("folder_path")

OPTIMIZER_SYSTEM_PROMPT = """You are a metasurface optimizer. You need to optimize metasurface's phase array for specific tasks and evaluate the performance.

You have access to tools:
1. read_file: To read the content of a local file. This is the only way to access local files. 
The only files you can directly access without tools are those in your virtual file system, which are private and accessible only to your.
Files created by other agents or existing project code stored in local directories are not directly accessible. To access these files, you must use this tool. 
2. read_folder: To retrieve all file names in a specified folder. 
This is useful for verifying whether files have been successfully saved during training or testing processes.
3. train: To optimize metasurface's phase array. 
4. test: To evaluate the performance of the optimized metasurface.
5. search_paper: For academic paper search.
6. internet_search: For web search.

The optimization code comprises four modules:
1. FrontNetwork: To generate amplitude arrays for different incident frequencies on the metasurface surface. For the **Focus** and **Holography** tasks, the incident waves are plane waves. For the **Generator** task, the incident wave is an information-carrying amplitude that has been processed by a neural network.
2. AS (Angular Spectrum method): To calculate propagation dynamics of light from the metasurface to the focal plane.
3. DataFlow: To package the entire data processing pipeline to a PyTorch neural network for subsequent optimization.
4. LossFunction: Task-specific loss functions.

Please ensure:
1. A group of sub-Agents will assist you to write code. **You are NOT required to write any code by yourself.** You just need to analyze the code in the report.
The report file should not have any parent folder; that is, the file path should be directly y.md, not x/y.md.
2. Only analyze the codes and reports directly relevant to the current task. For example, if solving the 'Holography' task, **do not** analyze code for 'Focus' or 'Generator'. 
3. After completing each reasoning step, always conclude by calling **write_file** to output a report."""

TEST_RETURN = """Performance of metasurface is evaluated.

{performance}

The optimized phase array is saved as {phase}, and the evaluation results are saved in the folder {results_folder}."""

@tool
def train(
        task: str,
        frequencies: list[int]
):
    """To optimize metasurface's phase array.

    Input:
        task: The specific task to be implemented, 'Focus', 'Holography' or 'Generator'.
        - 'Focus': RGB Metalens design.
        - 'Holography': Computer-generated holography.
        - 'Generator': Image Style Transfer.

        frequencies: Incident frequency array in THz."""
    try:
        os.makedirs(folder_path + f"/{task}/SavedModel")
    except:
        pass

    best_loss = kwargs["best_loss"]
    network = MetaOptim(task, frequencies)
    f_loss = OptimLoss(task)
    optimizer = torch.optim.Rprop(network.parameters(), lr=2e-4)

    # Initialize network parameters
    try:
        network.load_state_dict(torch.load(folder_path + f"/{task}/SavedModel/network.pt"))
        optimizer.load_state_dict(torch.load(folder_path + f"/{task}/SavedModel/optimizer.pt"))
        print('=' * 20, " Load pretrained model ", "=" * 20)
    except:
        pass

    for epoch in range(kwargs["epochs"]):
        outputs = network()
        loss = f_loss(outputs)
        optimizer.zero_grad()
        loss.backward(torch.ones_like(loss))
        optimizer.step()
        print('Epoch [{}/{}] \tLoss: {}\t.'.format(epoch + 1, kwargs["epochs"], loss))
        if loss < best_loss:
            best_loss = loss
            torch.save(network.state_dict(), folder_path + f"/{task}/SavedModel/network.pt")
            torch.save(optimizer.state_dict(), folder_path + f"/{task}/SavedModel/optimizer.pt")

    return f"The trained model is saved in the file {os.path.join(folder_path, task, "SavedModel")}"

@tool
def test(
        task: str,
        frequencies: list[int]
):
    """To evaluate the performance of the optimized metasurface, and upload optimized phase array.

    Input:
        task: The specific task to be implemented, 'Focus', 'Holography' or 'Generator'.
        - 'Focus': RGB Metalens design.
        - 'Holography': Computer-generated holography.
        - 'Generator': Image Style Transfer.

        frequencies: Incident frequency array in THz.

    Returns:
        The optimized phase array."""
    network = MetaOptim(task, frequencies)
    network.load_state_dict(torch.load(folder_path + f"/{task}/SavedModel/network.pt"))
    print('=' * 20, " Load pretrained model ", "=" * 20)

    phase = network.phase.detach().numpy()%(2*math.pi)
    phase = phase[phase.shape[0]//4: 3*phase.shape[0]//4, phase.shape[1]//4: 3*phase.shape[1]//4]
    plt.imshow(phase, cmap='gray')
    plt.colorbar()
    plt.axis('off')
    plt.savefig(folder_path + f"/{task}/SavedModel/phase.png",dpi=500, bbox_inches='tight', pad_inches=0)
    plt.show()
    np.save('phase.npy', phase)

    outputs = network()
    Visual(task)(outputs)
    performance = Evaluate(task,outputs)()
    return TEST_RETURN.format(performance=performance,phase=folder_path+'\phase.npy', results_folder=os.path.join(folder_path, task, "SavedModel"))

optimizer_agent = create_deep_agent(
    model="deepseek:deepseek-chat",
    checkpointer=checkpointer,
    system_prompt=OPTIMIZER_SYSTEM_PROMPT,
    tools=search_paper+[internet_search, train, test, read_file, read_folder],
)