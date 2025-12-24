# GCP Cloud Storage (GCS) - PCA Exam Cram Sheet

## 1. Overview
Object storage service for companies of all sizes. Stores any amount of data and retrieves it as often as you like.
*   **Type:** Object Storage (not Block, not File).
*   **Capacity:** Unlimited.
*   **Consistency:** Strong global consistency for all operations (read-after-write, overwrite, delete).
*   **Protocol:** HTTP/HTTPS (REST API).
*   **Naming:** **Globally Unique**. Bucket names share a single global namespace. You cannot name a bucket `test` because someone else took it.
    *   *Analogy:* Like a Domain Name (DNS). `my-bucket` is unique across **ALL** Google Cloud customers.
    *   *Why?* Because every bucket is accessible via a public URL: `https://storage.googleapis.com/YOUR_BUCKET_NAME`. If names weren't unique, these URLs wouldn't work.
    *   **Note:** This only applies to the **Bucket**. Folders (sub-directories) *inside* the bucket do **not** need to be globally unique. You can have `gs://company-a/finance` and `gs://company-b/finance`.
    *   **Reuse after Deletion:**
        *   **Same Project:** Available **Immediately** (typically).
        *   **Different Project:** Can take **10+ minutes** (up to hours) to release. Do not rely on fast release for transfer between projects.

### 1.1 Object vs. Block Storage (Fundamental)
The exam often checks if you know when to use GCS vs. Persistent Disk.

| Feature | Object Storage (Cloud Storage) | Block Storage (Persistent Disk) |
| :--- | :--- | :--- |
| **Data Structure** | Objects (Data + Metadata + ID). Flat structure. | Raw blocks. Formatted with Filesystem (ext4, NTFS). |
| **Access** | REST API (HTTP) over network. Globally accessible. | Mounted to a VM. acts like a physical hard drive. |
| **Latency** | Higher (ms). Good for throughput. | Lowest (sub-ms). Good for IOPS. |
| **Mutability** | **Immutable**. Objects are replaced, not edited. | **Mutable**. You can edit specific bytes/blocks of a file. |
| **Best For** | Images, Backups, Static Web, Data Lakes. | VM Boot, Databases (SQL/NoSQL), App Binaries. |

### 1.2 Disaster Recovery Terms (Exam Critical)
*   **RPO (Recovery Point Objective):** "How much **Data** can I lose?"
    *   Measured in *Time* (e.g., "RPO of 15 mins" means if a crash happens, you lose the last 15 mins of data).
    *   **Near-Zero RPO** = No data loss.
*   **RTO (Recovery Time Objective):** "How much **Time** until I'm online again?"
    *   "RTO of 4 hours" means the system will be down for 4 hours.

---

## 2. Storage Classes (CRITICAL)
Memorize the use cases and minimum storage durations.

| Class | Use Case | Storage Cost | Retrieval Cost | Min Duration | Availability |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard** | Hot data, frequent access. | **Highest** | **None** | None | 99.95% |
| **Nearline** | Monthly access. Backups. | Medium | Low | 30 days | 99.95% |
| **Coldline** | Quarterly access. DR. | Low | High | 90 days | 99.90% |
| **Archive** | Yearly access. Tape repl. | **Lowest** | **Highest** | 365 days | 99.90% |

*   **Autoclass:** Automatically transitions objects to appropriate classes based on access patterns.

### 2.1 What is "Retrieval Cost"?
It is a **Fee per GB** for reading data.
*   **Standard:** $0.00 per GB (Free to read your own data).
*   **Nearline:** ~$0.01 per GB.
*   **Coldline:** ~$0.02 per GB.
*   **Archive:** ~$0.05 per GB.
*   *Exam Tip:* If you have a 10TB backup in **Archive** and you need to restore the *entire* thing, it will cost you a lot ($500+). But storing it for the year only cost you peanuts.

---

## 3. Location Types
*   **Region:** Specific geographic place (e.g., `us-central1`). Lowest cost. Redundant within zones (Zonal failure protection).
*   **Dual-Region:** Two specific regions (e.g., `nam4` = Iowa + SC). 
    *   **Availability:** High (99.95% Standard).
    *   **Disaster Recovery:** Geo-redundancy. 
    *   **RPO:** **Turbo Replication** (premium) guarantees RPO < 15 minutes.
*   **Multi-Region:** Large area (e.g., `US`, `EU`). Highest availability (99.95% Standard). Content distribution. Geo-redundant.

---

## 4. Security & Access Control
### Access Control Methods
1.  **IAM (Identity and Access Management):** Broad, project/bucket level permissions. **Recommended**.
2.  **ACLs (Access Control Lists):** Legacy. Object-level granularity. **Avoid** unless necessary.
3.  **Uniform Bucket-Level Access:** Disables ACLs. Enforces IAM on the whole bucket. **Google Best Practice**.

### Encryption
*   **Default:** Google-managed keys (automatic).
*   **CMEK (Customer-Managed Encryption Keys):** You manage keys in Cloud KMS. Google uses them.
*   **CSEK (Customer-Supplied Encryption Keys):** You keep keys on-prem, send them with request. Google never stores the key.

### Specialized Access
*   **Signed URLs:** Give time-limited access to a specific object for a user *without* a generic GCP account.
*   **Signed Policy Documents:** Specify what can be uploaded (size, type) for users uploading content directly to GCS.

### 4.1 Cloud Storage for Firebase (Mobile/Web Focus)
If the exam asks about **"Mobile App Users uploading photos directly"**, this is the answer.
*   **What is it?** A wrapper around standard GCS buckets.
*   **Key Features:**
    *   **Mobile SDKs:** Handles flaky networks (pauses/resumes uploads automatically) for iOS/Android/Web.
    *   **Security:** Integrates with **Firebase Authentication** (not just IAM). You write "Security Rules" like `allow read if request.auth != null`.
*   **Under the hood:** It stores files in *your* GCS bucket. You can access them via `gsutil` or Python API on the backend just like normal GCS objects.

---

## 5. Performance & Interaction
*   **gsutil:** Command line tool (Python based).
    *   Use `-m` flag for parallel (multi-threaded/multi-processing) operations.
    *   `gsutil rsync`: Synchronize directory to bucket.
*   **Composite Objects:** `gsutil compose` to combine smaller objects into one larger one (good for parallel uploads).
*   **FUSE (gcsfuse):** Mount bucket as file system. *Performance penalty*. Not POSIX compliant. Avoid for high-performance DBs.

## 6. Data Transfer options
*   **Online Transfer (gsutil):** Small to medium data.
*   **Storage Transfer Service:** Cloud-to-Cloud (AWS S3 -> GCS), or On-Prem HTTP/HTTPS/Object Store to GCS. Manager service. Good for large recurring transfers.
*   **Transfer Appliance:** Physical box shipped to you. For Petabytes of data where network is too slow (`Time to upload > 1 week`).

---

## 7. Lifecycle Management
Rules to automatically move or delete objects.
*   **Action:** SetStorageClass, Delete.
*   **Condition:** Age (days), CreatedBefore, NumberOfNewerVersions, IsLive (for versioned objects).
*   *Example:* Move from Standard -> Nearline after 30 days -> Coldline after 90 days -> Delete after 365 days.

## 8. Object Versioning
*   Keeps history of object overwrites/deletes.
*   Increases storage costs (you pay for every version).
*   Critical for preventing accidental deletion/overwrite.

---

## 9. PCA Exam Tips (The "Secret Sauce")
*   **Websites:** Static website hosting? -> Use GCS Bucket with a Load Balancer (or just direct public access).
*   **Global Access:** If requirements say "Low latency global access" -> Multi-Region.
*   **Cost vs. Access:** "Data accessed once a month" -> Nearline. "Once a year" -> Archive.
*   **Immutable Storage:** "Regulatory requirement to ensure data isn't deleted" -> **Bucket Lock (Retention Policy)**.
*   **Consistency:** Is GCS consistent? **YES**. It used to be eventually consistent for listings, but now it is **strong global consistency**. Don't fall for old traps.
*   **Upload Speed:** "Upload large file faster?" -> Parallel composite upload.

## 10. Common Traps (Don't fall for these)
*   **GCS is NOT a File System:** Do not put a typical Database (SQL/NoSQL) on mounted GCS. It's too slow and not transactional. Use Persistent Disk or Filestore.
*   **Latency:** Standard has millisecond latency. Nearline/Coldline/Archive *also* have millisecond latency (time to first byte). The difference is *cost*, not speed.
*   **Search:** GCS is not searchable by content. You scan keys or use metadata. For search, index metadata in Datastore/SQL.
*   **Resumable Uploads:** Use for large files to handle network failures. `gsutil` handles this automatically.

