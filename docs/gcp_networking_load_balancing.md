# GCP Networking: Load Balancing & CDN (PCA Study Guide)

Choosing the correct Load Balancer is the #1 Networking question type on the PCA exam.

---

## 1. Load Balancer Categories

### A. Global vs. Regional
*   **Global LB**:
    *   **Single Anycast IP**: One IP address for the whole world.
    *   **Cross-Region Failover**: If `us-east1` breaks, traffic instantly goes to `eu-west1`.
    *   **Types**: HTTP(S), SSL Proxy, TCP Proxy.
*   **Regional LB**:
    *   Traffic stays in one region.
    *   Preserves Client IP (Passthrough).
    *   **Types**: Network TCP/UDP, Internal HTTP(S), Internal TCP/UDP.

### B. Internal vs. External
*   **External**: Internet-facing.
*   **Internal**: VPC-facing (Private IPs only).

---

## 2. Layer 7: HTTP(S) Load Balancing

*   **Traffic Type**: HTTP and HTTPS (Web sites, APIs).
*   **Architecture**: proxy-based (GFE - Google Front End).
*   **Key Features**:
    *   **URL Maps**: Route `/video` to the Video Backend and `/images` to the Storage Backend.
    *   **SSL Termination**: The LB handles the heavy encryption work.
    *   **Cloud CDN Integration**: Check a box to cache content at the edge.
    *   **Cloud Armor Integration**: Attach WAF policies here.

---

## 3. Layer 4: TCP/UDP Load Balancing

### A. Network Load Balancer (Passthrough)
*   **Type**: External, Regional.
*   **Maglev**: The underlying tech.
*   **Use Case**: Non-HTTP traffic (gaming, VOIP) OR when you need to see the **Original Client IP** on the VM itself.
*   **Note**: No SSL termination.

### B. SSL Proxy / TCP Proxy
*   **Type**: External, Global.
*   **Use Case**: You have non-HTTP traffic (like a custom TCP protocol) but you WANT SSL termination at the edge or Global Anycast.

---

## 4. Cloud CDN (Content Delivery Network)

*   **How to enable**: It is a checkbox on the **Backend Service** of an HTTP(S) Load Balancer.
*   **Cache Keys**: Defaults to the URI. You can customize to ignore query parameters (e.g., `session_id`).
*   **Signed URLs**: Give temporary access to a paid file (e.g., "premium video") for a specific user for 10 minutes.

---

## 5. PCA Decision Tree (Memorize This)

**Question 1: Is the traffic HTTP/HTTPS?**
*   **YES** -> Use **HTTP(S) Load Balancer**.
    *   Global? -> Global External HTTP(S).
    *   Private? -> Internal HTTP(S).

**Question 2: Is it TCP/UDP (Non-HTTP)?**
*   **YES**:
    *   Do you need SSL offload? -> **SSL Proxy**.
    *   Do you need Global Anycast? -> **TCP Proxy**.
    *   Do you need to see the Original Client IP? -> **Network TCP/UDP LB**.
    *   Is it Internal only? -> **Internal TCP/UDP LB**.

**Question 3: Does the app use Websockets?**
*   HTTP(S) LB supports Websockets natively.

---

## Summary Cheat Sheet

| Load Balancer | Scope | Protocols | Key Feature |
| :--- | :--- | :--- | :--- |
| **HTTP(S)** | Global | HTTP/S | URL Maps, CDN, Armor |
| **SSL Proxy** | Global | TCP (w/SSL) | SSL Termination for non-Web |
| **TCP Proxy** | Global | TCP | Global IP for TCP |
| **Network LB** | Regional | TCP/UDP | Passthrough (Client IP visible) |
| **Internal LB** | Regional | TCP/UDP/HTTP | Private IP only |
