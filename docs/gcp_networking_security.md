# GCP Networking: Security (PCA Study Guide)

In GCP, security is based on the **Zero Trust** model. You don't trust the network, you trust the Identity.

---

## 1. Firewalls

### VPC Firewall Rules
*   **Stateful**: If you allow traffic IN (Ingress), the return traffic (Egress) is automatically allowed.
*   **Implied Deny**: By default, ALL ingress traffic is blocked. ALL egress traffic is allowed.
*   **Targets**:
    *   **Tags**: Legacy method (e.g., target-tag: `web-server`).
    *   **Service Accounts**: **Recommended/Secure method**. "Only allow VMs running as `backend-sa` to talk to `db-sa`." Identity-based security.

### Hierarchical Firewall Policies
*   **Level**: Applied at the **Organization** or **Folder** level.
*   **Purpose**: Central governance. e.g., "Ban port 22 (SSH) from the public internet for the entire company."
*   **Precedence**: Evaluated *before* VPC firewalls. A project admin cannot override an Org-level deny rule.

---

## 2. Cloud Armor (WAF & DDoS)

*   **Role**: Web Application Firewall. Sits at the **Global Load Balancer** edge.
*   **Capabilities**:
    *   Filters Top 10 OWASP attacks (SQLi, XSS).
    *   Geo-blocking / IP Rate Limiting.
    *   **DDoS Protection**:
        *   **Standard**: Free, always on (L3/L4 volumetric attacks).
        *   **Managed Protection Plus**: Paid, adds L7 protection and adaptive tuning.

---

## 3. Remote Access: Identity-Aware Proxy (IAP)

*   **The Problem**: Exposing SSH (22) or RDP (3389) to the public internet is dangerous (Brute force attacks).
*   **The Solution**: IAP TCP Forwarding.
*   **Flow**:
    1.  Admin runs `gcloud compute ssh my-vm`.
    2.  Command tunnels traffic via HTTPS to Google (Auth check happens here).
    3.  If authorized, Google forwards traffic to the VM's internal IP.
    4.  **Result**: You can SSH into a VM that has **NO Public IP**.

---

## 4. VPC Service Controls (VPC SC)

*   **Concept**: Data Exfiltration Prevention.
*   **Service Perimeter**: Creates a virtual boundary around "API-based" services like BigQuery, Cloud Storage, and SQL.
*   **Effect**:
    *   A VM *inside* the perimeter can allow saving data to the GCS bucket.
    *   If a user tries to copy that data to a personal Ggmail bucket *outside* the perimeter, it is **BLOCKED**.
    *   Even IAM permissions (Owner) cannot bypass the perimeter.

---

## 5. Private Service Connect (PSC)

*   **The Modern "Peering"**: Connects a "Consumer" VPC to a "Producer" VPC (or Google Service) via a created Endpoint IP.
*   **Differences from Peering**:
    *   **Transitive-like**: Easier to chain services.
    *   **No IP Conflicts**: The consumer sees the producer as just one IP address, not a whole subnet range.
    *   **Secure**: One-way traffic initiation.

---

## 6. Cloud NAT (Network Address Translation)

*   **Definition**: NAT allows multiple VMs to share a single public IP address for *outbound* connections.
*   **The Problem**: Private GKE Clusters and secure VMs often have **No External IP address** to reduce attack surface. However, they still need to download OS patches or Docker images from the internet.
*   **The Solution**: **Cloud NAT**.
    *   **Outbound Only**: Allows private VMs to initiate connections to the internet.
    *   **No Inbound**: It does *not* allow the internet to initiate connections to the VM.
    *   **Managed Service**: It is regional, high availability, and not a single instance (no bottleneck).

---

## PCA Decision Matrix: Network Security

| Requirement | Solution |
| :--- | :--- |
| "Block SQL Injection/XSS attacks" | **Cloud Armor** |
| "SSH to VM without Public IP / VPN" | **Identity-Aware Proxy (IAP)** |
| "Prevent data theft to personal Gmail buckets" | **VPC Service Controls** |
| "Company-wide blocking of RDP port" | **Hierarchical Firewall Policy** |
| "Allow updates on Private VM" | **Cloud NAT** |
| "Connect to 3rd party SaaS securely" | **Private Service Connect (PSC)** |
