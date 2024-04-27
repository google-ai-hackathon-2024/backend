import json
import librosa
import io

from google.cloud import storage

def init_storage_client(credential_path:str):
    client = storage.Client.from_service_account_json(credential_path)
    return client

def get_public_url(gsutil_url:str):
    gsutil_prefix = "gs://"
    public_prefix = "https://storage.googleapis.com/"
    return gsutil_url.replace(gsutil_prefix, public_prefix)

def upload_to_gcs(client:storage.Client, bucket_name, source_file_path, blob_name):

    # Get the target bucket
    bucket = client.bucket(bucket_name)

    # Upload the file to the bucket
    print(f"Initialize Blob storage instance..")
    blob = bucket.blob(blob_name)
    print(f"Upload file into the Blob")
    blob.upload_from_filename(source_file_path)

    gsutil_url = f"gs://{bucket_name}/{blob_name}"
    print(f"File {source_file_path} uploaded to {gsutil_url}")

    return get_public_url(gsutil_url)

def get_json_from_gcs(client:storage.Client, bucket_name, blob_name):

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Download the contents of the blob as a string and then parse it using json.loads() method
    return json.loads(blob.download_as_string(client=None))

def get_audio_from_gcs(client:storage.Client, bucket_name, blob_name):

    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    return librosa.load(io.BytesIO(blob.download_as_string(client=None)), sr=16000)