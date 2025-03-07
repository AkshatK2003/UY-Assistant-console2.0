from openai import OpenAI
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
import configparser
from langchain.agents import tool
load_dotenv()
openai=OpenAI()
config = configparser.ConfigParser()
config.read("config.ini")

# db_type = config["Database"]["db_type"]
# password = config["Database"]["password"]
# host = config["Database"]["host"]
# port = config["Database"]["port"]
# database= config["Database"]["database"]
# username = config["Database"]["username"]
# auth_plugin= config["Database"]["auth_plugin"]

class productAgent:
    def __init__(self,baseurl,customerID,db):
        self.db = db
        self.customerID=customerID
        self.baseurl=baseurl

    def format_data(self,data):
        return "\n".join([f"  - {name} → {id}" for id, name in data])

    def generateURL(self,query):
        system_prompt=f""""### GOAL: you are a URL generator that generates URL for the user.If you don't know just answer you don't know.look at the examples below and then create the URL like the examples given below

        just print the url
        
        product list (name → id):
        {self.format_data(eval(self.db.run(f"select id,productName from Product where customerId={self.customerID} and isDeleted=0;")))}

        ### WARNINGS
        CAREFULLY MAP IDS WITH THE ENTITIES
        carefully look at the ids of the corresponding entities and then come up with the answer
        
        look at the examples given below to create the appropriate URL
        
        example 1:to view the product list
        url: {self.baseurl}products/all
        
        example 2: to view or edit product with product id 4438
        url: {self.baseurl}products/all/view/4438
        
        example 3: to create a new product
        url: {self.baseurl}products/all/new

        example 4: to enable product with id 4438
        url: {self.baseurl}products/all/view/4438

        example 5: to disable product with id 4438
        url: {self.baseurl}products/all/view/4438

        example 6: to delete a product with id 42
        url: {self.baseurl}products/all/view/42
        """

        user_prompt=query
        
        res=openai.chat.completions.create(
            messages=[
                {'role':'system','content':system_prompt},
                {'role':'user','content':user_prompt}
            ],
            model='gpt-4o-mini',
            temperature=0
        )
        return res.choices[0].message.content
        