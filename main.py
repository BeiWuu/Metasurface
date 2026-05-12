from deepagents import create_deep_agent
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.tools import tool
from Optimizer import optimizer_agent
from Researcher import researcher_agent
import os
import time
from FileManager import read_file,read_folder
from Simulator import simulation
from parameters import kwargs
from DatasetManager import focus_data,holography_data,generator_data

load_dotenv()
folder_path = kwargs.get("folder_path")
DB_URI=os.getenv("DB_URI")

SOLVER_SYSTEM_PROMPT = """You are an experienced computational optics scientist. 
You need to solve one of the following three tasks based on user prompt.
1. **Focus**: Design an **RGB metalens** with a specific focal length. The metalens should focus red, green, and blue lights at different positions on the focal plane.
2. **Holography**: Achieve computer-generated holography by optimizing the metasurface phase array, forming holographic images on multiple focal planes.
3. **Generator**: Perform image style transfer by jointly optimizing a lightweight front neural network (which takes content images, and outputs RGB amplitude arrays incident on the Metasurface) and the metasurface phase array, producing a style-transferred image on the focal plane.

Your should: 
1. Guide the user to deeply understand the specific task domain ('RGB Metalens design', 'Computer-generated holography' or 'Image Style Transfer').
2. Optimize the metasurface phase array.
3. Analyze the optimization code of this project (including FrontNetwork.py, AS.py, DataFlow.py and LossFunction.py).

You have access to these tools:
1. read_file: To read the content of a local file. This is the only way to access local files. 
The only files you can directly access without tools are those in your virtual file system, which are private and accessible only to your.
Files created by other agents or existing project code stored in local directories are not directly accessible. To access these files, you must use this tool. 
2. read_folder: To retrieve all file names in a specified folder. 
This is useful for verifying whether files have been successfully saved during training or testing processes.
3. researcher: To gather relevant academic and technical information.
4. simulation: Simulate the phase relationship between different frequencies in the meta-atom using CST software. This tool is essential for optimizing the metasurface and must be called before the optimization process begins.
The default structure of the meta-atom is a nanopillar with a radius of 50 nm, and the phase modulation is achieved by adjusting the height of the nanopillar. The nanopillar material is TiO2, and the substrate material is SiO2. The period of the meta-atom is 160nm multiplies 160 nm.
This tool first simulates the linear relationship between the nanopillar height and the phase under different incident frequencies using CST software. Then, based on these relationships, this tool calculates the relationship between different incident frequencies and the phases.
5. focus_data: Create a dataset for the RGB metalens design (Focus) task.
6. holography_data: Create a dataset for the holography task.
7. generator_data: Create a dataset for the image style transfer (Generator) task.
8. metasurface_optimize: To optimize the metasurface's phase array, and evaluate its performance.

You should note that:
A verifier will evaluate your chain of thought. Assess this feedback first. If the suggestions are valid, produce revised and improved answers based on the feedback.

Please ensure:
1. A group of sub-Agents are responsible for writing code to assist you. **You are NOT required to write any code by yourself.** You only need to communicate appropriately with the sub-Agents.
2. After completing each reasoning step, always conclude by calling **write_file** to output a report, and continue to refine it throughout the process. 
The report file should not have any parent folder; that is, the file path should be directly y.md, not x/y.md.
3. The final report should cover **all stages**, including the revising stage. If the report is too long, split it into several sub-reports and save them separately."""

VERIFIER_SYSTEM_PROMPT = """You are a strict optical researcher. Your task is to evaluate the chain of thought. 
If you identify any errors, clearly identify them and provide concrete, feasible improvement suggestions. Otherwise, state 'No improvements needed.'

You have access to these tools:
1. read_file: To read the content of a local file. This is the only way to access local files. 
The only files you can directly access without tools are those in your virtual file system, which are private and accessible only to your.
Files created by other agents or existing project code stored in local directories are not directly accessible. To access these files, you must use this tool. 
2. read_folder: To retrieve all file names in a specified folder. 
This is useful for verifying whether files have been successfully saved during training or testing processes.
3. researcher: To gather relevant academic and technical information.
4. simulation: Simulate the phase relationship between different frequencies in the meta-atom using CST software. The default structure of the meta-atom is a nanopillar with a radius of 50 nm, and the phase modulation is achieved by adjusting the height of the nanopillar. The nanopillar material is TiO2, and the substrate material is SiO2. The period of the meta-atom is 160nm multiplies 160 nm.
5. focus_data: Create a dataset for the RGB metalens design (Focus) task.
6. holography_data: Create a dataset for the holography task.
7. generator_data: Create a dataset for the image style transfer (Generator) task.
8. metasurface_optimize: To optimize the metasurface's phase array, and evaluate its performance.

Please ensure:
Always conclude by calling **write_file** to output a report. If the report is too long, split it into several sub-reports and save them separately.
The report file should not have any parent folder; that is, the file path should be directly y.md, not x/y.md."""

USER_QUERY = """Achieve image style transfer using an an optoelectronic hybrid neural network. The incident RGB frequencies are 480 THz, 560 THz, and 640 THz. The filenames for the content image and the style image are "cont.png" and "style.png", respectively. The focal length is 50 micrometers. In addition, you should conduct a comprehensive research of relevant academic and technical information."""

@tool
def metasurface_optimize(request:str)->str:
    """Optimize the metasurface phase array, and evaluate its performance using natural language.

    Use this when the user wants to:
    1. Optimize the metasurface's phase array.
    2. Evaluate the performance of the optimized metasurface.
    3. Upload optimized phase array.

    Input: Natural language request (e.g., 'Optimize the metasurface phase array, with incident frequencies being [480, 560, 640] THz.')"""
    StartTime = time.time()
    config = {"configurable": {"thread_id": "2"}}
    step = 1
    for event in optimizer_agent.stream(
            {"messages": [{"role":"user","content":request}]},
            stream_mode="values",
            stream_usage=True,
            config=config
    ):
        msg = event["messages"][-1]
        msg.pretty_print()
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            EndTime = time.time()
            print('😊Optimizer agent. Step:', step, ', consumes tokens:', usage["total_tokens"], ', running time:', EndTime-StartTime)
            step+=1
            StartTime = EndTime
        if "files" in event and len(event["files"]) > 0:
            file_names = list(event["files"].keys())
            for file_name in file_names:
                file = open(folder_path + file_name, "w+", encoding='utf-8')
                file.truncate()
                for code in event["files"][file_name]["content"]:
                    file.write(code)
                    file.write("\n")
                file.close()
    return f'\nThe optimizer report is stored in the local files {file_names}. You should call tools to read all files.'

@tool
def researcher(request:str)->str:
    """Gather relevant academic and technical information using natural language.

    Use this when the user wants to conduct in-depth research.

    Input: Natural language request (e.g., 'What is RGB metalens? Break down the task into subtasks for research.')"""
    StartTime = time.time()
    config = {"configurable": {"thread_id": "3"}}
    step = 1
    for event in researcher_agent.stream(
            {"messages": {"role": "user", "content": request}},
            stream_mode="values",
            stream_usage=True,
            config=config
    ):
        msg = event["messages"][-1]
        msg.pretty_print()
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            EndTime = time.time()
            print('😊Researcher agent. Step:', step, ', consumes tokens:', usage["total_tokens"], ', running time:', EndTime-StartTime)
            step+=1
            StartTime = EndTime
        if "files" in event and len(event["files"]) > 0:
            file_names = list(event["files"].keys())
            for file_name in file_names:
                file = open(folder_path + file_name, "w+", encoding='utf-8')
                file.truncate()
                for code in event["files"][file_name]["content"]:
                    file.write(code)
                    file.write("\n")
                file.close()
    return f'\nThe researcher report is stored in the local file {file_names}. You should call tools to read all files.'

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()

    solver_agent = create_deep_agent(
        model="deepseek:deepseek-chat",
        tools=[metasurface_optimize, researcher, read_file, read_folder, simulation, focus_data,holography_data,generator_data],
        system_prompt=SOLVER_SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

    verifier_agent = create_deep_agent(
        model="deepseek:deepseek-chat",
        tools=[metasurface_optimize, researcher, read_file, read_folder, simulation, focus_data,holography_data,generator_data],
        system_prompt=VERIFIER_SYSTEM_PROMPT,
        checkpointer=checkpointer
    )

    config = {"configurable": {"thread_id": "1"}}
    StartTime = time.time()
    step = 1
    for event in solver_agent.stream(
            {"messages": {"role": "user", "content": USER_QUERY}},
            stream_mode="values",
            stream_usage=True,
            config=config
    ):
        msg = event["messages"][-1]
        msg.pretty_print()
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            EndTime = time.time()
            print('😊Solver agent. Step:', step, ', consumes tokens:', usage["total_tokens"], ', running time:', EndTime-StartTime)
            step+=1
            StartTime = EndTime

        if "files" in event and len(event["files"]) > 0:
            file_names = list(event["files"].keys())
            for file_name in file_names:
                file = open(folder_path + file_name, "w+", encoding='utf-8')
                file.truncate()
                for code in event["files"][file_name]["content"]:
                    file.write(code)
                    file.write("\n")
                file.close()

    StartTime = time.time()
    step = 1
    for event in verifier_agent.stream(
            {"messages": {"role": "user", "content": 'Verify the accuracy of the above chain of thought.'}},
            stream_mode="values",
            stream_usage=True,
            config=config
    ):
        msg = event["messages"][-1]
        msg.pretty_print()
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            EndTime = time.time()
            print('😊Verifier agent. Step:', step, ', consumes tokens:', usage["total_tokens"], ', running time:', EndTime-StartTime)
            step+=1
            StartTime = EndTime
        if "files" in event and len(event["files"]) > 0:
            file_names = list(event["files"].keys())
            for file_name in file_names:
                file = open(folder_path + file_name, "w+", encoding='utf-8')
                file.truncate()
                for code in event["files"][file_name]["content"]:
                    file.write(code)
                    file.write("\n")
                file.close()

    StartTime = time.time()
    step = 1
    for event in solver_agent.stream(
            {"messages": {"role": "user", "content": 'Assess previous feedback. If suggestions are valid, produce revised answers accordingly; otherwise, ignore them.'}},
            stream_mode="values",
            stream_usage=True,
            config=config
    ):
        msg = event["messages"][-1]
        msg.pretty_print()
        usage = getattr(msg, "usage_metadata", None)
        if usage:
            EndTime = time.time()
            print('😊Correction agent. Step:', step, ', consumes tokens:', usage["total_tokens"], ', running time:', EndTime-StartTime)
            step+=1
            StartTime = EndTime
        if "files" in event and len(event["files"]) > 0:
            file_names = list(event["files"].keys())
            for file_name in file_names:
                file = open(folder_path + file_name, "w+", encoding='utf-8')
                file.truncate()
                for code in event["files"][file_name]["content"]:
                    file.write(code)
                    file.write("\n")
                file.close()