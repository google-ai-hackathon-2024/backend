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





Basically, the thing we can do for backend now is…

- Chenck how to implement RAG with current backend system and what we need to do for Front-end for this
- ⁠Improving Sp2txt: the performance of this function is not that good. It can‘t recognize the speaker well. We might look the parameter we can set together. Or any evaluation matrices to show them our perf. and the room for improvement.
- ⁠Improving Prompt: Sometimes, the summary format wasn‘t followed strictly and have some variant. How can we prevent this scenario by prompt engineering.