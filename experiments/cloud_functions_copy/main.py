import functions_framework
from google.cloud import storage
import os

# Initialize the storage client
storage_client = storage.Client()

@functions_framework.cloud_event
def copy_file(cloud_event):
    """
    Triggered by a change to a Cloud Storage bucket.
    Copies the file to a destination bucket.
    """
    data = cloud_event.data

    # Extract file and bucket details from the event
    bucket_name = data["bucket"]
    file_name = data["name"]
    
    # Destination bucket name from environment variable
    destination_bucket_name = os.environ.get("DESTINATION_BUCKET")
    
    if not destination_bucket_name:
        print("DESTINATION_BUCKET environment variable not set.")
        return

    # Avoid infinite loops if src and dest were the same bucket
    if bucket_name == destination_bucket_name:
        print(f"Source and destination are the same ({bucket_name}). Skipping.")
        return

    print(f"Processing file: {file_name} from bucket: {bucket_name}")

    source_bucket = storage_client.bucket(bucket_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    source_blob = source_bucket.blob(file_name)
    
    try:
        # Copy the blob to the destination bucket
        # copy_blob returns the new blob object
        new_blob = source_bucket.copy_blob(source_blob, destination_bucket, file_name)
        print(f"Successfully copied {file_name} to {destination_bucket_name}.")
    except Exception as e:
        print(f"Error copying file {file_name}: {e}")
