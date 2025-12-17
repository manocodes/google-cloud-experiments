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
