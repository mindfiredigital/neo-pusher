# neoagent/agent.py
"""This module creates a agent that will push data to neo4j"""
from langchain import hub
from langchain_openai import ChatOpenAI

from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor


from langchain_experimental.tools import PythonREPLTool


class NeoAgent:
    '''Neo4j data pusher '''
    tools = [PythonREPLTool()]
    instructions = """You are an agent designed to write
    and execute python code to answer questions.
    You have access to a python REPL, which you can use to execute python code.
    If you get an error, debug your code and try again.
    Only use the output of your code to answer the question.
    if you need to download the file or some installation need to be done do it.
    You might know the answer without running any code, but you should still run the code to get the answer.
    If it does not seem like you can write code to answer the question, just return "I don't know" as the answer.
    """
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)

    def __init__(self, apikey, model="gpt-4o"):
        '''
        Parameters:
        apikey (str): The OpenAI API key.
        model (str): The OpenAI model to use. Defaults to "gpt-4o".
        '''
        agent = create_openai_functions_agent(
            ChatOpenAI(temperature=0, api_key=apikey,
                       model=model, verbose=True),
            self.tools, self.prompt)
        self.agent_executor = AgentExecutor(
            agent=agent, tools=self.tools, verbose=True, handle_parsing_errors=True)

    def run(self, path, username, password, url, data=None):
        '''
        Parameters:
        path (str): The path to the CSV file.
        username (str): The username for the Neo4j database.
        password (str): The password for the Neo4j database.
        url (str): The URL of the Neo4j database.
        data (str): The head of the CSV file. Defaults to None.

        Returns:
        response from LLM

        '''
        prompt = f"""
        You are given head of the csv files. Your work is to study the head of the csv files and generate neo4j schema.
        Then write and execute the code that will push the data to neo4j db with proper label name and relationship.
        If you encounter error, rerun and solve it.
        Here's head of the csv files: {data}
        Here's path: {path}
        Username of neo4j: {username}
        Password of neo4j: {password}
        URL of neo4j: {url}
        NOTE:
        - Use neo4j package to connect and push data to neo4j
        - Do not miss any columns in the data
        - Before pushing data preprocess it to check for any data inconsistencies.
        - If you find any inconsistencies in data, preprocess it and clean it
        """
        res = self.agent_executor.invoke({"input": prompt})
        return res["output"]
