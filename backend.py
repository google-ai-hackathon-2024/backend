from flask import Flask, request
from flask_cors import CORS

from pathlib import Path
import datetime

import tasks

# ----------------------------------
# Create Flask
# ----------------------------------
app = Flask(__name__)

# ----------------------------------
# Initialize GCP Clients
# ----------------------------------
CREDENTIALS_FILE = "./google_api/credential/key.json"
PROJECT_ID = "southern-field-419613"
LOCATION = "us-central1" 
START_TIMESTAMP = str(datetime.datetime.now())

class Variables():
    def __init__(self):
        self.storage_client, self.speech_client = tasks.init_gcp_client(CREDENTIALS_FILE, PROJECT_ID, LOCATION)
        self.chatbot_runnable = {}

var = Variables()

# ----------------------------------
# Create Cache folder if not exist
# ----------------------------------
directory_path = Path('./cache')
directory_path.mkdir(parents=True, exist_ok=True)

# ----------------------------------
# Define REST entries
# ----------------------------------
@app.get("/")
def read_root():
    return {"Root_message": f"Backend is running (since {START_TIMESTAMP})"}

@app.route('/audio', methods=['POST']) 
def upload_audio_to_gcpbucket():
    """
    Upload a conversation audio file into the GCP bucket for the future use.

    Request : 
        - filepath <string> : The file path of conversation audio 

    Response :
        - convID <string> : Unique ID for the conversation
        - audioURL <string> : Audio file public URL in GCP bucket
    """
    
    # conv_id = tasks.id_generator()
    # audio_cache_path = Path(f"./cache/{conv_id}")
    # audio_cache_path.mkdir(parents=True, exist_ok=True)

    audio_file = request.files["audio"]
    # audio_path = f"{audio_cache_path}/audio.wav"
    # audio_file.save(audio_path)

    return tasks.upload_audio_to_gcpbucket(var.storage_client, audio_file)

@app.route('/config', methods=['POST']) 
def set_config_for_transcript():
    """
    Get basic configuration and generate transcript.

    Request : 
        - convID <string> : Unique ID for the conversation
        - speakerCnt <int> : The number of speakers in conversation
    
    Response :
        - convid <string> : Unique ID for the conversation
        - audioURLs <list:string> : Public GCP bucket link for sample audio chunks by each speaker
    """
    jdata = request.get_json()
    return tasks.set_config_for_transcript(var.storage_client, var.speech_client, jdata)

@app.route('/result', methods=['POST']) 
def generate_result():
    """
    Get information of speaker name, conversation type, and title to generate the final transcript.
    Finally, return the summary link and chatbot link

    Request : 
        - convID <string> : Unique ID for the conversation
        - convType <int> : Conversation type
                            0. biz-meeting 1. debating 2. interview 3. monologue
        - convTitle <string> : Conversation title set by user
        - speakerName <list:string> : The name of speaker
    
    Response :
        - convID <string> : Unique ID for the conversation
        - transcriptURL <string> : Public GCP bucket link for the summary
        - summaryURL <string> : Public GCP bucket link for the summarization
    """
    jdata = request.get_json()
    return tasks.generate_result(var.storage_client, jdata)

@app.route('/chatbot', methods=['GET'])
def init_chatbot():
    """
    Initialize and run AI chatbot. This chatbot can retrieve info. of conversation with convID.

    Request : 
        - convID <string> : Unique ID for the conversation
    
    Response :

    """
    conv_id = request.args.get('convID')
    var.chatbot_runnable[conv_id] = tasks.init_chatbot(conv_id)
    return {'convID':conv_id}

@app.route('/chatbot', methods=['POST'])
def answer_from_chatbot():
    """
    Initialize and run AI chatbot. This chatbot can retrieve info. of conversation with convID.

    Request : 
        - input <string> : User input
    
    Response :
        - answer <string> : Answer from chatbot
    """
    conv_id = request.args.get('convID')
    jdata = request.get_json()
    return tasks.answer_from_chatbot(var.chatbot_runnable[conv_id], jdata)

@app.route('/sharing', methods=['GET']) 
def get_result():
    """
    Get conversation ID and return the result page

    Request : 
        - convID <string> : Unique ID for the conversation
    
    Response :
        - convID <string> : Unique ID for the conversation
        - transcriptURL <string> : Public GCP bucket link for the summary
        - summaryURL <string> : Public GCP bucket link for the summarization
        - chatbotURL <string> : Chatbot activation link
    """
    conv_id = request.args.get('convID')
    return tasks.get_result(conv_id)




# ----------------------------------
# Run Flask
# ----------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)
    CORS(app)