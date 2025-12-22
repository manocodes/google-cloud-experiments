import functions_framework
from google.cloud import storage
import google.cloud.logging
import os
import logging

# 1. Initialize the Cloud Logging client
log_client = google.cloud.logging.Client()
# 2. Connect the standard Python logging module to Google Cloud Logging
log_client.setup_logging()

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
        logging.error("DESTINATION_BUCKET environment variable not set.")
        return

    # Avoid infinite loops if src and dest were the same bucket
    if bucket_name == destination_bucket_name:
        logging.warning(f"Source and destination are the same ({bucket_name}). Skipping.")
        return

    logging.info(f"Processing file: {file_name} from bucket: {bucket_name}")

    source_bucket = storage_client.bucket(bucket_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    source_blob = source_bucket.blob(file_name)
    
    try:
        # Copy the blob to the destination bucket
        new_blob = source_bucket.copy_blob(source_blob, destination_bucket, file_name)
        
        # 3. STRUCTURED LOGGING: Using a dictionary for powerful searching
        logging.info("File copy successful", extra={
            "json_fields": {
                "file_name": file_name,
                "source_bucket": bucket_name,
                "dest_bucket": destination_bucket_name,
                "event_id": cloud_event["id"]
            }
        })

    except Exception as e:
        # logging.exception automatically includes the stack trace
        logging.exception(f"Error copying file {file_name}: {e}")
