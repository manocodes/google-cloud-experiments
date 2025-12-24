# GCP Storage Data Transfer - PCA Exam Cram Sheet

## 1. Decision Matrix (The Rule of Thumb)
The exam tests your ability to choose the *fastest* and *most reliable* method.

| Scenario | Volume | Tool |
| :--- | :--- | :--- |
| **Local/Ad-hoc** | Small (< 1 TB) | **gsutil** (CLI) |
| **Cloud-to-Cloud** | Any (S3/Azure -> GCS) | **Storage Transfer Service** |
| **On-Prem to Cloud** | Medium (> 1 TB), Recurring | **Storage Transfer Service** (with Agents) |
| **Offline/Slow Net** | Huge (> 20 TB / PBs) | **Transfer Appliance** |
| **Database** | Live Migration | **Database Migration Service** (DMS) |

---

## 2. Transfer Appliance (The "Sneakernet")
A high-capacity physical server shipped by Google to your datacenter.
*   **Use Case:** Migration would take **> 1 Week** over the network.
*   **Formula:** `Days = (Total Bytes) / (Network Speed)`
*   **Process:**
    1.  Request appliance (Console).
    2.  Receive & Rack it in your DC.
    3.  Copy data (NFS share) to Appliance.
    4.  Ship back to Google.
    5.  Google uploads to GCS.
*   **Capacities:** usually ~40TB or ~300TB models.
*   **Security:** Data is encrypted. You keep the encryption key (Customer-Managed) until it's safe in GCS, then you decrypt.

---

## 3. Storage Transfer Service (STS)
Fully managed service. Scalable and reliable.
*   **Cloud-to-Cloud:**
    *   Source: AWS S3, Azure Blob, or another GCS bucket.
    *   No infrastructure needed. Just setup the job in Console.
    *   **Features:** Scheduling, Incremental syncs (delete source after transfer), Filter by file dates.
*   **On-Premises (File Data):**
    *   Source: NFS mounts, local disks.
    *   **Requirement:** You must install **Orchestration Agents** (Docker containers) on your on-prem servers to push the data.
    *   **Features:** Maximizes bandwidth, retries on failure, secure (TLS).

---

## 4. `gsutil` (Command Line)
Best for developers and small ops.
*   **Parallelism:** ALWAYS use `gsutil -m cp ...` for multi-threading. Increases speed significantly for many small files.
*   **Composite Uploads:** For large files, it splits them into chunks, uploads in parallel, and composes them in GCS.
*   **Resumable Uploads:** Enabled by default for large files. If connection drops, it picks up where it left off.
*   **Limitations:**
    *   **Local Machine:** Stops if you close laptop.
    *   **Cloud Shell:** Stops if the session times out (~1 hour of inactivity). It is **NOT** a background worker.
    *   **Fix:** Use a **VM** (Compute Engine) with `screen`/`tmux` or Storage Transfer Service for long jobs.

---

## 5. Specialized Transfer Tools
*   **BigQuery Data Transfer Service:**
    *   Automated ingestion from SaaS (Salesforce, Google Ads, YouTube) directly into **BigQuery**.
    *   *Not* for general file storage.
*   **Transfer Service for On-Premises Data:** (Specific subset of STS)
    *   Designed for moving **FileSystem** data to GCS or Filestore.

---

## 6. Exam "Traps" & Tips
*   **"Cost vs Speed":**
    *   Appliance is often *faster* for Petabytes but takes logistical time (shipping).
    *   VPN/Interconnect is *immediate* setup but limited by physics (bandwidth).
*   **"10TB Data":**
    *   Don't use Transfer Appliance for 10TB unless you have a 56k modem. 10TB over a 1 Gbps link takes ~1 day. Just use **gsutil** or **STS**.
*   **"S3 to GCS":**
    *   Never suggest downloading to local and re-uploading. Use **Storage Transfer Service** (Direct cloud-to-cloud).
*   **"Small Files Problem":**
    *   Uploading 1 million 1KB files is slower than 1 1GB file (overhead).
    *   *Solution:* Use `gsutil -m` or zip them first (if processing allows).

---

## 7. Mathematical Rules (For the Exam)
You don't need a calculator, but know the benchmarks:
*   **1 Gbps** = ~10 TB per day (ideal).
*   **10 Gbps** = ~100 TB per day.
*   **If Transfer Time > 1 Week:** -> **Use Transfer Appliance**.
