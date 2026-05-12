from langgraph.checkpoint.postgres import PostgresSaver
from dotenv import load_dotenv
import os

# 通过外部数据库PostgresSaver查询历史对话的消息

load_dotenv()

DB_URI=os.getenv("DB_URI")
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    # 获取所有checkpoint
    checkpointer.delete_thread("1") # 删除数据表
    checkpoints = checkpointer.list(
        {"configurable": {"thread_id": "1"}}
    )

    for checkpoint in checkpoints:
        messages = checkpoint[1]["channel_values"]["messages"]
        for message in messages:
            message.pretty_print()
        break