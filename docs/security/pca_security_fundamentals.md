# PCA Security: Fundamentals

This guide covers the foundational security philosophies and models relevant to the Google Cloud Architect exam.

## 1. Shared Responsibility Model

The industry-standard model that defines the security boundary between Google and the Customer.

*   **Google:** Responsible for Security **OF** the Cloud.
    *   (Physical hardware, Data Centers, Global Network, Hypervisor).
*   **Customer:** Responsible for Security **IN** the Cloud.
    *   (Customer Data, IAM, Firewall Rules, Application Logic).

### The Sliding Scale (Exam Critical)
The most important aspect of this model for the exam is how the line moves depending on the compute service type.

| Service Model | Google Cloud Service | Google Responsibilities | Customer Responsibilities |
| :--- | :--- | :--- | :--- |
| **IaaS** | Compute Engine (GCE), GKE (Standard Nodes) | Hardware, Network, Physical Security. | **Operating System (Patching)**, Network Firewalls, App Code, Data, Identity. |
| **PaaS** | App Engine, Cloud Run, GKE Autopilot | Hardware, Network, **Operating System**, **Runtime**. | **Application Code**, Data, Identity. |
| **SaaS/Managed** | BigQuery, Cloud Storage, Workspace | Everything up to the Application layer. | **Data**, **Access Policies (IAM)**, Configuration. |

**Exam Trap:**
*   **Scenario:** A security vulnerability is discovered in the Linux kernel.
*   **If GCE:** YOU must patch it.
*   **If Cloud Run/App Engine:** GOOGLE patches it.

---

## 2. Shared Fate

Shared Fate is Google's evolved, proactive version of Shared Responsibility.

*   **Philosophy:** "It's not just your problem; we actively help you prevent issues."
*   **Components:**
    1.  **Active Assistance:** Tools like **IAM Recommender** ("You gave this user too much power, remove it") and **Security Command Center** proactively warn you of risks.
    2.  **Secure Blueprints:** Google provides "Secure by Default" Terraform templates (Google Cloud Foundation Toolkit) so you don't start from scratch.
    3.  **Risk Protection:** Programs connecting security posture with cyber insurance.

---

## 3. Core Security Principles

These are the philosophical "laws" that should guide every architecture decision on the exam.

### A. Principle of Least Privilege (PoLP)
*   **Definition:** identities (users, service accounts) should have *only* the permissions necessary to do their job, and nothing more.
*   **The "Why":** Minimizes the "Blast Radius" if credentials are compromised.
*   **Exam Implementation:**
    *   **Avoid Basic Roles** (Owner/Editor/Viewer) unless absolutely necessary (or for small POCs).
    *   **Use Predefined Roles** (e.g., `roles/storage.objectViewer`) that are granular.
    *   **Use Custom Roles** if even Predefined Roles are too broad.
    *   **Service Accounts:** Create dedicated Service Accounts for each application (don't use the default Compute Engine SA for everything).

### B. Separation of Duties (SoD)
*   **Definition:** Critical actions should be divided among multiple people or systems so that no single individual can compromise the whole system.
*   **The "Why":** Prevents fraud and error.
*   **Exam Implementation:**
    *   The person who **writes** the code should not be the same person who **deploys** it to production.
    *   **Auditors** (Security Team) should have `roles/logging.viewer` or `roles/iam.securityReviewer`, but **NO** write/edit permissions.

### C. Zero Trust (BeyondCorp)
*   **Definition:** "Never trust, always verify." Do not trust a request just because it comes from inside your corporate network (VPN).
*   **The "Why":** The network perimeter is porous. Attackers might already be inside.
*   **Exam Implementation:**
    *   **Identity-Aware Proxy (IAP):** Shift access checks from the network level (VPN) to the user identity level.
    *   Every request is authenticated, authorized, and encrypted, regardless of where it comes from.

### D. Security by Design ("Shift Left")
*   **Definition:** Security is not a "gate" at the end of the project; it is integrated early in the development lifecycle.
*   **The "Why":** It is cheaper and safer to find bugs in code than in production.
*   **Exam Implementation:**
    *   Scanning container images for vulnerabilities **in the CI/CD pipeline** (before deployment).
    *   Using **Binary Authorization** to block images that haven't passed security tests.

### E. Defense in Depth
*   **Definition:** The strategy of layering multiple security controls so that if one fails, another catches the threat. Google applies this at every level.
*   **The "Why":** No single security control is perfect; redundancy reduces risk.
*   **The Layers (Outside -> In):**
    1.  **Edge:**
        *   **Cloud Armor:** Blocks DDoS and OWASP Top 10 attacks (SQL Injection, XSS) before they hit your VPC.
        *   **Global Load Balancing:** Absorbs volumetric attacks.
    2.  **Network:**
        *   **VPC Firewalls:** Control port/protocol access.
        *   **VPC Service Controls:** Prevent data exfiltration (GCS buckets cannot speak to outside world).
        *   **Private Google Access:** VMs reach APIs without public IPs.
    3.  **Identity:**
        *   **IAM:** Least Privilege (Role-based access).
        *   **BeyondCorp (IAP):** Zero Trust access to internal apps without VPNs.
        *   **MFA / 2SV:** Strong authentication.
    4.  **Compute:**
        *   **Shielded VMs:** Protect boot integrity (prevent rootkits).
        *   **Binary Authorization:** Ensure only trusted containers run on GKE.
        *   **OS Login:** Manages SSH access via IAM.
    5.  **Data:**
        *   **Encryption:** All data encrypted at rest (default) and in transit.
        *   **Cloud DLP:** Detects and redacts sensitive PII/Credit Cards.

### F. Continuous Detection & Auditing (Transparency)
*   **Definition:** You cannot protect what you cannot see. Security is an ongoing lifecycle, not a one-time setup.
*   **The "Why":** Attacks (and mistakes) happen. You must detect them immediately to respond.
*   **Exam Implementation:**
    *   **Cloud Audit Logs:** Ensure Admin Activity (always on) and **Data Access Logs** (needs enabling) are flowing to a secure sink.
    *   **Log Sinks:** Aggregate logs to a centralized BigQuery dataset for analysis or Cloud Storage bucket for long-term retention (WORM).
    *   **Security Command Center (SCC):** Use "Event Threat Detection" to find anomalies like "Cryptomining" or "Brute Force SSH" in real-time.

---

## 5. Exam Cheat Sheet: Mapping Principles to Tools

Quickly map the abstract principle to the concrete Google Cloud service answer.

| Abstract Principle | Service / Feature Answer |
| :--- | :--- |
| **"Detect Misconfigurations"** (Static) | **SCC Standard Tier** (Health Analytics) |
| **"Detect Active Attacks / Threats"** (Dynamic) | **SCC Premium Tier** (Event Threat Detection) |
| **"Centralized Visibility / Single Pane of Glass"** | **Security Command Center (SCC)** |
| **"Least Privilege" (Automated)** | **IAM Recommender** ("Policy Intelligence") |
| **"Zero Trust"** | **Identity-Aware Proxy (IAP)** |
| **"Secure Supply Chain"** | **Binary Authorization** (+ Artifact Registry) |
| **"Data Transparency"** | **Access Transparency** (See when Google Support accesses data) |
| **"Defense in Depth" (Edge)** | **Cloud Armor** |

---

## 6. Security Foundations Blueprint (Landing Zones)

**PCA Exam Priority:** 🔥 **HIGH (4/5)** — The architectural patterns are tested heavily through scenarios.

### What It Is
A **pre-configured, secure-by-default organizational structure** that you deploy BEFORE migrating workloads. The exam tests the *concepts*, not the specific "Cloud Foundation Toolkit" name.

### The Four Pillars (Exam Critical)

#### A. Resource Hierarchy (Structure)
**Purpose:** Separate workloads by environment, business unit, or compliance boundary.

**Typical Structure:**
```
Organization (yourdomain.com)
  ├── Folder: Production
  │     ├── Project: app-prod-frontend
  │     └── Project: app-prod-backend
  ├── Folder: Development  
  │     └── Project: app-dev
  └── Folder: Shared Services
        ├── Project: central-logging
        └── Project: shared-vpc-host
```

**Exam Scenario:**
> *"You have 50 applications. Each needs isolation, but Security wants centralized control. What do you do?"*

**Answer:** Use **Folders** to group by environment/team + Apply **Organization Policies** at the Org/Folder level.

---

#### B. Centralized Logging (Audit Trail)
**Purpose:** All logs flow to ONE secure project for compliance and analysis.

**How It's Achieved:**
1.  Create **Aggregated Log Sink** at **Organization or Folder** level.
2.  Route logs to **BigQuery** (queryable) or **Cloud Storage** (archival).
3.  Apply **Bucket Lock** (WORM) to prevent deletion.

**Exam Trap:**
> *Q: "Audit logs must be retained for 7 years and cannot be modified. Where do you export them?"*
- ❌ WRONG: "Keep them in default Cloud Logging (30-day retention)."
- ✅ CORRECT: "Export via **Log Sink** to GCS bucket with **Retention Policy + Bucket Lock**."

---

#### C. Shared VPC (Network Centralization)
**Purpose:** Network admins control VPC/Firewall; App teams deploy workloads but cannot change network rules.

**Structure:**
*   **Host Project:** Contains the VPC, subnets, firewall rules (managed by Network team).
*   **Service Projects:** App teams deploy VMs/GKE into the shared network (no network admin access).

**Exam Scenario:**
> *"Your company has 20 projects, each with its own VPC. Security wants centralized firewall control. What should you migrate to?"*

**Answer:** **Shared VPC**. Consolidate all VPCs into one Host Project.

**Exam Trap:**
- ❌ "VPC Peering" → Doesn't centralize management (each VPC still has separate firewall rules).

---

#### D. Organization Policies (Guardrails)
**Purpose:** Enforce company-wide rules that even Project Owners cannot bypass.

**Common PCA Policies:**
| Policy Constraint | What It Does | Exam Trigger |
| :--- | :--- | :--- |
| `compute.requireShieldedVm` | All VMs must be Shielded VMs. | "Prevent rootkits org-wide." |
| `iam.allowedPolicyMemberDomains` | Only `@yourcompany.com` can get IAM roles. | "Block external Gmail accounts." |
| `compute.vmExternalIpAccess` | Deny public IPs on VMs. | "VMs must be private." |
| `compute.restrictVpcPeering` | Control which VPCs can peer. | "Prevent unauthorized peering." |

**Exam Scenario:**
> *"Developers keep assigning public IPs to VMs. The CISO wants to block this org-wide. What do you use?"*

**Answer:** **Organization Policy**: `constraints/compute.vmExternalIpAccess = DENY`.

---

### Exam Decision Matrix: Where to Apply Security Controls

| Requirement | Solution |
| :--- | :--- |
| "Enforce MFA for ALL users across ALL projects." | **Org Policy** at Organization level. |
| "Separate Prod/Dev with different access controls." | **Folders** (Prod folder, Dev folder). |
| "Centralize logs from 100 projects for compliance." | **Aggregated Log Sink** at Org/Folder level → BigQuery. |
| "Network team controls firewalls; App teams deploy VMs." | **Shared VPC** (Host + Service Projects). |
| "Prevent ANY project from creating VMs without Shielded VM." | **Org Policy**: `compute.requireShieldedVm`. |

---

### What You Can SKIP
*   The exact name "Cloud Foundation Toolkit" (CFT).
*   Terraform/GitHub repo details.
*   How to run specific `gcloud` commands.

### What You MUST Know
*   The **4 Pillars**: Hierarchy, Logging, Shared VPC, Org Policies.
*   **When to use Org Policy vs IAM** (Org Policy = "What is allowed to exist"; IAM = "Who can do what").
*   **Inheritance**: Policies set at Org level flow down to all Folders/Projects.

---

### Architecture Diagram Reference (1-12)

| # | Component | What It Is | PCA Exam Purpose |
|:---:|:---|:---|:---|
| **1** | **Cloud Identity** | User/Group directory (LDAP/SSO/Workspace) | Authentication source for the entire org |
| **2** | **Cloud IAM** | Role-based access control | "Who can do what" (permissions) |
| **3** | **Org Policies** | Organizational constraints/guardrails | "What is allowed to exist" (blocks actions org-wide) |
| **4** | **Shared VPC Project (Host)** | Centralized VPC controlled by Network team | Network admins manage VPC; App teams use it |
| **5** | **Region 1** | Primary geographic region for workloads | Multi-region for HA; regional for data residency |
| **6** | **Cloud Router** | BGP router for hybrid connectivity | Enables dynamic routing for VPN/Interconnect |
| **7** | **Internet App Interface** | Public-facing endpoint (protected by Cloud Armor) | Edge defense layer (DDoS/WAF protection) |
| **8** | **Cloud Log Sink** | Aggregated log export router | Routes all org logs to centralized BigQuery/GCS |
| **9** | **Chronicle** | Google's SIEM platform | Security analytics / Threat intelligence |
| **10** | **Service Project** | Project where workloads run | Attached to Shared VPC (#4); isolated per app/team |
| **11** | **VPC Service Control** | Data exfiltration prevention | Creates security perimeter around sensitive data |
| **12** | **VM** | Compute instance | Must comply with Org Policies (#3); protected by Shielded VM |

---

## 7. Deep Infrastructure Security (Hardware & Host)

While "Shared Responsibility" says Google owns the hardware, the **PCA Exam** tests your ability to explain *why* that hardware is secure (usually for clients with high compliance needs).

### A. Titan (Hardware Root of Trust)
**"The Anchor"**
*   **What it is:** A custom-built security chip physically soldered onto Google’s servers.
*   **PCA Goal:** Supply Chain Security.
*   **Exam Scenario:**
    *   *Question:* "How does Google ensure the server hasn't been tampered with before your VM even boots?"
    *   *Answer:* **Titan** verifies firmware/BIOS signatures attempting to run on the machine.

### B. Google KVM Hypervisor (The Sandbox)
**"The Wall"**
*   **What it is:** A heavily hardened version of the open-source KVM hypervisor.
*   **PCA Goal:** Tenant Isolation.
*   **Exam Scenario:**
    *   *Question:* "A bank is afraid of 'noisy neighbors' or malicious actors on the same physical server accessing their RAM."
    *   *Answer:* Google's **Hardened KVM** provides a strict security sandbox preventing VM escape.

### C. vTPM (Virtual Trusted Platform Module)
**"The Watchdog"**
*   **What it is:** A virtualized TPM chip attached to your VM instance (Guest OS).
*   **PCA Goal:** Guest Integrity (Shielded VM).
*   **Exam Scenario:**
    *   *Question:* "You need to ensure the bootloader or kernel of your VM hasn't been modified by a rootkit."
    *   *Answer:* Enable **Shielded VMs** (which uses vTPM for **Measured Boot** and Integrity Monitoring).

> **Definition: Shielded VM**
> A hardened VM instance that uses **Secure Boot** (verifies signatures), **vTPM** (stores secrets/hashes), and **Integrity Monitoring** to ensure the OS hasn't been compromised by rootkits or boot-level malware.

> Shielded GKE Nodes extend this protection to Kubernetes. They ensure that the underlying node (VM) hosting your containers hasn't been tampered with. **Crucial Distinction:** Shielded Nodes protect the *Host OS*, whereas **Binary Authorization** protects the *Container Software*.

### D. Confidential Computing (Data in Use)
**"The Black Box"**
*   **What it is:** Encrypts data *while it is being processed* in RAM.
*   **Mechanism:** Uses hardware-based memory encryption (e.g., AMD SEV). Even the kernel or hypervisor cannot read the application's memory in cleartext.
*   **PCA Goal:** **Encryption in Use** (Privacy).
*   **Exam Scenario:**
    *   *Question:* "You have highly sensitive financial data. Compliance requires that data be encrypted at Rest, in Transit, AND **during processing**."
    *   *Answer:* Enable **Confidential VM** (or **Confidential GKE Nodes**).
*   **Performance Impact:** Slight performance penalty due to real-time memory encryption/decryption.

> **Exam Summary Table: Integrity vs Privacy**
> *   **Shielded VM** = Integrity (Prevent Modification/Rootkits).
> *   **Confidential VM** = Privacy (Prevent Viewing/Reads in RAM).





