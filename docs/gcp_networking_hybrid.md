# GCP Networking: Hybrid & Inter-VPC Connectivity (PCA Study Guide)

This guide covers how to connect your VPC to the outside world (On-Prem) and to other VPCs.

---

## 1. Connecting to On-Premise

### A. Cloud VPN
Encrypted traffic over the **Public Internet**.
*   **HA VPN (High Availability)**:
    *   **Standard for Prod**: Uses 2 interfaces (tunnels) + BGP.
    *   **SLA**: 99.99% (if both tunnels configured).
    *   **Bandwidth**: Up to 3 Gbps per tunnel.
*   **Classic VPN**: Deprecated. Avoid in new designs.

### B. Cloud Interconnect
Private traffic over a **dedicated physical line** (Traffic does NOT touch the public internet).
*   **Dedicated Interconnect**:
    *   **Physical**: You run a cable directly to a Google Colocation Facility (e.g., Equinix).
    *   **Capacity**: 10 Gbps or 100 Gbps pipes.
    *   **Use Case**: Massive data transfer (Petabytes), strict compliance/security requirements.
*   **Partner Interconnect**:
    *   **Physical**: You connect to a Service Provider (ISP) who connects to Google.
    *   **Capacity**: Flexible (50 Mbps up to 10 Gbps).
    *   **Use Case**: You aren't physically near a Google facility, or don't need a full 10 Gbps pipe.

### C. Direct Peering / Carrier Peering
*   **NOT for VPC access**: This connects to Google *Public* Services (YouTube, Workspace APIs) without hitting the public internet. It does *not* give you access to your private VPC VMs.
*   **Exam Trap**: If the question asks to connect to a *private VM*, Peering is the Wrong Answer. Use Interconnect or VPN.

---

## 2. Dynamic Routing: Cloud Router
*   **BGP (Border Gateway Protocol)**: The language routers use to talk.
*   **Cloud Router**: Google's managed BGP speaker.
    *   Required for **HA VPN** and **Interconnect**.
    *   Automatically learns new subnets added on-premise and advertises new GCP subnets back to on-premise.
*   **Global vs Regional Routing**:
    *   **Regional**: Only advertises subnets in the *same region* as the Cloud Router.
    *   **Global**: Advertises *all* subnets in the VPC to the on-prem router.

---

## 3. Connecting VPC to VPC

### A. VPC Peering
*   **Concept**: Fuses two VPCs together so internal IPs can talk.
*   **Constraint: Non-Transitive**:
    *   If A peers with B, and B peers with C... **A cannot talk to C**.
    *   This is the biggest architectural limitation.
*   **Constraint: CIDR Overlap**: You cannot peer if both VPCs use `10.0.0.0/24`.

### B. Shared VPC (Hub and Spoke)
*   **Concept**: Centralized Network Administration.
*   **Host Project**: Owns the network (VPC, Subnets, Firewalls, VPNs).
*   **Service Projects**: Attach to the Host Project and *consume* its subnets.
*   **Benefit**: Security admins verify rules once in the Host; Developers just deploy VMs in Service projects. Separation of Duties.

---

## PCA Decision Matrix: Hybrid Connectivity

| Requirement | Solution |
| :--- | :--- |
| "Low cost, quick setup, encrypted" | **Cloud VPN** |
| "High bandwidth (10Gbps+), Private Line" | **Dedicated Interconnect** |
| "< 10Gbps, Private Line, no local Google PoP" | **Partner Interconnect** |
| "SLA: 99.99%" | **HA VPN** (2 tunnels) or **Interconnect** (4 circuits/2 regions) |
| "Different Orgs need private connection" | **VPC Peering** |
| "Centralized Network Admin + Dept Isolation" | **Shared VPC** (Host/Service Projects) |
