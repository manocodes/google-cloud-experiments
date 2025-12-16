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
