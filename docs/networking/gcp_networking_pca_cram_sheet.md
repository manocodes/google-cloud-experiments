# GCP Networking: The PCA "Cram Sheet"

**Relax.** You are taking an **Architect** exam, not a Network Engineering exam. You do not need to know how to configure BGP buffers orsubnet masks perfectly.

You need to know **Which Box to Pick** on a whiteboard.

---

## 1. The "Golden Rules" of GCP Networking

1.  **VPCs are GLOBAL**. Subnets are **REGIONAL**.
    *   *Exam Trick*: "Connect a VM in Tokyo to a VM in New York." -> **Use the same VPC**. No VPN needed.
2.  **Google is "Zero Trust"**.
    *   Just because you are in the same network doesn't mean you can talk. Firewalls block everything by default.
3.  **Identity > IP Addresses**.
    *   *Exam Tip*: Never pick "Filter by IP address" if "Filter by Service Account" is an option. It's more secure.

---

## 2. The Decision Keywords (Memorize These)

When you see a keyword in the question, pick the corresponding product.

| If you see... | You pick... |
| :--- | :--- |
| "Global Website", "Anycast", "Cross-region failover" | **Global External HTTP(S) Load Balancer** |
| "UDP", "Gaming", "VOIP" | **Network Load Balancer** |
| "Private Line", "Security Compliance", "10Gbps+" | **Dedicated Interconnect** |
| "Cost-effective connectivity", "Encrypted over Internet" | **Cloud VPN** |
| "Centralized Network Administration", "Separate Depts" | **Shared VPC** |
| "Simple connection between 2 projects" | **VPC Peering** |
| "SQL Injection", "DDoS", "OWASP Top 10" | **Cloud Armor** |
| "SSH without Public IP" | **Identity-Aware Proxy (IAP)** |
| "Private VM needs internet for updates" | **Cloud NAT** |
| "Data Exfiltration Protection", "BigQuery Security" | **VPC Service Controls** |
| "Intrusion Detection", "Packet Capture" | **Packet Mirroring / Cloud IDS** |
| "Consume/Publish Service privately" | **Private Service Connect (PSC)** |

---

## 3. The "One-Liners" (Quick Concepts)

*   **Cloud DNS**: It's 100% SLA. Use "Split-Horizon" to give different answers to Internal vs External users.
*   **CDN**: Check a box on the Load Balancer to cache static content. Saves money and speed.
*   **Private Google Access**: Lets VMs without internet talk to Google APIs (Storage, BigQuery).
*   **Alias IPs**: Used when running Containers (Pods) on a VM.

---

## 4. How to Study (The 80/20 Rule)

1.  **Ignore**: Configuring routes, calculating CIDR math (mostly), legacy TCP/SSL proxies.
2.  **Focus**:
    *   **Hybrid**: Choosing VPN vs Interconnect.
    *   **Load Balancing**: Choosing HTTP vs Network.
    *   **Security**: How to secure a private VM (IAP + NAT).

If you stick to these high-level decision points, you will pass the networking section.
