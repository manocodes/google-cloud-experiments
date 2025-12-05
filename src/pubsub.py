from google.cloud import pubsub_v1
from google.api_core import exceptions
import os
from dotenv import load_dotenv

load_dotenv()   

try:
    publisher = pubsub_v1.PublisherClient() #this is publisher too
    subscriber = pubsub_v1.SubscriberClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    project_path = f"projects/{project_id}"
except Exception as e:
    print(f"\n❌ Error creating client: {e}")
    exit()

def display_Project():
    print(f"\n✅ Project: {project_id}")

display_Project()

def list_all_topics():
    display_Project()
    """List all PubSub topics"""
    try:
        
        print("\n" + "="*80)
        print("PUBSUB TOPICS LIST")
        print("="*80)
        
        topics = publisher.list_topics(request={"project": project_path})
        
        topic_count = 0
        for topic in topics:
            topic_count += 1
            print(f"\n{topic_count}. Topic ID: {topic.name}")
            print("-" * 80)
        
        if topic_count == 0:
            print("\nNo topics found.")
            print("Make sure you have the 'pubsub.topics.list' permission.")
        else:
            print(f"\nTotal Topics Found: {topic_count}")
        
        print("="*80)
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'pubsub.topics.list' permission")
    except Exception as e:
        print(f"\n❌ Error listing topics: {e}")

def list_subscriptions(topic_id):
    display_Project()
    """List all subscriptions (for a given topic)"""

    try:
        if topic_id:
            topic_path = f"{project_path}/topics/{topic_id}"
            print("\n" + "="*80)
            print(f"SUBSCRIPTIONS FOR TOPIC: {topic_id}")
            print("="*80)
            subscriptions = publisher.list_topic_subscriptions(request={"topic": topic_path})
        else:
            topic_path = f"{project_path}"
            print("\n" + "="*80)
            print(f"SUBSCRIPTIONS FOR PROJECT: {project_id}")
            print("="*80)   
            subscriptions = subscriber.list_subscriptions(request={"project": project_path})

        subscription_count = 0
        for subscription in subscriptions:
            subscription_count += 1
            print(f"\n{subscription_count}. Subscription ID: {subscription}")
            print("-" * 80)
        
        if subscription_count == 0:
            print("\nNo subscriptions found for topic.")
            print("Make sure you have the 'pubsub.subscriptions.list' permission.")
        else:
            print(f"\nTotal Subscriptions Found: {subscription_count}")
        
        print("="*80)
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'pubsub.subscriptions.list' permission")
    except Exception as e:
        print(f"\n❌ Error listing subscriptions: {e}")

def create_topic(topic_name):
    display_Project()
    """Create a new PubSub topic"""
    try:
        topic_path = f"projects/{project_id}/topics/{topic_name}"
        
        topic = publisher.create_topic(request={"name": topic_path})
        
        print(f"\n✅ Topic '{topic_name}' created successfully")
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'pubsub.topics.create' permission")
    except exceptions.AlreadyExists as e:
        print(f"\n❌ Topic '{topic_name}' already exists")
    except Exception as e:
        print(f"\n❌ Error creating topic: {e}")

def create_subscription(topic_name, subscription_name):
    display_Project()
    """Create a new PubSub subscription"""
    try:
        topic_path = f"projects/{project_id}/topics/{topic_name}"
        subscription_path = f"projects/{project_id}/subscriptions/{subscription_name}"
        
        subscription = subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
        
        print(f"\n✅ Subscription '{subscription_name}' created successfully")
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'pubsub.subscriptions.create' permission")
    except exceptions.NotFound as e:
        print(f"\n❌ Topic '{topic_name}' not found")
    except exceptions.AlreadyExists as e:
        print(f"\n❌ Subscription '{subscription_name}' already exists")
    except Exception as e:
        print(f"\n❌ Error creating subscription: {e}")     

def delete_topic(topic_name):
    display_Project()
    """Delete a PubSub topic"""
    try:
        topic_path = f"projects/{project_id}/topics/{topic_name}"
        
        publisher.delete_topic(request={"topic": topic_path})
        
        print(f"\n✅ Topic '{topic_name}' deleted successfully")
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'pubsub.topics.delete' permission")
    except exceptions.NotFound as e:
        print(f"\n❌ Topic '{topic_name}' not found")
    except Exception as e:
        print(f"\n❌ Error deleting topic: {e}")

def delete_subscription(subscription_name):
    display_Project()
    """Delete a PubSub subscription"""
    try:
        subscription_path = f"projects/{project_id}/subscriptions/{subscription_name}"
        
        subscriber.delete_subscription(request={"subscription": subscription_path})
        
        print(f"\n✅ Subscription '{subscription_name}' deleted successfully")
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'pubsub.subscriptions.delete' permission")
    except exceptions.NotFound as e:
        print(f"\n❌ Subscription '{subscription_name}' not found")
    except Exception as e:
        print(f"\n❌ Error deleting subscription: {e}")

def main_menu():
    """Interactive menu for PubSub operations"""
    while True:
        print("\n" + "="*60)
        print("PUBSUB MENU")
        print("="*60)
        print("1. List all topics")
        print("2. List all subscriptions")
        print("3. Create a topic")
        print("4. Create a subscription")
        print("5. Delete a topic")
        print("6. Delete a subscription")
        print("7. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\n📋 Listing all topics...")
            list_all_topics()
        elif choice == "2":
            topic_id = input("\nEnter Topic ID: (Keep empty for all subscription) ").strip()
            list_subscriptions(topic_id)
        elif choice == "3":
            topic_name = input("\nEnter Topic Name: ").strip()
            if topic_name:
                create_topic(topic_name)
            else:
                print("❌ Topic name cannot be empty")
        elif choice == "4":
            topic_name = input("\nEnter Topic Name: ").strip()
            subscription_name = input("\nEnter Subscription Name: ").strip()

            if topic_name and subscription_name:
                create_subscription(topic_name, subscription_name)
            else:
                print("❌ Topic name and Subscription name cannot be empty")
        elif choice == "5":
            topic_name = input("\nEnter Topic Name: ").strip()
            if topic_name:
                delete_topic(topic_name)
            else:
                print("❌ Topic name cannot be empty")
        elif choice == "6":
            subscription_name = input("\nEnter Subscription Name: ").strip()

            if subscription_name:
                delete_subscription(subscription_name)
            else:
                print("❌ Subscription name cannot be empty")
        elif choice == "7":
            print("\n👋 Exiting...")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main_menu()