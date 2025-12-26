# GCP Storage PCA Practice Exam Questions

This document contains exam-style questions covering Cloud Storage, Persistent Disk, Filestore, and data transfer services.

---

## Section 1: Cloud Storage

### Question 1: Storage Classes and Lifecycle

**Scenario**: A media company stores raw video files (100 TB total) that are:
- Accessed frequently for the first 30 days after upload (editing phase).
- Accessed occasionally (1-2 times) between 30-90 days (review phase).
- Rarely accessed after 90 days but must be retained for 7 years for compliance.

**What is the most cost-effective storage strategy?**

A. Store everything in Standard storage for 7 years  
B. Use Standard storage for all files, manually move to Nearline after 90 days  
C. Configure lifecycle policy: Standard → Nearline (30 days) → Coldline (90 days)  
D. Use Archive storage immediately (cheapest option)  

**Answer: C** ✅

**Explanations**:
- **A (Wrong)**: Standard storage costs **$0.020/GB/month**. For 100 TB over 7 years:
  - Cost = 100,000 GB × $0.020 × 84 months = **$168,000**.
  Most of this data is rarely accessed (after 90 days), so paying Standard rates for 7 years is wasteful.

- **B (Wrong)**: Manual migration has several problems:
  - **Operational burden**: Someone must remember to move files every 90 days.
  - **Error-prone**: Forget to move files → paying Standard rates unnecessarily.
  - **Doesn't optimize 30-90 day period**: Still using Standard when Nearline would be cheaper.
  Lifecycle policies **automate** this at zero operational cost.

- **C (Correct)**: ✅ Lifecycle policy automates cost optimization:
  - **0-30 days**: Standard ($0.020/GB/month) for frequent access.
  - **30-90 days**: Nearline ($0.010/GB/month) for occasional access (50% cheaper).
  - **90+ days**: Coldline ($0.004/GB/month) for rare access (80% cheaper).
  - **Calculation**: (30 days × Standard) + (60 days × Nearline) + (7 years × Coldline) = **~$50,000** (70% savings vs all-Standard).
  Google Cloud automatically transitions objects based on age—zero manual work.

- **D (Wrong)**: Archive storage ($0.0012/GB/month) is the cheapest, but:
  - **Retrieval time**: Hours (not milliseconds).
  - **Early deletion fee**: If you need to access a file within the first 365 days, you pay a penalty.
  - **Scenario mismatch**: Files are "accessed frequently for the first 30 days"—Archive is for data accessed < once/year.
  Using Archive immediately would make editing impossible (hours to retrieve each file).

---

### Question 2: Cloud Storage Location Types

**Scenario**: A global e-commerce company serves product images to users in US, EU, and Asia. They want:
- Low latency for image delivery worldwide.
- High availability (99.99%+).
- Automatic geo-redundancy.

**Which Cloud Storage configuration should they use?**

A. Multi-region bucket (`nam-eur-asia`) + Cloud CDN  
B. Regional bucket (`us-central1`) + Cloud CDN  
C. Dual-region bucket (`us-east1 + us-west1`)  
D. Regional bucket in each continent (`us`, `eu`, `asia`) with custom load balancing  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ Multi-region bucket + Cloud CDN is the optimal solution:
  - **Multi-region bucket**: Data stored in **at least 3 regions** across continents (`nam`, `eur`, `asia`).
  - **Availability SLA**: 99.95% (higher than regional: 99.9%).
  - **Geo-redundancy**: Automatic replication across continents (survives region failure).
  - **Cloud CDN**: Caches images at **edge locations** worldwide (100+ locations), reducing latency to < 50ms globally.
  - **Automatic origin**: CDN fetches from nearest multi-region bucket location.

- **B (Wrong)**: Regional bucket (`us-central1`) stores data in a **single region**:
  - Users in Europe/Asia experience **high latency** (100-200ms+) fetching from US.
  - **Single point of failure**: If `us-central1` region fails, entire app is down.
  - Cloud CDN helps (edge caching), but initial cache misses still go to a single region.
  For global workloads, multi-region is superior.

- **C (Wrong)**: Dual-region buckets (e.g., `us-east1 + us-west1`) provide:
  - **Replication** between two regions (better than single region).
  - **Lower latency** within the dual-region pair (e.g., US East/West Coast).
  - But **still limited to one continent** (US). Users in Europe/Asia still experience high latency.
  Use dual-region for **regional high availability**, not global distribution.

- **D** (Wrong)**: Creating separate regional buckets in each continent requires:
  - **Manual replication**: You write scripts to sync data across 3 buckets.
  - **Complex routing**: Load balancer must route requests to the nearest bucket (requires latency-based routing logic).
  - **Operational burden**: Managing 3 buckets, 3 sync jobs, monitoring replication lag.
  Multi-region buckets do this **automatically**—don't reinvent the wheel.

---

### Question 3: Signed URLs

**Scenario**: A SaaS platform allows users to upload private files to Cloud Storage. Each file should be accessible only by the uploading user for 24 hours via a direct download link. The application should not proxy the download (to save bandwidth).

**What is the secure, Google-recommended solution?**

A. Make the bucket public and send users the object URL  
B. Generate a signed URL with 24-hour expiration  
C. Use IAM to grant each user Object Viewer role on their files  
D. Stream the file through the application server (application downloads from GCS and sends to user)  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Making the bucket public (`allUsers: Storage Object Viewer`) means:
  - **Anyone** with the object URL can download **any** file (not just their own).
  - No expiration (files accessible forever unless manually deleted).
  - **Security disaster**: Leaked URLs = all user files exposed.
  This violates the principle of least privilege.

- **B (Correct)**: ✅ Signed URLs provide **temporary, scoped access**:
  - **How it works**: Application generates a URL with a **cryptographic signature** using a service account key.
  - **Expiration**: URL expires after 24 hours (parameter: `expiration_time`).
  - **Scoped**: URL grants access to **one specific object**, not the entire bucket.
  - **No proxy**: Users download **directly** from Cloud Storage (application doesn't proxy, saving bandwidth).
  - Example: `https://storage.googleapis.com/bucket/file.pdf?X-Goog-Signature=<sig>&X-Goog-Expires=86400`

- **C (Wrong)**: Granting IAM roles (`Object Viewer`) per user has problems:
  - **IAM propagation delay**: Up to 7 minutes for role bindings to take effect.
  - **Complexity**: Managing thousands of users × thousands of files = millions of IAM bindings (unscalable).
  - **Revocation**: Revoking access after 24 hours requires background jobs to clean up IAM bindings.
  Signed URLs are **designed** for this use case (time-limited access without IAM changes).

- **D (Wrong)**: Proxying through the application server defeats the purpose:
  - **Bandwidth cost**: Application downloads from GCS → sends to user (2x bandwidth charged).
  - **Latency**: Extra hop through application server.
  - **Scaling**: Application server becomes bottleneck (must handle all download traffic).
  Signed URLs let users download **directly** from Cloud Storage (optimal).

---

## Section 2: Persistent Disk & Block Storage

### Question 4: Zonal vs Regional Persistent Disk

**Scenario**: A critical PostgreSQL database runs on Compute Engine with 500 GB of data. The company requires:
- RTO (Recovery Time Objective) < 1 hour.
- RPO (Recovery Point Objective) < 1 minute.
- Automatic failover across zones.

**Which storage option provides this?**

A. Zonal Persistent Disk + daily snapshots  
B. Regional Persistent Disk (synchronous replication across zones)  
C. Local SSD (physically attached for speed)  
D. Cloud Filestore  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Zonal Persistent Disk stores data in a **single zone**:
  - If that zone fails, the disk is unavailable until the zone recovers.
  - **Snapshots** (taken daily) provide backups, but:
    - RPO = 24 hours (last snapshot taken yesterday → lose up to 24 hours of data).
    - RTO = **manual restore time** (restore 500 GB from snapshot → 30-60 minutes, but requires manual intervention).
  - Doesn't meet RPO < 1 minute or automatic failover requirements.

- **B (Correct)**: ✅ Regional Persistent Disk provides **zone-level failover**:
  - **Synchronous replication**: Data written to **two zones simultaneously**.
  - **RPO = 0**: Zero data loss (both zones have identical data).
  - **RTO < 1 hour**: Failover is automatic (attach disk to VM in healthy zone).
  - **Use case**: Stateful workloads requiring HA (databases, file servers).
  - **Cost**: 2x the price of zonal disk (paying for replication), but worth it for critical data.

- **C (Wrong)**: Local SSD is **ephemeral** (data lost when VM stops):
  - No persistence across zone failures.
  - No snapshots or backups.
  - Use cases: Temporary cache, scratch space.
  - **Does NOT meet** any of the requirements (RTO/RPO).

- **D (Wrong)**: Cloud Filestore is a **managed NFS** service, not block storage:
  - Use case: Shared file systems (multiple VMs reading/writing shared files).
  - **Not optimized** for database workloads (databases use block storage, not NFS).
  - Latency is higher than Persistent Disk.

---

### Question 5: Snapshot Scheduling

**Scenario**: A development team wants automated daily snapshots of 10 Persistent Disks at 2:00 AM UTC. Snapshots should be retained for 30 days, then automatically deleted.

**What is the BEST approach?**

A. Create a Cloud Scheduler job that runs `gcloud compute disks snapshot` daily  
B. Configure a snapshot schedule policy with daily frequency and 30-day retention  
C. Use a Cloud Function triggered by cron to create snapshots  
D. Manually create snapshots daily and delete old ones  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: While Cloud Scheduler + `gcloud` CLI works, it has issues:
  - **Retention management**: You must write a separate script to delete snapshots older than 30 days.
  - **Monitoring**: Custom logging/alerting for snapshot failures.
  - **Per-disk scripting**: Script must loop through 10 disks (error-prone).
  This is **manual scripting** when Google provides a built-in feature.

- **B (Correct)**: ✅ Snapshot schedule policies are **purpose-built** for this:
  - **Create once, apply to many**: One policy → attach it to all 10 disks.
  - **Automatic scheduling**: Google handles the cron timing.
  - **Automatic retention**: Snapshots older than 30 days are **auto-deleted** (no cleanup script needed).
  - **Monitoring**: Built-in metrics in Cloud Monitoring.
  - **Example**:
    ```bash
    gcloud compute resource-policies create snapshot-schedule daily-snapshots \
      --start-time=02:00 --daily-schedule --retention-days=30
    gcloud compute disks add-resource-policies disk-1 --resource-policies=daily-snapshots
    ```

- **C (Wrong)**: Similar to option A—Cloud Function + cron works but requires:
  - Writing Function code to snapshot disks.
  - Managing retention logic.
  - Monitoring Function failures.
  Don't use Functions for tasks that have native GCP features (snapshot schedules).

- **D (Wrong)**: Manual snapshots are:
  - **Error-prone**: Forget one day → lose backup window.
  - **Not scalable**: Works for 1 disk, unsustainable for 100 disks.
  - **Operational burden**: Someone on-call to run snapshots daily.
  Automation exists to avoid this.

---

## Section 3: Cloud Filestore

### Question 6: Filestore vs Cloud Storage FUSE

**Scenario**: A rendering farm (100 VMs) needs to access a shared 5 TB dataset of 3D model files. All VMs must read/write the same files simultaneously. The application uses standard POSIX file system operations (`open()`, `read()`, `write()`).

**Which storage solution should be used?**

A. Cloud Storage with FUSE mount on each VM  
B. Cloud Filestore (managed NFS)  
C. Persistent Disk attached to all VMs in read-only mode  
D. Local SSD on each VM with syncing scripts  

**Answer: B** ✅

**Explanations**:
- **A (Partially Wrong)**: Cloud Storage FUSE allows mounting buckets as filesystems, but:
  - **Not true POSIX**: Many file system operations are **emulated** (slower, some operations unsupported).
  - **Performance**: High latency for small file operations (10-50ms per `open()`), terrible for workloads with many small files.
  - **Consistency**: **Eventually consistent** (one VM's write might not be immediately visible to another VM).
  While FUSE works for *some* use cases (migration from NFS to object storage), it's not ideal for high-performance shared file systems.

- **B (Correct)**: ✅ Cloud Filestore is **managed NFS** (Network File System):
  - **POSIX-compliant**: Full support for `open()`, `read()`, `write()`, `chmod()`, etc.
  - **Performance**: Low latency (1-3ms for file operations), optimized for rendering/compute workloads.
  - **Multi-writer**: 100 VMs can mount the same Filestore volume simultaneously with strong consistency.
  - **Fully managed**: Google handles scaling, backups, HA.
  This is the **standard solution** for "shared file system across VMs."

- **C (Wrong)**: Persistent Disk can be attached to **multiple VMs in read-only mode**, but:
  - **Read-only**: VMs cannot write to the disk (violates "read/write the same files").
  - **Use case**: Distributing static assets (e.g., ML model weights) that never change.
  For read-write shared access, use Filestore, not Persistent Disk.

- **D (Wrong)**: Local SSD on each VM with syncing scripts is a **DIY solution** that:
  - Requires custom scripts to sync files across 100 VMs.
  - High risk of **data conflicts** (two VMs modify same file → which version wins?).
  - **Operational nightmare**: Managing sync failures, monitoring replication lag.
  This is reinventing NFS—use Filestore instead.

---

## Section 4: Data Transfer Services

### Question 7: Data Transfer Method Selection

**Scenario**: A company needs to transfer 500 TB of historical data from an on-premises data center to Cloud Storage. Their internet connection is 1 Gbps. The data must arrive within 2 weeks.

**Which transfer method should they use?**

A. gsutil (CLI upload)  
B. Storage Transfer Service (online transfer)  
C. Transfer Appliance (physical shipping)  
D. Dataflow pipeline  

**Answer: C** ✅

**Explanations**:
- **A (Wrong)**: Let's do the math for `gsutil`:
  - **Bandwidth**: 1 Gbps = 125 MB/sec (theoretical max).
  - **Realistic throughput**: 50-70% utilization = ~70 MB/sec (accounting for TCP overhead, packet loss).
  - **Time**: 500 TB = 500,000,000 MB. Time = 500,000,000 MB / 70 MB/sec = **83 days**.
  - Even with perfect 100% utilization (impossible), it would take **58 days**.
  This **does NOT meet** the 2-week (14 days) deadline.

- **B (Wrong)**: Storage Transfer Service (STS) is for online transfers, so it faces the same bandwidth limitation as `gsutil`:
  - **Advantage**: Better reliability (automatic retries, checksum validation).
  - **Bandwidth**: Still limited to 1 Gbps → **83 days**.
  STS is great for **large but not massive** datasets (< 100 TB) or scheduled periodic transfers (S3 → GCS daily sync).

- **C (Correct)**: ✅ Transfer Appliance is a **physical device** Google ships to you:
  - **How it works**:
    1. Request an appliance (rack-mounted server with 100 TB or 480 TB capacity).
    2. Copy data to the appliance on-premises (local network speed = 10 Gbps+, **5 TB/day**).
    3. Ship the appliance back to Google via secure courier.
    4. Google uploads data to Cloud Storage within 2-3 days.
  - **Timeline**: 2 days setup + 5 days copy + 2 days shipping + 2 days upload = **11 days** (meets deadline).
  - **When to use**: > 20 TB of data with slow internet (rule of thumb: if online transfer > 1 week, use appliance).

- **D (Wrong)**: Dataflow is a **data processing** service (streaming/batch ETL pipelines), not a data transfer service. You'd still need to get the data to GCP first (gsutil, STS, or Transfer Appliance), then Dataflow processes it.

---

### Question 8: Storage Transfer Service SLA

**Scenario**: A company syncs 10 TB of data from AWS S3 to Cloud Storage daily. They configure Storage Transfer Service to run at 2:00 AM daily. One day, the transfer fails due to an S3 outage.

**What happens?**

A. STS automatically retries until successful  
B. STS sends an email notification; manual retry required  
C. STS fails permanently; data is lost  
D. STS rolls back the partial transfer  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ Storage Transfer Service has **built-in retry logic**:
  - **Transient failures** (network errors, S3 throttling): Automatic retries with exponential backoff.
  - **Permanent failures** (invalid credentials): Marked as failed, logged.
  - **Partial transfers**: STS resumes from the last successful checkpoint (doesn't re-copy already transferred files).
  This is why STS is better than `gsutil` for large scheduled transfers.

- **B (Wrong)**: While STS does send **notifications** (via Cloud Pub/Sub or Cloud Logging), it doesn't require manual intervention for transient failures. You only need to intervene for permanent errors (e.g., fix invalid credentials).

- **C (Wrong)**: Data is **never lost** during transfer failures:
  - Source data remains in S3 (read-only operation).
  - STS retries or allows manual retry.

- **D (Wrong)**: STS doesn't "roll back" transfers. If 5 TB out of 10 TB transferred successfully before failure, those 5 TB remain in Cloud Storage. STS resumes from 5 TB on retry (doesn't delete and restart).

---

## Answer Key Summary

1. **C** - Lifecycle policy (Standard → Nearline → Coldline)
2. **A** - Multi-region bucket + Cloud CDN for global distribution
3. **B** - Signed URLs for time-limited access
4. **B** - Regional Persistent Disk for zone failover
5. **B** - Snapshot schedule policy for automation
6. **B** - Cloud Filestore for shared NFS
7. **C** - Transfer Appliance for 500 TB with deadline
8. **A** - STS auto-retries on failure

---

## Study Tips

1. **Cloud Storage**: Memorize storage class costs and use cases (Standard vs Nearline vs Coldline vs Archive).
2. **Lifecycle Policies**: Automatic transitions save operational burden (exam loves automation).
3. **Persistent Disk**: Zonal vs Regional (RTO/RPO requirements are key).
4. **Filestore**: Default answer for "shared file system across VMs."
5. **Data Transfer**: 
   - < 20 TB + good internet → gsutil/STS
   - > 20 TB or bad internet → Transfer Appliance
6. **Signed URLs**: Time-limited access without IAM changes.
