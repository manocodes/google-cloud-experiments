# Google Cloud Compute Engine Study Plan (PCA Focused)

## Goal
Master the nuances of Google Compute Engine (GCE) specifically for the Professional Cloud Architect exam. The exam focuses less on "how to click the buttons" and more on "when to use what feature" and "architecture decision making".

## Study Modules

### 1. VM Instances & Machine Types
**Key Concepts:**
*   **Machine Families:**
    *   *General Purpose (E2, N2, N2D)*: Default choice. Balanced Web servers, App servers, DBs.
    *   *Compute Optimized (C2)*: High performance computing (HPC), gaming, ad serving.
    *   *Memory Optimized (M1, M2)*: Large in-memory databases (SAP HANA, Redis).
    *   *Accelerator Optimized (A2)*: ML/AI (GPUs).
*   **Preemptible / Spot VMs:**
    *   *Exam Gold*: Short-lived, batch processing, fault-tolerant workloads.
    *   *Terms*: Spot VMs are the modern replacement for Preemptible, but the exam may use both terms.
    *   *Max duration*: 24h (Preemptible) vs No limit but can be killed anytime (Spot).
    *   *Cost savings*: 60-91%.
*   **Sole-Tenant Nodes:**
    *   Dedicated hardware.
    *   *Use case*: BYOL (Bring Your Own License) requirements, strict compliance/isolation needs.

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

### 4. Operations & Lifecycle
**Key Concepts:**
*   **Live Migration:**
    *   GCP differentiator. VMs move to new hardware without rebooting during maintenance.
    *   *Exam Note*: Reduces downtime (Host Maintenance Policy: Migrate).
*   **Availability Policies:**
    *   *On Host Maintenance*: Migrate (Default) or Terminate.
    *   *Automatic Restart*: True (Default).
*   **OS Login:**
    *   The "secure" way to manage SSH access using IAM roles instead of managing SSH keys in metadata.
    *   Connects SSH access to the corporate identity (useful for deprovisioning).

### 5. Cost Optimization
**Key Concepts:**
*   **Sustained Use Discounts (SUD):** Automatic. The longer you run, the cheaper it gets (N1/N2 mostly).
*   **Committed Use Discounts (CUD):** Contract (1 or 3 years). No upfront payment required on GCP (unlike AWS RIs).
*   **Rightsizing Recommendations:** Stackdriver/Monitoring feature to suggest smaller instance types based on usage.

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
