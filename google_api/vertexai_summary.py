from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel

from string import Template 

CONV_TYPE = ['biz-meeting', 'debating', 'interview', 'monologue']

def create_credential(credential_path:str) -> Credentials:

    credentials = Credentials.from_service_account_file(
        credential_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    if credentials.expired:
        credentials.refresh(Request())
        
    return credentials

def init_vertex_ai(project_id:str, location:str, credentials:Credentials):
    vertexai.init(project=project_id, location=location, credentials = credentials)

def generate_summary(template:Template, transcript:str, conv_title:str) -> str:
    """
    Generate summary based on either a selected category with a specific template
    """
    # Construct the prompt based on the title and transcript
    print("Generate Prompt!")
    prompt = template.substitute(conv_title=conv_title, transcript=transcript)

    # Call the model to generate the summary
    print("Waiting the summarization result!")
    print(f"Title by User: {conv_title}")
    generation_model = GenerativeModel("gemini-1.0-pro")
    generation_config = GenerationConfig(temperature=0.2, max_output_tokens=2048, top_k=40, top_p=0.8)
    response = generation_model.generate_content(contents=prompt, generation_config=generation_config)
    print("Completed!")
    print()
    return response.text