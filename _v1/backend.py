"""
export FLASK_APP=backend.py
flask run --host=0.0.0.0 
"""

from flask import Flask, request
import utils

app = Flask(__name__)

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
    jdata = request.get_json()
    return utils.upload_audio_to_gcpbucket(jdata)

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
    return utils.set_config_for_transcript(jdata)

@app.route('/summary', methods=['POST']) 
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
        - chatbotURL <string> : Chatbot activation link
    """
    jdata = request.get_json()
    return utils.generate_result(jdata)

@app.route('/result', methods=['GET']) 
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
    return utils.get_result(conv_id)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)