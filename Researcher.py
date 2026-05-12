from deepagents import create_deep_agent
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain_community.agent_toolkits.load_tools import load_tools
from langgraph.checkpoint.memory import InMemorySaver
from parameters import kwargs
from FileManager import read_file,read_folder
from Coder import internet_search

load_dotenv()
checkpointer = InMemorySaver()
folder_path = kwargs.get("folder_path")

RESEARCHER_SYSTEM_PROMPT = """You are a professional researcher.

You may use the following tools:
1. read_file: To read the content of a local file. This is the only way to access local files. 
The only files you can directly access without tools are those in your virtual file system, which are private and accessible only to your.
Files created by other agents or existing project code stored in local directories are not directly accessible. To access these files, you must use this tool. 
2. read_folder: To retrieve all file names in a specified folder. 
This is useful for verifying whether files have been successfully saved during training or testing processes.
3. search_paper: For academic paper search.
4. internet_search: For web search.

Please ensure:
1. Conduct a comprehensive search to gather information.
2. Always conclude by calling **write_file** to output a report, and always update the report. If the report is too long, split it into several sub-reports and save them separately.
The report file should not have any parent folder; that is, the file path should be directly y.md, not x/y.md."""

tavilyClient = TavilyClient()
search_paper = load_tools(["arxiv"])

researcher_agent = create_deep_agent(
    model="deepseek:deepseek-chat",
    tools=search_paper+[internet_search, read_file, read_folder],
    checkpointer=checkpointer,
    system_prompt=RESEARCHER_SYSTEM_PROMPT
)
