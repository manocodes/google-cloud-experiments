# Google Cloud Experiments

A Python project for experimenting with Google Cloud Platform features.

## Project Structure

google-cloud/
├── docs/                 # STUDY GUIDES (The core value)
│   ├── compute/          # GCE, GKE, Cloud Run, Functions
│   ├── databases/        # SQL, Spanner, Bigtable, Firestore
│   ├── networking/       # VPC, LB, Interconnect, Security
│   ├── storage/          # GCS, Block, Filestore, Transfer
│   ├── security/         # IAM, Org Policy, Hierarchy
│   └── general/          # Case Studies, Tips, Concepts
├── src/
│   └── experiments/      # Python code experiments
├── requirements.txt      # Dependencies
└── README.md             # This file


## Setup

### 1. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Google Cloud project details:
- `GOOGLE_CLOUD_PROJECT`: Your GCP project ID
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your service account key (optional if using default credentials)

### 4. Authenticate with Google Cloud

You can authenticate using one of these methods:

**Option A: Application Default Credentials (Recommended for local development)**
```bash
gcloud auth application-default login
```

**Option B: Service Account Key**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

## Available Google Cloud Services

This project includes dependencies for:
- **Cloud Storage**: File storage and retrieval
- **Firestore**: NoSQL database
- **Pub/Sub**: Messaging service
- **Cloud Run**: Serverless containers
- **Vertex AI**: Machine learning
- **Secret Manager**: Secure credential storage
- **Cloud Monitoring**: Metrics and monitoring
- **BigQuery**: Data warehouse and analytics

## Running Experiments

Create your experiment scripts in `src/experiments/`. For example:

```bash
python src/experiments/storage_example.py
```

## Testing

Run tests with pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src tests/
```

## Project Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
ruff check src/

# Format code
black src/ tests/
```

## Resources

- [Google Cloud Python Client Libraries](https://cloud.google.com/python/docs/reference)
- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Python Best Practices](https://google.github.io/styleguide/pyguide.html)
