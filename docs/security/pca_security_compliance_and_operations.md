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
    *   **Container Threat Detection:** Detects attacks inside GKE.
    *   **Compliance Monitoring:** Checks against PCI, CIS Benchmarks, NIST.

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

### Exam Scenarios
*   "You need to upload logs to BigQuery but they contain PII (Email addresses). The analytics team needs to query the logs but shouldn't see expenses." -> **Use DLP API to redact/mask PII before ingestion.**
*   "You need to scan an existing storage bucket for credit card numbers." -> **Create a DLP Inspection Job.**

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
*   **Aggregated Sinks:** Use specific "Log Router Sinks" to export logs from all projects to a centralized BigQuery dataset or Storage Bucket for long-term retention + compliance analysis.
*   **Immutability:** Use "Bucket Lock" (Retention Policy) on the log bucket to ensure logs cannot be deleted for X years (WORM compliance).

---

## 4. Compliance Standards (General Awareness)

You don't need to be a lawyer, but know which architectures fit which compliance:
*   **PCI-DSS (Payment Card Industry):** Requires strict scope isolation. Use **VPC Service Controls** and a separate project for PCI data. Tokenize credit card numbers (DLP).
*   **HIPAA (Health):** Requires BAA (Business Associate Agreement). Most GCP services are HIPAA compliant *if configured correctly* (Encryption, Access Control).
*   **GDPR (Europe Privacy):** Data Residency. Use **Regional** resources (e.g., `europe-west1`) instead of Global/Multi-region if residence is mandated.
*   **SOX (Financial):** Heavy emphasis on Audit Logs and separation of duties.
