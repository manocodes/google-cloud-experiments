# GCP Networking Core: VPC & Fundamentals (PCA Study Guide)

For the Professional Cloud Architect (PCA) exam, you must understand the "Global" nature of the VPC and how it differs from other cloud providers.

---

## 1. The Virtual Private Cloud (VPC)

### Global Software-Defined Network
*   **Global Resource**: A VPC in Google Cloud allows you to have subnets in **multiple regions** effectively communicating over private IP addresses without needing VPNs to connect regions.
*   **Regional Subnets**: While the VPC is global, **Subnets are Regional**.
    *   *Example*: A connection from a VM in `us-central1` to a VM in `asia-northeast1` (in the same VPC) travels over Google's backbone, not the public internet.

### Types of VPC Mode
1.  **Auto Mode**:
    *   Creates a subnet in *every* GCP region automatically.
    *   Good for testing/POCs.
    *   **Bad for Production**: Wastes IP space, potential conflict with VPN/Peering ranges.
2.  **Custom Mode**:
    *   Starts empty. You explicitely create subnets only in regions you need.
    *   **PCA Recommendation**: Always choose **Custom Mode** for production designs.

---

## 2. IP Addressing & Subnets

### Secondary IP Ranges (Alias IPs)
*   **Concept**: A subnet has a primary CIDR range (e.g., `10.0.0.0/24`). You can add "Secondary" ranges to the same subnet.
*   **Critical Use Case**: **GKE Chains**. In GKE VPC-Native clusters, the Node gets an IP from the Primary range, while Pods and Services get IPs from Secondary ranges.
*   **Exam Tip**: If a question asks about "Managing many secondary IPs for containers," think **Alias IPs**.

### Expanding Subnets
*   You can expand a subnet (e.g., `/24` to `/20`) **without downtime**.
*   **Constraint**: You cannot *shrink* a subnet or change its base IP range, only expand the mask.

---

## 3. Routes & Traffic Flow

GCP Routing Order of Precedence (The strict logic):
1.  **Most Specific Destination** (Longest Prefix Match).
    *   `10.1.1.0/24` beats `10.1.0.0/16`.
2.  **Highest Priority** (Lowest Number).
    *   Priority `100` beats Priority `1000`.

### System Routes (Immutable)
*   **Subnet Routes**: Automatically created access to all subnets in the VPC.
*   **Default Internet Route**: `0.0.0.0/0` to Default Internet Gateway.

### Custom Routes
*   **Tag-Based Routing**: You can apply a route only to VMs with a specific Network Tag.
    *   *Scenario*: "Route outgoing traffic from the `dev-instances` tag through a NAT instance."

---

## 4. Cloud DNS

A managed, authoritative DNS service offering 100% SLA.

### Zone Types
*   **Public Zone**: Visible to the internet.
*   **Private Zone**: Visible only within your specified VPC(s).

### DNS Policies (Inbound/Outbound)
*   **Inbound Query Forwarding**: Allows on-premise servers to resolve GCP hostnames (VPN required).
*   **Outbound Query Forwarding**: Allows GCP VMs to resolve on-premise hostnames (forwarding queries to your on-prem BIND/AD DNS).

### Split-Horizon DNS
*   **Scenario**: You want `myapp.example.com` to resolve to a Public IP (External LB) for users on the internet, but to a Private IP (Internal LB) for employees inside the VPC.
*   **Solution**: Create a **Private Zone** for `example.com` attached to your VPC with the private record. Public DNS stays public.

---

## 5. Private Google Access (PGA)

*   **The Problem**: A VM has **no external IP** (for security). It needs to copy data to a Cloud Storage bucket.
*   **The Solution**: Enable **Private Google Access** on the **Subnet**.
*   **How it works**: It routes traffic destined for Google APIs (`storage.googleapis.com`) through the internal default gateway, keeping it on Google's private network.
*   **Note**: This creates a route to the default internet gateway but *only* for Google's public IP ranges used by APIs. The VM still cannot reach `google.com` (Search) or `cnn.com`.

---

## PCA Decision Matrix: Core Networks

| Requirement | Use Solution |
| :--- | :--- |
| "Different regions, same private network" | **Global VPC** (standard behavior) |
| "Assign multiple internal IPs to one Interface" | **Alias IP Ranges** |
| "Access GCS/BigQuery from private VM" | **Private Google Access (PGA)** |
| "Resolve on-prem hostnames from GCP" | **Cloud DNS Outbound Forwarding** |
| "Ensure Prod doesn't overlap with On-Prem" | **Custom Mode VPC** |
