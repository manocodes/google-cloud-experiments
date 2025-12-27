# PCA Security: Security Command Center (SCC)

This guide focuses purely on **Security Command Center (SCC)**, Google Cloud's centralized vulnerability and threat detection service. For the PCA exam, you must know **when to use it**, **which tier to choose**, and **how to automate responses**.

## 1. Top-Level Concept: "Single Pane of Glass"
*   **What it is:** The central dashboard where you see *all* security assets, misconfigurations, and active threats across your **entire Organization**.
*   **Exam Trigger:** "You need centralized visibility into the security posture of all projects in the organization." -> **Enable SCC.**

---

## 2. Standard vs. Premium (The #1 Exam Topic)
The exam loves to test if you know what is Free vs. Paid.

### A. standard Tier (Free)
**Focus:** "Static Misconfigurations" (Did you configure it wrong?)
*   **Security Health Analytics (SHA) - Basic:** Checks for obvious bad settings.
    *   *Examples:* Public Storage Buckets, Open Firewall Ports (0.0.0.0/0), MFA not enforced, Legacy IAM roles used.
*   **Web Security Scanner (Custom Scan):** Limited scanning for public URLs.

**Exam Scenario (Standard):**
> "You need to ensure no storage buckets are publicly accessible and firewalls do not allow SSH from the internet." -> **SCC Standard.**

### B. Premium Tier (Paid)
**Focus:** "Active Threats" (Is someone hacking me right now?) & "Compliance".
*   **Event Threat Detection (ETD):** Analyzes *logs* (Cloud Logging) to find patterns.
    *   *Examples:* Brute Force SSH, Malicious Tor Exit Nodes, Cryptomining.
*   **Container Threat Detection (CTD):** Analyzes *runtime* container activity.
    *   *Examples:* Reverse shell opened inside a pod, malicious binary execution.
*   **Compliance Reports:** One-click reports for PCI-DSS, CIS Benchmarks, NIST, ISO 27001.

**Exam Scenario (Premium):**
> "You need to detect if any VM is being used for cryptocurrency mining." -> **SCC Premium.**
> "You need to verify compliance with PCI-DSS standards." -> **SCC Premium.**

---

## 3. Key Detection Services (Deep Dive)

| Service | Tier | What It Scans | Exam Keyword |
| :--- | :--- | :--- | :--- |
| **Security Health Analytics (SHA)** | Standard* | Configuration (Assets) | "Misconfiguration", "Public Bucket", "Open Port" |
| **Event Threat Detection (ETD)** | **Premium** | Logs (Network/Audit) | "Brute Force", "Malicious IP", "Cryptomining" |
| **Container Threat Detection (CTD)** | **Premium** | GKE Runtime | "Reverse Shell", "Malicious Binary in Pod" |
| **Web Security Scanner (WSS)** | Standard* | App URL (OWASP) | "XSS", "SQL Injection" (Scanner, not WAF) |
| **Rapid Vulnerability Detection** | **Premium** | OS/Software | "Zero-day vulnerability", "N-day patch missing" |

*\*Note: SHA and WSS have basic versions in Standard and advanced versions in Premium, but for the exam, usually map Misconfig -> Standard, Threats -> Premium.*

---

## 4. Automating Remediation (Exam Logic)
SCC just *detects* things. It doesn't fix them automatically unless you build it.

**The Architecture:**
1.  **Detect:** SCC finds a "Public Bucket."
2.  **Notify:** SCC publishes the finding to **Pub/Sub**.
3.  **Act:** A **Cloud Function** subscribes to the topic.
4.  **Remediate:** The Cloud Function runs a script to remove the `allUsers` IAM binding.

**Exam Scenario:**
> "You want to **automatically block** any SSH keys added to project-wide metadata."
> *   **Step 1:** SCC detects the change.
> *   **Step 2:** Export finding to Pub/Sub.
> *   **Step 3:** Trigger Cloud Function to revert the change.

---

## 5. Exam Decision Matrix

| Requirement | Solution |
| :--- | :--- |
| **"Identify misconfigured firewalls"** | **SCC Standard** (Security Health Analytics) |
| **"Detect active cryptomining"** | **SCC Premium** (Event Threat Detection) |
| **"Detect compromised GKE containers"** | **SCC Premium** (Container Threat Detection) |
| **"Prove PCI Compliance"** | **SCC Premium** (Compliance Dashboard) |
| **"Scan web app for XSS vulnerabilities"** | **Web Security Scanner** (in SCC) |
| **"Fix the issue automatically"** | SCC -> **Pub/Sub** -> **Cloud Function** |

---

## 6. Access & Organization
*   SCC is activated at the **Organization Level**.
*   You generally need the **Organization Admin** or **Security Center Admin** role to set it up.
*   Findings are aggregated at the Org level but can be viewed per project.
