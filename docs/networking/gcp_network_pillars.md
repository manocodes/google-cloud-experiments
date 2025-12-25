# Google Cloud Network Pillars

A concise guide to Google Cloud's networking strategy: **Connect, Scale, Secure, and Optimize**.

## 1. Connect
*Bridge on-premises, other clouds, and users to Google's global network.*

*   **Cloud VPN**: Encrypted IPsec tunnel over the public internet (low cost, up to 3 Gbps).
*   **Cloud Interconnect**: Dedicated physical connection.
    *   *Dedicated*: Direct cable to Google (10-100 Gbps).
    *   *Partner*: Connection via service provider.
*   **Virtual Private Cloud (VPC)**: Global software-defined network. Subnets span regions automatically.

## 2. Scale
*Handle massive global traffic automatically via Software-Defined Networking (SDN).*

*   **Cloud Load Balancing**: Single global Anycast IP. Automatically routes users to the nearest healthy region.
*   **Cloud CDN**: Caches content at the edge (PoPs) to lower latency for users.
*   **Cloud DNS**: 100% SLA managed DNS service running on Google’s reliable infrastructure.

## 3. Secure
*Zero-trust protection for perimeter, data, and services.*

*   **Cloud Armor**: Global Edge security and Web Application Firewall (WAF) to block DDoS and web attacks.
*   **Identity-Aware Proxy (IAP)**: Secure access to internal VMs (SSH/RDP) and apps without a VPN.
*   **VPC Service Controls**: Security perimeter preventing data exfiltration for managed services (e.g., BigQuery, Storage).
*   **Cloud NAT**: Outbound internet access for private VMs without exposing them to inbound traffic.

## 4. Optimize
*Visibility, troubleshooting, and cost/performance control.*

*   **Network Intelligence Center**:
    *   *Connectivity Tests*: Simulate traffic to verify firewall rules. **Exam Answer** for "Why can't VM A reach VM B?".
    *   *Network Topology*: Visualize traffic flow across your infrastructure.
*   **Network Service Tiers**:
    *   *Premium*: Traffic rides Google's high-speed private backbone (faster, reliable).
    *   *Standard*: Traffic rides the public internet until it hits the destination region (cheaper).
