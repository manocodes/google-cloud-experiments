# PCA Security: Encryption & Key Management

This guide covers critical encryption concepts for the Professional Cloud Architect (PCA) exam, focusing on the decision-making process between different key management strategies.

## 1. Encryption Basics

By default, **Google Cloud encrypts all data at rest** (using AES-256: **Advanced Encryption Standard**) and **in transit** (using TLS: **Transport Layer Security**). You do not need to configure anything for this standard protection.

*   **Encryption at Rest:** Data is broken into chunks; each chunk is encrypted with a specific data key; data keys are wrapped by a master key (KEK).
*   **Encryption in Transit:** Data traveling between Google and the user (internet) or between Google data centers.

---

## 2. Key Management Logic (The Exam Decision Tree)

The exam will test your ability to choose the "right" encryption level based on compliance requirements and operational overhead.

| Strategy | Term | Who Manages the Key? | Where is the Key Stored? | Compliance/Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Default Encryption** | **Google-Managed Keys** | Google | Google KMS (Internal) | Standard use cases. No specific compliance requirements. Lowest operational overhead. |
| **CMEK** | **Customer-Managed Encryption Keys** | **YOU** (via Cloud KMS) | Google Cloud KMS | Customer requires control over key rotation, destruction, and location. Common for internal compliance. |
| **Cloud HSM** | **Hardware Security Module** | **YOU** | Google Cloud HSM (FIPS 140-2 Level 3) | Same as CMEK, but requires keys to be generated in hardware. Higher security standard. |
| **CSEK** | **Customer-Supplied Encryption Keys** | **YOU** | **On-Premise** (Google *never* stores the key permanently) | "Hold Your Own Key" (HYOK). Extreme trust issues. Google only holds the key in RAM while processing. If you lose the key, data is lost forever. |
| **EKM** | **External Key Manager** | External Vendor | Third-party Key Manager (e.g., Thales, Fortanix) | Keys stored outside of Google entirely. Used when regulations forbid keys from entering the cloud provider's infrastructure. |

### 🔍 Deep Dive: CMEK (Customer-Managed Encryption Keys)
*   **How it works:** You create a key in Cloud KMS. You grant a Google Service (like BigQuery or GCS) permission to Encrypt/Decrypt using that key.
*   **Key Rotation:** You can configure automatic rotation (e.g., every 90 days). Google handles the new version creation.
*   **Destruction:** If you destroy the key version, the data encrypted with it is **cryptographically shredded** (irretrievable).

### 🔍 Deep Dive: CSEK (Customer-Supplied Encryption Keys)
*   **How it works:** You generate the AES-256 key on your local machine. You verify it. You send it with your API request (e.g., `gsutil cp file.txt gs://bucket -o encryption_key:my-key`). 
*   **Limitations:** Not supported by all services. Adds significant management overhead (you must store the key safely).
*   **Exam Tip:** If a question asks for "complete control where Google cannot see the keys at rest," think CSEK or EKM.

---

## 3. Cloud KMS (Key Management Service)

Cloud KMS is the central service for managing cryptographic keys.

*   **Key Ring:** A logical group of keys (Organizational structure). Keys sit inside Key Rings. Key Rings sit inside **Locations** (Regions/Multi-regions).
    *   *Constraint:* You cannot move a Key Ring or Key to a different region after creation.
*   **Key Version:** The actual cryptographic material. Keys have multiple versions.
*   **Permissions:** Separation of duties is critical.
    *   `Cloud KMS Admin`: Can manage keys (create, rotate, destroy) but **cannot encrypt/decrypt**.
    *   `Cloud KMS CryptoKey Encrypter/Decrypter`: Can use the key to encrypt/decrypt data.

---

## 4. Secret Manager (vs. KMS)

CONFUSION ALERT: Do not confuse **Secret Manager** with **KMS**.

| Feature | **Cloud KMS** | **Secret Manager** |
| :--- | :--- | :--- |
| **Primary Use** | Encrypting **Data encryption keys** (DEKs) or large files. | Storing **API Keys, Passwords, Certificates, Database Strings**. |
| **Payload** | Handles encryption *operations*. | Handles storage of *small text/binary blobs*. |
| **Versioning** | Yes (Key Versions). | Yes (Secret Versions). |
| **Use Case** | "I need to encrypt my BigQuery Dataset." | "My application needs the database password at runtime." |

### Secret Manager Key Features for PCA:
*   **Versioning:** Allows you to rotate secrets (e.g., `latest` points to the new password).
*   **IAM Integration:** Control exactly *who* (Service Account) can access *which* secret.
*   **Regional Replication:** You can choose where to replicate secrets (Automatic/Global or User-Managed).

---

## 5. Signed URLs (Cloud Storage)

While not strictly "Encryption," this is often grouped in data security questions.
*   **Use Case:** Give temporary access to a private object without making the bucket public or creating a Google Account for the user.
*   **Mechanism:** Access is granted via a crytographic signature in the URL query string.
*   **Time-bound:** Valid for a specific duration (e.g., 15 minutes).
*   **Canonical Extension:** Signed **Policy Documents** allow uploads.

---

## 6. Exam Scenarios & Cheat Sheet

1.  **Requirement:** "Strict regulatory requirement that keys must be managed by the customer."
    *   **Answer:** CMEK using Cloud KMS.
    
2.  **Requirement:** "Keys must be stored in a dedicated hardware device validated to FIPS 140-2 Level 3."
    *   **Answer:** Cloud KMS with **Cloud HSM** backend.
    
3.  **Requirement:** "We don't trust Google with our keys at rest. We want to keep keys on-premises."
    *   **Answer:** CSEK (Customer-Supplied).
    
4.  **Requirement:** "Store database credentials and API keys securely with rotation."
    *   **Answer:** Secret Manager.
    
5.  **Requirement:** "An application needs to manipulate encrypted credit card data."
    *   **Answer:** Use Cloud KMS to encrypt the data field-level (Application Layer Encryption).
