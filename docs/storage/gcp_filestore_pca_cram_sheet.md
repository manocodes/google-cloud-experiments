# GCP Cloud Filestore - PCA Exam Cram Sheet

## 1. Fundamentals
Fully managed **NFS (Network File System)** server for applications that need a shared filesystem.
*   **Protocol:** NFSv3 (Linux compatible).
*   **Access:** Mounted by thousands of COMPUTE instances (GCE, GKE) simultaneously.
*   **The "Why":** For "Lift and Shift" legacy apps that hardcode file paths names like `/data/shared/` and expect POSIX compliance (read/write/lock).

---

## 2. Service Tiers (CRITICAL)
Memorize the use cases. The exam will ask you to choose the "Most cost-effective" or "Highest performance" tier.

| Tier | Use Case | Performance | Capacity Range | Availability |
| :--- | :--- | :--- | :--- | :--- |
| **Basic HDD** | File sharing, Web hosting, simple backups. **Cost Optimized**. | Low | 1 TB - 63.9 TB | 99.9% (Zonal) |
| **Basic SSD** | High-performance apps, random I/O. | Medium/High | 2.5 TB - 63.9 TB | 99.9% (Zonal) |
| **Enterprise** | **Critical Apps** (SAP), High Availability. | High | 1 TB - 10 TB | **99.99% (Regional)** |
| **High Scale** | **HPC**, Video Rendering, Genome Sequencing. Massive throughput. | **Highest** | 10 TB - 100 TB | 99.9% (Zonal) |

*   **Key Differentiator:** Only **Enterprise** is Regional (HA). All others are Zonal (if zone dies, data is inaccessible until zone returns).

---

## 3. Networking Essentials
Filestore lives in a Google-managed VPC, so it must be "connected" to your VPC.
*   **Private IP:** Filestore instances are ONLY accessible via internal Private IP. No public internet access.
*   **Connection Method:**
    *   **VPC Peering:** (Classic method) Peering strictures apply (no transitive peering).
    *   **Private Service Access (PSA):** Allocates a /29 CIDR block.
*   **Access Scope:** Can be accessed by VMs in the *same* VPC, or connected VPCs via Shared VPC / VPN (if routes are exported properly).

---

## 4. Backups & Snapshots
*   **Backups:** Copy of the file share stored in Cloud Storage (Object Storage). Regional/Multi-Region availability.
*   **Snapshots:** Supported on **Enterprise** and **Basic** tiers. Point-in-time view.
*   **Recovery:** You can restore a backup to a *new* instance, not overwrite the existing one in-place easily.

---

## 5. PCA Exam Tips (The "Secret Sauce")
*   **"Shared Storage for Linux"**: If you see "Linux VMs need shared RW access" -> **Filestore**.
*   **"Shared Storage for Windows"**: If you see "Windows VMs" or "SMB protocol" -> **Filestore is WRONG**. Use **NetApp Cloud Volumes Service** or a Windows File Server on GCE.
*   **"Legacy App Lift & Shift"**: "App assumes a local filesystem and cannot be rewritten to use Object Storage" -> **Filestore**.
*   **"HPC / Rendering"**: "Thousands of cores rendering a movie needing shared assets" -> **High Scale SSD**.
*   **"SAP / Critical Database"**: -> **Enterprise Tier** (Regional HA).

---

## 6. Common Traps (Don't fall for these)
*   **Booting:** You **CANNOT BOOT** a VM from Filestore. You boot from Persistent Disk, then *mount* Filestore.
*   **Object Storage Replacement:** Don't use Filestore for "Data Lakes" or storing petabytes of user uploads. Use GCS (cheaper, infinite scale).
*   **Transitive Peering:** If VM is in VPC A, and Filestore is in VPC B, and A is peered to B... it works. But if you have VPN -> A -> B, transitive routing issues might block access unless carefully configured with Custom Route Advertisement.

---

## 7. Quick Exam Drill
*   **"Linux Shared Dir"** -> **Filestore**
*   **"Windows Shared Dir (SMB)"** -> **NetApp CVO / Windows Server** (Not Filestore)
*   **"High Availability / Regional"** -> **Enterprise Tier**
*   **"Massive Throughput / HPC"** -> **High Scale Tier**
*   **"Cheap shared storage"** -> **Basic HDD**
*   **"Can I boot from it?"** -> **NO**
