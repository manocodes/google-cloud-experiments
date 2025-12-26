# PCA Security: Authentication (Users & Machines)

This guide covers everything related to **Authentication** ("Who are you?"), distinguishing between Human identities (Cloud Identity) and Machine identities (ADC/Workload Identity).

## 1. Human Authentication: Cloud Identity & SSO

Before we talk about code, we must understand how **Users** get into Google Cloud.

### Cloud Identity
Cloud Identity is the **IDaaS** (Identity as a Service) layer. It replaces the "Consumer Gmail" model with an Enterprise directory.
*   **Google Cloud Directory Sync (GCDS):**
    *   **Function:** Syncs users/groups from your on-prem Active Directory (LDAP) to Cloud Identity.
    *   **Direction:** **One-Way** (AD -> Google). It *never* writes back to AD.
    *   **Mechanism:** Runs as a scheduled task on a server in your network.
*   **Single Sign-On (SSO):**
    *   You delegate authentication to an external IdP (Identity Provider) like Azure AD (Entra ID), Okta, or Ping.
    *   User types email -> Redirected to Okta -> Logs in -> Redirected back with SAML Token.

### Best Practices (Exam):
*   **Super Admins:** Should *not* use SSO. Keep them purely in Cloud Identity for recovery (in case SSO breaks). Enforce strong 2SV (Hardware Keys/Titan Keys) on them.
*   **MFA/2SV:** Enforce at the Organization level in Cloud Identity.

---

## 2. Machine Authentication: Application Default Credentials (ADC)

**Application Default Credentials (ADC)** is a strategy used by Google Cloud client libraries to automatically find your credentials. It acts as a "Black Box" that abstracts away the complexity of authentication.

### The Search Order (Exam Critical)
When you initialize a client (e.g., `storage.Client()`), ADC checks for credentials in this specific order:

1.  **Environment Variable (`GOOGLE_APPLICATION_CREDENTIALS`):**
    *   Checks if this variable is set. If yes, it uses the key file or WIF config defined there.
2.  **Local User Credentials:**
    *   Checks if you authenticated locally via the gcloud CLI (`gcloud auth application-default login`).
3.  **Attached Service Account:**
    *   Checks the internal Metadata Server (if running on GCE, Cloud Run, Cloud Functions, GKE).

### Code Example
```python
# GOOD: The library automatically finds credentials using ADC strategies
from google.cloud import storage
client = storage.Client()
```
This single block of code works on your laptop (using your user creds) and in production (using the Service Account).

---

## 3. Workload Identity Federation (WIF)

**Workload Identity Federation** allows external workloads (running on AWS, Azure, GitHub Actions, or On-Prem) to impersonate a Google Cloud Service Account without managing long-lived Service Account Keys (JSON files).

### The Solution: "Keyless" Access
1.  **Trust Relationship:** You configure GCP to trust an external Identity Provider (like AWS IAM or GitHub OIDC).
2.  **Exchange:** The external workload sends its own token (e.g., AWS Role Token) to GCP STS (Security Token Service).
3.  **Access:** GCP validates it and swaps it for a short-lived Google Access Token.

---

## 4. Understanding Principals

In Google Cloud IAM, a **Principal** is the "Who".

| Principal Type | Best Use Case |
| :--- | :--- |
| **Google Account** | Specific person (`alice@gmail.com`). |
| **Service Account** | Application/VM (`my-app@project-id...`). |
| **Google Group** | Teams (`admins@example.com`). **Best Practice:** Always assign IAM roles to Groups, not individuals. |
| **Cloud Identity Domain** | Entire org (`domain:example.com`). |

---

## 5. Practical Implementation strategies

### The "Golden Rule" of GCP Auth
**Avoid managing long-lived Service Account Key files (JSON) whenever possible.**

| Environment | Preferred Method | Why? |
| :--- | :--- | :--- |
| **Local Laptop** | `gcloud auth application-default login` | Uses your User Identity. No keys to manage. |
| **GCP (Cloud Run/GCE)** | **Attached Service Account** | Metadata server handles rotation automatically. No files. |
| **External (AWS/Azure)** | **Workload Identity Federation** | Uses ephemeral tokens. No secrets. |
| **Legacy/On-Prem** | **Service Account Key (Last Resort)** | If OIDC/WIF is impossible. Risk of theft. |

---

## 6. Exam Scenarios & Cheat Sheet

1.  **Scenario:** "Code works on developer's laptop but fails in Cloud Run with 403 Forbidden."
    *   **Diagnosis:** The developer likely has permissions (Owner) that the Cloud Run Service Account (Default Compute) lacks.
    *   **Fix:** Grant the necessary IAM Role (e.g., `Storage Object Viewer`) to the **Cloud Run Service Account**.

2.  **Scenario:** "You need to access BigQuery from an application running in AWS."
    *   **Answer:** Configure **Workload Identity Federation**. Do NOT create a Service Account Key and copy it to AWS.

3.  **Scenario:** "You have Active Directory on-premise. You want users to use the same credentials for GCP."
    *   **Answer:** Setup **Google Cloud Directory Sync (GCDS)** to sync users, and configure **SSO** with your IdP.

4.  **Scenario:** "An application needs to authenticate as a user to access a spreadsheet."
    *   **Answer:** This is OAuth 2.0 (User Consent), not strictly ADC (Service Auth). But for the exam, distinctions focus heavily on **Service Accounts vs. User Accounts**.

5.  **Scenario:** "How to secure Super Admin accounts?"
    *   **Answer:** Do not sync them from AD. Keep them Cloud-only. Enforce Titan Security Keys.
