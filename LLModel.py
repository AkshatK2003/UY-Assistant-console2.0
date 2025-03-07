from RAG import RAG
from openai import OpenAI
from dotenv import load_dotenv
from url_agents.urlAgent import urlAgent

load_dotenv()
openai=OpenAI()
MODEL="gpt-4o-mini"
rag=RAG()

class LLModel:
    def __init__(self,baseurl,model=MODEL,rag=rag,temperature=0):
        self.model=MODEL
        self.rag=rag
        self.temperature=temperature
        self.messages=[{},]
        self.url_agent=urlAgent(baseurl)

    def make_message(self,query,n):
        system_prompt=f"""Use the following pieces of context to answer the user's question. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
dont use phrases like 'same Tab' and use the Tab name
when something like "Outlets > Store" is given it means go to Outlet Tab or Section and then go to Stores Tab
first mention the tab and then mention sub tab example don't respond 'stores list in the outlet tab' first mention outlets and then mention stores
Respond like steps and not in a line or paragraph
Brands are present in 'My Brands' tab
------------------------
info:{self.rag.retrieve(query,n)}
"""
        
        user_prompt=query

        self.messages[0]={"role":"system","content":system_prompt}
        self.messages.append({"role":"user","content":user_prompt})
        return self.messages

    
        
    def generate(self,query,n=8):
        res=openai.chat.completions.create(
            messages=self.make_message(query,n),
            model=MODEL,
            temperature=self.temperature,
        )
        result=res.choices[0].message.content
        url=self.url_agent.generateURL(query)
        if (url!="I don't know" and url!="I don't know." and url!="i don't know" and url!="i don't know."):
            result+="\n"
            result+="URL for the task is:\n"
            result+=url
        assistant={"role":"assistant","content":""}
        assistant["content"]+=result
        # print("DONE")
        self.messages.append(assistant)
        return result