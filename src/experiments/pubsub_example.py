"""Example: Google Cloud Pub/Sub operations."""

import os
from google.cloud import pubsub_v1
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()


def publish_message(project_id: str, topic_name: str, message: str):
    """Publish a message to a Pub/Sub topic.
    
    Args:
        project_id: GCP project ID
        topic_name: Name of the Pub/Sub topic
        message: Message to publish
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    
    # Data must be a bytestring
    data = message.encode("utf-8")
    
    # Publish message
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    
    print(f"Published message ID: {message_id}")
    return message_id


def publish_with_attributes(project_id: str, topic_name: str, message: str, **attributes):
    """Publish a message with custom attributes to a Pub/Sub topic.
    
    Args:
        project_id: GCP project ID
        topic_name: Name of the Pub/Sub topic
        message: Message to publish
        **attributes: Additional message attributes
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    
    data = message.encode("utf-8")
    
    # Publish with attributes
    future = publisher.publish(topic_path, data, **attributes)
    message_id = future.result()
    
    print(f"Published message with attributes. ID: {message_id}")
    return message_id


def subscribe_messages(project_id: str, subscription_name: str, timeout: float = 5.0):
    """Subscribe to messages from a Pub/Sub subscription.
    
    Args:
        project_id: GCP project ID
        subscription_name: Name of the Pub/Sub subscription
        timeout: Time to listen for messages in seconds
    """
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    
    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        if message.attributes:
            print(f"Attributes: {dict(message.attributes)}")
        message.ack()
    
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...\n")
    
    # Listen for messages in a separate thread
    try:
        streaming_pull_future.result(timeout=timeout)
    except Exception as e:
        streaming_pull_future.cancel()
        print(f"Listening stopped: {e}")


def create_topic(project_id: str, topic_name: str):
    """Create a new Pub/Sub topic.
    
    Args:
        project_id: GCP project ID
        topic_name: Name for the new topic
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    
    try:
        topic = publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {topic.name}")
        return topic
    except Exception as e:
        print(f"Error creating topic: {e}")
        return None


def list_topics(project_id: str):
    """List all Pub/Sub topics in the project.
    
    Args:
        project_id: GCP project ID
    """
    publisher = pubsub_v1.PublisherClient()
    project_path = f"projects/{project_id}"
    
    print(f"Topics in project {project_id}:")
    for topic in publisher.list_topics(request={"project": project_path}):
        print(f"  - {topic.name}")


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_name = os.getenv("PUBSUB_TOPIC", "test-topic")
    subscription_name = os.getenv("PUBSUB_SUBSCRIPTION", "test-subscription")
    
    if not project_id:
        print("Error: GOOGLE_CLOUD_PROJECT environment variable not set")
        exit(1)
    
    try:
        # Example: List topics
        list_topics(project_id)
        
        # Example: Publish a message
        # publish_message(project_id, topic_name, "Hello from Pub/Sub!")
        
        # Example: Publish with attributes
        # publish_with_attributes(
        #     project_id,
        #     topic_name,
        #     "Message with metadata",
        #     origin="python-script",
        #     priority="high"
        # )
        
        # Example: Subscribe to messages
        # subscribe_messages(project_id, subscription_name, timeout=10.0)
        
    except Exception as e:
        print(f"Error: {e}")
