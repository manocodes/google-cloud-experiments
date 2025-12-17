# Google Cloud Platform Concepts Summary

This document summarizes key Google Cloud Platform (GCP) concepts, tools, and best practices discussed.

## 1. Principals (Identity)
A **Principal** is the "Who" in IAM (Identity and Access Management). It represents an identity that can be granted access to a resource.

### Common Types
*   **Google Account**: A human user (e.g., `alice@gmail.com`).
*   **Service Account**: A non-human account for applications (e.g., `my-app@project.iam.gserviceaccount.com`). This is utilized in code to make authorized API calls.
*   **Google Group**: A collection of accounts (e.g., `admins@example.com`).
*   **Google Workspace Domain**: All users in an organization (`@company.com`).

## 2. IAM Role Types
Roles define "What" a principal can do. They are collections of permissions.

| Role Type | Managed By | Granularity | Description | Example |
| :--- | :--- | :--- | :--- | :--- |
| **Basic** (Primitive) | Google | Coarse | Legacy roles affecting the entire project. **Avoid in production.** | `Owner`, `Editor`, `Viewer` |
| **Predefined** | Google | Fine | Service-specific roles maintained by Google. Updates automatically when new features are added. | `Storage Object Viewer`, `Pub/Sub Editor` |
| **Custom** | You | Precise | User-defined list of permissions. Must be manually maintained. | `My Custom Audit Role` |

## 3. Cloud Shell vs. Cloud SDK
The distinction lies between the *environment* and the *toolset*.

| Feature | Cloud SDK | Cloud Shell |
| :--- | :--- | :--- |
| **Definition** | A **toolset** (CLI binaries) installed on your machine. | A **temporary VM** in the browser with tools pre-installed. |
| **Location** | Local (Your Mac/PC). | Remote (Google Cloud). |
| **Persistence** | Permanent (until uninstalled). | **Ephemeral**. VM resets after inactivity, but `$HOME` directory (`5GB`) is saved. |
| **Use Case** | Daily development, specialized workflows. | Quick fixes, testing without installation, emergency access. |

### Cloud Shell Ephemerality
*   **System Packages**: Installed via `sudo apt-get` are **lost** when the session ends.
*   **User Files**: Files in `$HOME` (and imports installed via `pip install --user`) are **saved**.

## 4. Coding: Client Libraries vs. Cloud SDK
How your code interacts with GCP.

| Method | Component | Target Audience | Usage |
| :--- | :--- | :--- | :--- |
| **Client Libraries** | `google-cloud-storage`, etc. | **Developers** (Code) | Implemented inside Python/Node/Java code to call APIs efficiently. |
| **Cloud SDK** | `gcloud`, `gsutil`, `bq` | **Operators** (CLI) | Used in terminal or shell scripts for management tasks. |
| **REST API** | `requests` | **Advanced** | Manual HTTP calls. Use only as a last resort. |

**Key Takeaway**: "SDK" usually refers to the CLI tools in GCP. For Python code, use **Client Libraries**.

## 5. Installation: Brew vs. Pip
Distinguishing system tools from project dependencies.

| Manager | Installs | Target | Example |
| :--- | :--- | :--- | :--- |
| **Homebrew** (`brew`) | **Binaries / Tools** | System-wide (Your Mac) | `brew install --cask google-cloud-sdk` (Installs `gcloud` CLI) |
| **Pip** (`pip`) | **Libraries** | Project / Virtual Env | `pip install google-cloud-storage` (Installs Python package) |

*   Use **Brew** to set up your environment (get the `gcloud` command).
*   Use **Pip** to set up your project (get `import google.cloud` capability).

## 6. Terraform & APIs
Terraform interacts with Google Cloud almost exclusively via the **REST API**.

*   **Mechanism**: Terraform acts as a wrapper that translates HCL code (e.g., `resource "google_storage_bucket"`) into HTTP REST calls (POST, GET, PUT, DELETE).
*   **Provider**: The `google` provider handles the translation and authentication.
*   **Why REST?**: Terraform's CRUD (Create, Read, Update, Delete) model maps perfectly to RESTful HTTP verbs.

## 7. gRPC vs. REST
Understanding the protocols underlying GCP services.

| Feature | REST (Traditional) | gRPC (Modern) |
| :--- | :--- | :--- |
| **Format** | **JSON** (Text-based, human-readable). | **Protobuf** (Binary, machine-readable). |
| **Efficiency** | Heavy. Requires parsing text. | Lightweight. 5-10x smaller payload. |
| **Transport** | HTTP/1.1 (One request at a time). | HTTP/2 (Multiplexed streaming). |
| **Use Case** | Management, Control Plane, Terraform. | High-volume data (Pub/Sub, Bigtable), internal Google communication. |

## 8. Google Cloud Marketplace
A digital storefront to find, deploy, and manage third-party software and Google-built solutions on GCP.

### Key Benefits (Why use it?)
1.  **Speed**: Deploys complex stacks (like LAMP or Deep Learning environments) in minutes with pre-configured settings.
2.  **Consolidated Billing**: Third-party costs (e.g., MongoDB, Gitlab) appear on your single Google Cloud invoice.
3.  **Simplicity**: Avoids "Driver Hell" or dependency conflicts. Images come with compatible Drivers/OS/Libraries pre-installed.
4.  **Trust**: Images are security-scanned and vetted by Google.

### Types of Solutions
*   **Virtual Machine (IaaS) Solutions**:
    *   **What you get**: A raw VM with software pre-installed (e.g., "WordPress by Bitnami", "Deep Learning VM").
    *   **Your Responsibility**: You have full root access but must maintain the OS (updates, patches).
*   **SaaS / Managed Services**:
    *   **What you get**: Access to a fully managed platform (e.g., "MongoDB Atlas", "Redis Enterprise").
    *   **Your Responsibility**: You just use the data/app. The vendor manages reliability, backups, and OS pathcing.

### Marketplace vs. Workspace
*   **Google Cloud Marketplace**: For **Developers/Ops** building apps (databases, dev tools, security appliances).
*   **Google Workspace Marketplace**: For **End Users** enhancing productivity (DocuSign for Gmail, Trello for Sheets).

## 9. Cloud Emulators
Emulators allow you to run "fake" versions of Google Cloud services locally (Bigtable, Pub/Sub, Firestore) without internet or cost.

### Why use them?
1.  **Cost**: Avoids the high minimum cost of services like **Bigtable** (~$0.65/hour) during testing.
2.  **Speed**: Instant startup (milliseconds) vs. Cloud provisioning (minutes).
3.  **Safety**: Experiment with destructive actions (deleting tables) without risking production data.

### How it works
You do not need to change your code. You only change the **environment**.
1.  **Start Emulator**: `gcloud beta emulators bigtable start` (Runs on localhost).
2.  **Set Env Variable**: `export BIGTABLE_EMULATOR_HOST=localhost:8086`.
3.  **Run Code**: The Google Client Libraries detect the variable and redirect traffic to localhost.
4.  **Deploy to Prod**: Simply **unset** the variable. The code defaults back to real Google Cloud.
