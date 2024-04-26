# google-ai-hackathon

To run the backend on the local machine, you need a GCP credential key in JSON format and locate like below.
```
gcp-credential/key.json
```
Q. How to generate JSON Key of GCP service account?


Following the guidline
https://cloud.google.com/iam/docs/keys-create-delete


Q. Which roles are needed for the GCP service account?
- Cloud Speech Administrator	
- Storage Admin	
- Vertex AI Administrator	


"""
export FLASK_APP=backend.py
flask run --host=0.0.0.0 
"""