# 🎙️MinuteTaker AI🚀
## Inspiration
We get and share a lot of information through conversations in our daily lives. Not only that, but conversations are also the most effective way to understand yourself and the other person. But conversations are more easily forgotten in our minds than we think. Sometimes they are interpreted or distorted in their own way. Recording is the most basic way to record a conversation, but how much time do we have to spend listening to Recording again.

Through 🎙️*MinuteTaker AI*🚀, we want to create an effective and smart solution that can record and understand all kinds of conversations.

## What it does
🎙️*MinuteTaker AI*🚀 is a combination of Recording and Generative AI technology. Going beyond the Recording function, which was simply recording voices, MinuteTakser AI converts Speech into Text and extracts and summarizes the key parts. Furthermore, the user will get a chatbot tailored to this given conversation. By chatting interactively, the user can get not only information of the conversation but also surrounding knowledge to help them understanding easily and much better.


## How to run Backend?
1. Setup GCP Service Account with 'key.json' file and move ***key.json*** to ***./google_api/credential***.
    ```
    ├──google_api
    │   └──credential
    │       └──key.json
    ```
    Q. how to get 'key.json'?

    - ***Option A.*** Using Google Cloud Platform set by our team.

        Our team's private ***key.json*** are not pushed in this repo since credential issue. Alternatively, you can download it through our private google drive link ([link](https://drive.google.com/file/d/1wh1IND5zmJfqhMWCV6aJcPFmaeMaOVSE/view?usp=sharing)).
        
        ***NOTE:*** The google drive link will be expired on 31th May. If you need it for the other reason, please send a request to kreative24hk@gmail.com.

    - ***Option B.*** Using your own Google Cloud Platform

        Get you GCP Service Account following this [link](https://cloud.google.com/iam/docs/keys-create-delete).
    
        You need 3 roles to run the backend.
        - Cloud Speech Administrator
        - Vertex AI Administrator	
        - Storage Admin	

        ***NOTE:*** Before running the backend, Be sure to create a bucket at Google Storage and named it ***'talking-dataset'***

2. Run Docker on your local machine. 

    If you don't have Docker in your local machine, download and install via the official website [link](https://docs.docker.com/get-docker/).

3. Build Docker image
    ```
    docker build -t minute-taker-ai-backend .
    ```

4. Run Docker container
    ```
    docker run -p 5000:5000 minute-taker-ai-backend
    ```
5. Check Backend is running
    ```
    http://localhost:5000/

    Response :
    {"Root_message":"Backend is running (since 20xx-xx-xx xx:xx:xx)"}
    ```


## Developing environment

Python 3.8 with Flask framework.

### Main libraries

- [**Google Cloud Speech**](): This service utilizes the speech-to-text API to generate a conversation transcript and clusters the words spoken by each speaker.
- [**Google Vertex AI**](): It summarizes the conversation transcript and generates answers for user questions related to the conversation.
- [**Google Cloud Storage**](): This component saves the processed results of each conversation into a Google bucket, which can then be used for the result-sharing function.
- [**LangChain**](https://python.langchain.com/docs/get_started/introduction): It is an open-source LLM orchestration framework to build Retrieval Augmented Generation(RAG) environment.
- [**chromadb**](https://www.trychroma.com/): It is a AI-native open-source vector database embedding documents and quries.
- [**librosa**](https://librosa.org/doc/main/index.html) and [**ffmpeg**](): These libraries are used to varify audio files into the same form and create audio samples by trimming.


## Contact
Hyeongkyun Kim (hyeongkyun.kim@uzh.ch or kreative24hk@gmail.com)
