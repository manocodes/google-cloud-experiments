"""Example: Google Cloud Firestore operations."""

import os
from google.cloud import firestore
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()


def initialize_firestore():
    """Initialize and return a Firestore client."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
    
    return firestore.Client(project=project_id)


def add_document(collection_name: str, document_data: dict):
    """Add a document to a Firestore collection.
    
    Args:
        collection_name: Name of the collection
        document_data: Dictionary containing document data
    """
    db = initialize_firestore()
    doc_ref = db.collection(collection_name).add(document_data)
    print(f"Document added with ID: {doc_ref[1].id}")
    return doc_ref[1].id


def get_document(collection_name: str, document_id: str):
    """Retrieve a document from Firestore.
    
    Args:
        collection_name: Name of the collection
        document_id: ID of the document to retrieve
    """
    db = initialize_firestore()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    
    if doc.exists:
        print(f"Document data: {doc.to_dict()}")
        return doc.to_dict()
    else:
        print("Document does not exist")
        return None


def list_documents(collection_name: str):
    """List all documents in a collection.
    
    Args:
        collection_name: Name of the collection
    """
    db = initialize_firestore()
    docs = db.collection(collection_name).stream()
    
    print(f"Documents in collection '{collection_name}':")
    for doc in docs:
        print(f"  {doc.id} => {doc.to_dict()}")


def update_document(collection_name: str, document_id: str, updates: dict):
    """Update a document in Firestore.
    
    Args:
        collection_name: Name of the collection
        document_id: ID of the document to update
        updates: Dictionary containing fields to update
    """
    db = initialize_firestore()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.update(updates)
    print(f"Document {document_id} updated successfully")


def delete_document(collection_name: str, document_id: str):
    """Delete a document from Firestore.
    
    Args:
        collection_name: Name of the collection
        document_id: ID of the document to delete
    """
    db = initialize_firestore()
    db.collection(collection_name).document(document_id).delete()
    print(f"Document {document_id} deleted successfully")


if __name__ == "__main__":
    collection = os.getenv("FIRESTORE_COLLECTION", "experiments")
    
    try:
        # Example: Add a document
        doc_data = {
            "name": "Test Experiment",
            "description": "Testing Firestore operations",
            "timestamp": datetime.now(),
            "status": "active"
        }
        doc_id = add_document(collection, doc_data)
        
        # Example: Get the document
        get_document(collection, doc_id)
        
        # Example: List all documents
        list_documents(collection)
        
        # Example: Update the document
        # update_document(collection, doc_id, {"status": "completed"})
        
        # Example: Delete the document
        # delete_document(collection, doc_id)
        
    except Exception as e:
        print(f"Error: {e}")
