#!/usr/bin/env python3
"""
Test script to verify service account key from Secret Manager works.

This script:
1. Retrieves the service account key from Secret Manager
2. Authenticates using that key
3. Tests the credentials by listing projects
"""

import json
from google.cloud import secretmanager
from google.oauth2 import service_account
from google.cloud import resourcemanager_v3


def get_credentials_from_secret_manager():
    """Retrieve service account credentials from Secret Manager."""
    
    # Create Secret Manager client (uses your default credentials)
    client = secretmanager.SecretManagerServiceClient()
    
    # Build the secret name
    secret_name = "projects/devlead-companion/secrets/devlead-companion-svc-acc/versions/latest"
    
    print(f"📥 Fetching secret from Secret Manager: {secret_name}")
    
    # Access the secret
    response = client.access_secret_version(request={"name": secret_name})
    
    # Get the secret payload (the JSON key file content)
    secret_payload = response.payload.data.decode("UTF-8")
    
    print("✅ Successfully retrieved secret from Secret Manager")
    
    # Parse JSON and create credentials
    credentials_dict = json.loads(secret_payload)
    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    
    # Display which service account we're using
    print(f"🔑 Service Account: {credentials_dict.get('client_email')}")
    print(f"🆔 Private Key ID: {credentials_dict.get('private_key_id')}")
    
    return credentials


def test_credentials(credentials):
    """Test the credentials by making an API call."""
    
    print("\n🧪 Testing credentials by listing projects...")
    
    try:
        # Create a client using the credentials
        projects_client = resourcemanager_v3.ProjectsClient(credentials=credentials)
        
        # List projects (this is a simple read operation)
        request = resourcemanager_v3.ListProjectsRequest(
            parent="projects/devlead-companion"
        )
        
        # This will fail if credentials don't work
        response = projects_client.list_projects(request=request)
        
        print("✅ Credentials are valid! Successfully authenticated.")
        print(f"📊 Service account has access to make API calls")
        
        return True
        
    except Exception as e:
        print(f"❌ Credential test failed: {e}")
        print("\nThis might mean:")
        print("  - The service account doesn't have necessary permissions")
        print("  - The key is invalid or expired")
        return False


def main():
    """Main execution function."""
    
    print("=" * 60)
    print("🔐 Service Account Key Test (from Secret Manager)")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Get credentials from Secret Manager
        credentials = get_credentials_from_secret_manager()
        
        # Step 2: Test the credentials
        test_credentials(credentials)
        
        print("\n" + "=" * 60)
        print("✅ Test Complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. You're authenticated: gcloud auth application-default login")
        print("  2. Secret Manager API is enabled")
        print("  3. Your user has permission to read secrets")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
