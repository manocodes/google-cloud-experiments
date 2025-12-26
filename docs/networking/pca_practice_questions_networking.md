# GCP Networking PCA Practice Exam Questions

This document contains exam-style questions covering VPC, Load Balancing, Hybrid Connectivity, and Network Security.

---

## Section 1: VPC Fundamentals

### Question 1: VPC Subnets and IP Addressing

**Scenario**: A company creates a VPC with a single subnet (CIDR: `10.0.0.0/24`) in `us-central1`. They deploy 200 VMs. Now they need to expand to `europe-west1` but want VMs in both regions to be in the same VPC.

**What should they do?**

A. Delete the VPC and create a new one with /16 CIDR to have more IPs  
B. Create a new subnet in `europe-west1` within the same VPC  
C. Create a new VPC in `europe-west1` and use VPC Peering  
D. Expand the existing subnet's CIDR from /24 to /16  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Deleting the VPC would require:
  - Deleting all 200 VMs first (downtime).
  - Recreating everything (days of work).
  - **Misunderstanding**: VPCs in Google Cloud are **global** (span all regions). The mistake is thinking VPC = subnet. A VPC can have subnets in multiple regions.

- **B (Correct)**: ✅ Google Cloud VPCs are **global resources**:
  - **One VPC** can have **multiple subnets** across different regions.
  - Each subnet is **regional** (tied to a region, e.g., `us-central1` or `europe-west1`).
  - **Solution**: Add a new subnet to the existing VPC:
    ```bash
    gcloud compute networks subnets create europe-subnet \
      --network=my-vpc \
      --region=europe-west1 \
      --range=10.1.0.0/24
    ```
  - VMs in `us-central1` (subnet `10.0.0.0/24`) can communicate directly with VMs in `europe-west1` (subnet `10.1.0.0/24`) via internal IPs (same VPC).

- **C (Wrong)**: VPC Peering is for connecting **two separate VPCs**:
  - Use case: Connecting your VPC to a partner's VPC or cross-project networking.
  - Unnecessary here—you already have one VPC. Just add a subnet.

- **D (Wrong)**: Subnet CIDR ranges **cannot be changed** after creation. If you need more IPs:
  - Create a **new subnet** with a larger range.
  - Migrate workloads to the new subnet (or run both in parallel).

---

### Question 2: Firewall Rules Priority

**Scenario**: A VPC has these firewall rules:
- Rule 1 (Priority 1000): DENY all traffic from `0.0.0.0/0` on port 22.
- Rule 2 (Priority 500): ALLOW traffic from `203.0.113.0/24` on port 22.

An admin from IP `203.0.113.5` tries to SSH to a VM. What happens?

**What is the result?**

A. SSH succeeds (ALLOW rule takes precedence)  
B. SSH fails (DENY rule takes precedence)  
C. SSH fails (both rules conflict, default is DENY)  
D. SSH succeeds (implicit ALLOW SSH for VPCs)  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ Firewall rules are evaluated by **priority** (lower number = higher priority):
  - **Priority 500 (ALLOW)** is evaluated **before** Priority 1000 (DENY).
  - Source IP `203.0.113.5` matches the ALLOW rule's source range (`203.0.113.0/24`).
  - SSH **succeeds** because the first matching rule determines the outcome.
  - **Key principle**: Google Cloud firewall rules are "first match wins" based on priority.

- **B (Wrong)**: This would be true if priorities were reversed (DENY had priority 500, ALLOW had priority 1000). But in this scenario, ALLOW has higher priority.

- **C (Wrong)**: Firewall rules don't "conflict"—they're evaluated in priority order. Only one rule applies (the first match). There's no "default DENY" evaluation when multiple rules match.

- **D (Wrong)**: There's no implicit ALLOW for SSH or any service in GCP. All traffic is **denied by default** unless explicitly allowed by a firewall rule.

---

## Section 2: Load Balancing

### Question 3: Global vs Regional Load Balancer

**Scenario**: A web application serves users globally. It needs:
- HTTPS termination.
- Automatic failover to healthy backends if one region goes down.
- Route users to the closest backend for lowest latency.

**Which load balancer should be used?**

A. Regional Network Load Balancer  
B. Global HTTP(S) Load Balancer  
C. Regional Internal Load Balancer  
D. Cloud CDN alone  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Regional Network Load Balancer is:
  - **Layer 4** (TCP/UDP), not Layer 7 (HTTP/HTTPS).
  - **Regional scope**: Only routes to backends **within one region**.
  - **No HTTPS termination**: Doesn't decrypt SSL (passes encrypted traffic to backends).
  For global distribution and HTTPS, this is the wrong choice.

- **B (Correct)**: ✅ Global HTTP(S) Load Balancer provides:
  - **Global anycast IP**: Users connect to the **closest Google edge location** (100+ PoPs worldwide).
  - **Automatic routing**: Sends requests to the **closest healthy backend** (cross-region failover built-in).
  - **HTTPS termination**: Decrypts SSL at the edge (backends receive plain HTTP).
  - **Layer 7**: Can route based on URL path (`/api/*` → backend A, `/static/*` → backend B).
  This is the **standard choice** for global web apps.

- **C (Wrong)**: Internal Load Balancer is for **private** traffic **within a VPC**:
  - Not accessible from the internet.
  - Use case: Load balancing between internal tiers (frontend → backend microservices).
  The scenario requires public-facing HTTPS, so internal LB is wrong.

- **D (Wrong)**: Cloud CDN is a **caching layer**, not a load balancer:
  - Caches static content (images, CSS, JS).
  - Requires a load balancer as its origin (CDN sits **in front** of the LB).
  CDN + Global HTTPS Load Balancer is the optimal combo, but CDN alone can't route dynamic traffic.

---

### Question 4: SSL/TLS Termination

**Scenario**: A security team requires that SSL/TLS connections remain encrypted all the way to the backend VMs (end-to-end encryption). The load balancer should not decrypt traffic.

**Which load balancer supports this?**

A. Global HTTP(S) Load Balancer (terminates SSL at LB)  
B. Global Network Load Balancer (Layer 4 passthrough)  
C. Regional Internal Load Balancer  
D. Cloud CDN with SSL  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: HTTP(S) Load Balancer **terminates SSL** at the load balancer:
  - Decrypts HTTPS → sends HTTP to backends.
  - Backends receive plain HTTP (or re-encrypted with a different cert if you configure backend HTTPS).
  - Doesn't meet "SSL all the way to backends" requirement.

- **B (Correct)**: ✅ Network Load Balancer (Layer 4) does **SSL passthrough**:
  - Forwards encrypted TCP traffic directly to backends without decryption.
  - Backends handle SSL termination (VM decrypts the traffic).
  - **End-to-end encryption** preserved.
  - Trade-off: **No Layer 7 features** (no URL routing, no HTTP header inspection).

- **C (Wrong)**: Internal Load Balancer is for private VPC traffic, not internet-facing. It doesn't solve the SSL passthrough requirement.

- **D (Wrong)**: Cloud CDN requires an origin (load balancer). It's not a load balancer itself.

---

## Section 3: Hybrid Connectivity

### Question 5: Cloud VPN vs Dedicated Interconnect

**Scenario**: A company needs to connect their on-premises data center to Google Cloud with these requirements:
- Bandwidth: 5 Gbps.
- Latency: < 10ms.
- SLA: 99.9% uptime.
- Budget: Moderate (not unlimited).

**Which connectivity option should they choose?**

A. Cloud VPN (encrypted over public internet)  
B. Dedicated Interconnect (10 Gbps physical link)  
C. Partner Interconnect (via service provider)  
D. Direct Peering (BGP with Google)  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Cloud VPN has limitations:
  - **Bandwidth**: Max **3 Gbps per tunnel** (can use multiple tunnels, but complex). Scenario requires 5 Gbps.
  - **Latency**: Over public internet → unpredictable (typically 20-50ms, not guaranteed < 10ms).
  - **SLA**: 99.9% SLA **only for HA VPN** (requires 2 tunnels + 2 Cloud VPN gateways). Standard VPN is 99.0%.
  While VPN is **cheapest**, it doesn't meet bandwidth/latency requirements.

- **B (Correct)**: ✅ Dedicated Interconnect provides:
  - **Bandwidth**: 10 Gbps or 100 Gbps links (far exceeds 5 Gbps requirement).
  - **Latency**: < 10ms (private link, bypasses public internet via colocation facility).
  - **SLA**: 99.9% or 99.99% (depending on redundancy).
  - **Cost**: Higher than VPN (monthly port fee + data egress), but meets all requirements.
  This is the **enterprise-grade** solution for high-bandwidth, low-latency needs.

- **C (Wrong)**: Partner Interconnect is similar to Dedicated Interconnect but uses a **service provider** (Equinix, AT&T, etc.):
  - Use if your data center isn't near a Google colocation facility.
  - Slightly higher latency than Dedicated (extra hop through partner).
  - Good alternative to option B if colocation isn't possible, but option B is more direct.

- **D (Wrong)**: Direct Peering is for accessing **Google Workspace and YouTube**, not Google Cloud:
  - No SLA.
  - Not for VPC connectivity (can't route to your Cloud VMs).
  - Use Dedicated Interconnect for VPC access.

---

### Question 6: Cloud VPN - HA vs Classic

**Scenario**: A company currently uses a single Classic VPN tunnel for hybrid connectivity. The tunnel occasionally fails due to maintenance on the Google side, causing 15-minute outages. They need higher availability.

**What should they do?**

A. Create a second Classic VPN tunnel for redundancy  
B. Migrate to HA VPN with two tunnels and two Cloud VPN gateways  
C. Switch to Dedicated Interconnect  
D. Use Cloud VPN + Cloud Router with BGP  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Classic VPN with **two tunnels** helps, but:
  - No guaranteed active/active (manual failover).
  - **No SLA** (Classic VPN = 99.0% SLA, even with two tunnels).
  - Google is deprecating Classic VPN—migrate to HA VPN.

- **B (Correct)**: ✅ HA VPN provides a **99.99% SLA** with this setup:
  - **Two Cloud VPN gateways** (in different zones for redundancy).
  - **Two tunnels** (gateway A → peer A, gateway B → peer B).
  - **Active-active**: Both tunnels forward traffic simultaneously (load balancing).
  - **Automatic failover**: If one tunnel fails, traffic instantly reroutes to the other (no 15-minute outage).
  This is the **recommended HA configuration** for VPN.

- **C (Wrong)**: Dedicated Interconnect is overkill if the company just needs HA for VPN:
  - Much more expensive.
  - Requires colocation facility.
  If VPN bandwidth (3 Gbps/tunnel) is sufficient, HA VPN is cheaper.

- **D (Wrong)**: Cloud Router + BGP is required for **dynamic routing** (automatically learning routes), but it doesn't improve availability by itself. You still need **multiple tunnels** (HA VPN).

---

## Section 4: Network Security

### Question 7: VPC Service Controls

**Scenario**: A healthcare company stores patient data in BigQuery. Regulatory requirements mandate that data must not leave Google Cloud. A developer accidentally tries to export data to their personal Google Drive.

**How can this be prevented?**

A. Use IAM to deny BigQuery export permissions  
B. Configure VPC Service Controls to create a security perimeter around BigQuery  
C. Use Cloud Data Loss Prevention (DLP) to scan exports  
D. Enable Private Google Access  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: IAM controls **who** can export, not **where** they can export to:
  - You'd need to deny `bigquery.tables.export` permission to all users.
  - But legitimate exports to Cloud Storage (within the same project) would also be blocked.
  - IAM is "all or nothing" for permissions—can't block specific destinations.

- **B (Correct)**: ✅ VPC Service Controls create a **security perimeter**:
  - **What it does**: Defines a "secure zone" (e.g., Project A, BigQuery, Cloud Storage).
  - **Blocks**: Data movement **outside** the perimeter (e.g., exporting to personal Drive).
  - **Allows**: Data movement **within** the perimeter (BigQuery → Cloud Storage in same project).
  - **Example**: Developer tries to export BigQuery → Google Drive (outside perimeter) → **Blocked**.
  This is the **recommended solution** for data exfiltration prevention (compliance requirement for healthcare, finance).

- **C (Wrong)**: Cloud DLP **detects** sensitive data (PII, PHI) but doesn't **prevent** exports:
  - DLP scans data and marks sensitive fields.
  - It can log/alert, but it doesn't block actions.
  VPC Service Controls **actively blocks** unauthorized data movement.

- **D (Wrong)**: Private Google Access allows VMs **without public IPs** to access Google services (BigQuery, Cloud Storage):
  - Solves a different problem (connectivity, not security).
  - Doesn't prevent data exfiltration.

---

### Question 8: Cloud Armor

**Scenario**: A web application behind a Global HTTP(S) Load Balancer is experiencing a DDoS attack from IP ranges `198.51.100.0/24` and `203.0.113.0/24`. The security team needs to block these IPs immediately while allowing all other traffic.

**What is the fastest solution?**

A. Update VPC firewall rules to deny traffic from those IPs  
B. Configure Cloud Armor security policy to deny those IP ranges  
C. Use IAP (Identity-Aware Proxy) to require authentication  
D. Enable HTTP(S) Load Balancer's built-in DDoS protection  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: VPC firewall rules operate at the **VPC level** (protecting VMs):
  - The attack hits the **load balancer** before reaching VMs.
  - Firewall rules don't protect the load balancer itself (LB is outside the VPC).
  - Traffic would still consume load balancer bandwidth (costly, slow).

- **B (Correct)**: ✅ Cloud Armor is designed for **edge protection**:
  - Attaches to the **HTTP(S) Load Balancer** (Layer 7).
  - **Blocks requests at the edge** (before they reach backends).
  - **IP allowlist/denylist**: Block `198.51.100.0/24` and `203.0.113.0/24`.
  - **GeoIP blocking**: Can also block entire countries.
  - **Rate limiting**: Limit requests per IP (e.g., 100 req/min).
  - **Deploy time**: Seconds (instant policy update).
  This is the **standard DDoS mitigation** tool for GCP.

- **C (Wrong)**: IAP (Identity-Aware Proxy) requires users to **authenticate** (Google account, OAuth):
  - Use case: Internal apps that need user authentication.
  - **Doesn't block bots/DDoS**: Attackers can still flood the login page.
  IAP is for access control, not DDoS mitigation.

- **D (Wrong)**: Global HTTP(S) Load Balancer has **built-in** DDoS protection (absorbs large traffic spikes), but:
  - It's **automatic** (always on), not something you "enable."
  - For **targeted attacks** (specific IPs), you need Cloud Armor to create custom rules.

---

## Section 5: Advanced Networking

### Question 9: Shared VPC

**Scenario**: A large organization has 10 teams, each with their own GCP project. The network team wants to centrally manage the VPC (subnets, firewall rules) while allowing each team to deploy their own VMs in their projects.

**What should they configure?**

A. VPC Peering between all 10 projects  
B. Shared VPC with host project and service projects  
C. Each team creates their own VPC and connects with Cloud VPN  
D. Use a single project for all teams  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: VPC Peering connects two VPCs bidirectionally, but:
  - Requires peering **every pair** of projects (10 projects = 45 peering connections in a full mesh).
  - **No centralized management**: Each project manages its own VPC firewall rules.
  - Transitive peering is **not supported** (if A peers with B, and B peers with C, A cannot reach C directly).

- **B (Correct)**: ✅ Shared VPC is designed for **centralized network management**:
  - **Host project**: The network team creates the VPC, subnets, and firewall rules here (single source of truth).
  - **Service projects**: Teams attach their projects to the host project's VPC. They deploy VMs in shared subnets but cannot modify network settings.
  - **Benefits**:
    - Centralized billing (all network egress from one project).
    - Centralized security (firewall rules managed by network team).
    - Teams maintain project-level isolation for IAM (can't see each other's VMs).

- **C (Wrong)**: Creating separate VPCs and connecting with Cloud VPN is overengineering:
  - VPN is for **hybrid** connectivity (on-prem ↔ cloud), not for connecting GCP projects.
  - Adds latency and cost.
  - No centralized management.

- **D (Wrong)**: Single project for all teams violates **security** and **billing** best practices:
  - No IAM isolation (all teams see all resources).
  - Billing can't be attributed to individual teams.
  - Difficult to enforce resource quotas per team.

---

### Question 10: Private Google Access

**Scenario**: A VM in a VPC has **no external IP**. The application running on the VM needs to access Cloud Storage and BigQuery.

**What must be enabled?**

A. Cloud NAT  
B. Private Google Access  
C. VPC Peering  
D. Public IP on the VM  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Cloud NAT allows VMs **without external IPs** to access the **public internet** (e.g., download packages from `apt.com`):
  - Not needed for Google services (BigQuery, Cloud Storage), which have internal endpoints.
  - Use Cloud NAT for non-Google destinations.

- **B (Correct)**: ✅ Private Google Access allows VMs **without external IPs** to access Google APIs:
  - **How it works**: Google services (BigQuery, Cloud Storage) have **internal IP endpoints** (`private.googleapis.com`).
  - **Enable per subnet**: `gcloud compute networks subnets update <subnet> --enable-private-ip-google-access`
  - **Benefits**: No egress charges (traffic stays on Google's network), no public IP needed.

- **C (Wrong)**: VPC Peering connects two VPCs, not VMs to Google services.

- **D (Wrong)**: Adding a public IP works but:
  - Incurs **egress charges** (traffic to BigQuery/Storage goes over the internet).
  - Increases attack surface (VM is directly reachable from the internet if firewall allows).
  Private Google Access is the **recommended secure approach**.

---

## Answer Key Summary

1. **B** - Create subnet in new region (VPCs are global)
2. **A** - ALLOW rule (priority 500) wins over DENY (priority 1000)
3. **B** - Global HTTP(S) Load Balancer for global HTTPS
4. **B** - Network Load Balancer for SSL passthrough
5. **B** - Dedicated Interconnect for 5 Gbps + low latency
6. **B** - HA VPN for 99.99% SLA
7. **B** - VPC Service Controls to prevent data exfiltration
8. **B** - Cloud Armor for DDoS mitigation
9. **B** - Shared VPC for centralized network management
10. **B** - Private Google Access for VMs without external IP

---

## Study Tips

1. **VPC Basics**: VPCs are global, subnets are regional. You can't change subnet CIDR after creation.
2. **Firewall Rules**: Priority (lower number = higher priority). First match wins.
3. **Load Balancers**: 
   - Global HTTP(S) = Layer 7, HTTPS termination, global routing.
   - Network LB = Layer 4, SSL passthrough, regional.
4. **Hybrid Connectivity**: 
   - VPN = < 3 Gbps, encrypted.
   - Dedicated Interconnect = 10+ Gbps, low latency.
5. **Security**: 
   - Cloud Armor = DDoS protection at LB.
   - VPC Service Controls = Data exfiltration prevention.
6. **Shared VPC**: Host project (network team) + service projects (app teams).
7. **Private Google Access**: VMs without public IPs can reach Google services.
