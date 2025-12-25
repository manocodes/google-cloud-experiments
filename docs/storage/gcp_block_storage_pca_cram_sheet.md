# GCP Block Storage (Persistent Disk) - PCA Exam Cram Sheet

## 1. Overview
Network-attached storage (NAS) that behaves like a physical hard drive.
*   **Type:** Block Storage.
*   **Attachment:** Mounted to Compute Engine (GCE) or GKE nodes.
*   **Decoupled:** Exists independently of the VM. If VM is deleted, disk *can* persist (if configured).
*   **Bootable:** Yes. You boot the OS from a Persistent Disk (PD).

---

## 2. Disk Types (CRITICAL)
Memorize the use cases for the 4 main types + Local SSD.

| Type | Name | Use Case | Performance Indicator |
| :--- | :--- | :--- | :--- |
| **Standard** | `pd-standard` | **Cost save**. Cold data, backups, logging. HDD based. | Low IOPS. |
| **Balanced** | `pd-balanced` | **Default choice**. Web apps, general DBs. SSD based. | Medium IOPS. |
| **SSD** | `pd-ssd` | **Performance**. High-perf NoSQL/SQL databases. | High IOPS. |
| **Extreme** | `pd-extreme` | **Massive Scale DBs** (e.g. running Oracle, SAP HANA). | Provisioned IOPS (Target). |
| **Hyperdisk** | `hyperdisk` | **Next Gen**. Extreme high performance (throughput/IOPS decoupled). | Highest Cloud Performance. |
| **Local SSD** | `local-ssd` | **Cache / Temp**. Scratch space. Ephemeral. | **Highest** Latency/IOPS. |

### Note on Local SSD (The "Trap")
*   **Ephemeral:** Data is **LOST** if you `Stop` the VM.
*   **Physical:** Attached directly to the server (not network).
*   **Use Case:** Cache layers (Redis), temp processing, NoSQL with app-level replication (Cassandra). **NEVER** for critical persistent data.

### 2.1 Critical Concept: IOPS vs. Throughput
*   **IOPS (Input/Output Operations Per Second):** The number of individual read/write actions.
    *   *Analogy:* **Car Engine RPM**. How fast the engine spins.
    *   *Importance:* Critical for **Transaction Processing (OLTP)** databases (e.g., Many users buying tickets at once). Small, random reads/writes.
*   **Throughput (MB/s):** The total volume of data moved.
    *   *Analogy:* **Car Speed (MPH)**. How much distance (data) you cover.
    *   *Importance:* Critical for **Streaming & Analytics (OLAP)** (e.g., Reading a large video file or scanning a whole table). Large, sequential reads/writes.
*   **The Formula:** `Throughput = IOPS * Block Size`
    *   *Exam Tip:* If your IOPS are high but Throughput is low, your Block Size is too small.

### 2.2 HDD vs. SSD (The Physics)
*   **HDD (Hard Disk Drive) -> `pd-standard`**
    *   **Mechanism:** Spinning magnetic platters with a mechanical arm.
    *   **Pros:** Cheap ($), Good for purely sequential reads (large video files).
    *   **Cons:** **High Latency**. The arm takes time to physically move to the data. **Low IOPS** for random access.
*   **SSD (Solid State Drive) -> `pd-ssd`, `pd-balanced`**
    *   **Mechanism:** Flash memory chips (Microchips). No moving parts.
    *   **Pros:** **Instant Access** (Low Latency), **High IOPS** (Random reads/writes are fast).
    *   **Cons:** Expensive ($$$).

---

## 3. Availability & Replication
### Zonal Application (Standard)
*   **Scope:** Lives in **1 Zone** (e.g., `us-central1-a`).
*   **Risk:** If zone fails -> Disk is inaccessible.

### Regional Persistent Disk (Synchronous Replication)
*   **Scope:** Replicated across **2 Zones** in the same Region (e.g., `us-central1-a` AND `us-central1-b`).
*   **Use Case:** Critical Databases (MySQL/Postgres) requiring High Availability (HA).
*   **Trade-off:** slightly higher write latency (needs to write to both zones) and double cost.
*   **Failover:** If Zone A dies, force-attach disk to VM in Zone B.

---

## 4. Lifecycle & Backups (Snapshots)
*   **Incremental:** Snapshots only store *changes* since the last snapshot. Efficient.
*   **Global:** Snapshots are stored in Cloud Storage (Object Store), meaning they are **Region/Multi-Region** available.
*   **Cross-Project:** You can share snapshots across projects.
*   **Schedule:** Use "Snapshot Schedules" for automated backups.

---

## 5. Operations & Scaling
*   **Resize:** You can **Increase** size online (without stopping VM). You generally **cannot Decrease** size.
*   **Performance Scaling:** IOPS and Throughput often scale with **Disk Size** (Bigger disk = Faster disk), up to a limit.
*   **Multi-Writer:** generally ONLY for **Read-Only** mode (hundreds of VMs reading AI models).
    *   *Exception:* Hyperdisk/NFS solutions allows multi-write, but typically standard PD is Single-Writer.

---

## 6. Shared Filesystems (Filestore)
Sometimes "Block" isn't the answer. If the exam asks for "Shared RW access for many VMs" (POSIX compliant):
*   **Filestore:** Managed NFS (Network File System).
    *   *Use Case:* Lift & Shift, Shared Home Dirs, Video Rendering farms.
    *   *Tiers:* Basic (HDD/SSD), High Scale, Enterprise (Critical).

---

## 7. PCA Exam Tips (The "Secret Sauce")
*   **"Speed vs. Persistence":**
    *   Need SPEED and don't care about data loss? -> **Local SSD**.
    *   Need SPEED and MUST keep data? -> **pd-ssd** or **pd-extreme**.
*   **"High Availability DB":**
    *   Option A: GCE with 1 Zonal Disk. (Bad)
    *   Option B: GCE with **Regional PD**. (Correct - protects against Zonal failure).
*   **"Disaster Recovery":**
    *   How to move a VM to another Region? -> Create **Snapshot** (Global) -> Create Image from Snapshot in new Region -> Boot VM.
*   **"Capacity Planning":** "We need more IOPS but can't change disk type." -> **Increase the Disk Size**.
*   **"Encryption":** All PDs are encrypted at rest by default. You can use CMEK (Customer Managed) or CSEK (Customer Supplied).

## 8. Common Traps
*   **Boot Disk:** You *can* boot from a Network PD. You *cannot* boot from a Filestore bucket.
*   **Local SSD Persistence:** Do not believe options saying "Local SSD persists after shutdown". It persists on *Reboot* (Live Migration), but NOT on *Stop/Shutdown*.
*   **Throughput Limits:** If your disk is fast (`pd-ssd`) but performance is slow, check the **VM Network Bandwidth** limit. Tiny VMs (e.g., e2-small) have capped network speeds that throttle disk access.

## 9. Quick Exam Drill
*   **"High IOPS, data can be lost"** -> **Local SSD**
*   **"High IOPS, data must be safe"** -> **PD-SSD** or **PD-Extreme**
*   **"Shared File System for Linux"** -> **Filestore** (NFS)
*   **"Boot Disk"** -> **Persistent Disk** (Standard/SSD/Balanced)
*   **"Need more speed without changing disk type"** -> **Increase the Disk Size**

