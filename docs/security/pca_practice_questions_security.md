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
