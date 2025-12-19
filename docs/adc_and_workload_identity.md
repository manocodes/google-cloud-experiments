# Understanding Application Default Credentials (ADC), Workload Identity, and Principals

This document explains the core mechanisms Google Cloud uses to handle authentication ("Who are you?") and how modern strategies like Workload Identity Federation automate this process securely.

## 1. Application Default Credentials (ADC)

**Application Default Credentials (ADC)** is a strategy used by Google Cloud client libraries to automatically find your credentials. It acts as a "Black Box" that abstracts away the complexity of authentication, allowing you to write code that is portable across different environments.

### The "Black Box" Concept
1.  **Code In**: Your code simply initializes a client (e.g., `storage.Client()`).
2.  **Black Box (ADC)**: The library checks multiple potential locations for credentials.
3.  **Credentials Out**: The correct credentials are retrieved transparently.

### The Search Order
When you initialize a Google Cloud client, ADC checks for credentials in this specific order:

1.  **Environment Variable**: Checks `GOOGLE_APPLICATION_CREDENTIALS`. If set, it uses the file defined there (either a Service Account Key or a WIF Config).
2.  **Local User Credentials**: Checks if you authenticated locally via the gcloud CLI (`gcloud auth application-default login`).
3.  **Attached Service Account**: Checks the internal Metadata Server (if running on GCE, Cloud Run, Cloud Functions, GKE).

### Code Example

**The Wrong Way (Hardcoding):**
```python
# BAD: Hardcoding paths or keys makes code brittle and insecure
from google.cloud import storage
client = storage.Client.from_service_account_json('/path/to/my/key.json')
```

**The Right Way (ADC):**
```python
# GOOD: The library automatically finds credentials using ADC strategies
from google.cloud import storage
client = storage.Client()
```
This single block of code works on your laptop (using your user creds) and in production (using the Service Account).

---

## 2. Workload Identity Federation (WIF)

**Workload Identity Federation** allows external workloads (running on AWS, Azure, GitHub Actions, or On-Prem) to impersonate a Google Cloud Service Account without managing long-lived Service Account Keys (JSON files).

### The Problem with Keys
Historically, to let AWS talk to GCP, you had to:
1.  Download a long-lived Service Account JSON key.
2.  Copy it to AWS.
3.  Hope it doesn't get stolen.

### The Solution: WIF
WIF "hijacks" Step 1 of the ADC flow. Instead of pointing `GOOGLE_APPLICATION_CREDENTIALS` to a secret key, you point it to a **Configuration File**.

1.  **Trust Relationship**: You configure GCP to trust an external Identity Provider (like AWS IAM or GitHub OIDC).
2.  **No Secrets**: You download a JSON config file. This file contains **no secrets**; it simply describes *how* to exchange the external token for a Google token.
3.  **The Handshake**:
    *   Your code runs `storage.Client()`.
    *   ADC reads the config file.
    *   ADC grabs the *local* credential (e.g., the AWS role token).
    *   ADC sends the AWS token to GCP's Security Token Service (STS).
    *   GCP verifies the AWS token and returns a temporary Google Access Token.

---

## 3. Understanding Principals

In Google Cloud IAM (Identity and Access Management), a **Principal** (formerly "Member") is the "Who" requesting access to a resource. ADC is simply the mechanism used to *authenticate* as one of these principals.

### Common Types of Principals

| Principal Type | Description | Best Use Case |
| :--- | :--- | :--- |
| **Google Account** | A specific person (e.g., `alice@gmail.com`). | Human access, developers running `gcloud auth login`. |
| **Service Account** | A non-human account associated with an application or VM (e.g., `my-app@project-id.iam.gserviceaccount.com`). | Applications running inside GCP (Compute Engine, Cloud Run). |
| **Google Group** | A collection of Google Accounts and Service Accounts (e.g., `admins@example.com`). | Managing permissions for teams (Best Practice: Assign roles to Groups, not individuals). |
| **Cloud Identity Domain** | Represents all accounts in an organization (e.g., `domain:example.com`). | Granting broad, low-level access to everyone in the company. |
| **Workload Identity Pool Principal** | Represents an external identity (e.g., `principal://iam.googleapis.com/.../subject/repo:my-org/my-repo:ref:refs/heads/main`). | Granting access to a specific GitHub Action repo or AWS Role without using a Service Account Key. |

### How It Connects
*   **On your laptop**: ADC authenticates you as a **Google Account** principal.
*   **On Cloud Run**: ADC authenticates the app as a **Service Account** principal.
*   **On AWS (via WIF)**: ADC authenticates the external workload as a **Workload Identity User**, which then impersonates a Service Account.

---

## 4. Practical Implementation & The "Golden Rule"

### How to set `GOOGLE_APPLICATION_CREDENTIALS`
When you *must* use a file (Step 1 of ADC), you set this environment variable to the **absolute path** of the file.

```bash
# Temporary (Current Session)
export GOOGLE_APPLICATION_CREDENTIALS="/Users/JN9THQT/path/to/credentials.json"

# Permanent (Add to ~/.zshrc or ~/.bashrc)
echo 'export GOOGLE_APPLICATION_CREDENTIALS="/Users/JN9THQT/path/to/credentials.json"' >> ~/.zshrc
source ~/.zshrc
```

### The "File" Difference: Key vs. Config
The file you point to determines your security posture:
1.  **Service Account Key (JSON)**: Contains a PRIVATE KEY.
    *   **Risk**: 🚨 **High**. If stolen, the attacker IS the service account.
    *   **Use Case**: Legacy systems unable to use OIDC/WIF.
2.  **Workload Identity Config (JSON)**: Contains specific instruction mappings.
    *   **Risk**: ✅ **Low**. Contains no secrets. Only works if the runner also has a valid external identity (e.g., a valid AWS role).
    *   **Use Case**: AWS, Azure, On-Prem, GitHub Actions.

### The "Golden Rule" of GCP Auth
**Avoid managing files whenever possible.**

| Environment | Preferred Method | Why? |
| :--- | :--- | :--- |
| **Local Laptop** | `gcloud auth application-default login` | Uses your User Identity. No keys to manage. |
| **GCP (Cloud Run/GCE)** | **Attached Service Account** | Metadata server handles rotation automatically. No files. |
| **External (AWS/Azure)** | **Workload Identity Federation** | Uses ephemeral tokens. No long-lived secrets. |

**Only use `GOOGLE_APPLICATION_CREDENTIALS` pointing to a SA Link when you absolutely have to (e.g. legacy on-prem apps with no OIDC provider).**

