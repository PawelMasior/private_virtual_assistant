#import os
import time
import random
from google.cloud import storage
client_GCP = storage.Client()
bucket_name = 'ai-agents-browsers'

def retry(max_attempts=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        return f'Error: {e}'
                    time.sleep(delay + random.uniform(0.1, 1))
        return wrapper
    return decorator

@retry(max_attempts=3, delay=1)
def blobs_clean(agent_folder):
    bucket = client_GCP.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f'{agent_folder}/prtscn/')
    for blob in blobs:
        if '.png' in blob.name: blob.delete()

@retry(max_attempts=3, delay=1)
def img_to_bucket(file_source, file_destination):
    bucket = client_GCP.bucket(bucket_name)
    blob = bucket.blob(file_destination)
    blob.upload_from_filename(file_source)
    return blob.public_url

# @retry(max_attempts=3, delay=1)
# def img_to_bucket(bucket_name, source_file_name, destination_blob_name):
#     bucket = client_GCP.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)
#     blob.upload_from_filename(source_file_name)
#     return blob.public_url