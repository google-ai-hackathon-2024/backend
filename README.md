# MinuteTaker AI
(Description)

## How to run the backend?
1. Get you GCP Service Account following this [link](https://cloud.google.com/iam/docs/keys-create-delete)    and Move ***key.json*** to ***./google_api/credential***
    
    You need 3 roles to run the backend.
    - Cloud Speech Administrator
    - Vertex AI Administrator	
    - Storage Admin	

    ***NOTE:*** Before running the backend, Be sure to create a bucket at Google Storage and named it ***'talking-dataset'***

    ***NOTE:*** Our team's private ***key.json*** are not pushed in this repo since credential issue. If you need it for the evaluation, please send a request to kreative24hk@gmail.com or mrkim6470@gmail.com.

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
