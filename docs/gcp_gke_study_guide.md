# GCP Kubernetes Engine (GKE) Study Guide for PCA

Google Kubernetes Engine (GKE) is a managed, production-ready environment for running containerized applications. For the Professional Cloud Architect (PCA) exam, the focus is on **architectural decisions**, **security**, and **operational efficiency**.

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

## 3. GKE Networking (Critical)

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

## 4. Security Framework

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

## 5. Storage Options

- **Persistent Disk (PD)**: Standard block storage. Use **Regional PD** for high availability across zones.
- **Filestore**: Managed NFS for applications requiring shared read/write access (RWX).
- **Cloud Storage FUSE**: For massive scale / unstructured data access as a filesystem.

---

## 6. Optimization & Best Practices

- **Preemptible / Spot VMs**: Use for fault-tolerant batch jobs to save up to 80% cost.
- **Horizontal Pod Autoscaler (HPA)**: Scales pods based on CPU/Mem.
- **Vertical Pod Autoscaler (VPA)**: Recommends/sets the right resource requests.
- **Cluster Autoscaler (CA)**: Adds/removes nodes based on pod demand.
- **Taints and Tolerations**: Keep specific workloads on specific nodes (e.g., GPU pods on GPU nodes).

---

## 7. PCA Decision Matrix

| Requirement | Recommendation |
| :--- | :--- |
| "Minimize operational overhead" | **GKE Autopilot** |
| "Zero-downtime during control plane upgrades" | **Regional Cluster** |
| "Isolate workloads from the public internet" | **Private Cluster + Cloud NAT** |
| "Access BigQuery from a Pod securely" | **Workload Identity** |
| "Shared storage for multiple pods (RWX)" | **Filestore (NFS)** |
| "Massive scale web traffic with SSL termination" | **GKE Ingress (Global L7 LB)** |

---

## Hands-On Exercise Ideas
1.  **Deploy a "Hello World" Container**: Use `kubectl` to create a deployment and expose it via a LoadBalancer.
2.  **Configure Workload Identity**: Bind a KSA to a GSA and verify access to Cloud Storage.
3.  **Horizontal Autoscaling**: Use a load generator to trigger HPA and Cluster Autoscaler.
