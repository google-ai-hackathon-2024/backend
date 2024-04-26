import os
import recording as rec
import gcp_bucket as bucket

BUCKET_NAME = "talking-dataset"
CREDENTIALS_FILE = "../gcp-credential/key_new.json"

if __name__ == "__main__":

    BLOB_NAME = 'test.txt'
    gsutil_url = bucket.upload_to_gcs(source_file_path='./tmp.txt',
                                        bucket_name=BUCKET_NAME, 
                                        destination_blob_name=BLOB_NAME, 
                                        credentials_file=CREDENTIALS_FILE)
    print()
    print()