import os
import recording as rec
import gcp_bucket as bucket

BUCKET_NAME = "talking-dataset"
CREDENTIALS_FILE = "../gcp-credential/key.json"

if __name__ == "__main__":

    # folders = "../dataset/monologue"
    # audio_files = rec.get_audio_files_in_folder(folders)
    # print()

    # # -------------------------------------------------------------------
    # for f in audio_files:
    #     NEW_AUDIO_FILE = rec.check_and_convert_audio(f)
    #     print()

    #     # -------------------------------------------------------------------
    #     # To use GCP Speech API with long audio file(>1min), it should be located in the Google Cloud Storage.
    #     BLOB_NAME = os.path.join(*NEW_AUDIO_FILE.split('/')[-2:])
    #     gsutil_url = bucket.upload_to_gcs(source_file_path=NEW_AUDIO_FILE,
    #                                       bucket_name=BUCKET_NAME, 
    #                                       destination_blob_name=BLOB_NAME, 
    #                                       credentials_file=CREDENTIALS_FILE)
    #     print()
    #     print()
    
    BLOB_NAME = 'test.txt'
    gsutil_url = bucket.upload_to_gcs(source_file_path='./tmp.txt',
                                        bucket_name=BUCKET_NAME, 
                                        destination_blob_name=BLOB_NAME, 
                                        credentials_file=CREDENTIALS_FILE)
    print()
    print()