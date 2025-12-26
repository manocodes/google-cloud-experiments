# GCP Compute PCA Practice Exam Questions

This document contains exam-style questions covering Compute Engine, GKE, Cloud Run, Cloud Functions, and App Engine.

---

## Section 1: Compute Engine

### Question 1: Preemptible VMs

**Scenario**: A data science team runs nightly batch jobs that process sensor data (duration: 3-6 hours). The jobs can be interrupted and restarted without data loss. Current monthly compute costs are $8,000 using standard n1-standard-8 VMs.

**How can they reduce costs while maintaining the same processing capacity?**

A. Use committed use discounts (1-year contract)  
B. Switch to preemptible VMs  
C. Use sole-tenant nodes for better pricing  
D. Migrate to Cloud Functions for serverless pricing  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Committed use discounts provide ~30-40% savings for predictable workloads that run 24/7. While this helps, nightly batch jobs (6 hours/day) represent 25% utilization. You're paying for 18 hours of idle time daily. Preemptible VMs are still cheaper.

- **B (Correct)**: ✅ Preemptible VMs offer **60-91% discount** (typically ~80%) compared to standard VMs. Perfect for this scenario because:
  1. Jobs are **fault-tolerant** (can be interrupted and restarted).
  2. Jobs run < 24 hours (preemptible VMs run for up to 24 hours before forced preemption).
  3. Cost: $8,000 × 20% = **$1,600/month** (80% savings).
  4. Google guarantees 30-second termination warning (ACPI G2 signal) to save checkpoint.
  The only downside is occasional preemption (typically < 5-10%), which is acceptable for batch jobs.

- **C (Wrong)**: Sole-tenant nodes provide **dedicated hardware** for compliance/licensing, but they're **more expensive**, not cheaper. Use cases:
  - Windows Server licenses (BYOL - Bring Your Own License).
  - Regulatory compliance requiring physical isolation.
  This is the opposite of cost optimization.

- **D (Wrong)**: Cloud Functions is for **event-driven workloads** (< 9 minutes execution time by default, max 60 minutes for 2nd gen). A 3-6 hour batch job exceeds the limits. Additionally, Functions pricing is per invocation/GB-sec—running for hours would be expensive. Batch jobs belong on Compute Engine or Dataflow, not Functions.

---

### Question 2: Managed Instance Groups (MIG) Autoscaling

**Scenario**: A web application runs on a Managed Instance Group with autoscaling configured based on average CPU utilization (target: 70%). During flash sales, traffic spikes from 100 req/sec to 10,000 req/sec in 30 seconds. However, new VMs take 5 minutes to boot, causing users to see errors during the spike.

**What is the BEST solution?**

A. Switch autoscaling metric from CPU to HTTP request rate  
B. Pre-warm instances using a scheduled script before sales events  
C. Use Cloud Run instead (instant autoscaling)  
D. Increase minimum instance count to handle peak traffic  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ HTTP request rate (RPS - Requests Per Second) autoscaling triggers **faster** than CPU-based scaling:
  - **CPU-based**: VMs must physically receive traffic → CPU increases → metric reported → autoscaler triggers (lag: 60-90 seconds).
  - **RPS-based**: Load balancer sees traffic spike → immediately triggers autoscaler (lag: 10-30 seconds).
  - For sudden traffic spikes, RPS-based autoscaling provides **30-60 seconds faster response**.
  Combined with reducing boot time (using smaller images, preloaded dependencies), this minimizes error rate.

- **B (Wrong)**: Pre-warming helps if you know the exact sale time, but:
  - Requires manual intervention (not fully automated).
  - What if the sale time changes? Or an unplanned spike occurs?
  - You're paying for idle pre-warmed instances before the sale.
  RPS-based autoscaling is automatic and doesn't require prediction.

- **C (Wrong)**: Cloud Run **does** provide instant autoscaling (cold start < 1 second), making it theoretically better for traffic spikes. However, migrating an existing VM-based web app to Cloud Run requires:
  - Containerizing the application.
  - Refactoring to be stateless (Cloud Run is ephemeral).
  - Testing compatibility.
  This is a **months-long migration**, not a quick fix. The question asks for the "best solution" given the current MIG setup. Option A is a configuration change (hours), not a migration (months).

- **D (Wrong)**: Setting minimum instances = peak capacity (e.g., 100 VMs) solves the spike problem but wastes money:
  - Outside of sales events (99% of the time), you're paying for 99 idle VMs.
  - Cost = $24/day/VM × 99 idle VMs × 30 days = **$71,280/month** in waste.
  This violates cost optimization principles. Autoscaling exists to avoid this.

---

### Question 3: Persistent Disk vs Local SSD

**Scenario**: A database workload requires:
- 500 GB storage
- Sub-millisecond latency for random I/O
- Data must survive VM restarts

**Which storage option should be used?**

A. Standard Persistent Disk (HDD)  
B. SSD Persistent Disk  
C. Local SSD  
D. Cloud Filestore  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Standard Persistent Disk (HDD) provides:
  - Latency: **10-20ms** (spinning disks).
  - Use case: Sequential large file access (logs, backups).
  - **Does NOT meet** the "sub-millisecond" requirement for random I/O.

- **B (Correct)**: ✅ SSD Persistent Disk is the right balance:
  - Latency: **1-3ms** for random I/O (meets "sub-millisecond" if interpreted as single-digit milliseconds; if truly < 1ms, see explanation for C).
  - **Durability**: Data persists when VM stops/restarts.
  - Network-attached: Can be detached and reattached to different VMs.
  - Snapshots: Supports automatic backups.
  For most database workloads, SSD Persistent Disk is the standard choice.

- **C (Wrong)**: Local SSD provides the **fastest** latency (< 1ms for random I/O, physically attached to host), BUT:
  - **Ephemeral storage**: Data is **lost** when the VM stops (violates "data must survive VM restarts").
  - Use cases: Temporary cache, scratch space, rebuild-from-replica data.
  - Not for databases requiring durability.

- **D (Wrong)**: Cloud Filestore is a **managed NFS** service for shared filesystems:
  - Use case: Shared storage across multiple VMs (e.g., home directories, legacy apps).
  - Protocol: NFS (network file system).
  - **Not optimized** for database workloads (databases use block storage, not file storage).
  - Higher latency than SSD Persistent Disk.

---

## Section 2: Google Kubernetes Engine (GKE)

### Question 4: GKE Autopilot vs Standard

**Scenario**: A startup with 2 engineers wants to deploy containerized microservices on GKE. They don't have Kubernetes expertise and want to minimize operational burden. They need basic autoscaling and don't require node-level customization.

**Which GKE mode should they choose?**

A. GKE Standard (maximize control)  
B. GKE Autopilot (managed Kubernetes)  
C. Cloud Run (fully serverless)  
D. App Engine Flexible (managed containers)  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: GKE Standard provides full control over:
  - Node pools (machine types, OS images).
  - Networking (VPC config, custom subnets).
  - Node-level DaemonSets and customizations.
  However, this requires **Kubernetes expertise** to:
  - Right-size node pools.
  - Configure node auto-repair and auto-upgrade.
  - Manage security (patch OS, update Kubernetes versions).
  For a 2-person startup without K8s expertise, Standard mode means **high operational burden**.

- **B (Correct)**: ✅ GKE Autopilot is **opinionated Kubernetes**:
  - **Google manages nodes**: No node pools to configure. Autopilot dynamically provisions nodes based on pod requests.
  - **Pay per pod** (not per node): If pods request 2 vCPUs, you pay for 2 vCPUs (no idle node capacity waste).
  - **Auto-upgrades/patches**: Google handles Kubernetes version upgrades and security patches.
  - **Best practices enforced**: Autopilot requires workloads to follow best practices (limits/requests, no privileged pods).
  Perfect for the scenario: "minimize operational burden, no K8s expertise."

- **C (Wrong)**: Cloud Run is fully serverless (no clusters, instant autoscaling to zero), making it **simpler** than GKE Autopilot. However:
  - The scenario says "microservices" (plural), implying service-to-service communication, likely service mesh (Istio).
  - GKE provides advanced features (StatefulSets, DaemonSets, Jobs) that Cloud Run doesn't.
  - If the startup explicitly wants Kubernetes (perhaps for portability or future migration), Cloud Run doesn't provide that.
  Cloud Run is the **simplest** choice IF they don't specifically need Kubernetes. But given "deploy on GKE," Autopilot is the answer.

- **D (Wrong)**: App Engine Flexible uses containerized instances but:
  - Tied to App Engine's opinionated structure (services, versions, traffic splitting).
  - No service mesh (Istio).
  - No Kubernetes ecosystem (Helm charts, K8s manifests).
  If they want containers but not Kubernetes, App Engine Flexible works. But the scenario implies they want "GKE."

---

### Question 5: GKE Workload Identity

**Scenario**: A GKE pod needs to read objects from a Cloud Storage bucket. The development team is currently downloading a service account JSON key and mounting it as a Kubernetes Secret.

**What is the secure, Google-recommended approach?**

A. Continue using JSON key mounted as Secret (works fine)  
B. Configure Workload Identity to bind Kubernetes Service Account to Google Service Account  
C. Grant the GKE node pool's service account Storage Admin role  
D. Use a Cloud Storage FUSE mount instead  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Mounting JSON keys as Secrets is a **security anti-pattern**:
  - **Long-lived credentials**: JSON keys don't expire (unless manually rotated).
  - **Leakage risk**: Keys can be extracted from the pod, logged accidentally, or exposed if the cluster is compromised.
  - **Rotation burden**: Manually rotating keys across all pods is error-prone.
  Google explicitly recommends **never** using JSON keys for GKE workloads.

- **B (Correct)**: ✅ Workload Identity is the **secure, keyless** authentication method:
  1. Create a Kubernetes Service Account (KSA) in the pod namespace.
  2. Create a Google Service Account (GSA) with Storage Admin role.
  3. Bind KSA to GSA via IAM policy: `gcloud iam service-accounts add-iam-policy-binding ...`
  4. Annotate the KSA with the GSA email: `iam.gke.io/gcp-service-account: my-gsa@project.iam.gserviceaccount.com`
  5. Pods using the KSA automatically get **short-lived tokens** to act as the GSA (no keys needed).
  This is the **12-Factor App principle** (Factor III: Config in environment, not hardcoded keys).

- **C (Wrong)**: Granting the node pool's service account broad permissions (Storage Admin) is a **privilege escalation risk**:
  - **All pods** on the node inherit that permission (even pods that shouldn't access Storage).
  - Violates **least privilege** principle.
  - If one pod is compromised, the attacker gets Storage Admin across all pods.
  Workload Identity provides **per-pod** permissions, not per-node.

- **D (Wrong)**: Cloud Storage FUSE allows mounting buckets as filesystems, but it doesn't solve the **authentication** problem—you still need credentials to access the bucket. FUSE is a convenience layer (mount GCS as `/mnt/bucket`), not a security solution.

---

## Section 3: Cloud Run

### Question 6: Cloud Run vs Cloud Functions

**Scenario**: A team needs to process uploaded images:
- When an image is uploaded to Cloud Storage, generate 3 thumbnails (small, medium, large).
- Processing takes 30 seconds per image.
- Traffic: ~10 images/hour (low frequency).

**Which service is most appropriate?**

A. Cloud Run (container-based)  
B. Cloud Functions 1st gen (event-driven)  
C. Cloud Functions 2nd gen (Cloud Run under the hood)  
D. App Engine Standard (web app)  

**Answer: B** OR **C** (Both acceptable, but **B** is simpler for this use case) ✅

**Explanations**:
- **A (Partially Wrong)**: Cloud Run can absolutely handle this (it's what Cloud Functions 2nd gen uses internally), but:
  - Requires containerizing the code (Dockerfile).
  - Requires manual trigger setup (Eventarc or Pub/Sub subscriber).
  - More setup than Cloud Functions (which has built-in GCS triggers).
  Cloud Run is better for **HTTP-triggered services** or when you need custom runtimes. For simple event-driven tasks, Functions is simpler.

- **B (Correct for Simplicity)**: ✅ Cloud Functions 1st gen is **purpose-built** for this exact use case:
  - **Built-in GCS trigger**: `gcloud functions deploy --trigger-resource gs://bucket --trigger-event google.storage.object.finalize`
  - **Language support**: Python, Node.js, Go (no Dockerfile needed).
  - **Execution time**: 30 seconds fits well within limits (9 minutes default, 60 minutes max for 2nd gen).
  - **Pay per invocation**: At 10 images/hour × 30 seconds = 5 minutes of compute/hour → **very cheap** (cents/month).

- **C (Correct for Future-Proofing)**: ✅ Cloud Functions 2nd gen is **built on Cloud Run**, providing:
  - All the simplicity of 1st gen (built-in triggers).
  - Cloud Run benefits: longer execution time (60 minutes), larger instance sizes, better concurrency.
  - Future-proof: Google is investing in 2nd gen (1st gen is in maintenance mode).
  For new projects, **use 2nd gen**. But for the exam, **1st gen is acceptable** since it's simpler for this specific use case.

- **D (Wrong)**: App Engine Standard is for **web applications** (HTTP servers), not event-driven background tasks. You'd need to:
  - Run an HTTP endpoint that listens for Pub/Sub messages.
  - Set up a Pub/Sub topic to notify on GCS uploads.
  - Keep an App Engine instance running 24/7 to listen (wastes money for 10 images/hour).
  This is overengineering. Use Functions, not App Engine.

---

## Section 4: App Engine

### Question 7: App Engine Standard vs App Engine Flexible

**Scenario**: A Python Flask web app needs:
- Automatic scaling to zero when idle (no traffic at night).
- Support for Python 3.11.
- Startup time < 5 seconds.
- No custom system libraries required.

**Which App Engine environment should be used?**

A. App Engine Standard  
B. App Engine Flexible  
C. Cloud Run  
D. Compute Engine with autoscaling  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ App Engine Standard is the perfect fit:
  - **Scales to zero**: When idle, no instances run (zero cost for compute).
  - **Startup**: < 1 second (Standard uses sandboxed runtimes, very fast).
  - **Supported languages**: Python 3.11 is a **standard runtime** (officially supported).
  - **No custom OS libraries**: Standard provides pre-configured runtimes (Python, Node.js, Go, Java, etc.).
  - **Free tier**: 28 instance-hours/day free (great for low-traffic apps).

- **B (Wrong)**: App Engine Flexible uses **Docker containers** and provides more flexibility (custom system libraries, SSH access), but:
  - **Does NOT scale to zero**: Minimum 1 instance always running (wastes money during idle periods).
  - **Startup**: 30-60 seconds (slower than Standard).
  - **Cost**: Significantly more expensive than Standard.
  Use Flexible only if you need custom system libraries (e.g., C extensions, specific OS packages) that Standard doesn't support.

- **C (Wrong)**: Cloud Run could work (it scales to zero, fast startup), but:
  - Requires containerization (Dockerfile).
  - App Engine Standard is **simpler** (just `gcloud app deploy`, no Dockerfile).
  If the app was already containerized, Cloud Run would be a good choice. But given it's a simple Flask app, Standard is easier.

- **D (Wrong)**: Compute Engine with autoscaling:
  - **Does NOT scale to zero**: Minimum instance count is typically ≥ 1.
  - Requires manual setup (load balancer, instance template, MIG).
  - More operational burden than App Engine Standard.

---

## Section 5: Stateless vs Stateful Design

### Question 8: Session Management

**Scenario**: A web application stores user sessions in memory (in-process). When traffic spikes, Cloud Run creates multiple instances, causing users to lose their sessions when requests are routed to different instances.

**What is the 12-Factor App compliant solution?**

A. Enable sticky sessions in the load balancer to pin users to instances  
B. Store sessions in Memorystore (Redis)  
C. Use Cloud Run minimum instances = maximum instances to ensure single instance  
D. Store sessions in Cloud Storage  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Sticky sessions (session affinity) route users to the same instance based on a cookie. While this "works," it:
  - Violates **Factor VI (Stateless Processes)** of the 12-Factor App.
  - Creates uneven load distribution (some instances overloaded, others idle).
  - Fails during instance replacement (instance crashes → all sessions lost).
  - Prevents true horizontal scaling.

- **B (Correct)**: ✅ Memorystore (Redis) is the **stateless solution**:
  - All instances share the same Redis cache (central session store).
  - Sessions survive instance crashes, restarts, or scaling events.
  - Sub-millisecond latency (Redis is in-memory).
  - Follows **12-Factor App Factor VI**: Processes are stateless; state lives in **backing services** (Redis).

- **C (Wrong)**: Forcing a single instance defeats the purpose of Cloud Run's autoscaling:
  - Can't handle traffic spikes (single instance bottleneck).
  - No high availability (instance crashes → entire app down).
  - Violates cloud-native principles (horizontal scaling).

- **D (Wrong)**: Cloud Storage is **object storage** (high latency: 10-50ms), not suitable for real-time session lookups. Every request would incur:
  - API call overhead.
  - Network latency.
  - Cost (storage operations are charged per request).
  Use Memorystore (microsecond latency), not Cloud Storage.

---

## Answer Key Summary

1. **B** - Preemptible VMs for batch jobs (80% cost savings)
2. **A** - RPS-based autoscaling for traffic spikes
3. **B** - SSD Persistent Disk for database storage
4. **B** - GKE Autopilot for minimal ops burden
5. **B** - Workload Identity for keyless GKE auth
6. **B/C** - Cloud Functions (1st or 2nd gen) for event-driven tasks
7. **A** - App Engine Standard for scale-to-zero web apps
8. **B** - Memorystore for stateless session management

---

## Study Tips

1. **Compute Engine**: Understand preemptible VMs, MIG autoscaling metrics, Persistent Disk types.
2. **GKE**: Autopilot vs Standard trade-offs, Workload Identity (no JSON keys!).
3. **Cloud Run**: When to use vs Functions (HTTP vs events).
4. **App Engine**: Standard vs Flexible (scale to zero is the key differentiator).
5. **12-Factor App**: Factor VI (Stateless) comes up repeatedly in compute questions.
