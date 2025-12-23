# Google Cloud Professional Cloud Architect (PCA) Exam Tips

This guide summarizes the high-yield strategies and service differentiators needed to pass the PCA exam.

## 1. The "T-Shaped" Strategy
You do not need to memorize the specs of all 100+ Google Cloud products. Instead, focus on **Deep Knowledge** for the core services and **High-Level Awareness** for the rest.

### The Core 20 (Deep Knowledge Required)
Understand use cases, scaling limits, consistency models, and failure modes for these:

| Category | Services | what to Study |
| :--- | :--- | :--- |
| **Compute** | Compute Engine, GKE, Cloud Run, Cloud Functions, App Engine | VM vs. Container vs. Serverless trade-offs. |
| **Storage** | Cloud Storage, Persistent Disk | Storage classes (Standard/Nearline/Coldline/Archive) and lifecycle rules. |
| **Database** | Cloud SQL, Spanner, Bigtable, Firestore, BigQuery | ACID compliance, regional vs. global, relational vs. NoSQL. |
| **Network** | VPC, Load Balancing, Interconnect, VPN, CDN | Hybrid connectivity and global vs. regional load balancing. |
| **Security** | IAM, KMS, Security Command Center | Service Accounts, Roles, and encryption keys. |
| **Ops** | Cloud Monitoring, Cloud Logging | Observability and debugging. |

### Secondary Tier (High-Level Awareness)
Know a 1-sentence definition to rule these **in** or **out** as distractors.
*   **Data/AI**: Dataflow, Dataproc, Pub/Sub, Vertex AI.
*   **Security**: Cloud Armor, DLP API.
*   **Migration**: Migrate for Compute Engine.

---

## 2. Service Decision Cheat Sheet (The "Versus" Guide)
The exam frequently asks you to choose between two similar services. Use this logic:

### Compute Decision Tree
*   **General Limits?** -> **Compute Engine (GCE)** (Most flexible, most management).
*   **Containerized?**
    *   Standard Web App / Microservices? -> **Cloud Run** (Serverless, easiest).
    *   Complex orchestration / Legacy limits? -> **GKE** (K8s standard).
*   **Event Driven (e.g., file upload)?** -> **Cloud Functions** (Snippet of code).
*   **Legacy App (Java/Python/Go) with no container?** -> **App Engine** (Standard for scale to zero, Flexible for custom runtimes).

### Database Decision Tree
*   **Relational (SQL)?**
    *   **Regional** (single region) or < 30TB? -> **Cloud SQL**.
    *   **Global** (multi-region active-active) or Infinite scale? -> **Cloud Spanner** (More expensive).
*   **NoSQL?**
    *   **Analytics / High Throughput / IoT / Time Series?** -> **Cloud Bigtable** (Flat, fast, requires optimization).
    *   **Mobile / Web App Backend / Documents?** -> **Firestore** (Hierarchical, flexible).
*   **Data Warehousing (SQL for Analytics)?** -> **BigQuery**.

### Data Processing Decision Tree
*   **New Pipeline / Streaming / Serverless?** -> **Dataflow** (Apache Beam).
*   **Existing Hadoop/Spark Migration?** -> **Dataproc** (Managed Hadoop cluster).

### Connectivity Decision Tree
*   **High Speed (>10Gbps) / Reliability Critical?** -> **Dedicated Interconnect** (Physical cable).
*   **Quick Setup / Low Cost / Encrypted over Public Internet?** -> **Cloud VPN**.

---

## 3. Exam Strategy: Case Studies
You will be presented with 4 case studies (e.g., Mountkirk Games, TerramEarth). Do not memorize the text, but memorize the **patterns**:

*   **Mountkirk Games (Mobile Game)**: Needs global autoscaling, low latency.
    *   *Solution:* GKE or Cloud Run (Compute), Spanner (Global DB), Global Load Balancer.
*   **TerramEarth (Industrial IoT)**: Needs massive data ingestion from sensors.
    *   *Solution:* IoT Core (Concepts) -> Pub/Sub -> Dataflow -> BigQuery (Analytics) & Bigtable (Hot storage).
*   **EHR Healthcare (Legacy Migration)**: Needs compliance, security, hybrid connectivity.
    *   *Solution:* Interconnect/VPN, GKE (Anthos) for hybrid, DLP API for sensitive data.
*   **Helicopter Racing League (Real-time stream)**: Needs real-time video/telemetry processing.
    *   *Solution:* Pub/Sub, Dataflow, Video Intelligence API.

## 4. Key Concepts to "Watch Out" For
*   **Global vs. Regional**: Load Balancers comes in both flavors. Know which is which.
*   **Managed vs. Unmanaged**: Google prefers **Managed** services (e.g., Cloud SQL over installing MySQL on GCE) unless specific requirements prevent it.
*   **Preemptible / Spot VMs**: Always the answer for "reducing costs" on batch/fault-tolerant jobs.
*   **Nearline / Coldline**: Always the answer for "infrequently accessed data" cost optimization.

## 5. Common Distractors & Anti-Patterns
These are almost **always wrong** answers in the exam:

*   **"Install [Database] on Compute Engine"**: Google wants you to use Managed Services (Cloud SQL). Only do this if they specifically mention "OS tuning" or an unsupported database version.
*   **"Use local SSD for persistent storage"**: Local SSD is ephemeral. It dies when the VM stops. Never use it for data you can't afford to lose.
*   **"Cloud Bigtable for < 1 TB"**: Bigtable is for massive scale (Petabytes). For small data, it's too expensive and slow to warm up. Use Firestore or Cloud SQL.
*   **"Transfer Appliance for < 10 TB"**: Physical shipping takes weeks. For "small" big data (< 10TB), sticking it over the network (gsutil/Storage Transfer Service) is faster.
*   **Niche Products as Default Answers**: Products like *Cloud Talent Solution*, *Genomics API*, or *Game Servers* are usually distractors unless the question is explicitly about HR, Biology, or Gaming.

## 6. Exam Mechanics Tips
*   **Eliminate the "Lazy" option**: Answers that say "Email Google Support" or "File a ticket" are rarely correct for technical problems.
*   **Eliminate the "Insecure" option**: Any option that suggests `0.0.0.0/0` (open to world) or "Grant Owner role" is wrong.
*   **Key Words**:
    *   "Global" + "Low Latency" + "Relational" = **Spanner**.
    *   "Standard SQL" + "Analytics" = **BigQuery**.
    *   "Lift and Shift" + "No Code Changes" = **Migrate for Compute Engine**.
    *   "Cost Optimization" + "Batch" = **Preemptible/Spot VMs**.

## 7. Resource Hierarchy & Organization Policies
This is a **High Priority** topic. You must understand how governance flows down.

### The Hierarchy
1.  **Organization** (Root Node): The company. Top-level billing and policy powerhouse.
    *   *Requirement:* Needs Google Workspace or Cloud Identity.
2.  **Folders** (Departments/Teams): Logical grouping for isolation (e.g., "HR", "Engineering" or "Prod", "Test").
3.  **Projects** (Trust Boundary): The atomic unit of billing and permissions.
    *   *Rule:* Resources (VMs, Buckets) live inside Projects. They DO NOT live in folders directly.
4.  **Resources**: The actual services (VMs, Buckets, Tables).

### Organization Policies (The "Guardrails")
Unlike IAM (which says *WHO* can do something), Org Policies check *WHAT* is being done.
*   **Inheritance**: Policies set at the Org level apply to ALL folders and projects unless overridden.
*   **Common Exam Scenarios**:
    *   *Scenario:* "Ensure no developers can create public load balancers."
        *   *Answer:* Set an **Organization Policy** constraint (`compute.restrictLoadBalancerCreationForTypes`) on the specific Folder for developers.
    *   *Scenario:* "Restrict resources to only the 'us-central1' region for compliance."
        *   *Answer:* Set the `gcp.resourceLocations` Org Policy constraint.
    *   *Distractor Alert:* Do NOT use IAM for these constraints. IAM controls access, not configuration.


### Best Practices for the Exam
*   **Environment Isolation**: Use **Separate Projects** for Dev, Test, and Prod. Do NOT put them in the same project just to save time.
*   **Billing**: Billing Accounts are linked to Projects. A single Billing Account can pay for multiple Projects (centralized billing).
*   **Least Privilege**: Apply broad permissions (e.g., "Viewer") at the Folder level, and specific permissions (e.g., "Storage Admin") at the Project level.

## 8. Identity & Authentication Strategy (ADC & Workload Identity)
The exam tests if you know the **secure** way to connect diverse systems.

### The "No Keys" Rule
*   **Anti-Pattern (Wrong)**: "Download a Service Account JSON key" or "Store keys in code/config/metadata."
    *   *Why:* Keys are long-lived secrets that get leaked.
*   **The "Correct" Pattern (Google Internal)**: Use **Attached Service Accounts**.
    *   *Action:* Attach the Service Account to the VM/function. Use simple client code (`storage.Client()`) which relies on **ADC**.
*   **The "Correct" Pattern (External/Multi-Cloud)**: Use **Workload Identity Federation**.
    *   *Scenario:* AWS EC2, Azure VM, or GitHub Actions needs to access BigQuery.
    *   *Action:* Configure a Workload Identity Pool. Exchange the AWS/Azure token for a short-lived Google token. **No JSON keys involved.**

### Debugging Access Issues
*   **"Works on my machine, fails in prod"**: This is almost always an **ADC Identity Mismatch**.
    *   *Local:* Uses YOUR user credentials (`gcloud auth application-default login`).
    *   *Prod:* Uses the Service Account attached to the resource.
    *   *Fix:* Check the IAM roles granted to the **Service Account**, not your user.

### IAM Management
*   **Users vs. Groups**: ALWAYS grant roles to **Google Groups**, never individual users.
    *   *Reason:* It allows you to add/remove team members without updating IAM policies on every project.



## 9. Detailed Study Guides
*   **Compute Engine**: [gcp_compute_engine_study_plan.md](./compute/gcp_compute_engine_study_plan.md) - Comprehensive deep dive into GCE, including machine types, MIGs, and storage options.
*   **App Engine**: [gcp_app_engine_study_guide.md](./compute/gcp_app_engine_study_guide.md) - Deep dive into GAE Standard vs. Flexible and exam strategy.
*   **Cloud Storage**: [gcp_storage_pca_cram_sheet.md](./storage/gcp_storage_pca_cram_sheet.md) - Cram sheet for Cloud Storage classes, locations, and consistency.
*   **Block Storage**: [gcp_block_storage_pca_cram_sheet.md](./storage/gcp_block_storage_pca_cram_sheet.md) - Deep dive into Persistent Disk, Local SSD, and Filestore.
*   **Filestore**: [gcp_filestore_pca_cram_sheet.md](./storage/gcp_filestore_pca_cram_sheet.md) - Managed NFS for shared filesystems and legacy apps.
*   **Storage Comparison**: [gcp_storage_comparison.md](./storage/gcp_storage_comparison.md) - The "Big 3" Comparison Table (Object vs Block vs File).
