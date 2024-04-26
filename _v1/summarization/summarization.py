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

import json
import sys
import vertexai
import pandas as pd
from vertexai.generative_models import GenerationConfig, GenerativeModel


PROJECT_ID = "hackathon-419908"  # @param {type:"string"}
LOCATION = "us-central1"  # @param {type:"string"}


vertexai.init(project=PROJECT_ID, location=LOCATION)
generation_model = GenerativeModel("gemini-1.0-pro")
generation_config = GenerationConfig(temperature=0.2, max_output_tokens=256, top_k=40, top_p=0.8)

def generate_summary(transcript_json, category=None, custom_prompt=None):
    """
    Generate summary based on either a selected category with a specific template
    or a custom prompt provided by the user.
    """
        # Check if transcript_json is a file path and load it
    print(transcript_json)
    if isinstance(transcript_json, str):
        with open(transcript_json, 'r') as file:
            transcript_data = json.load(file)
    else:
        transcript_data = transcript_json

    # Predefined templates for each category
    templates = {
        "debate": "Analyze the following debate transcript and summarize the topics discussed by each side, including their main arguments. Format the summary in parts with sections for \"topic\", \"debaters_main_arguments\":",
        "interview": "Summarize the following interview transcript, focusing on the main questions asked and the summary of the interviewee's responses. Format the summary in parts with sections for \"interviewee_description\", \"questions\", and \"responses\":",
        "business meeting": "Summarize the following business meeting discussion, focusing on what has been accomplished so far, what needs to be done, any problems we're facing, and any major wins. Format the summary in parts with sections for \"accomplishments\", \"to_do\", \"problems\", and \"wins\":",
        "monologue": "Summarize the following monologue, identifying the main topic and the speaker's main arguments. Format the summary in parts with sections for \"topic\" and \"main_arguments\":"
    }

    # Construct the prompt based on the category or custom prompt
    prompt = custom_prompt if custom_prompt else templates.get(category, "")

    # Append transcript data to the prompt
    for item in transcript_data:
        prompt += f'\n\nSpeaker {item["Speaker"]}: {item["Contents"]}'

    # Call the model to generate the summary
    response = generation_model.generate_content(contents=prompt, generation_config=generation_config)
    summary_text = response.text  # Assuming .text contains the summary

    # Construct and return JSON response
    summary_json = {
        "summary": summary_text
    }
    # Specify the path where you want to save the JSON file
    file_path = "interview_summary.json"

    # Save the summary in JSON format to the specified file
    with open(file_path, "w") as file:
        json.dump(summary_json, file, indent=2)


    
    return summary_json

generate_summary("/Users/oroikon/Projects/google-ai-hackathon/speech2text/results/interview/Dalia_Mogahed_16k/transcript.json","interview",)