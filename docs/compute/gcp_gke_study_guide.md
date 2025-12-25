# GCP Kubernetes Engine (GKE) Study Guide for PCA

Google Kubernetes Engine (GKE) is a managed, production-ready environment for running containerized applications. For the Professional Cloud Architect (PCA) exam, the focus is on **architectural decisions**, **security**, and **operational efficiency**.

---

## 0. Kubernetes vs. GKE: The Distinction
| Layer | **Kubernetes (Internal Core)** | **GKE (GCP Integration)** |
| :--- | :--- | :--- |
| **Logic** | API Server, Scheduler, Controller Manager. | Managed Control Plane, Auto-Upgrades. |
| **Network** | Pod-to-Pod communication (Kube-proxy). | **VPC-Native (Alias IP)**, Global Load Balancers. |
| **Storage** | Persistent Volumes (CSI). | **Google Persistent Disks**, Filestore. |
| **Security** | RBAC, Network Policies. | **Workload Identity**, IAM Integration, Binary Authorization. |
| **Operations** | `kubectl apply` lifecycle. | **Autopilot Scale**, Cluster Autoscaler, Cloud Monitoring. |

---

## 0. GKE and Compute Engine: The Relationship

One of the most important concepts for the PCA exam is understanding that **GKE is built on top of Compute Engine**.

### 💡 Key Concept: Nodes are just VMs!
It is a common PCA exam mistake to think GKE is its own hardware.
- **GKE Nodes = Compute Engine VMs**: They are managed by a **Managed Instance Group (MIG)** under the hood.
- **Autopilot Invisibility**: In Autopilot, Google **hides these VMs** from your `Compute Engine > VM Instances` console. You can only see them via `kubectl get nodes`.
- **Standard Visibility**: In GKE Standard, the VMs are fully visible and editable in your console.
- **Why this matters for Security**: Organization Policies still apply even if the VMs are "hidden" from the UI.
- **Why this matters for Scaling**: Autopilot scales by adding more VMs (Nodes) to the cluster when pods have no place to sit.

*   **Nodes are VMs**: Every "Node" in your GKE cluster is actually a Compute Engine VM instance.
*   **Infrastructure Management**: When you create a GKE cluster, GKE uses **Managed Instance Groups (MIGs)** behind the scenes to provision and manage these VMs.
*   **The Control Plane**: GKE manages the Kubernetes Control Plane (the "brains") for you as a managed service. You only interact with the Nodes (the "workers").
*   **Abstraction levels**:
    *   **Compute Engine**: Bare VMs. You manage OS, patches, and runtime. (IaaS)
    *   **GKE Standard**: Managed Kubernetes. You see the VMs in your console and can customize them. (Hybrid IaaS/PaaS)
    *   **GKE Autopilot**: Fully-managed. Google hides the VMs and scales based on Pod needs. (PaaS-like experience for Containers)

**PCA Tip**: If an exam question asks for "Maximum control over the underlying OS or kernel," go with **Compute Engine**. If it asks for "Container orchestration with control over VM machine types," go with **GKE Standard**.

---

## 0.1 Underlying Technology: Hypervisors vs. Containers

To understand GKE, you must distinguish between the "House" (VM) and the "Apartment" (Container).

### The Hypervisor (Virtual Machine Layer)
*   **What it is**: Software that virtualizes **hardware**. It slices one physical server into multiple VMs.
*   **Google's Tech**: Google uses a hardened version of **KVM** (Type 1 Bare Metal Hypervisor).
*   **Isolation**: High. Each VM has its own **OS Kernel**. If one VM's kernel crashes, others are unaffected.
*   **Speed**: Slow to boot (minutes).

### The Container (Kubernetes Layer)
*   **What it is**: Software that virtualizes the **Operating System**.
*   **Isolation**: Process-level. All containers on a node **share the same host OS kernel**.
*   **Speed**: Faster to boot (seconds).
*   **GKE Security**: In GKE, containers run *inside* a VM. This gives you two layers of isolation: Google's Hypervisor (protecting the VM) and Namespaces/Cgroups (protecting the containers).

---

## 1. Cluster Modes: Standard vs. Autopilot

Choosing the right mode is a common exam scenario.

| Feature | **GKE Autopilot** (Recommended) | **GKE Standard** |
| :--- | :--- | :--- |
| **Management** | Google manages nodes and infrastructure. | You manage nodes and configuration. |
| **Scaling** | Automatic scaling based on Pod specs. | Manual or Cluster Autoscaler (CA). |
| **Pricing** | Pay for Pod resources (CPU, Mem, Disk). | Pay for VM instances and management fee. |
| **Control** | Opinionated, secure by default. | Full control over node configuration. |
| **Use Case** | Most production workloads; "hands-off". | Specialized hardware (GPUs), specific kernels. |
| **Availability** | **Regional** by default (Higher SLA). | Zonal or Regional. |
| **Networking** | **VPC-Native** enforced. | VPC-Native optional (but recommended). |

> **UI Tip**: If you don't see "GKE Standard" when creating a cluster, look for the **"SWITCH TO STANDARD CLUSTER"** button in the top-right corner of the Autopilot configuration page.


---

## 2. Cluster Topology & Availability

### Zonal Clusters
- Single control plane in one zone.
- **Single-zone**: Nodes in the same zone.
- **Multi-zonal**: Nodes spread across multiple zones in a region.
- *Risk*: If the zone with the control plane goes down, you lose management capability (though existing pods keep running).

### Regional Clusters (Best Practice for PCA)
- Control plane replicas spread across three zones in a region.
- High availability for the Kubernetes API.
- Zero-downtime upgrades.
- *Cost*: Management fee is higher (unless using the Free Tier).

---

## 3. GKE Architecture Details

### The Control Plane (Google Managed)
The "Brain" of the cluster. In GKE, Google manages this entirely.
- **API Server**: Entry point for all commands (`kubectl`).
- **etcd**: Source of Truth - distributed key-value store for cluster state.
- **Scheduler**: Decides which **Node** a newly created **Pod** should live on.
- **Controller Manager**: Regulates the state (Self-healing).

### The Data Plane (The Worker Nodes)
The actual VMs where your code runs.
- **Kubelet**: Agent on each node ensuring containers are running in Pods.
- **Kube-proxy**: Manages network rules (Pod-to-Pod communication).
- **Container Runtime**: GKE uses **`containerd`** (formerly Docker).

---

### 3.1 Node Pools (Standard Mode)
In Standard mode, you manage nodes via **Node Pools**. A node pool is a subset of nodes within a cluster that all have the same configuration.

**Key Benefits for PCA Scenarios:**
*   **Heterogeneous Hardware**: Mix machine types (e.g., one pool for high-CPU, one for GPU).
*   **Cost Optimization**: Use **Spot/Preemptible VMs** for one pool (batch jobs) and **On-Demand** for another (web servers).
*   **Isolation**: Use **Taints and Tolerations** to ensure specific pods (like monitoring tools) run on their own dedicated nodes.
*   **Independent Scaling**: The Cluster Autoscaler can scale each pool independently (e.g., scaling the GPU pool to 0 when not in use).
*   **Upgrade management**: Create a new pool with a newer K8s version, migrate workloads, then delete the old pool.

---

## 4. Workload Resources (The Managers)


| Resource | Purpose | PCA Use Case |
| :--- | :--- | :--- |
| **Deployment** | Stateless replication & updates. | Web APIs, Microservices. |
| *Note* | *Manages ReplicaSets under the hood. Use this for Rolling Updates.* | |
| **StatefulSet** | Stable identities & persistent storage. | Databases, Kafka. |
| **DaemonSet** | One pod on every node. | Logging agents, Monitoring. |
| **Job** | Run-to-completion tasks. | Batch processing, Migrations. |
| **CronJob** | Scheduled tasks. | Backups, Reports. |

---

## 5. GKE Networking (Critical)

### VPC-Native Clusters (Alias IP)
- **Standard now**: Uses Alias IP ranges for Pods and Services.
- **Benefits**: Scalability, direct VPC integration, no more "route limits".
- **Required for**: Shared VPC, Private Google Access, Cloud Interconnect.

### Private Clusters
- Nodes do **not** have public IP addresses.
- Control plane can be public or private (via Authorized Networks).
- Requires a **Cloud NAT** for nodes to access the internet (e.g., for pulling images from external registries).

### Services & Ingress
- **ClusterIP**: Internal only.
- **NodePort**: Exposes on a port on every node (rarely used in GCP).
- **LoadBalancer**: Creates a Regional L4 Network Load Balancer.
- **Ingress**: Uses the **GKE Ingress Controller** to create a Global L7 HTTP(S) Load Balancer. Support for Google-managed SSL and Identity-Aware Proxy (IAP).

---

## 6. Security Framework

### Workload Identity (Top Exam Topic)
- **Problem**: Mounting Service Account keys as secrets is insecure.
- **Solution**: Maps a Kubernetes Service Account (KSA) to a Google Service Account (GSA).
- Pods inherit the GSA permissions automatically without keys.

### Binary Authorization
- Ensures only "trusted" images are deployed.
- Integrates with Artifact Analysis and CI/CD pipelines.

### Shielded GKE Nodes
- Hardened nodes with Secure Boot and Integrity Monitoring.

---

## 7. Storage Options

- **Persistent Disk (PD)**: Standard block storage. Use **Regional PD** for high availability across zones.
- **Filestore**: Managed NFS for applications requiring shared read/write access (RWX).
- **Cloud Storage FUSE**: For massive scale / unstructured data access as a filesystem.
- **Backup for GKE**: Fully managed service to backup and restore GKE workloads (including persistent volumes).
    - *Exam Tip*: "Disaster recovery for Kubernetes state" -> **Backup for GKE**. comparison: Do not use generic snapshots if you need application-consistent backups.

---

## 8. Optimization & Best Practices

- **Preemptible / Spot VMs**: Use for fault-tolerant batch jobs to save up to 80% cost.
- **Horizontal Pod Autoscaler (HPA)**: Scales pods based on CPU/Mem.
- **Vertical Pod Autoscaler (VPA)**: Recommends/sets the right resource requests.
- **Cluster Autoscaler (CA)**: Adds/removes nodes based on pod demand.
- **Taints and Tolerations**: Keep specific workloads on specific nodes (e.g., GPU pods on GPU nodes).

---

## 9. PCA Decision Matrix

| Requirement | Recommendation |
| :--- | :--- |
| "Minimize operational overhead" | **GKE Autopilot** |
| "Zero-downtime during control plane upgrades" | **Regional Cluster** |
| "Isolate workloads from the public internet" | **Private Cluster + Cloud NAT** |
| "Access BigQuery from a Pod securely" | **Workload Identity** |
| "Shared storage for multiple pods (RWX)" | **Filestore (NFS)** |
| "Massive scale web traffic with SSL termination" | **GKE Ingress (Global L7 LB)** |

---

## 10. Study Resources & Tools

*   **Google Cloud Skills Boost (Official)**: The primary source for hands-on labs (formerly Qwiklabs).
*   **Killercoda**: Great for CKA/CKAD style interactive Kubernetes practice.
*   **Cloud Shell**: Your best friend for testing `gcloud` and `kubectl` commands for free.
*   ⚠️ **Katacoda Warning**: Katacoda was discontinued in 2022. If you see it mentioned in older study guides, ignore it and use Skills Boost or Killercoda instead.

---

## 11. Tricky Scenarios & PCA Exam Tips

These are high-probability scenarios often encountered on the PCA exam.

### 💡 High-Availability (HA) Traps
*   **The Scenario:** "Ensure the Kubernetes API remains available even during a total zone failure."
*   **The Correct Choice:** **Regional Cluster**. In a Zonal cluster, the Control Plane lives in only one zone. If that zone dies, you can't run `kubectl` or manage the cluster until it's back.
*   **The "Zero Downtime" Choice:** Use **Regional Clusters** and **Multiple Node Pools** to ensure updates don't kill all instances of a pod at once.

### 💡 The "Secret" to Google Cloud Access
*   **The Scenario:** "A pod needs to upload files to a Cloud Storage bucket with the least possible management of credentials."
*   **The Correct Choice:** **Workload Identity**. 
*   **Why?** Service Account JSON keys are "long-lived" and a major security risk. Workload Identity uses short-lived tokens and maps K8s Service Accounts (KSA) to GCP Service Accounts (GSA).

### 💡 Troubleshooting Pod Failures
*   **Scenario: Pod is `Pending` forever.**
    *   **Cause:** Insufficient resources (CPU/RAM) in the cluster.
    *   **Fix:** Check **Cluster Autoscaler** settings or increase Node size.
*   **Scenario: `ImagePullBackOff`**
    *   **Cause:** Typo in the image name OR the GKE service account doesn't have permissions to the **Artifact Registry**.
*   **Scenario: `CrashLoopBackOff`**
    *   **Cause:** The application inside the container is crashing (check logs with `kubectl logs [POD_NAME]`). Common reasons: missing environment variables or database connection errors.

### 💡 Storage Nuances (RWO vs RWX)
*   **Requirement:** "Multiple pods on different nodes must write to the same shared directory."
*   **Incorrect:** Persistent Disk (standard PD). It is **ReadWriteOnce (RWO)**—only one node can mount it.
*   **Correct:** **Filestore (NFS)** or **Google Cloud Storage (via FUSE)**. These support **ReadWriteMany (RWX)**.

### 💡 Private Cluster Connectivity
*   **Problem:** "My nodes in a Private Cluster cannot download updates from the internet."
*   **Solution:** **Cloud NAT**. Nodes in a private cluster have no external IPs, so they need a NAT gateway to initiate outbound connections for updates/patches.

### 💡 Modern Image Registry
*   **The Transition:** Google is moving from **Container Registry (GCR)** to **Artifact Registry (AR)**.
*   **Exam Tip:** If both are options, **Artifact Registry** is the more modern, regional, and recommended choice for architectural designs.
