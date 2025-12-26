# Cloud SQL for PCA

## Fundamentals
- **Service Type**: Fully managed relational database service (RDBMS).
- **Engines**: MySQL, PostgreSQL, SQL Server.
- **Use Cases**: General-purpose web frameworks (Django, Rails, etc.), CRM, ERP, eCommerce (uCommerce), current relational database migration to cloud (lift and shift).
- **Scaling**: 
  - **Vertical**: Increase machine type (CPU/RAM). Requires restart.
  - **Horizontal**: Read replicas for read scaling. *Not* for write scaling (creates consistency lag).
- **High Availability (HA)**: Regional (Multi-Zone). Standby instance in a different zone in the same region. Automatic failover (synchronous replication).
- **Maintenance**: Automated patching. **Requires downtime** (usually < 60s). HA setup minimizes this but does *not* eliminate it.

---

## Why Cloud SQL vs Self-Managed Database on Compute Engine?
*This is a **critical exam question pattern**. The exam tests whether you understand **Total Cost of Ownership (TCO)** and **Operational Excellence**.*

### The Scenario (Common Exam Trap)
> "A startup wants to run a MySQL database. They have a small team. Should they use Cloud SQL or install MySQL on a Compute Engine VM?"

**Wrong Answer**: "VMs are cheaper, so use Compute Engine."

**Right Answer**: **Cloud SQL** (unless there's a specific blocker).

### Why Cloud SQL Wins (The Hidden Costs of VMs)

| Operational Task | Cloud SQL | Self-Managed on Compute Engine |
| :--- | :--- | :--- |
| **Patching/Updates** | Automatic (Google handles it). | You must SSH, `apt-get update`, test, reboot. |
| **Backups** | Automatic daily + Point-in-Time Recovery. | You write scripts (cron + `mysqldump`), manage storage. |
| **High Availability** | One checkbox (Automatic failover). | You architect Primary + Standby, configure replication, set up health checks, write failover scripts. |
| **Networking** | Private IP (VPC Peering/PSC), Cloud SQL Proxy (auto-encrypts), Authorized Networks. | You manually configure VPC firewall rules, bastion hosts, VPN/Interconnect routing, subnet design, public/private IP management. |
| **Data Import/Export** | Console UI or `gcloud sql import/export` (direct from/to Cloud Storage). Automated serverless jobs. | Write custom scripts, manage temporary storage, handle character encoding issues, monitor transfer manually. |
| **Schema Updates** | Apply directly via Cloud Console, `gcloud`, or client. Cloud SQL manages connections during update. | SSH to VM, run migration scripts, manually coordinate app downtime, handle connection draining, rollback manually if it fails. |
| **Monitoring** | Integrated Cloud Monitoring (built-in). | You install Prometheus/Grafana or Cloud Ops Agent manually. |
| **Scaling** | API call or Console click. | Provision new VM, migrate data, coordinate downtime. |
| **Security** | Automated SSL, IAM Database Auth, Private IP. | You configure SSL certificates, firewall rules, key rotation. |
| **Disaster Recovery** | Cross-region read replicas (managed). | You configure async replication, test failover manually. |
| **Cost (TCO)** | Higher $ upfront, **Lower Total Cost**. | Lower $ upfront, **Higher Total Cost** (engineer time). |

### The TCO Formula (Exam Perspective)
```
Total Cost = Infrastructure Cost + Operational Cost
```

- **Cloud SQL**: High infra cost ($200/month), Low ops cost (5 hrs/month × $100/hr = $500) = **$700/month**.
- **Self-Managed VM**: Low infra cost ($50/month), High ops cost (40 hrs/month × $100/hr = $4000) = **$4050/month**.

**Exam Insight**: The "cheaper" VM is actually **5-10x more expensive** when you factor in engineer time.

### When to Use Self-Managed VM Instead
You should **only** recommend Compute Engine + MySQL if:
1. **The database engine is NOT supported** by Cloud SQL (e.g., Oracle on Linux, Db2).
2. **Extreme customization** is required (custom kernel modules, weird OS-level tweaks).
3. **Regulatory/Compliance** mandates self-management (rare, but some audits require "full control").
4. **Cost Optimization for MASSIVE scale**: If you're running 500+ database instances and have a dedicated DBA team, VMs *might* be cheaper at that scale (but then you'd likely use Kubernetes + operators).

### Exam Keywords to Watch
- **"Small team"** → Cloud SQL (they can't afford the ops burden).
- **"Focus on core business"** → Cloud SQL (don't waste time on undifferentiated heavy lifting).
- **"Reduce operational overhead"** → Cloud SQL.
- **"Must have full OS control"** → Compute Engine VM.
- **"Non-standard database engine"** → Compute Engine VM or Bare Metal Solution.

---

## Critical Information
- **Storage Limit**: Up to 64 TB (varies by engine, but 64 TB is the general max for Postgres/MySQL).
- **Replication**:
  - **Read Replicas**: For offloading read traffic. Cross-region read replicas supported for disaster recovery (DR) and read-locality.
  - **High Availability**: Synchronous replication to standby.
- **Backups**:
  - **Automated**: Daily, retained for 7 backups (default).
  - **On-demand**: User initiated.
  - **Point-in-Time Recovery (PITR)**: By enabling binary logs (MySQL) or write-ahead logs (Postgres).
- **Maintenance**: Defines a window for OS/database patching. Connection drops during maintenance.

## Traps & "Gotchas"
1. **Write Scaling**: Cloud SQL does **NOT** scale writes horizontally. If you need massive write scaling (millions of QPS), Cloud SQL is the wrong answer. -> Look at **Cloud Spanner**.
2. **Global Reach**: Cloud SQL is a **Regional** resource. If you need a strictly global database with active-active consistency across continents -> Look at **Cloud Spanner**.
3. **Capacity**: If your dataset exceeds 64 TB or requires petabytes -> Look at **Cloud Spanner** or **Bigtable** (if NoSQL).
4. **IAM Auth**: You can use IAM database authentication to log in without a password, but you still need a database user.

## Important Points / Exam Clues
- Keywords: "Relational", "Existing MySQL/Postgres", "Web Framework", "Lift and Shift", "Transactional", "Strong Consistency".
- **Cloud SQL Auth Proxy** (also called "Cloud SQL Proxy"):
    - **They are the SAME tool** (naming confusion!). Official name: "Cloud SQL Auth Proxy".
    - **What it does**: Secure tunnel from your app (GKE, Compute Engine, local machine) to Cloud SQL.
    - **Benefits**:
        1. **Automatic Encryption**: No need to manage SSL certificates.
        2. **IAM Authentication**: Uses service account credentials instead of database passwords.
        3. **No Public IP Needed**: Works with Private IP instances.
        4. **No Firewall Rules**: Doesn't require opening Cloud SQL to the internet via Authorized Networks.
    - **Exam Pattern**: "How to securely connect GKE to Cloud SQL?" → **Use Cloud SQL Auth Proxy as a sidecar container**.
- **Private Service Connect (PSC)**: The modern, preferred way to connect securely within VPCs (prevents IP peering exhaustion issues of the older Private Services Access).

## Tips
- Always check if the requirements mention "Global Scale" or "Regional". Regional = Cloud SQL is a contender. Global = Spanner.
- If the exam asks about "migrating an existing PostgreSQL database" with minimal changes -> Cloud SQL for PostgreSQL.
- **Downtime**: Changing machine type (vertical scaling) causes downtime. HA failover causes a brief downtime (seconds).
