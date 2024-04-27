# google-ai-hackathon

## How to run the backend?
1. Get you GCP Service Account following this [link](https://cloud.google.com/iam/docs/keys-create-delete)
    
    You need 3 roles to run the backend.
    - Cloud Speech Administrator	
    - Storage Admin	
    - Vertex AI Administrator

    and Move ***key.json*** to ***./google_api/credential***

2. Build Docker image
    ```
    docker build -t minute-taker-ai-backend .
    ```
3. Run Docker container
    ```
    docker run -p 5000:5000 minute-taker-ai-backend
    ```
4. Check Backend is running
    ```
    http://localhost:5000/

    Response :
    {"Root_message":"Backend is running (since 20xx-xx-xx xx:xx:xx)"}
    ```
