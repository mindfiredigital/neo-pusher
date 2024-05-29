import streamlit as st
import openai
from neo4j import GraphDatabase
import pandas as pd
import os
import io
from dotenv import load_dotenv


from neoagent.agent import NeoAgent
from neoagent.get_link import GetLink

from streamlit_chat import message
from timeit import default_timer as timer

from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
# from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

load_dotenv()

# Initialize the Streamlit app
st.title("Chat Interface with OpenAI and Neo4j")

# Ensure the downloads directory exists
os.makedirs("downloads", exist_ok=True)


# Sidebar for credentials input
with st.sidebar:
    st.header("Enter your credentials")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    neo4j_url = st.text_input("Neo4j URL")
    neo4j_username = st.text_input("Neo4j Username")
    neo4j_password = st.text_input("Neo4j Password", type="password")
    submit_button = st.button(label='Submit')

llm = ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0
        )

        # Cypher generation prompt
cypher_generation_template = """
        You are an expert Neo4j Cypher translator who converts English to Cypher based on the Neo4j Schema provided, following the instructions below:
        1. Generate Cypher query compatible ONLY for Neo4j Version 5
        2. Do not use EXISTS, SIZE, HAVING keywords in the cypher. Use alias when using the WITH keyword
        3. Use only Nodes and relationships mentioned in the schema
        4. Always do a case-insensitive and fuzzy search for any properties related search. Eg: to search for a Client, use `toLower(client.id) contains 'neo4j'`. To search for Slack Messages, use 'toLower(SlackMessage.text) contains 'neo4j'`. To search for a project, use `toLower(project.summary) contains 'logistics platform' OR toLower(project.name) contains 'logistics platform'`.)
        5. Never use relationships that are not mentioned in the given schema
        6. Relate the query context to below data schema find relevant matching properties using case-insensitive matching and the OR-operator, E.g, to find a logistics platform -project, use `toLower(project.summary) contains 'logistics platform' OR toLower(project.name) contains 'logistics platform'`.

        schema: {schema}


        Examples:
        Question: Which client's projects use most of our people?
        Answer: ```MATCH (c:CLIENT)<-[:HAS_CLIENT]-(p:Project)-[:HAS_PEOPLE]->(person:Person)
        RETURN c.name AS Client, COUNT(DISTINCT person) AS NumberOfPeople
        ORDER BY NumberOfPeople DESC```
        Question: Which person uses the largest number of different technologies?
        Answer: ```MATCH (person:Person)-[:USES_TECH]->(tech:Technology)
        RETURN person.name AS PersonName, COUNT(DISTINCT tech) AS NumberOfTechnologies
        ORDER BY NumberOfTechnologies DESC```

        Question: {question}
        """

cypher_prompt = PromptTemplate(
            template=cypher_generation_template,
            input_variables=["schema", "question"]
        )

CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
        The information part contains the provided information that you must use to construct an answer.
        The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
        Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
        If the provided information is empty, say that you don't know the answer.
        Final answer should be easily readable and structured.
        Information:
        {context}

        Question: {question}
        Helpful Answer:"""

qa_prompt = PromptTemplate(
            input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
        )





# Initialize OpenAI API and Neo4j database connection
if submit_button:
    openai.api_key = openai_api_key
    # llm.api_key = openai_api_key

    try:
        neo4j_driver = GraphDatabase.driver(
            neo4j_url, auth=(neo4j_username, neo4j_password))
        # OpenAI API configuration
        

        st.sidebar.success("Connected to Neo4j database successfully!")
    except Exception as e:
        st.sidebar.error(f"Error connecting to Neo4j database: {e}")


def query_graph(user_input):
    graph = Neo4jGraph(url=neo4j_url, username=neo4j_username,
                       password=neo4j_password, enhanced_schema=True)
    # chain = GraphCypherQAChain.from_llm(
    #     ChatOpenAI(temperature=0, api_key=os.getenv("api_key")),
    #     return_intermediate_steps=True,
    #     graph=graph,
    #     verbose=True,

    # )
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        qa_prompt=qa_prompt
    )
    # result = chain.invoke({"query":user_input})
    return chain.invoke({"query": user_input})


# File upload and link input
st.sidebar.header("Upload files or provide file links")
uploaded_files = st.sidebar.file_uploader(
    "Choose CSV files", accept_multiple_files=True)
file_links = st.sidebar.text_area("File links (one per line)")
process_datas = st.sidebar.button("Enter")


dataframes = []
file_paths = []

# Handle file uploads
if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # Save each uploaded file to the downloads directory
            file_path = os.path.join("downloads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Read the file into a DataFrame
            data = pd.read_csv(file_path).head(5).to_string()
            dataframes.append(data)
            file_paths.append(file_path)
            st.sidebar.success(
                f"File '{uploaded_file.name}' uploaded successfully! Saved to {file_path}")
        except Exception as e:
            st.sidebar.error(
                f"Error reading uploaded file '{uploaded_file.name}': {e}")

# Handle file links
if file_links:
    for file_link in file_links.splitlines():
        try:
            # Read the file from the provided link into a DataFrame
            data = pd.read_csv(file_link)

            # Save the file to the downloads directory
            file_name = file_link.split("/")[-1]
            file_path = os.path.join("downloads", file_name)
            data.to_csv(file_path, index=False)

            dataframes.append(data)
            file_paths.append(file_path)
            st.sidebar.success(
                f"File loaded from link '{file_link}' successfully! Saved to {file_path}")
        except Exception as e:
            st.sidebar.error(
                f"Error reading file from link '{file_link}': {e}")

if process_datas:
    data_s = ""
    for i, d in enumerate(dataframes):
        data_s += ("data"+str(i+1) + " :" + d + "\n")
    print("================")
    print(data_s)
    print("=======================")
    print(len(file_paths), len(dataframes))
    print("==================")
    agent = NeoAgent(openai_api_key)
    result = agent.run(path=file_path, username=neo4j_username,
                       password=neo4j_password, url=neo4j_url, data=data_s)

# Display the data if available
for i, data in enumerate(dataframes):
    st.write(f"Data Preview from {file_paths[i]}:")
    # st.write(data.head())

    # Display the file path
    st.write(f"File saved to: {file_paths[i]}")

# Chat interface
st.header("Chat with OpenAI")
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Display previous messages
for message in st.session_state['messages']:
    st.write(message)

# Input for the user's message
user_input = st.text_area("Your message", height=100)

# Button to send the message
if st.button("Send"):
    if user_input:
        # Save the user's message
        st.session_state['messages'].append(f"You: {user_input}")

        try:
            # Send the user's message to OpenAI API
            result = query_graph(user_input)

            intermediate_steps = result["intermediate_steps"]
            cypher_query = intermediate_steps[0]["query"]
            database_results = intermediate_steps[1]["context"]

            answer = result["result"]
            st.write(answer)

            # Save the response from OpenAI
            st.session_state['messages'].append(f"Bot: {answer}")

        except Exception as e:
            st.error(f"Error communicating with OpenAI: {e}")

        # Clear the input box
