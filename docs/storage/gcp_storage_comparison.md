# GCP Storage Comparison - PCA Exam Cheat Sheet

## 1. The "Big 3" Comparison Table
This is the ultimate summary to decide which storage service to pick in the exam.

| Feature | **Object Storage** (Cloud Storage) | **Block Storage** (Persistent Disk) | **File Storage** (Filestore) |
| :--- | :--- | :--- | :--- |
| **Data Type** | **Unstructured** (Blobs, Images, Backups). | **Structured** (Raw Blocks, Filesystem). | **Structured** (Files, Directories). |
| **Protocol** | **HTTP/HTTPS** (REST API). | **Native Block Device** (NVMe/SCSI). | **NFSv3** (Network File System). |
| **Access** | **Global** URL. Accessible from anywhere (Internet). | **Zonal/Regional**. Attached to a specific VM. | **VPC Internal**. Network mounted by many VMs. |
| **Bootable?** | No. | **Yes** (Boot Disk). | No. |
| **Editability** | **Immutable** (Write once, Replace). | **Mutable** (Edit specific bytes). | **Mutable** (Edit specific bytes). |
| **Capacity** | **Unlimited** (Petabytes+). | **Limited** (up to 64TB per disk). | **High** (up to 100TB per instance). |
| **Throughput** | High (Parallel reads/writes). | Very High (Local IOPS). | High (Networked IOPS). |
| **Latency** | Medium (ms). | **Lowest** (sub-ms). | Low (ms). |
| **Cost** | **Lowest** ($). | **Medium** ($$). | **Highest** ($$$). |
| **Typical Use** | Web assets, Data Lake, Backups, Archives. | OS Boot, Databases (SQL), Scratch space. | Legacy Apps, Shared Home Dirs, CMS, Rendering. |

---

## 2. Decision Flowchart (Mental Model)

1.  **Do you need to run an Operating System or a Database?**
    *   **Yes:** -> **Block Storage (Persistent Disk)**.
        *   *Check:* Is it for a temporary cache? -> **Local SSD**.
        *   *Check:* Is it for a critical DB? -> **Regional PD**.

2.  **Do you need to share files between multiple Linux VMs?**
    *   **Yes:** -> **Filestore** (NFS).
        *   *Constraint Check:* Does the app use "File System APIs" (Open/Read/Write/Close)? -> **Filestore**.

3.  **Is it unstructured data (Images, Videos, Logs) or Backups?**
    *   **Yes:** -> **Cloud Storage (GCS)**.
        *   *Constraint Check:* Does it need to be accessed globally via URL? -> **GCS**.
        *   *Constraint Check:* Is it for long-term archiving? -> **GCS Archive Class**.

---

## 3. Exam Keywords Mapping

| If the question says... | You think... |
| :--- | :--- |
| "Global access", "Immutable", "Websites", "Streaming" | **Cloud Storage** |
| "Boot", "Install OS", "Database storage", "Raw block" | **Persistent Disk** |
| "Shared directory", "NFS", "Legacy Application", "Lift and Shift" | **Filestore** |
| "SMB", "Windows Shared" | **NetApp Cloud Volumes** (Not Filestore!) |
| "Transient", "Cache", "Scratch", "lost on stop" | **Local SSD** |
