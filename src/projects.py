"""
GCP Projects Management Script
Lists and manages Google Cloud Platform projects
"""
from google.cloud import resourcemanager_v3
from google.api_core import exceptions
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def list_all_projects():
    """List all GCP projects accessible to the authenticated user"""
    try:
        # Create a client
        client = resourcemanager_v3.ProjectsClient()
        
        print("\n" + "="*80)
        print("GCP PROJECTS LIST")
        print("="*80)
        
        # Search for all projects (doesn't require parent parameter)
        # Use query="state:ACTIVE" to only show active projects, or "" for all
        request = resourcemanager_v3.SearchProjectsRequest(
            query="state:ACTIVE"  # Change to "" to include deleted projects
        )
        projects = client.search_projects(request=request)
        
        project_count = 0
        for project in projects:
            project_count += 1
            print(f"\n{project_count}. Project ID: {project.project_id}")
            print(f"   Name: {project.display_name}")
            print(f"   State: {project.state.name}")
            if project.parent:
                print(f"   Parent: {project.parent}")
            print(f"   Created: {project.create_time}")
            print("-" * 80)
        
        if project_count == 0:
            print("\nNo projects found.")
            print("Make sure you have the 'resourcemanager.projects.get' permission.")
        else:
            print(f"\nTotal Projects Found: {project_count}")
        
        print("="*80)
        
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
        print("Make sure your service account has 'resourcemanager.projects.get' permission")
    except Exception as e:
        print(f"\n❌ Error listing projects: {e}")
        print("\nTip: The 'invalid parent name' error usually means you need to use")
        print("search_projects() instead of list_projects(), or specify a valid parent.")

def get_project_details(project_id):
    """Get detailed information about a specific project"""
    try:
        client = resourcemanager_v3.ProjectsClient()
        
        # Get project details
        name = f"projects/{project_id}"
        project = client.get_project(name=name)
        
        print("\n" + "="*80)
        print(f"PROJECT DETAILS: {project_id}")
        print("="*80)
        print(f"Display Name: {project.display_name}")
        print(f"Project ID: {project.project_id}")
        print(f"Project Number: {project.name.split('/')[-1]}")
        print(f"State: {project.state.name}")
        print(f"Created: {project.create_time}")
        print(f"Updated: {project.update_time}")
        if project.parent:
            print(f"Parent: {project.parent}")
        if project.labels:
            print("\nLabels:")
            for key, value in project.labels.items():
                print(f"  {key}: {value}")
        print("="*80)
        
    except exceptions.NotFound:
        print(f"\n❌ Project '{project_id}' not found")
    except exceptions.PermissionDenied as e:
        print(f"\n❌ Permission Denied: {e}")
    except Exception as e:
        print(f"\n❌ Error getting project details: {e}")


def search_projects(query):
    """Search for projects by name or ID"""
    try:
        client = resourcemanager_v3.ProjectsClient()
        
        print("\n" + "="*80)
        print(f"SEARCHING PROJECTS: '{query}'")
        print("="*80)
        
        # Use search_projects with a query filter
        # Query format: "displayName:*query* OR projectId:*query*"
        search_query = f"(displayName:{query}* OR id:{query}*) AND state:ACTIVE"
        request = resourcemanager_v3.SearchProjectsRequest(query=search_query)
        projects = client.search_projects(request=request)
        
        results = list(projects)
        
        if results:
            for idx, project in enumerate(results, 1):
                print(f"\n{idx}. Project ID: {project.project_id}")
                print(f"   Name: {project.display_name}")
                print(f"   State: {project.state.name}")
                print("-" * 80)
            print(f"\nFound {len(results)} matching project(s)")
        else:
            print(f"\nNo projects found matching '{query}'")
        
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error searching projects: {e}")


def main_menu():
    """Interactive menu for GCP project operations"""
    while True:
        print("\n" + "="*60)
        print("GCP PROJECTS MENU")
        print("="*60)
        print("1. List all projects")
        print("2. Get project details")
        print("3. Search projects")
        print("4. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            print("\n📋 Listing all projects...")
            list_all_projects()
        elif choice == "2":
            project_id = input("\nEnter Project ID: ").strip()
            if project_id:
                get_project_details(project_id)
            else:
                print("❌ Project ID cannot be empty")
        elif choice == "3":
            query = input("\nEnter search query (project ID or name): ").strip()
            if query:
                search_projects(query)
            else:
                print("❌ Search query cannot be empty")
        elif choice == "4":
            print("\n👋 Exiting...")
            break
        else:
            print("\n❌ Invalid choice! Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main_menu()