# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import vertexai
from vertexai.generative_models import GenerationConfig, GenerativeModel

from string import Template 

PROJECT_ID = "southern-field-419613"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}
CONV_TYPE = ['biz-meeting', 'debating', 'interview', 'monologue']

def generate_summary(credentials:str, template:Template, transcript:str, conv_title:str) -> str:
    """
    Generate summary based on either a selected category with a specific template
    """
    print("Initialize Google VertexAI!")
    # Create credentials object
    credentials = Credentials.from_service_account_file(
        credentials,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    if credentials.expired:
        credentials.refresh(Request())
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials = credentials)

    # Construct the prompt based on the title and transcript
    print("Generate Prompt!")
    prompt = template.substitute(conv_title=conv_title, transcript=transcript)

    # Call the model to generate the summary
    print("Waiting the summarization result!")
    print(f"Title by User: {conv_title}")
    generation_model = GenerativeModel("gemini-1.0-pro")
    generation_config = GenerationConfig(temperature=0.2, max_output_tokens=256, top_k=40, top_p=0.8)
    response = generation_model.generate_content(contents=prompt, generation_config=generation_config)
    print("Completed!")
    print()
    return response.text