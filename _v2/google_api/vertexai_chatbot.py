
# Utils
import requests

# GCP Vertex AI
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.cloud import aiplatform
import vertexai

# Langchain
import langchain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo
from langchain.docstore.document import Document
from langchain_core.runnables.base import Runnable

TEXT_MODEL = "gemini-1.0-pro"
EMBEDDING_MODEL = "textembedding-gecko@003"
EMBEDDING_NUM_BATCH = 5

def create_credential(credential_path:str) -> Credentials:

    credentials = Credentials.from_service_account_file(
        credential_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    if credentials.expired:
        credentials.refresh(Request())

    return credentials

def init_vertex_ai(project_id:str, location:str, credentials:Credentials):
    vertexai.init(project=project_id, location=location, credentials = credentials)

def initialize_chatbot(convID:str, template:str) -> Runnable:

    print(f"LangChain version: {langchain.__version__}")
    print(f"Vertex AI SDK version: {aiplatform.__version__}")

    # Craete Object:Document including conversation informations.
    print("Create Document!")
    url_summary = f"https://storage.googleapis.com/talking-dataset/{convID}/summary.txt"
    url_transcript = f"https://storage.googleapis.com/talking-dataset/{convID}/transcript.txt"

    res_summary = requests.get(url_summary).text
    res_transcript = requests.get(url_transcript).text

    page_content = f"Summary:\n<summary>{res_summary}\n</summary>\n\n\n\
                    Transcript:\n<transcript>{res_transcript}\n</transcript>"

    text_splitter = CharacterTextSplitter(chunk_size=8192, chunk_overlap=128)
    doc = text_splitter.split_documents([
        Document(page_content=page_content, metadata={"contents": "summary and transcript"})
    ])
    print(f"summary: {url_summary}\ntranscript: {url_transcript}")

    # Create a Chroma vectorstore
    print("Create Vectorstore!")
    embeddings = VertexAIEmbeddings(
        model_name=EMBEDDING_MODEL, batch_size=EMBEDDING_NUM_BATCH
    )
    vectorstore = Chroma.from_documents(doc, embeddings, collection_name=convID)

    #  Intialising the Vertex Language model with required parameters
    print("Create LLM!")
    llm = VertexAI(
        model=TEXT_MODEL,
        max_output_tokens=2048,
        temperature=0.2,
        top_p=0.8,
        top_k=40,
        verbose=True,
    )
    
    # Create prompt template
    print("Create Prompt Template!")
    prompt = PromptTemplate.from_template(template)

    # Create Self-Query retriever
    print("Create Retriever!")
    document_content_description = "Conversation summary and its original transcript"
    metadata_field_info = [
        AttributeInfo(
            name="contents",
            description="What kinds of contents it has",
            type="string",
        ),
    ]
    retriever = SelfQueryRetriever.from_llm(
        llm,
        vectorstore,
        document_content_description,
        metadata_field_info
    )

    # Create the retrieval chain
    print("Create Retrieval Chain!")
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    print("Done!")
    return retrieval_chain

def get_chatbot_answer(retrieval_chain:Runnable, question:str) -> str:
    print(f"User Input:\n'{question}'")
    print(f"Waiting...")
    response = retrieval_chain.invoke({"input": question})['answer']
    if len(response) > 100:
        short_response = response[:100]
    else:
        short_response = response
    print(f"Response:\n{short_response}")
    return response