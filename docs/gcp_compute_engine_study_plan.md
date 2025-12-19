# Google Cloud Compute Engine Study Plan (PCA Focused)

## Goal
Master the nuances of Google Compute Engine (GCE) specifically for the Professional Cloud Architect exam. The exam focuses less on "how to click the buttons" and more on "when to use what feature" and "architecture decision making".

## Study Modules

### 1. VM Instances & Machine Types
**Key Concepts:**
*   **Machine Families:**
    *   *General Purpose (E2, N2, N2D)*: Default choice. Balanced Web servers, App servers, DBs.
    *   *Compute Optimized (C2)*: High performance computing (HPC), gaming, ad serving.
    *   *Tau (T2D, T2A)*: Scale-out workloads (Web servers, microservices). High price-performance.
    *   *Memory Optimized (M1, M2)*: Large in-memory databases (SAP HANA, Redis).
    *   *Accelerator Optimized (A2)*: ML/AI (GPUs).

| Family | Sub-type | Best For | Key Exam Differentiator |
| :--- | :--- | :--- | :--- |
| **General** | N2 / E2 | Balanced, Dev/Test | Standard default choice. |
| **Compute** | C2 | HPC, Gaming | Maximize per-thread performance. |
| **Tau** | **T2D** | Scale-out Web/Microservices | **Best Price-Performance (x86)**. |
| **Tau** | **T2A** | Arm-compatible apps | **Cost efficiency on Arm architecture**. |
| **Memory** | M2 | SAP HANA, Redis | Maximize RAM per vCPU. |
*   **Preemptible / Spot VMs:**
    *   *Exam Gold*: Short-lived, batch processing, fault-tolerant workloads.
    *   *Terms*: Spot VMs are the modern replacement for Preemptible, but the exam may use both terms.
    *   *Max duration*: 24h (Preemptible) vs No limit but can be killed anytime (Spot).
    *   *Cost savings*: 60-91%.
*   **Sole-Tenant Nodes:**
    *   Dedicated physical hardware for your use only.
    *   **Workflow**: Requires creating a **Node Template** -> **Node Group** -> **VM Placement**.
    *   **Node Affinity labels**: Used to "pin" or "affinitize" VMs to specific nodes or groups.
    *   **Live Migration**: Supported *within* the sole-tenant group to maintain availability.
    *   *Key Use Case*: **BYOL** (Windows/Oracle licenses tied to physical cores) and extreme **Compliance** (Physical isolation required).

### 2. Instance Groups (The "Scalability" Unit)
**Key Concepts:**
*   **Managed Instance Groups (MIGs):**
    *   Identical VMs created from an Instance Template.
    *   **Stateless vs. Stateful:**
        *   **Stateless MIGs (Standard)**: The "Cattle" approach. VMs are replaceable terminators. Logic is "process and forget". State is stored in Cloud SQL/Storage.
        *   **Stateful MIGs**: The "Pet" approach. Preserves the disk (data) and IP address of a VM even if it is recreated. Use this for legacy apps that save data to local disk or databases running on GCE.
    *   **Externalizing State (Deep Dive)**: [stateful_vs_stateless.md](./stateful_vs_stateless.md) - **Read this** to understand why "Stateless App + Stateful Database" is the exam's preferred architecture.
    *   **Features**: Autoscaling, Auto-healing (health checks), Regional (Multi-zone) vs Zonal availability.
*   **Unmanaged Instance Groups:**
    *   Dissimilar VMs.
    *   *Use case*: Legacy apps where you can't template the instances. Not recommended for modern architectures.
    *   *Limitation*: No autoscaling, no auto-healing (managed by load balancer health checks only, not the group itself).

### 3. Compute Storage
**Key Concepts:**
*   **Persistent Disk (PD):**
    *   Network block storage (not physically attached).
    *   *Zonal PD*: Standard if you don't need HA across zones.
    *   *Regional PD*: Replicated across 2 zones in same region. **Critical for HA Database architectures on GCE.**
*   **Local SSD:**
    *   Physically attached to the server. Extreme IOPS.
    *   *Ephemeral*: Data is lost if VM stops (mostly). Good for scratch data, cache.
    *   *Exam Trap*: Never use Local SSD for durable storage.
*   **Snapshots:**
    *   Incremental backups of PDs.
    *   Can be stored regionally or multi-regionally.
*   **Filestore (Managed NFS):**
    *   *Shared File System*: Multiple VMs can mount the same drive via NFS.
    *   *Exam Tip*: Use for legacy apps that need a shared `POSIX` file system (e.g., shared web content, media processing).
*   **Cloud Storage (GCS) Buckets:**
    *   *Object Storage*: Not a real disk. Accessed via API or `gcsfuse`.
    *   *Exam Tip*: Use for high-latency, massive scale, or "Stateless" apps where data is global (images, logs, static assets).

### 4. Operations & Lifecycle
**Key Concepts:**
*   **Live Migration:**
    *   GCP differentiator. VMs move to new hardware without rebooting during maintenance.
    *   *Exam Note*: Reduces downtime (Host Maintenance Policy: Migrate).
    *   **The Nuance (Crucial for Exam):**
        *   **Local SSD**: *Can* be live-migrated (data is preserved).
        *   **GPUs**: *Cannot* be live-migrated. The VM must be set to `Terminate and Restart`.
*   **Availability Policies:**
    *   *On Host Maintenance*: Migrate (Default) or Terminate.
    *   *Automatic Restart*: True (Default).
*   **OS Login:**
    *   The "secure" way to manage SSH access using IAM roles instead of managing SSH keys in metadata.
    *   Connects SSH access to the corporate identity (useful for deprovisioning).

### 5. Cost Optimization
**Key Concepts:**
*   **Sustained Use Discounts (SUD):** Automatic. The longer you run, the cheaper it gets (N1/N2 mostly).
*   **Committed Use Discounts (CUD):** Contract for 1 or 3 years.
    *   **Resource-based CUD**: Commit to a specific amount of **vCPU and RAM** in a specific region. Best for "steady-state" predictable workloads.
    *   **Spend-based (Flexible) CUD**: Commit to a specific **hourly spend** ($/hr). More flexible; covers different machine families and even multiple services (like Cloud SQL).
    *   *Exam Tip*: CUDs are **not** automatic (unlike SUD). You must proactively purchase them.
*   **Rightsizing Recommendations:** Stackdriver/Monitoring feature to suggest smaller instance types based on usage.

### 6. Security & Hardening
**Key Concepts:**
*   **Shielded VMs:** Hardened VMs to prevent boot-level malware (Rootkits).
    *   *Secure Boot*: Only boots signed code.
    *   *vTPM*: Virtual security chip for storing secrets/keys.
    *   *Integrity Monitoring*: Alerts if the boot baseline changes.
*   **Confidential VMs:** Protects data **in-use** by encrypting RAM. Use for highly sensitive PII or financial data where even the cloud provider shouldn't see memory contents.

### 7. Networking for Compute Engine
**Key Concepts:**
*   **Global VPC / Regional Subnets:** The VPC is global (reaches across continents), but VMs live in a specific **Regional Subnet**.
*   **Private Google Access (PGA):**
    *   *Scenario*: VM has no External IP but needs to upload to Cloud Storage (GCS).
    *   *Mechanism*: Enable PGA on the **Subnet** level.
*   **Cloud NAT:**
    *   *Scenario*: VM has no External IP but needs to download OS updates from the internet.
    *   *Mechanism*: Cloud NAT allows egress (outbound) without allowing ingress (inbound).
*   **Firewall Rules (Tags vs. Service Accounts):**
    *   *Network Tags*: Easy to use, but anyone with compute update permission can change tags.
    *   *Service Accounts*: **The Secure way.** Define a rule as "Allow `Target: Web-SA` to receive traffic from `Source: LB-SA`". Even if the VM's tag changes, the rule stays bound to the identity.
*   **Network Service Tiers:**
    *   *Premium Tier*: Traffic stays on Google's backbone (Global Fiber). Default & Fast.
    *   *Standard Tier*: Traffic enters the public internet as soon as it leaves the GCP region. Cheaper but higher latency.
*   **Alias IP Ranges:** Allows you to assign multiple internal IP addresses to a single VM. Historically critical for containers (GKE).

#### Web-Tier Exam Tips (NGINX/Frontend)
*   **Startup Scripts**: On the exam, if you need to install NGINX on 100 VMs, you do it via an **Instance Template** using a **Startup Script** (Metadata: `startup-script`).
*   **Health Checks**: GCLB (Load Balancer) doesn't just check if the VM is "on"; it checks if NGINX is responding correctly (usually on port 80/443).
*   **SSL Termination**: While NGINX can handle SSL, the "Google Recommended" architecture is to terminate SSL at the **Global HTTP(S) Load Balancer** to offload the work from your VMs.

### 8. Workload Signal Dictionary (Trigger Keywords)
Match these keywords in exam questions to the correct architectural choice:

| Keyword | GCP Meaning / Solution | Why? |
| :--- | :--- | :--- |
| **SAP HANA** | **Memory-Optimized (M-series)** | HANA is an in-memory DB; needs massive RAM. |
| **CUDA / NVIDIA** | **Accelerator-Optimized (A-series)** | Signals GPU workloads for ML or complex math. |
| **POSIX compliant** | **Filestore (NFS)** | Standard disks aren't shared; GCS isn't POSIX. |
| **Redis / Memcached** | **Memorystore** | Managed in-memory data store for caching. |
| **Lift-and-Shift** | **Compute Engine (VMs)** | Moving legacy apps as-is without refactoring. |
| **Monolithic** | **Compute Engine (VMs)** | Single large app that can't be containerized yet. |
| **Windows / Oracle** | **Sole-Tenant Nodes** | Usually implies complex per-core licensing (BYOL). |
| **Batch / Stateless** | **Spot VMs** | Workloads that can be interrupted to save cost. |
| **NGINX / Apache** | **Web-tier (MIG)** | High-performance reverse proxy for frontend traffic. |

## Practical "Mini-Labs" Checklist
Don't just read. Do these to cement the knowledge:
1.  [ ] **Create a Web Server MIG**: Create an Instance Template (with a startup script installing Apache), then a Zonal MIG.
2.  [ ] **Break it & Heal it**: Delete a VM in the MIG manually. Watch the Auto-healer bring it back.
3.  [ ] **Regional HA**: Create a Regional MIG. Simulate a zone failure (if possible) or just verify VMs are spread across zones.
4.  [ ] **Access Control**: Enable OS Login on a project/instance and try SSH-ing with a user who has `Compute Viewer` but not `Compute OS Login` role (it should fail).
5.  [ ] **Spot VM Test**: Spin up a Spot VM and see how the creation process differs.

## Exam "Watch Out" Scenarios
*   **Scenario**: "Application requires high availability and must survive a zonal outage."
    *   **Solution**: **Regional** Managed Instance Group.
*   **Scenario**: "Batch processing job runs every night, takes 3 hours, can resume if interrupted."
    *   **Solution**: **Spot VMs** (or Preemptible).
*   **Scenario**: "Legacy application needs specific MAC address or physically dedicated hardware for licensing."
    *   **Solution**: **Sole-tenant Nodes**.
*   **Scenario**: "Maximize IOPS for a temporary scratch disk."
    *   **Solution**: **Local SSD**.
*   **Scenario**: "Need to update the OS image for all instances in a MIG with zero downtime."
    *   **Solution**: Perform a **Rolling Update** on the Managed Instance Group.
*   **Scenario**: "Multiple VMs need a shared file system that is POSIX compliant."
    *   **Solution**: **Filestore**.
*   **Scenario**: "Global application needs to store and serve millions of user profile images cheaply."
    *   **Solution**: **Cloud Storage (GCS)**.
*   **Scenario**: "Ensure that a VM's boot process hasn't been compromised and that the kernel is trusted."
    *   **Solution**: **Shielded VM** with **Integrity Monitoring**.
*   **Scenario**: "A machine learning VM with an attached GPU needs to stay available during hardware maintenance."
    *   **Solution**: **Note: It cannot live-migrate.** You must design the app to handle a restart (e.g., using a MIG with Auto-healing and a "Terminate" maintenance policy).
*   **Scenario**: "You have a predictable, 24/7 production database workload and want the maximum possible discount."
    *   **Solution**: **3-year Resource-based Committed Use Discount (CUD)**.
*   **Scenario**: "You want to reduce costs across multiple machine families (N2, N1, C2) and potentially across multiple projects."
    *   **Solution**: **Spend-based (Flexible) CUD**.
*   **Scenario**: "Internal-only VMs need to access Google BigQuery securely without using public internet IPs."
    *   **Solution**: Enable **Private Google Access** on the subnet.
*   **Scenario**: "A fleet of backend VMs with no external IPs needs to download security patches from an external repository."
    *   **Solution**: **Cloud NAT**.
*   **Scenario**: "You need to minimize network latency for global users accessing a web app hosted on GCE."
    *   **Solution**: **Premium Network Service Tier**.
*   **Scenario**: "A large organization wants to centralize firewall and IP management in one project but allow other projects to use the network."
    *   **Solution**: **Shared VPC**.
