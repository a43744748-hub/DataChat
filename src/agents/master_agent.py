import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit


def agent_creation(model, db_path, system_prompt, metadata):


    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")


    toolkit = SQLDatabaseToolkit(db=db, llm=model)


    tools = toolkit.get_tools()


    system_prompt = system_prompt.format(
        dialect=db.dialect,
        metadata=metadata,
    )


    agent = create_agent(
        model = model,
        tools = tools,
        system_prompt=system_prompt,
    )


    return agent

if __name__ == "_main_":
    from src.db_utils.load_metadata import load_metadata
    from src.llm_instance import LLM_INSTANCES
    model = LLM_INSTANCES["GPT_4_1"]["MODEL"]
    db_path = 'pharma.db'
    system_prompt = open("./src/prompts/agent_system_prompt.txt", "r").read()
    metadata = load_metadata('./data/metadata.yaml')


    print(agent_creation(model=model, db_path=db_path, system_prompt=system_prompt, metadata=metadata))