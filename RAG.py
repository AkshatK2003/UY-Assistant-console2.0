from langchain_chroma import Chroma
from variables import *
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
embeddings=OpenAIEmbeddings()

class RAG:
    def __init__(self,embeddings=embeddings):
        "vector store for page contents"
        self.vectorStores=vectorStores=Chroma(
            collection_name="ZE_Manual",
            embedding_function=embeddings,
            persist_directory="pdfs"
        )

        
    def retrieve(self,query,n=8):
        "Retriever"
        res=self.vectorStores.similarity_search(
            query,
            k=n
        )
        result=""
        for idx,r in enumerate(res):
            result+=r.page_content
        # print("-----------------------------------------------------------------------RETRIEVED DOC----------------------------------------------------------------------------------------")
        # print(result.encode("utf-8", "replace").decode("utf-8"))
        # print("-----------------------------------------------------------------------FINAL RESULT------------------------------------------------------------------------------------------")
        return result