from google.cloud import storage
from google.api_core import exceptions
import os
from dotenv import load_dotenv

load_dotenv()

def create_bucket(bucket_name):
    """Creates a Google Cloud Storage bucket."""
    try:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        storage_client = storage.Client(project=project_id)

        new_bucket = storage_client.create_bucket(bucket_name, location="US")
        print(f"\n✅ Bucket '{new_bucket.name}' created successfully.")
        
    except exceptions.Conflict:
        print(f"\n❌ Bucket '{bucket_name}' already exists.")
    except Exception as e:
        print(f"\n❌ Error creating bucket: {e}")

if __name__ == "__main__":
    create_bucket("test-cloud-code")