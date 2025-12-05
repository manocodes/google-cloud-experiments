"""Configuration management for different environments."""

import os
from dotenv import load_dotenv
from pathlib import Path


def load_environment(env: str = None):
    """Load environment variables from .env files.
    
    Args:
        env: Environment name (development, staging, production).
             If None, uses ENV environment variable or defaults to 'development'.
    
    Priority (later overrides earlier):
        1. .env (base configuration)
        2. .env.{environment} (environment-specific)
        3. .env.local (local overrides, gitignored)
    """
    if env is None:
        env = os.getenv('ENV', 'development')
    
    project_root = Path(__file__).parent.parent
    
    # Load base .env file
    base_env = project_root / '.env'
    if base_env.exists():
        load_dotenv(base_env)
        print(f"✓ Loaded {base_env}")
    
    # Load environment-specific file
    env_file = project_root / f'.env.{env}'
    if env_file.exists():
        load_dotenv(env_file, override=True)
        print(f"✓ Loaded {env_file}")
    
    # Load local overrides
    local_env = project_root / '.env.local'
    if local_env.exists():
        load_dotenv(local_env, override=True)
        print(f"✓ Loaded {local_env}")
    
    return env


def get_config():
    """Get current configuration as a dictionary."""
    return {
        'project_id': os.getenv('GOOGLE_CLOUD_PROJECT'),
        'gcs_bucket': os.getenv('GCS_BUCKET_NAME'),
        'firestore_collection': os.getenv('FIRESTORE_COLLECTION'),
        'pubsub_topic': os.getenv('PUBSUB_TOPIC'),
        'pubsub_subscription': os.getenv('PUBSUB_SUBSCRIPTION'),
        'bigquery_dataset': os.getenv('BIGQUERY_DATASET'),
        'bigquery_table': os.getenv('BIGQUERY_TABLE'),
    }


def print_config():
    """Print current configuration (useful for debugging)."""
    config = get_config()
    print("\n📋 Current Configuration:")
    print("=" * 50)
    for key, value in config.items():
        # Mask sensitive values partially
        if value and len(value) > 10:
            masked = f"{value[:5]}...{value[-3:]}"
        else:
            masked = value
        print(f"  {key:25} = {masked}")
    print("=" * 50)


if __name__ == "__main__":
    # Test the configuration loader
    import sys
    
    env = sys.argv[1] if len(sys.argv) > 1 else None
    current_env = load_environment(env)
    print(f"\n🌍 Environment: {current_env}")
    print_config()
