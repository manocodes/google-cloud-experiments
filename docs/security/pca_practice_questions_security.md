# PCA Practice Questions: Security

This document contains PCA-level scenario questions focused on Security, designed to test the concepts covered in the study guides.

---

## Question 1: Hybrid Authentication
**Scenario:** Your company controls user identities in an on-premises Active Directory layer. You want to give your developers access to Google Cloud Platform using their existing AD credentials. You want to minimize administrative overhead and ensure that if a user is disabled in AD, their access to GCP is revoked within hours.
**Requirement:** You need to implement the user synchronization and authentication strategy.

**Options:**
A. Export users from AD to a CSV and use a Python script to create users in Cloud Identity.
B. Use Google Cloud Directory Sync (GCDS) to sync users to Cloud Identity, and configure SAML SSO with your Identity Provider.
C. Use Google Cloud Directory Sync (GCDS) to sync users, and ask users to set a unique password for their Google Cloud account.
D. Configure an IPSec VPN and trust the on-premise domain controller to issue Kerberos tickets for GCP Console access.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why this acts as the "Best Practice":**
*   **GCDS (Google Cloud Directory Sync):** Automatically handles the provisioning/deprovisioning logic. If a user is disabled in AD, GCDS (running on a schedule) will suspend them in Cloud Identity.
*   **SAML SSO:** Delegating authentication means users don't have separate passwords. When they try to log in, Google redirects them to your IdP. If they are disabled on-prem, they can't log in instantly.

**Why others are wrong:**
*   **A:** Manual/Scripted CSV export is high overhead and prone to error (not "minimized overhead").
*   **C:** Asking users to manage separate passwords is bad user experience and less secure (no instant revocation if AD password changes).
*   **D:** GCP Console does not accept Kerberos tickets over VPN. It speaks SAML/OIDC.
</details>

---

## Question 2: Encryption Decision
**Scenario:** You are designing a document storage system for a Law Firm. The firm frequently handles highly sensitive data. A strict new regulation requires that **keys used to encrypt data must reside on a hardware device** managed by the customer, but the firm does not want the operational burden of managing physical keys on-premises. The encryption service must be FIPS 140-2 Level 3 validated.

**Options:**
A. Use Google Cloud Default Encryption (Google-Managed Keys).
B. Use Customer-Managed Encryption Keys (CMEK) with Cloud KMS (Software backend).
C. Use Customer-Managed Encryption Keys (CMEK) with Cloud HSM.
D. Use Customer-Supplied Encryption Keys (CSEK).

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Hardware Requirement:** The requirement specifies keys must be on a hardware device. This eliminates A and B (Software keys).
*   **Operational Burden:** The customer does *not* want to manage keys on-prem. This eliminates D (CSEK requires you to hold the key).
*   **FIPS 140-2 Level 3:** Cloud HSM meets this exact standard and is fully managed by Google (no physical maintenance for you).

**Why others are wrong:**
*   **A:** Google manages the keys; violates the "customer managed" requirement.
*   **B:** Cloud KMS software keys are FIPS 140-2 Level 1, not Level 3.
*   **D:** CSEK = "Hold Your Own Key" (On-prem). The prompt explicitly says they don't want on-prem burden.
</details>

---

## Question 3: Data Exfiltration
**Scenario:** You have a BigQuery dataset containing financial transaction logs. You have granted the `BigQuery Data Viewer` role to your data analysis team. A security audit identifies a risk: a malicious insider could run a query, export the results to a Google Cloud Storage bucket in their *personal* project (gmail account), and steal the data.
**Requirement:** You need to prevent this specific export vector without stopping the team from working on legitimate projects.

**Options:**
A. Remove the `BigQuery Data Viewer` role and assign a Custom Role with `bigquery.jobs.create` removed.
B. Implement VPC Service Controls and define a Service Perimeter around the project.
C. Enable Cloud DLP to redact the data before it is stored in BigQuery.
D. Use a Hierarchical Firewall Policy to block egress traffic to unknown IP addresses.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **VPC Service Controls (VPC-SC):** This is the textbook use case. VPC-SC creates a perimeter. Moving data *from* a protected project (Inside) *to* a personal project (Outside) is blocked by the perimeter, even if the user has IAM permissions.

**Why others are wrong:**
*   **A:** If you remove `bigquery.jobs.create`, they can't run queries at all. You stopped the work.
*   **C:** Redaction protects PII, but doesn't stop the *exfiltration* of the data itself. The exam asks to stop the export to personal projects.
*   **D:** Firewall rules create layer 3/4 blocks (IP addresses). BigQuery export is a Layer 7 API operation ("Copy to Bucket"). Firewalls cannot see/stop API calls between buckets.
</details>

---

## Question 4: Protecting Web Applications
**Scenario:** You are deploying a public-facing e-commerce application on the Global External HTTP(S) Load Balancer (GKE Backend). You need to protect the application from SQL Injection, Cross-Site Scripting (XSS), and Volumetric DDoS attacks.

**Options:**
A. Configure VPC Firewall Rules to allow traffic only on Port 443.
B. Use Cloud Armor with pre-configured WAF rules and Adaptive Protection.
C. Use Identity-Aware Proxy (IAP) to inspect the traffic.
D. Use Packet Mirroring to send traffic to a third-party IDS.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Cloud Armor:** It is Google's WAF and DDoS solution. It attaches to the Load Balancer.
*   **WAF Rules:** Specifically block SQLi and XSS (OWASP Top 10).
*   **Volumetric DDoS:** Cloud Armor handles this automatically.

**Why others are wrong:**
*   **A:** Firewall rules are L3/L4. They cannot see "inside" the packet to detect SQL Injection strings.
*   **C:** IAP is for *Authentication* (Zero Trust login), not for threat detection/WAF.
*   **D:** Packet Mirroring is for *detection/forensics*, not *prevention/blocking* in real-time (usually). Cloud Armor is the native solution.
</details>

---

## Question 5: SSH Access Management
**Scenario:** You have a fleet of 500 Linux VMs. You need to grant SSH access to a changing team of 50 contract developers. You want to avoid managing SSH keys manually and ensure that all SSH sessions are logged to Cloud Audit Logs. You also want to enforce 2-Factor Authentication (2FA) for SSH.

**Options:**
A. Create a shared SSH key pair and distribute the private key to the contractors via a secure email.
B. Use startup scripts to fetch public keys from a GCS bucket and add them to `~/.ssh/authorized_keys`.
C. Enable OS Login on the VMs and grant the `compute.osLogin` IAM role to the contractors.
D. Use Identity-Aware Proxy (IAP) TCP Forwarding, but let users manage their own keys.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **OS Login:** Links the Linux User to the Google Identity.
*   **2FA:** Because it uses the Google Identity, if the Google Account has 2FA, the SSH session requires it.
*   **Revocation:** Removing the IAM role instantly revokes access.
*   **Logging:** OS Login actions are tied to the user identity in Audit Logs.

**Why others are wrong:**
*   **A:** Shared keys are a massive security risk. No individual accountability (non-repudiation).
*   **B:** "Startup scripts" are static. Revoking a key requires running a script on 500 VMs. No 2FA support.
*   **D:** IAP handles the *network* path, but if users manage their own keys (metadata keys), you lose the centralized management and instant revocation benefits of OS Login.
</details>

---

## Question 6: Supply Chain Security
**Scenario:** Your regulator requires that no container image runs in your Production GKE cluster unless it has been scanned for vulnerabilities and digitally signed by your CI/CD pipeline.

**Options:**
A. Use a VPC Service Control perimeter to block access to Docker Hub.
B. Configure Binary Authorization with an Attestor that verifies the vulnerability scan signature.
C. Use Cloud IAM to restrict who can run `kubectl apply`.
D. Enable Shielded GKE Nodes.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Binary Authorization:** Specifically designed for this "Attestation" workflow. It acts as a gatekeeper that checks for the digital signature (Attestation) before allowing the Pod to start.

**Why others are wrong:**
*   **A:** Prevents network access, but doesn't verify the *integrity* or *scan status* of the image.
*   **C:** IAM controls *who* can deploy, not *what image* they are deploying (a trusted user could deploy a bad image).
*   **D:** Shielded Nodes protect the *VM Bootup*, not the *Container Image* contents.
</details>

---

## Question 7: Support Access (Transparency)
**Scenario:** You are a bank. You are migrating to GCP, but your legal team has a strict blocker: "We cannot allow Cloud Provider employees (Google Support) to access our data without our explicit, ticket-based approval for every single interaction."

**Options:**
A. Encrypt all data with CSEK (Customer-Supplied Encryption Keys).
B. Enable Access Transparency.
C. Enable Access Approval.
D. Use VPC Service Controls.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Access Approval:** The keyword is "Approval". This feature ensures Google cannot touch the project unless you click "Approve" (via email or API).
*   **Access Transparency:** (Choice B) is close, but it only *Logs* (Record) what they did. It doesn't *Block* them until you approve. The scenario requires *Approval*.

**Why others are wrong:**
*   **A:** CSEK hides data, but doesn't solve the *access* workflow. Google SREs might still need to see metadata or config.
*   **D:** VPC-SC is for external data theft, not for internal Support access controls.
</details>

---

## Question 8: IAM Inheritance
**Scenario:** You have an Organization Policy at the Root Node that sets `constraints/compute.vmExternalIpAccess` to **DENY** (Blocking Public IPs).
A specific project team "Marketing-Microsite" needs a Public IP to serve a temporary website.
How do you allow this exception with the *least privilege* and minimal impact?

**Options:**
A. Remove the constraints at the Organization Node.
B. Create a new Organization Policy on the "Marketing-Microsite" project that sets the policy to **ALLOW**, and toggle "Inherit from parent" to Off (Override).
C. Grant the Project Owner the `Organization Policy Administrator` role.
D. Use Cloud NAT instead.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Override:** Org Policies flow down. To make an exception, you must create a policy at the lower level (Project) and specifically set it to **Override** (or merge/allow) to break the inheritance from the parent.

**Why others are wrong:**
*   **A:** Removes protection for the *entire* company. Bad.
*   **C:** Granting the role lets the user *change* the policy, but doesn't technically *fix* the issue until they perform step B. Also, granting "Org Policy Admin" is dangerous/too broad.
*   **D:** Cloud NAT is for *Outbound* traffic. A website needs *Inbound* traffic, so NAT won't work for serving a site.
</details>

---

## Question 9: Active Threat Detection
**Scenario:** Your CISO requires immediate visibility into any "active threats" occurring within your environment, specifically **Cryptomining** binaries running on VMs and **Brute Force SSH** attacks. You also need to generate a one-click compliance report for **PCI-DSS**. You want to minimize configuration overhead.

**Options:**
A. Enable Security Command Center (SCC) Standard Tier.
B. Enable Security Command Center (SCC) Premium Tier.
C. Install the Cloud Logging Agent on all VMs and create a Log-Based Metric for SSH failures.
D. Use Packet Mirroring to send all traffic to a third-party Intrusion Detection System (IDS).

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Active Threats:** Detecting *runtime* threats like Cryptomining and Brute Force attacks (via Event Threat Detection) is a **Premium Tier** feature.
*   **Compliance Reports:** One-click compliance reports (PCI, NIST, ISO) are exclusive to **Premium Tier**.

**Why others are wrong:**
*   **A:** Standard Tier only detects **static misconfigurations** (e.g., Public Bucket, Open Firewall), not active attacks.
*   **C:** While you *could* build custom metrics for SSH, it doesn't detect Cryptomining or offer PCI reports. High overhead.
*   **D:** Third-party IDS is a valid approach but has significantly higher "configuration overhead" compared to enabling a native service toggle (SCC Premium).
</details>

---

## Question 10: Secrets Management
**Scenario:** You are deploying a microservice on Cloud Run that connects to a backend Cloud SQL database. The application needs the database password to connect. You want to follow Google's recommended security best practices for managing this credential. The password must be rotated every 90 days.

**Options:**
A. Hardcode the password in the container image and use a new image tag for rotation.
B. Store the password in a text file in a private Cloud Storage bucket and grant the Cloud Run Service Account `storage.objectViewer`.
C. Encrypt the password using Cloud KMS and store the ciphertext in the Code.
D. Store the password in Secret Manager and map it to the Cloud Run container as a volume or environment variable.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: D**

**Why:**
*   **Secret Manager:** Designed specifically for storage, rotation, and secure access of sensitive strings (API keys, passwords).
*   **Cloud Run Integration:** Has native integration to mount secrets as volumes or Env Vars.
*   **Rotation:** Native support for versioning and rotation.

**Why others are wrong:**
*   **A:** Hardcoding secrets is a critical security anti-pattern.
*   **B:** Valid-ish, but poor developer experience (race conditions, no version management UI) compared to Secret Manager.
*   **C:** KMS encrypts *data*, it doesn't store the secret itself for easy consumption. You'd still need to store the ciphertext somewhere. Secret Manager handles the encryption *and* the storage/retrieval.
</details>

---

## Question 11: Data Privacy in Use
**Scenario:** You are migrating a highly sensitive healthcare application. Regulations require that Patient Data must be encrypted at Rest, in Transit, and **DO NOT** appear in cleartext in the server's memory (RAM) while being processed, to protect against a malicious hypervisor or administrator.

**Options:**
A. Use Shielded VMs with Secure Boot enabled.
B. Use Confidential VMs (Confidential Computing).
C. Use Customer-Managed Encryption Keys (CMEK) for the Persistent Disks.
D. Implement Client-Side Encryption (CSEK) before uploading data.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Confidential VMs:** Use hardware-based memory encryption (e.g., AMD SEV) to encrypt data **in use** (in RAM). This prevents the host kernel/hypervisor from reading the memory.

**Why others are wrong:**
*   **A:** Shielded VMs protect **Integrity** (Bootloader/Rootkits), not **Privacy** of RAM.
*   **C:** CMEK encrypts data **at Rest** (Disk), not in RAM.
*   **D:** CSEK handles data upload security, but once the application decrypts it to process it, it would be vulnerable in RAM without Confidential VMs.
</details>

---

## Question 12: Network Architecture
**Scenario:** You have a centralized Networking team and 30 independent Application teams. The Networking team needs full control over the Subnets, Firewalls, and Cloud Routers. The Application teams need to deploy instances into these subnets but should not be able to modify network settings.

**Options:**
A. Create one VPC in the Networking Project. Use VPC Network Peering to connect it to all 30 Application Projects.
B. Use a Shared VPC. Designate the Networking Project as the Host Project and the Application Projects as Service Projects.
C. Create 30 separate VPCs. Use Cloud VPN to connect them all in a mesh topology.
D. Grant the Application teams `compute.networkAdmin` role on the Networking Project.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Shared VPC:** The textbook pattern for "Centralized Control, Decentralized Usage." Host Project holds the network; Service Projects use it.

**Why others are wrong:**
*   **A:** Peering connects networks, but each project still owns its own VPC and firewalls. It doesn't centralize *management*.
*   **C:** Massive management overhead (Mesh VPN for 30 projects).
*   **D:** Violates Least Privilege. Application teams should not be Admin on the network project.
</details>

---

## Question 13: Log Compliance
**Scenario:** Your regulator requires that all Admin Activity Audit Logs be retained for 5 years for forensic purposes. The standard retention is insufficient. These logs must be effectively immutable (Write Once, Read Many).

**Options:**
A. Go to the IAM Audit Logs settings and increase the retention period to 5 years.
B. Create an Aggregated Log Sink to export logs to a BigQuery dataset.
C. Create an Aggregated Log Sink to export logs to a Cloud Storage bucket. Apply a Retention Policy with a Bucket Lock used.
D. Export logs to Pub/Sub and use Dataflow to write them to a Spanner database.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Cloud Storage:** Best for long-term, low-cost retention (Archive class).
*   **Bucket Lock:** The key requirement is "Immutable" (WORM). Bucket Lock prevents deletion or modification for the specified period.

**Why others are wrong:**
*   **A:** You cannot change the retention period of the built-in `_Default` bucket to 5 years arbitrarily implies simply clicking a setting; usually requires export for long-term compliance storage.
*   **B:** BigQuery is editable (Mutable). It does not natively strictly enforce WORM like GCS Bucket Lock does, and is more expensive for simple cold storage.
</details>

---

## Question 14: DLP Automation
**Scenario:** Users upload customer support tickets (text files) to a Cloud Storage bucket. A backend process needs to index these tickets, but your legal team prohibits any Email Addresses or Credit Card numbers from being stored in the search index database. You need an automated, scalable solution.

**Options:**
A. Use a Cloud Function triggered by `google.storage.object.finalize`. Code the function to call the DLP API to inspect and redact the text, then write the clean result to the database.
B. Use a Cloud Function triggered by `google.storage.object.finalize`. Write regex (Regular Expressions) in Python to find and replace emails and credit cards.
C. Grant the Search Index service account the `dlp.user` role so it can ignore sensitive fields.
D. Use Using VPC Service Controls to block uploads containing PII.

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: A**

**Why:**
*   **DLP API:** The managed, enterprise-grade way to detect and redact sensitive info. It handles nuances (like Luhn check for credit cards) that simple Regex misses.
*   **Automation:** Cloud Function trigger is the standard pattern for "On-Upload processing."

**Why others are wrong:**
*   **B:** Writing your own Regex for Credit Cards/Emails is error-prone and "reinventing the wheel" (Anti-pattern).
*   **C:** Doesn't solve the storage requirement. The data would still land in the DB.
*   **D:** VPC-SC blocks *traffic*, it doesn't inspect *payload content* to redact text.
</details>
