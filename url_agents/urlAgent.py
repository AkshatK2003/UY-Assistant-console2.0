from url_agents.productCategoryAgent import productCategoryAgent
from url_agents.productAgent import productAgent
from url_agents.storeAgent import storeAgent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_community.utilities import SQLDatabase
import configparser
config = configparser.ConfigParser()
config.read("config.ini")

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

db_type = config["Database"]["db_type"]
password = config["Database"]["password"]
host = config["Database"]["host"]
port = config["Database"]["port"]
database= config["Database"]["database"]
username = config["Database"]["username"]
auth_plugin= config["Database"]["auth_plugin"]


class urlAgent:
    def __init__(self,baseurl,username=username,password=password,host=host,port=port,database=database,db_type=db_type,auth_plugin=auth_plugin):
        self.db = SQLDatabase.from_uri(f"mysql+mysqlconnector://{username}:{password}@{host}/{database}?auth_plugin={auth_plugin}")
        self.productURL=productAgent(baseurl,self.db)
        self.storeURL=storeAgent(baseurl,self.db)
        self.productCatURL=productCategoryAgent(baseurl,self.db)

    def generateURL(self,query):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""you are a brain for a URL generation architecture, you have to decide which is the most appropriate function to call for the task.
                    PLEASE try to figure out which tools to use by using all tools if URL is not retrieved from the tool before saying i don't know
                    you can generate URLs for creating , viewing list, editing, modifying related queries for stores products and product categories using functions or tools provided
                    for deleting queries pass view query to the function or tool and return the view URL
                    Pass the same query to the function. you have to decide weather the enetity is a product, productCategory or the store for appropriate function calling
                    please pass the 'create a new store' query to the productf function
                    just print the URL and don't print anything else and if you don't get it at last just say i don't know
        
                    if the entity seems like a product but the answer returns i don't know then fall back to product category and also do vice versa if opposite happens
                    
                    """
                ),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        @tool
        def productf(query):
            "Generates URLs for operations on products, including 'edit', 'modify', 'view', and 'create'. If the user query is about creating a new product, this function should be called."
            return self.productURL.generateURL(query)
        @tool
        def storef(query):
            "Generates URLs for operations on stores, including 'edit', 'modify', 'view', and 'create'. If the user query is about creating a new store, this function should be called."
            return self.storeURL.generateURL(query)
        @tool
        def productCatf(query):
            "Generates URLs for operations on product categories, including 'edit', 'modify', 'view', and 'create'. If the user query is about creating a new category, this function should be called."
            return self.productCatURL.generateURL(query)
            
        tools=[productf,storef,productCatf]
        llm_with_tools = llm.bind_tools(tools)
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                    x["intermediate_steps"]
                ),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        res=list(agent_executor.stream({"input": f"{query}"}))
        print(res[-1]['messages'][0].content)
        return res[-1]['messages'][0].content