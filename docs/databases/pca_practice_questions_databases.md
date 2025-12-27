# GCP Database PCA Practice Exam Questions

This document contains exam-style questions focused on Google Cloud databases, designed to test the concepts covered in the study guides.

---

## Question 1: Cloud SQL vs Self-Managed Database
**Scenario:** A startup with 5 engineers wants to deploy a PostgreSQL database for their web application. They are concerned about costs and have been quoted $150/month for Cloud SQL vs $40/month for a Compute Engine VM running PostgreSQL.

**Options:**
*   A. Use Compute Engine with PostgreSQL to minimize infrastructure costs
*   B. Use Cloud SQL despite higher infrastructure costs
*   C. Use Cloud Spanner for better scalability
*   D. Use Firestore to eliminate database management entirely

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Cloud SQL:** The $150/month includes automated backups, HA failover, patching, monitoring, and security. With only 5 engineers, they should focus on building features, not managing databases (12-Factor App principle: focus on core business). The TCO is lower when factoring in operational overhead (engineer hours).

**Why others are wrong:**
*   **A:** While the VM is cheaper upfront ($40/month), this doesn't account for operational costs. The startup will spend 30-40 engineer hours/month on patching, backups, HA setup, monitoring, and disaster recovery. Total Cost of Ownership (TCO) for the VM is actually much higher.
*   **C:** Cloud Spanner is overkill and extremely expensive ($1,000+/month minimum) for a startup web app. Spanner is for global-scale applications requiring horizontal write scaling.
*   **D:** Firestore is a NoSQL document database. The scenario explicitly mentions PostgreSQL, implying they have a relational schema. Migrating to Firestore would require complete application rewrite.
</details>

---

## Question 2: Cloud SQL Connectivity
**Scenario:** A GKE application needs to connect to a Cloud SQL database. The security team requires that the database must NOT be accessible from the public internet, and the connection must be encrypted without managing SSL certificates.

**Options:**
*   A. Enable Cloud SQL Public IP and add the GKE cluster's IP to Authorized Networks
*   B. Deploy the Cloud SQL Auth Proxy as a sidecar container in each Pod
*   C. Use Private Service Connect and connect directly via Private IP
*   D. Create a VPN tunnel between GKE and Cloud SQL

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Cloud SQL Auth Proxy:** It runs as a sidecar container, creates an encrypted tunnel (no SSL cert management needed), uses IAM authentication, and works with Private IP Cloud SQL. This is the Google-recommended pattern for GKE → Cloud SQL connectivity.

**Why others are wrong:**
*   **A:** Exposes Cloud SQL to the public internet (Public IP), violating the security requirement.
*   **C:** While Private Service Connect (PSC) is valid, it doesn't eliminate the need for SSL certificate management if you want encrypted connections. The Proxy handles encryption and IAM auth seamlessly.
*   **D:** VPN is for connecting on-premises networks to Google Cloud, not for connecting services within the same Google Cloud project.
</details>

---

## Question 3: Cloud SQL Scaling Limits
**Scenario:** A retail company's Cloud SQL database is experiencing 100% CPU during peak hours (Black Friday sales). They need to handle 500,000 writes per second globally. The database is already at the maximum machine type (96 vCPUs).

**Options:**
*   A. Add more read replicas to distribute the write load
*   B. Enable Cloud SQL High Availability to double write capacity
*   C. Migrate to Cloud Spanner for horizontal write scaling
*   D. Partition the database across multiple Cloud SQL instances

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Cloud Spanner:** Scales writes **horizontally** by adding nodes (Cloud SQL scales writes vertically, limited by max machine size). It can handle millions of QPS and provides global distribution (consistent with "globally" requirement) while maintaining ACID transactions.

**Why others are wrong:**
*   **A:** Read replicas only help with **read** scaling, not write scaling. All writes still go to the single primary.
*   **B:** HA provides a standby for failover, not increased write capacity. The standby allows for redundancy, not scaling.
*   **D:** Manual sharding allows scaling but creates massive operational burden (sharding logic, rebalancing, cross-shard transactions). Spanner solves this automatically.
</details>

---

## Question 4: Spanner Regional vs Multi-Region
**Scenario:** A US-based e-commerce company needs a database that can handle unlimited horizontal write scaling for their growing customer base (currently 10 million users in the US only). They need 99.99% SLA but not 99.999%. Write latency must be < 10ms.

**Options:**
*   A. Regional Spanner instance in `us-central1`
*   B. Multi-Region Spanner instance in `nam-eur-asia1`
*   C. Cloud SQL with read replicas
*   D. Bigtable regional cluster

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: A**

**Why:**
*   **Regional Spanner:** Meets the horizontal write scaling requirement. It costs **significantly less** than Multi-Region, provides 99.99% SLA, and offers lower latency for US users since data is not synchronized across continents.

**Why others are wrong:**
*   **B:** Multi-Region Spanner is ~3x more expensive and designed for global applications needing 99.999% SLA and survival of continent failure. Unnecessary for US-only users.
*   **C:** Cloud SQL scales writes vertically (limited). It cannot provide "unlimited horizontal write scaling."
*   **D:** Bigtable is NoSQL, lacking the relational schema and ACID transactions typically needed for e-commerce (orders, inventory).
</details>

---

## Question 5: Spanner Hotspotting
**Scenario:** A Cloud Spanner database for a logging system uses a primary key of `timestamp` (incrementing value). The operations team notices that write performance is poor and adding more nodes doesn't help. All writes are going to a single node.

**Options:**
*   A. Spanner is misconfigured; switch to Multi-Region for better distribution
*   B. The sequential primary key causes hotspotting; use UUIDv4 or bit-reverse the timestamp
*   C. Enable Spanner autoscaling to dynamically add nodes
*   D. Increase node count to 100 to handle the load

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Hotspotting:** Sequential primary keys cause all new writes to go to the single node responsible for the "end" of the key range. Solutions include using UUIDv4 (random distribution) or bit-reversed timestamps.

**Why others are wrong:**
*   **A:** Geographic configuration doesn't solve data distribution patterns.
*   **C:** Autoscaling (managed instance sizing) won't help if the key design forces all traffic to one split (node).
*   **D:** Adding nodes is useless if the traffic isn't distributed.
</details>

---

## Question 6: Bigtable vs Firestore
**Scenario:** A mobile gaming company needs to store player profile data (username, level, inventory items) for 100 million players. Players frequently query their own profile (~1,000 reads/sec per player during peak). The data structure is hierarchical (Player → Inventory → Items).

**Options:**
*   A. Firestore in Native mode
*   B. Cloud Bigtable
*   C. Cloud SQL
*   D. BigQuery

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: A**

**Why:**
*   **Firestore:** Optimized for hierarchical data (Document/Collection model), has native mobile SDKs (offline sync), handles real-time sync, and scales horizontally for millions of users. Excellent for "get profile" access patterns.

**Why others are wrong:**
*   **B:** Bigtable is for high-throughput analytics/time-series (millions of writes/sec) or massive flat data. Overkill and harder to use for hierarchical user profiles.
*   **C:** Storing 100M players in Cloud SQL requires massive vertical scaling. Hierarchical data is less efficient in relational tables (joins).
*   **D:** BigQuery is an OLAP warehouse (seconds latency), not an OLTP database for apps.
</details>

---

## Question 7: Bigtable Row Key Design
**Scenario:** A Bigtable table stores sensor data from IoT devices. The row key is currently `device_id#timestamp`. Performance is poor because queries like "get last 24 hours of data for device 12345" require scanning millions of rows.

**Options:**
*   A. Change to `timestamp#device_id` to sort by time
*   B. Use `reverse(device_id)#timestamp` to prevent hotspotting
*   C. Add a secondary index on `timestamp`
*   D. Partition the table by `device_id`

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: A**

**Why:**
*   **Row Key Design:** (Note based on common exam logic for *Timestamp Scans*): `timestamp#device_id` optimizes for "Get all data in Time Window X".
    *   *Correction/Refinement:* In reality, `timestamp` at the front creates massive hotspotting. But in the context of *filtering options provided*, A is the only one that allows scanning by time. Real-world best practice would be `hash(device)#timestamp` for device queries or field promotion, but for a "Time Scan" question, moving timestamp to front is the textbook answer (despite write hotspotting trade-offs).

**Why others are wrong:**
*   **B:** `reverse(device_id)` prevents hotspotting but randomizes data location, making range scans impossible.
*   **C:** Bigtable does not have secondary indexes.
*   **D:** Bigtable does not have explicit "partitioning" like BQ.
</details>

---

## Question 8: BigQuery Cost Optimization
**Scenario:** A data analyst runs this query daily on a 10 TB table in BigQuery: `SELECT * FROM logs WHERE DATE(timestamp) = '2025-12-25'`. The bill shows $50/day. How can costs be reduced?

**Options:**
*   A. Switch from On-Demand to Flat-Rate pricing
*   B. Partition the table by `timestamp` (DATE) and query specific partition
*   C. Create a materialized view for DATE = '2025-12-25'
*   D. Use BigQuery BI Engine to cache results

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Partitioning:** BigQuery charges by data scanned. Without partitioning, `SELECT *` scans the full 10 TB. With partitioning by DATE, it scans only the single day's partition (~30 GB), reducing cost by ~99%.

**Why others are wrong:**
*   **A:** Flat-rate requires high commitment ($2,000+/mo), more expensive for a single daily query.
*   **C:** Materialized views are for aggregations, not filtering `SELECT *`.
*   **D:** BI Engine is for dashboard caching (small results), not batch `SELECT *` dumps.
</details>

---

## Question 9: BigQuery vs Bigtable
**Scenario:** A company collects clickstream data (10 billion events/day). They need to: (1) Run complex SQL business intelligence reports weekly. (2) Serve real-time recommendations (query "last 10 clicks for user X" with < 10ms latency).

**Options:**
*   A. Store everything in BigQuery, query for both BI and real-time
*   B. Store everything in Bigtable, use BigQuery Federated Queries for BI
*   C. Store in Bigtable for real-time lookups, stream to BigQuery for BI
*   D. Store in Cloud Storage, query with BigQuery for BI, load into Firestore for real-time

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Lambda Architecture:** Use **Bigtable** for the high-throughput, low-latency "last 10 clicks" queries (Operational). Stream the data also to **BigQuery** for the complex weekly SQL analysis (Analytical). Best tool for each job.

**Why others are wrong:**
*   **A:** BigQuery has too high latency/cost for real-time app lookups.
*   **B:** Federated queries from BQ to Bigtable are slow and inefficient for complex BI joins.
*   **D:** Firestore is too expensive and has write limits (1 write/sec/doc) which might struggle with 10B events/day volume compared to Bigtable.
</details>

---

## Question 10: CAP Theorem Application
**Scenario:** A global social media platform needs a database for user posts. Requirements: Users in US, EU, and Asia must post simultaneously without waiting for cross-region replication. It's acceptable if a user in Japan sees a post from the US with a 2-second delay. The system must remain available even if the US-EU network link fails.

**Options:**
*   A. Cloud Spanner (CP)
*   B. Cassandra/DataStax (AP)
*   C. Cloud SQL (CA)
*   D. Bigtable (CP)

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **AP (Availability + Partition Tolerance):** The requirement allows for "eventual consistency" (2-second delay) but demands "availability during network failure." Cassandra is the classic AP choice.

**Why others are wrong:**
*   **A:** Spanner is CP (Strong Consistency). Writes would wait or fail during a partition to guarantee consistency, violating the "must post simultaneously without waiting" preference for availability over consistency.
*   **C:** Cloud SQL is regional (CA). It doesn't handle global distributed writes.
*   **D:** Bigtable is CP (Single master).
</details>

---

## Question 11: Database Migration Service vs Datastream
**Scenario:** A company has an on-premises Oracle database (5 TB). They want to: (1) Keep Oracle running on-premises for the core application. (2) Analyze historical transactions in BigQuery using SQL.

**Options:**
*   A. Use Database Migration Service to migrate Oracle → BigQuery
*   B. Use Datastream to replicate Oracle → BigQuery (CDC)
*   C. Export Oracle data monthly with `mysqldump` → Cloud Storage → BigQuery
*   D. Use BigQuery Federated Queries to query Oracle directly

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Datastream:** Purpose-built for serverless Change Data Capture (CDC). It streams changes from Oracle to BigQuery in real-time without stopping the on-prem database.

**Why others are wrong:**
*   **A:** DMS is for "Lift and Shift" migrations (e.g., Oracle to Cloud SQL/AlloyDB), not for continuous replication to BigQuery.
*   **C:** Monthly dumps result in stale data and are manual.
*   **D:** Querying on-prem Oracle from BQ is slow/unreliable and not natively supported as a high-performance pattern.
</details>

---

## Question 12: MongoDB Migration Decision
**Scenario:** A startup has a 500 GB MongoDB database backing their Node.js application. They want to migrate to Google Cloud within 3 months and want to minimize code changes.

**Options:**
*   A. Refactor the application to use Firestore Native mode
*   B. Deploy MongoDB Atlas from Google Cloud Marketplace
*   C. Migrate to Cloud Bigtable
*   D. Use BigQuery

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **MongoDB Atlas:** It's the "Lift and Shift" path. 100% API compatible, managed service, no code changes required.

**Why others are wrong:**
*   **A:** Firestore requires rewriting all query code (different API).
*   **C:** Bigtable is wide-column, not document. Requires rewrite.
*   **D:** BigQuery is OLAP, not suitable for app backend.
</details>

---

## Question 13: Memorystore Scaling
**Scenario:** A high-traffic application uses Memorystore for Redis. The dataset has grown to 450 GB, and the current instance is struggling. Maximum standalone size is 300 GB.

**Options:**
*   A. Upgrade the instance to the largest possible Basic Tier machine
*   B. Migrate to Memorystore for Redis Cluster
*   C. Use Cloud Bigtable for session management
*   D. Use Memorystore for Memcached for better vertical scaling

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Redis Cluster:** Supports sharding/horizontal scaling up to 5 TB. The standard move when you exceed the 300 GB limit of a standalone Redis instance.

**Why others are wrong:**
*   **A:** 300 GB is the hard limit for standalone.
*   **C:** Bigtable has higher latency (ms vs microseconds) than Redis.
*   **D:** Memcached also serves up to 300GB nodes usually and lacks Redis data structures needed for complex sessions.
</details>

---

## Question 14: BigQuery SQL Orchestration (Dataform)
**Scenario:** A data engineering team manages hundreds of SQL scripts in BigQuery. They struggle with manual execution orders, lack of versioning, and bad data reaching dashboards.

**Options:**
*   A. Cloud Data Fusion
*   B. Dataform
*   C. Cloud Composer (Airflow)
*   D. BigQuery Scheduled Queries

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Dataform:** Google's SQL-first transformation tool. It provides Git versioning, dependency graph (DAG) generation, and data quality assertions (validation).

**Why others are wrong:**
*   **A:** Data Fusion is a visual UI tool, less suited for "hundreds of script" engineers.
*   **C:** Cloud Composer (Airflow) is powerful but heavier/more complex to manage than Dataform for pure SQL pipelines.
*   **D:** Scheduled Queries lack version control and dependency management.
</details>

---

## Question 15: BigQuery Slot Management
**Scenario:** An "Executive Dashboard" fails to load during month-end because Data Science teams are running massive ad-hoc jobs in the same project, consuming all resources.

**Options:**
*   A. Move to BigQuery Flat-rate and increase slot limit
*   B. Use BigQuery Reservations to create a dedicated slot pool for the Dashboards
*   C. Partition the tables used by the Data Science team
*   D. Enable BI Engine for all Data Science datasets

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Reservations:** Allows you to isolate compute resources. You can assign a specific pool of slots (e.g., 500 slots) to the "Dashboard" project, ensuring it is never starved by the "Data Science" jobs.

**Why others are wrong:**
*   **A:** Increasing the limit usually just raises the ceiling; they will still fight for the shared pool.
*   **C:** Partitioning helps scan efficiency but doesn't solve compute contention.
*   **D:** BI Engine accelerates cached reads, but doesn't prevent huge queries from starving the system.
</details>

---

## Question 16: ETL Tool Selection
**Scenario:** Need to build an ETL pipeline from on-prem Oracle to BigQuery. The team consists of SQL analysts with no Java/Python experience. They need to see "Data Lineage".

**Options:**
*   A. Cloud Dataflow
*   B. Cloud Data Fusion
*   C. Cloud Dataproc
*   D. BigQuery Data Transfer Service

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Cloud Data Fusion:** Visual, point-and-click (no-code) interface perfect for non-coders. It has built-in Data Lineage tracking.

**Why others are wrong:**
*   **A:** Dataflow requires Java/Python coding.
*   **C:** Dataproc is for Hadoop/Spark (requires code).
*   **D:** DTS is simple ingestion, doesn't offer complex transformations or lineage visualization.
</details>

---

## Question 17: Privacy-Safe Data Collaboration
**Scenario:** An airline and credit card company want to analyze shared customers without revealing PII or raw transaction lists to each other.

**Options:**
*   A. Authorized Views
*   B. BigQuery Analytics Hub: Data Exchanges
*   C. BigQuery Data Clean Rooms
*   D. IAM-based dataset sharing

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Data Clean Rooms:** Specifically designed for multi-party compute where neither party sees the other's raw data. It enforces privacy thresholds (e.g., aggregations only).

**Why others are wrong:**
*   **A:** Authorized views filter data but don't prevent inference/joining if the raw data is underneath.
*   **B:** Exchanges act as a marketplace for subscription to datasets.
*   **D:** IAM sharing is full access.
</details>

---

## Question 18: File Formats for BigQuery Ingestion
**Scenario:** Designing a petabyte-scale daily ingestion pipeline into BigQuery. Deciding on the format for the "Raw Landing Zone" for best ingestion performance/reliability.

**Options:**
*   A. Compressed JSON (Gzip)
*   B. CSV with headers
*   C. Avro
*   D. Parquet

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: C**

**Why:**
*   **Avro:** Row-based, binary, split-table (parallel read), and includes schema in the header. It is the gold standard for high-throughput ingestion.

**Why others are wrong:**
*   **A:** JSON is slow to parse.
*   **B:** CSV is brittle (schema issues, delimiter issues).
*   **D:** Parquet is columnar (better for *reading*/*querying*), but Avro is faster for *writing/ingesting*.
</details>

---

## Question 19: Dashboard Performance Optimization
**Scenario:** A Looker dashboard querying a 500 GB BigQuery table is slow (8-10s). Data changes only once an hour. Need sub-second response.

**Options:**
*   A. Increase BigQuery slot reservation count
*   B. Enable BigQuery BI Engine with memory reservation
*   C. Cluster the table by `store_id` and `date`
*   D. Migrate the table to Memorystore for Redis

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **BI Engine:** In-memory caching layer for BigQuery. Delivers sub-second latency for dashboards by running from RAM.

**Why others are wrong:**
*   **A:** More slots = faster compute, but still scans disk.
*   **C:** Clustering improves prune speed (2-3s), but usually not sub-second.
*   **D:** Moving data warehouse data to Redis is architecturally complex/expensive.
</details>

---

## Question 20: Security for Hybrid Data Lakes
**Scenario:** Storing petabytes of historical files (Parquet/Iceberg) in Cloud Storage. Analysts need to query via BigQuery SQL with **Row-level security** enforced.

**Options:**
*   A. BigQuery Omni
*   B. BigLake
*   C. Cloud DLP API
*   D. Storage Transfer Service

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **BigLake:** Decouples the storage (GCS) from the compute/security (BigQuery). Allows you to define fine-grained security policies (Row/Column level) on files sitting in GCS.

**Why others are wrong:**
*   **A:** Omni is for multi-cloud (AWS/Azure).
*   **C:** DLP finds sensitive text, doesn't enforce row-level access control.
</details>

---

## Question 21: HIPAA BigQuery Access Control
**Scenario:** A healthcare provider must meet HIPAA requirements. They need fine-grained access to PHI datasets in BigQuery, ability to audit who accessed what, and protection against accidental public exposure.

**Options:**
*   A. BigQuery IAM at project level with only BigQuery Admin
*   B. BigQuery dataset-level IAM with Viewer, User, and custom roles plus Cloud Audit Logs for Data Access and org policies blocking public access
*   C. Rely on authorized views only
*   D. Export data to Cloud Storage and manage access via ACLs

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Dataset-level IAM with least-privilege roles:** Provides fine-grained access control.
*   **Cloud Audit Logs for Data Access:** Audits all data access operations.
*   **Organization policies:** Block public access, preventing accidental exposure.

**Why others are wrong:**
*   **A:** Project-level access with Admin role is far too broad and violates least privilege.
*   **C:** Authorized views are useful but not sufficient alone for complete access control and auditing.
*   **D:** Cloud Storage ACLs are less granular and BigQuery data queried via GCS doesn't provide the same audit trail.
</details>

---

## Question 22: BigQuery Streaming Optimization
**Scenario:** A streaming analytics pipeline uses Pub/Sub → Dataflow → BigQuery. BigQuery costs have risen sharply. You see many small streaming inserts.

**Options:**
*   A. Replace Dataflow with Cloud Functions
*   B. Use BigQuery Storage Write API with Dataflow and batch inserts, plus partitioned tables
*   C. Export Pub/Sub to Cloud Storage and load once per day
*   D. Disable streaming and rely on manual CSV uploads

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **BigQuery Storage Write API with batching:** Improves streaming efficiency and reduces costs compared to many small inserts.
*   **Partitioned tables:** Reduce storage and query costs by limiting data scanned.

**Why others are wrong:**
*   **A:** Cloud Functions don't address the BigQuery cost structure issue.
*   **C:** Daily batch loads may violate near real-time analytics requirements.
*   **D:** Manual uploads don't scale and lose real-time capabilities.
</details>

---

## Question 23: Database RTO/RPO
**Scenario:** A global SaaS app must have an RTO of 15 minutes and RPO of near-zero for its primary transactional database.

**Options:**
*   A. Single-region Cloud SQL with daily backups
*   B. Cloud SQL with cross-region read replica and planned failover automation
*   C. Bigtable single-cluster instance
*   D. Export database nightly to Cloud Storage

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Cross-region replicas with automated failover:** Offers low RPO (async replication lag typically < 1 minute) and RTO within minutes for regional outages, fitting the stated objectives.

**Why others are wrong:**
*   **A:** Single-region with daily backups has RPO of 24 hours and RTO of hours (restore time).
*   **C:** Bigtable single cluster doesn't provide cross-region redundancy.
*   **D:** Nightly exports have RPO of 24 hours.
</details>
