"""Example: Google Cloud Storage operations."""

import os
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def list_buckets():
    """List all buckets in the project."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    
    # Create a client
    client = storage.Client(project=project_id)
    
    # List buckets
    buckets = client.list_buckets()
    
    print(f"Buckets in project {project_id}:")
    for bucket in buckets:
        print(f"  - {bucket.name}")


def upload_blob(bucket_name: str, source_file: str, destination_blob_name: str):
    """Upload a file to Google Cloud Storage.
    
    Args:
        bucket_name: Name of the GCS bucket
        source_file: Path to the file to upload
        destination_blob_name: Name for the blob in GCS
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    
    blob.upload_from_filename(source_file)
    print(f"File {source_file} uploaded to {destination_blob_name} in bucket {bucket_name}")


def download_blob(bucket_name: str, source_blob_name: str, destination_file: str):
    """Download a file from Google Cloud Storage.
    
    Args:
        bucket_name: Name of the GCS bucket
        source_blob_name: Name of the blob in GCS
        destination_file: Path where the file will be saved
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    blob.download_to_filename(destination_file)
    print(f"Blob {source_blob_name} downloaded to {destination_file}")


if __name__ == "__main__":
    # Example usage
    try:
        list_buckets()
        
        # Uncomment to test upload/download
        # bucket_name = os.getenv("GCS_BUCKET_NAME")
        # upload_blob(bucket_name, "local_file.txt", "uploaded_file.txt")
        # download_blob(bucket_name, "uploaded_file.txt", "downloaded_file.txt")
        
    except Exception as e:
        print(f"Error: {e}")
