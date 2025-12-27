# PCA Security: Compliance & Operations

This guide covers monitoring, logging, and compliance services tailored for the Cloud Architect exam.

## 1. Cloud Security Command Center (SCC)

SCC is the centralized dashboard for security and risk management. It gives you a "single pane of glass" view.

### Tiers (Exam Distinction)
1.  **Standard Tier (Free):**
    *   **Security Health Analytics:** Detects common misconfigurations (e.g., "Public bucket found", "Firewall port 22 open").
    *   **Web Security Scanner (Custom Scan):** Limited.
2.  **Premium Tier (Paid):**
    *   **Event Threat Detection:** Uses logs to find threats (e.g., "Brute force SSH", "Cryptomining detected").
        > **Definition: Brute Force SSH:** An attacker uses a bot to try thousands of passwords per second (e.g., `admin/1234`, `root/password`) against your VM's Port 22 hoping to guess the login.
    *   **Container Threat Detection:** Detects attacks inside GKE.
    *   **Compliance Monitoring:** Checks against PCI, CIS Benchmarks, NIST.
        > *   **PCI (Payment Card Industry):** Standard for handling credit cards.
        > *   **CIS (Center for Internet Security):** Best-practice technical checklists (e.g., "Don't use port 80").
        > *   **NIST (National Institute of Standards and Technology):** US Gov security framework (very rigorous).
        > *   **ISO 27001:** International standard for Information Security Management.

### Key Capabilities
*   **Asset Discovery:** Automatically inventories all assets across the Org.
*   **Vulnerability Assessment:** Finds software flaws.
*   **Threat Detection:** Finds active attacks.

---

## 2. Cloud Data Loss Prevention (DLP)

Cloud DLP is a fully managed service designed to discover, classify, and protect sensitive data.

### Core Functions
1.  **Inspection (Discovery):** Scans Datastore, BigQuery, GCS, or generic text streams.
    *   Uses **InfoTypes** (e.g., `US_SOCIAL_SECURITY_NUMBER`, `CREDIT_CARD_NUMBER`).
    *   Supports custom InfoTypes (Regex/Dictionaries).
2.  **De-identification (Redaction):**
    *   **Masking:** `****-****-****-1234`
    *   **Replacement:** `[CREDIT_CARD]`
    *   **Tokenization (Format Preserving Encryption):** Replaces sensitive data with a token that preserves the format/length but hides real data. *Reversible* if you have the key.

### 3. DLP Advanced Use Cases & Automation (Exam Critical)

DLP is not just about "scanning." The exam tests how you integrate it into a real-time pipeline.

**A. Automating De-identification (Ingestion Pipeline)**
*   **Scenario:** You receive files containing PII (names, emails) but your analytics team must NOT see PII.
*   **Solution:** Use **Pub/Sub** + **Cloud Functions** + **DLP API**.
    1.  File lands in `Ingest-Bucket`.
    2.  `ObjectFinalize` event triggers **Cloud Function**.
    3.  Function calls **DLP API** to mask/tokenize PII.
    4.  Clean data is written to `Clean-Bucket` (or BigQuery).

**B. Separation of Duties (Re-Identification)**
*   **Scenario:** Data is tokenized (e.g., Credit Card `1234` -> `Token_XYZ`). The Analytics team sees `Token_XYZ`. Occasionally, a "Fraud Analyst" needs to see the real number.
*   **Solution:**
    *   **Tokens:** Use "Format Preserving Encryption" with a specific key.
    *   **Access:** Only the Fraud Analyst has the **KMS Key** to *decrypt* (re-identify) the token. The Analytics team does not.

**C. Notification & Alerting**
*   **Scenario:** You need to be alerted *immediately* if a developer uploads a file with >100 Credit Card numbers to a public bucket.
*   **Solution:**
    1.  Create a **DLP Job Trigger**.
    2.  Configure "Actions" -> **Publish to Pub/Sub**.
    3.  Connect Pub/Sub to **Cloud Functions** (to quarantine the file) or **Email/Slack** (to alert Security Team).

**D. Real-time (Content API) vs. Storage (Storage API)**
*   **Content API:** For streaming data or "on the fly" masking (e.g., user types into a chat window -> mask before saving).
*   **Storage API:** For scanning *static* data already sitting in BigQuery, GCS, or Datastore (batch jobs).

---

## 3. Cloud Audit Logs

Google Cloud automatically generates audit logs for activities.

### Types of Audit Logs
1.  **Admin Activity:**
    *   **What:** "Metadata" changes. (e.g., Create VM, Delete Bucket, Set IAM Policy).
    *   **Cost:** Free.
    *   **Retention:** 400 Days.
    *   **Enabled:** Always ON.
2.  **Data Access:**
    *   **What:** "Reading/Writing" data (e.g., `GetObject`, `Select *`).
    *   **Cost:** Paid (High Volume!).
    *   **Retention:** 30 Days.
    *   **Enabled:** OFF by default (except for BigQuery). Must be explicitly enabled.
3.  **System Event:**
    *   **What:** Google-initiated events (e.g., Live Migration).
4.  **Policy Denied:**
    *   **What:** Records when a user was blocked by VPC Service Controls or other policies.

### Best Practice: Log Sinks
> **Definition: Log Sink (Router):** A rule that says "If a log matches X, send a copy to Y." It allows you to export logs out of the temporary Logging buffer into long-term storage (BigQuery/GCS/PubSub).
*   **Aggregated Sinks:** Use specific "Log Router Sinks" to export logs from all projects to a centralized BigQuery dataset or Storage Bucket for long-term retention + compliance analysis.
*   **Immutability:** Use "Bucket Lock" (Retention Policy) on the log bucket to ensure logs cannot be deleted for X years (WORM compliance).

---

## 4. Compliance Standards (General Awareness)

You don't need to be a lawyer, but know which architectures fit which compliance:
*   **PCI-DSS (Payment Card Industry):** Requires strict scope isolation. Use **VPC Service Controls** and a separate project for PCI data. Tokenize credit card numbers (DLP).
*   **HIPAA (Health):** Requires BAA (Business Associate Agreement). Most GCP services are HIPAA compliant *if configured correctly* (Encryption, Access Control).
*   **GDPR (Europe Privacy):** Data Residency. Use **Regional** resources (e.g., `europe-west1`) instead of Global/Multi-region if residence is mandated.
*   **SOX (Financial):** Heavy emphasis on Audit Logs and separation of duties.

---

## 5. Advanced Compliance Features

### Access Approval (Transparency)
*   **Problem:** Occasionally, Google Support Engineers need to look at your detailed configuration or data to fix a support ticket.
*   **Solution:** Access Approval requires them to request **explicit approval** (via email/Time-based) from YOU before they can touch anything.
*   **Exam Trigger:** "Regulatory requirement that the cloud provider must not access data without customer consent."

### Binary Authorization (Supply Chain Security)
*   **Context:** GKE / Cloud Run.
*   **Function:** Ensures only **Trusted Container Images** are deployed.
*   **Mechanism:**
    1.  CI/CD pipeline builds image -> Vulnerability Scan passes -> "Attestor" signs the image.
    2.  GKE tries to pull image.
    3.  Binary Auth checks signature. If missing -> **BLOCK**.
*   **Exam Trigger:** "Prevent untrusted/unscanned code from running in production."

### Shielded VMs (Integrity)
*   **Function:** Verifies the integrity of the boot sequence (Firmware -> Bootloader -> Kernel).
*   **Components:**
    *   **Secure Boot:** Signs the kernel.
    *   **vTPM:** Virtual Trusted Platform Module (stores secrets/keys).
    *   **Integrity Monitoring:** Alerts if the boot baseline changes (Rootkit detection).
*   **Exam Trigger:** "Ensure host has not been compromised by a rootkit/boot-virus."
