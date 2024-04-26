
# Utils
import requests
import prompt_template

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

PROJECT_ID = "southern-field-419613"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
CREDENTIALS_FILE = "../gcp-credential/key.json"
TEXT_MODEL = "gemini-1.0-pro"
EMBEDDING_MODEL = "textembedding-gecko@003"
EMBEDDING_NUM_BATCH = 5

def initialize_chatbot(convID:str):

    print("Initialize Google VertexAI!")

    # Create credentials object
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    if credentials.expired:
        credentials.refresh(Request())
        
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials = credentials)

    print(f"LangChain version: {langchain.__version__}")
    print(f"Vertex AI SDK version: {aiplatform.__version__}")

    # Craete documents including conversation informations.
    url_summary = f"https://storage.googleapis.com/talking-dataset/{convID}/summary.txt"
    url_transcript = f"https://storage.googleapis.com/talking-dataset/{convID}/transcript.txt"

    res_summary = requests.get(url_summary).text
    res_transcript = requests.get(url_transcript).text

    page_content = f"Summary:\n<summary>{res_summary}\n</summary>\n\n\n\
                    Transcript:\n<transcript>{res_transcript}\n</transcript>"

    text_splitter = CharacterTextSplitter(chunk_size=8192, chunk_overlap=128)
    doc = text_splitter.split_documents([
        Document(page_content=page_content, metadata={"convType": "debating"})
    ])

    # Create a Chroma vectorstore
    embeddings = VertexAIEmbeddings(
        model_name=EMBEDDING_MODEL, batch_size=EMBEDDING_NUM_BATCH
    )
    vectorstore = Chroma.from_documents(doc, embeddings)

    #  Intialising the Vertex Language model with required parameters
    llm = VertexAI(
        model=TEXT_MODEL,
        max_output_tokens=2048,
        temperature=0.2,
        top_p=0.8,
        top_k=40,
        verbose=True,
    )
    
    # Create prompt template
    template = prompt_template.get_template()
    prompt = PromptTemplate.from_template(template)

    # Create Self-Query retriever
    document_content_description = "Conversation summary and its original transcript"
    metadata_field_info = [
        AttributeInfo(
            name="convType",
            description="Type of conversation",
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
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)