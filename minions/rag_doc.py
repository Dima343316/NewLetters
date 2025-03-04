import os
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()

# place your VseGPT key here
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_TOKEN_API')

def create_search_db(file_text,
                        knowledge_base_link,
                        chunk_size=1024,
                        chunk_overlap=200):

    splitter = RecursiveCharacterTextSplitter(['\n\n', '\n', ' '], chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    source_chunks = []

    # splitting to chunks
    for chunkID,chunk in enumerate(splitter.split_text(file_text)):
        source_chunks.append(Document(page_content=chunk, \
                            metadata={'source': knowledge_base_link,
                                      'chunkID': chunkID}))

    if len(source_chunks) > 0:
        embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_base = "https://api.vsegpt.ru/v1")
        db = FAISS.from_documents(source_chunks, embedding_model)
        db.save_local(knowledge_base_link)
        print("Docs.db search index created!")

def run_gpt_query(user_query, search_db):
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_base="https://api.vsegpt.ru/v1/")
    db = FAISS.load_local(search_db, embedding_model, allow_dangerous_deserialization=True)
    docs = db.similarity_search(user_query, 3) # число результатов схожих по эмбеддингу

    message_content = '\n\n'.join([doc.page_content for i, doc in enumerate(docs)])
    return message_content

if __name__ == "__main__":
    # # Read text from file
    # with open("sun.txt", "r", encoding="utf-8") as file:
    #     file_text = file.read()
    #
    # # Link to the knowledge base, can be a URL or some identifier string
    #     knowledge_base_link = "sun_knowledge_base"
    #     create_search_db(file_text, knowledge_base_link)
    knowledge_base_link = "FZ01"
    query="Как открывается общее собрание участников?"
    cool=run_gpt_query(query,knowledge_base_link)
    print(cool)
    # Run the create_search_db function
