# neo-pusher

`neo-pusher` is a Python package designed to facilitate the seamless transfer of data from CSV files to a Neo4j database. Leveraging the power of OpenAI's GPT models and the LangChain framework, `neo-pusher` automates the process of schema generation, data preprocessing, and data insertion into Neo4j, ensuring data consistency and integrity.

## Features

- **Automated Schema Generation**: Automatically generates a Neo4j schema based on the CSV file's headers.
- **Data Preprocessing**: Identifies and resolves inconsistencies in the data before pushing it to Neo4j.
- **Error Handling and Debugging**: The agent reruns and debugs code automatically if any errors are encountered during the process.
- **Multiple Dataset Support**: Capable of handling multiple datasets simultaneously, ensuring that all columns are properly represented in the database.

## Installation

To install `neo-pusher`, use pip:

```bash
pip install neo-pusher
```


## Usage

Here's an example of how to use `neo-pusher` to push data from a CSV file to a Neo4j database:

```python
from neo_pusher.agent import NeoAgent

# Initialize the NeoAgent with your OpenAI API key
agent = NeoAgent(apikey="your_openai_api_key",lang_chain_api_key="your_lang_chain_api_key")

# Define the parameters for your Neo4j database and CSV file
path = "path/to/your/csvfile.csv"
username = "neo4j_username"
password = "neo4j_password"
url = "bolt://localhost:7687"
data = "head of your csv data"

# Run the agent to push data to Neo4j
response = agent.run(path, username, password, url, data)
print(response)
```

### Parameters

- `apikey` (str): Your OpenAI API key.
- `langchain_api_key` (str): Your Langchain API key.
- `model` (str): The OpenAI model to use. Defaults to `"gpt-4o"`.
- `path` (str): The path to the CSV file.
- `username` (str): The username for the Neo4j database.
- `password` (str): The password for the Neo4j database.
- `url` (str): The URL of the Neo4j database.
- `data` (str): The head of the CSV file. Defaults to `None`.

### Return Value

- The `run` method returns a response from the LLM, including the results of the schema generation, data preprocessing, and data insertion into Neo4j.

## Example CSV Data

The following is an example of the CSV file headers that `neo-pusher` can process:

**Dataset 1:**

| order_details_id | order_id | pizza_id        | quantity |
|------------------|----------|-----------------|----------|
| 1                | 1        | hawaiian_m       | 1        |
| 2                | 2        | classic_dlx_m    | 1        |

**Dataset 2:**

| pizza_id | pizza_type_id | size | price |
|----------|---------------|------|-------|
| bbq_ckn_s | bbq_ckn       | S    | 12.75 |
| bbq_ckn_m | bbq_ckn       | M    | 16.75 |

## Notes

- The agent uses the `neo4j` Python package to connect to and push data into the Neo4j database.
- Before pushing data, the agent checks for any inconsistencies and cleans the data accordingly.

[Downloads](https://pepy.tech/project/neo-pusher)
