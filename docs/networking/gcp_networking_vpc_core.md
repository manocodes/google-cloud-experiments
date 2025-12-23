# GCP Networking Core: VPC & Fundamentals (PCA Study Guide)

For the Professional Cloud Architect (PCA) exam, you must understand the "Global" nature of the VPC and how it differs from other cloud providers.

---

## 1. The Virtual Private Cloud (VPC)

### Global Software-Defined Network
*   **Global Resource**: A VPC in Google Cloud allows you to have subnets in **multiple regions** effectively communicating over private IP addresses without needing VPNs to connect regions.
    *   **Crucial Concept**: The VPC *itself* has **NO IP Adress Range**. It is just a container. Only the **Subnets** inside it have IP ranges.
*   **Regional Subnets**: A subnet belongs to **exactly one region**. It cannot span across regions.
    *   *Clarification*: You CAN have **multiple subnets** in the same region (e.g., `subnet-a` and `subnet-b` both in `us-central1`).
    *   *Example*: A connection from a VM in `us-central1` to a VM in `asia-northeast1` (in the same VPC) travels over Google's backbone, not the public internet.

    *   *Example*: A connection from a VM in `us-central1` to a VM in `asia-northeast1` (in the same VPC) travels over Google's backbone, not the public internet.

### Project Relationship (1 Project : N VPCs)
*   **Ownership**: A VPC "lives" inside a Google Cloud Project. It is a resource just like a VM.
*   **Quotas**: By default, you can have **5 VPCs** per project (this is a soft limit, you can request more).
*   **Isolation**: By default, a VPC in `Project A` cannot talk to a VPC in `Project B` (unless you use Peering or Shared VPC).

### Types of VPC Mode
1.  **Auto Mode**:
    *   Creates a subnet in *every* GCP region automatically.
    *   Good for testing/POCs.
    *   **Bad for Production**: Wastes IP space, potential conflict with VPN/Peering ranges.
2.  **Custom Mode**:
    *   Starts empty. You explicitely create subnets only in regions you need.
    *   **PCA Recommendation**: Always choose **Custom Mode** for production designs.

---

## 1.1 Basics: CIDR Blocks & Addressing

**CIDR (Classless Inter-Domain Routing)** is how you define the "size" of your network.
*   **Format**: `IP_Address/Mask` (e.g., `10.0.0.0/24`).
*   **The Mask**: The number after the slash tells you how many IPs are available. **Lower number = More IPs**.

### CIDR "Cheat Sheet" for PCA
| CIDR Mask | Total IPs | Usable IPs (GCP reserves 4) | Use Case |
| :--- | :--- | :--- | :--- |
| **`/32`** | 1 | 0 (Host only) | Single IP (e.g., `/32` route to a specific VM). |
| **`/29`** | 8 | 4 | Smallest allowed GCP subnet. Good for interconnect. |
| **`/24`** | 256 | 252 | Standard subnet size. Good default. |
| **`/20`** | 4,096 | 4,092 | GKE Clusters (Pods need lots of IPs). |
| **`/16`** | 65,536 | 65,532 | Very large networks. |
| **`/0`** | All IPs | - | The entire Internet (`0.0.0.0/0`). |

> **Note**: GCP reserves **4 IP addresses** in every subnet (Network, Gateway, Reserved, Broadcast). A `/29` gives you only 4 usable IPs!

### Historical Note: Class A, B, C (The Old Way)
Before CIDR, networks were fixed sizes:
*   **Class A**: Massive networks (`/8`).
*   **Class B**: Medium networks (`/16`).
*   **Class C**: Small networks (`/24`).
*   **Importance for Exam**: **None**. Modern cloud networking uses CIDR. Ignore outdated references to "Class C networks" unless they just mean "a /24 subnet".

### RFC 1918: Private Ranges (Memorize These)
These are the IP ranges you *must* use for your private VPC subnets to avoid internet conflict.
1.  `10.0.0.0/8` (Most common in Cloud)
2.  `172.16.0.0/12`
3.  `192.168.0.0/16` (Common in home routers)

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
