# PCA Security: Network Defense & Zero Trust

This guide covers network security perimeters, DDoS protection, and the BeyondCorp model for the Professional Cloud Architect (PCA) exam.

## 1. VPC Service Controls (VPC-SC) (CRITICAL TOPIC)

VPC Service Controls is one of the most frequently asked topics. It prevents **Data Exfiltration**.
> **Data Exfiltration Definition:** The unauthorized transfer of data from a secure corporate system to an untrusted external location (e.g., copying a corporate database to a personal Google Drive).

### The Problem it Solves
"How do I prevent a user with valid credentials from copying data from my corporate BigQuery bucket to their personal Gmail bucket?" (IAM cannot stop this, as the user has permission to read the source).

### The Solution: Service Perimeters
VPC-SC creates a "Perimeter" around your Google Cloud resources (Projects).
*   **Inside the Perimeter:** Resources can talk to each other freely (e.g., VM talking to BigQuery).
*   **Crossing the Boundary:** By default, **ALL** communication crossing the perimeter is BLOCKED.

### Key Components:
1.  **Service Perimeter:** Groups projects and services to protect (e.g., BigQuery, GCS).
2.  **Access Levels (Context-Aware Access):** Allows access based on context (e.g., "Allow access if coming from Corp IP range" or "Device is managed").
3.  **Ingress/Egress Rules:** Explicit exceptions to allow communication between perimeters or from the internet.
4.  **VPC Service Controls Bridge:** Allows two different perimeters to communicate (deprecating in favor of Ingress/Egress rules, but still appears in exams).

*Exam Tip:* If the question mentions "Data Exfiltration" or "protecting services independent of IAM," the answer is **VPC Service Controls**.

---

## 2. Cloud Armor (WAF & DDoS)

Cloud Armor is Google's **Web Application Firewall (WAF)** and DDoS protection service. It sits at the global edge (Global Load Balancer).

### Features:
1.  **DDoS Protection:** Protects against Volumetric attacks (L3/L4) and Protocol attacks.
    *   *Standard:* Free, basic protection.
    *   *Managed Protection Plus:* Paid, covers L7 attacks, access to DDoS response team.

    > **Quick Ref: OSI Layers**
    > *   **L1 (Physical):** Cables/Fiber.
    > *   **L2 (Data Link):** MAC Addresses/Switches.
    > *   **L3 (Network):** IP Addresses/Routers (Volumetric Attacks hit here).
    > *   **L4 (Transport):** TCP/UDP Ports.
    > *   **L5 (Session):** Syn/Ack.
    > *   **L6 (Presentation):** Encryption/Encoding.
    > *   **L7 (Application):** HTTP/HTTPS Requests (SQLi, XSS, Scrapers hit here).

2.  **WAF Rules:** Protects against OWASP Top 10 (SQL Injection, XSS, etc.).
    > **OWASP:** (Open Web Application Security Project). A global nonprofit that publishes the "Top 10" list of the most dangerous web vulnerabilities (e.g., SQL Injection, Broken Auth). Cloud Armor's rules are tuned to block these specifically.
        > *   **Deep Dive: Cross-Site Scripting (XSS):**
        >     *   **How it works:** A hacker types a script (e.g., `<script>steal_cookies()</script>`) into a public comment box.
        >     *   **The Problem:** When *other* users view that comment, the script runs in *their* browser. It steals their Session Cookies.
        >     *   **Result:** The hacker hijacks the user's session.
    *   Pre-configured rules available.
3.  **Geo-Blocking:** "Block traffic from Country X."
4.  **Rate Limiting:** "Allow max 100 requests per minute from a single IP."
5.  **Adaptive Protection:** Uses ML to detect anomalies in traffic patterns.

*Integration:* Works ONLY with **Global External HTTP(S) Load Balancers** and **TCP/SSL Proxies**.

---

## 3. Identity-Aware Proxy (IAP) & BeyondCorp

IAP allows you to access applications and VMs **without VPNs** and **without public IPs**. It implements the **Zero Trust** model.

### Use Case 1: SSH/RDP Access (Replacing Bastion Hosts)
*   **Old Way:** Create a Bastion Host (Jump Box) with a public IP. Open Port 22. Highly vulnerable.
*   **IAP Way:**
    1.  VM has **NO Public IP** (Private only).
    2.  Create an IAP Firewall Rule to allow ingress from range `35.235.240.0/20` (Google's internal IAP range).
    3.  User runs `gcloud compute ssh my-vm --tunnel-through-iap`.
    4.  Google authenticates the user, then tunnels traffic to the VM.
    *   *Benefit:* No exposure to the public internet. Granular IAM access.

### Use Case 2: Web App Access
*   Put IAP in front of your App Engine or Balancer.
*   Requests are intercepted by Google.
*   User must sign in (Google Identity).
*   If valid, request is forwarded to the app. Code gets user identity via headers (`X-Goog-Authenticated-User-Email`).

---

## 4. Firewalls: VPC vs. Hierarchical

| Type | Application Level | Direction | Logic |
| :--- | :--- | :--- | :--- |
| **VPC Firewall Rules** | Applies to specific VPCs and instances (via Tags/Service Accounts). | Ingress/Egress | Allow/Deny. Implicit Deny Ingress. Implicit Allow Egress. |
| **Hierarchical Firewall Policies** | Applies to **Organization** or **Folders**. | Ingress/Egress | **Enforced across all child projects.** Cannot be overridden by local project admins if "Enforced". |

*   **Hierarchical Use Case:** "Security team wants to ensure Port 22 is blocked open to the world (0.0.0.0/0) for ALL projects in the organization."
*   **VPC Firewall Use Case:** "Allow web traffic to the Frontend tier only."

---

## 5. Cloud NAT (Network Address Translation)

While a networking tool, it's a security best practice.
*   **Function:** Allows instances with **no public IP** to access the internet (e.g., for updates/patching).
*   **Security Benefit:** The internet cannot initiate connections *IN* to the instances. Only return traffic is allowed.

---

## 6. Web Security Scanner

*   **Function:** Crawls your *public* App Engine, GKE, or Compute Engine web apps.
*   **Detects:** Outdated libraries, Cross-site scripting (XSS), Flash injection, Mixed content (HTTP in HTTPS).
*   **Exam Relevance:** Automated vulnerability scanning for web apps.
