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

class productCategoryAgent:
    def __init__(self,baseurl,db):
        self.db = db
        self.productCat=eval(db.run("select id,productCategoryName from ProductCategory where customerId=52 and isDeleted=0;"))
        self.baseurl=baseurl
        
    def format_data(self,data):
        return "\n".join([f"  - {name} → {id}" for id, name in data])

    def generateURL(self,query):
        system_prompt=f""""### GOAL: you are a URL generator that generates URL for the user.If you don't know just answer you don't know.look at the examples below and then create the URL like the examples given below

        just print the url
        
        product category (name -> id):
        {self.format_data(self.productCat)}

        ### WARNINGS
        CAREFULLY MAP IDS WITH THE ENTITIES
        carefully look at the ids of the corresponding entities and then come up with the answer
        
        look at the examples given below to create the appropriate URL
        
        example 1: to view list of products cateories
        url: {self.baseurl}products/category
        
        example 2: to view or edit product category with id 442
        url: {self.baseurl}products/category/view/442
        
        example 3: to create a new product Category
        url: {self.baseurl}products/category/new

        example 4: to enable a product category with id 42
        url: {self.baseurl}products/category/view/42

        example 5: to disable a product category with id 42
        url: {self.baseurl}products/category/view/42

        example 6: to delete a product category with id 42
        url: {self.baseurl}products/category/view/42
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
        