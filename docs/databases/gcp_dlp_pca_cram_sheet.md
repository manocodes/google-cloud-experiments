# Cloud DLP (Data Loss Prevention) for PCA

## Fundamentals
- **Service Type**: Fully managed service to inspect, classify, and de-identify sensitive data (PII).
- **Scope**: Can scan data in **Cloud Storage**, **BigQuery**, **Datastore** (Firestore), and even streams via API.
- **Key Function**: "Discover, Classify, Protect".

## Critical Concepts
1.  **InfoTypes**:
    *   Pre-defined detectors (Credit Card, SSN, Email, Passport).
    *   Custom InfoTypes (Regex, Dictionary).
    *   **Image Inspection**: Can use OCR to find sensitive text in images.
2.  **Inspection**:
    *   **Sampling**: Scan 100% or a random sample (cheaper).
    *   **Triggers**: Schedule periodic scans or trigger on new data upload (via Cloud Functions).
3.  **De-identification (Redaction)**:
    *   **Redaction**: Blacking out the value completely.
    *   **Masking**: `****-****-****-1234`.
    *   **Tokenization (Format Preserving Encryption)**: Replaces data with a token that looks like the original (same length/format) but is encrypted. *Reversible* if you have the key.
    *   **Bucketing**: Converting specific ages (24, 25, 27) to ranges (20-30).

## Exam Scenarios & Integration
-   **BigQuery Integration**:
    *   Scenario: "Analysts need to query dataset X, but it contains SSNs. They must NOT see the SSNs."
    *   Solution: Use DLP to scan and create a *sanitized copy* of the table? **NO**.
    *   Better Solution: Use **Policy Tags** (Column-level security) based on DLP classification. Or use a DLP pipeline (Dataflow) to de-identify data *before* it lands in BQ.
-   **Cloud Storage**:
    *   Scenario: "Before uploading files to a public bucket, ensure no PII."
    *   Solution: Automate a Cloud Function triggers on upload -> Calls DLP API -> If PII found, move to Quarantine Bucket.

## Traps & "Gotchas"
1.  **Performance/Cost**: Scanning petabytes of text is expensive and slow. Don't simply "Turn on DLP for everything". Use **Sampling** or scan only untrusted ingress points.
2.  **reversible vs irreversible**:
    *   **Hashing/Redaction**: Irreversible (One-way).
    *   **Tokenization/Crypto-hashing**: Reversible (if you manage the keys). Use this if the business app needs to retrieve the original email later.

## Templates
-   **Inspection Template**: Save your config of "What InfoTypes to look for" (e.g., "MyCompany_PII_Standard").
-   **De-identification Template**: Save your config of "How to mask it".
-   *Tip*: Using templates decouple configuration from code.
