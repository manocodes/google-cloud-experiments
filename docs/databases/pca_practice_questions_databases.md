# GCP Database PCA Practice Exam Questions

This document contains exam-style questions based on the database study guides. Each question has 4 options with detailed explanations.

---

## Section 1: Cloud SQL

### Question 1: Cloud SQL vs Self-Managed Database

**Scenario**: A startup with 5 engineers wants to deploy a PostgreSQL database for their web application. They are concerned about costs and have been quoted $150/month for Cloud SQL vs $40/month for a Compute Engine VM running PostgreSQL.

**What should they choose?**

A. Use Compute Engine with PostgreSQL to minimize infrastructure costs  
B. Use Cloud SQL despite higher infrastructure costs  
C. Use Cloud Spanner for better scalability  
D. Use Firestore to eliminate database management entirely  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: While the VM is cheaper upfront ($40/month), this doesn't account for operational costs. The startup will spend 30-40 engineer hours/month on patching, backups, HA setup, monitoring, and disaster recovery. At $100/hr engineer cost, that's $3,000-$4,000/month in hidden costs. Total Cost of Ownership (TCO) for the VM is actually $4,040/month vs $700/month for Cloud SQL.
  
- **B (Correct)**: ✅ Cloud SQL's $150/month includes automated backups, HA failover, patching, monitoring, and security. With only 5 engineers, they should focus on building features, not managing databases (12-Factor App principle: focus on core business). The TCO is lower when factoring in operational overhead.

- **C (Wrong)**: Cloud Spanner is overkill and extremely expensive ($1,000+/month minimum) for a startup web app. Spanner is for global-scale applications requiring horizontal write scaling. The scenario doesn't mention global users or massive scale.

- **D (Wrong)**: Firestore is a NoSQL document database. The scenario explicitly mentions PostgreSQL, implying they have a relational schema. Migrating to Firestore would require complete application rewrite (violates "minimal changes" principle for startups).

---

### Question 2: Cloud SQL Connectivity

**Scenario**: A GKE application needs to connect to a Cloud SQL database. The security team requires that the database must NOT be accessible from the public internet, and the connection must be encrypted without managing SSL certificates.

**What is the recommended solution?**

A. Enable Cloud SQL Public IP and add the GKE cluster's IP to Authorized Networks  
B. Deploy the Cloud SQL Auth Proxy as a sidecar container in each Pod  
C. Use Private Service Connect and connect directly via Private IP  
D. Create a VPN tunnel between GKE and Cloud SQL  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: This exposes Cloud SQL to the public internet (Public IP), violating the security requirement. Even though Authorized Networks limits access, the database still has a public IP that could be scanned/attacked.

- **B (Correct)**: ✅ The Cloud SQL Auth Proxy:
  1. Runs as a sidecar container in the same Pod as the application.
  2. Creates an encrypted tunnel (no SSL cert management needed).
  3. Uses IAM authentication (service account credentials).
  4. Works with Private IP Cloud SQL (no public exposure).
  5. Application connects to `localhost:3306`, proxy handles everything else.
  This is the Google-recommended pattern for GKE → Cloud SQL connectivity.

- **C (Wrong)**: While Private Service Connect (PSC) is a valid and modern approach for VPC connectivity, it doesn't eliminate the need for SSL certificate management if you want encrypted connections. The Cloud SQL Auth Proxy provides both encryption and IAM auth seamlessly, making it the better choice for this scenario.

- **D (Wrong)**: VPN is for connecting on-premises networks to Google Cloud, not for connecting services within the same Google Cloud project. This is overengineering and introduces unnecessary complexity and latency.

---

### Question 3: Cloud SQL Scaling Limits

**Scenario**: A retail company's Cloud SQL database is experiencing 100% CPU during peak hours (Black Friday sales). They need to handle 500,000 writes per second globally. The database is already at the maximum machine type (96 vCPUs).

**What should they do?**

A. Add more read replicas to distribute the write load  
B. Enable Cloud SQL High Availability to double write capacity  
C. Migrate to Cloud Spanner for horizontal write scaling  
D. Partition the database across multiple Cloud SQL instances  

**Answer: C** ✅

**Explanations**:
- **A (Wrong)**: Read replicas only help with **read** scaling, not write scaling. They replicate data asynchronously from the primary instance but do NOT accept writes. All writes still go to the single primary instance, which is already at 100% CPU.

- **B (Wrong)**: Cloud SQL HA (High Availability) provides a standby instance for automatic failover, but it does NOT increase write capacity. The standby is a hot backup that synchronously replicates data but doesn't serve traffic during normal operations.

- **C (Correct)**: ✅ Cloud Spanner is the correct answer because:
  1. It scales writes **horizontally** by adding nodes (Cloud SQL scales writes vertically, limited by max machine size).
  2. It can handle millions of QPS (500K writes/sec is well within its capability).
  3. It provides global distribution for the "globally" requirement in the scenario.
  4. It maintains ACID transactions despite horizontal scaling.
  Cloud SQL has hit its ceiling—this is the classic "Cloud SQL → Spanner migration" scenario.

- **D (Wrong)**: Manual sharding (partitioning across multiple Cloud SQL instances) is technically possible but creates massive operational burden:
  - Application must implement sharding logic (which rows go to which instance).
  - Cross-shard transactions become complex or impossible (violates ACID).
  - Rebalancing data when shards fill up requires application changes.
  This is what Spanner solves automatically—don't reinvent the wheel.

---

## Section 2: Cloud Spanner

### Question 4: Spanner Regional vs Multi-Region

**Scenario**: A US-based e-commerce company needs a database that can handle unlimited horizontal write scaling for their growing customer base (currently 10 million users in the US only). They need 99.99% SLA but not 99.999%. Write latency must be < 10ms.

**Which Spanner configuration should they choose?**

A. Regional Spanner instance in `us-central1`  
B. Multi-Region Spanner instance in `nam-eur-asia1`  
C. Cloud SQL with read replicas  
D. Bigtable regional cluster  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ Regional Spanner (`us-central1`) is the right choice because:
  1. Meets the horizontal write scaling requirement (hundreds to thousands of nodes).
  2. Costs **significantly less** than Multi-Region (~$0.90/node/hr vs ~$3.00/node/hr).
  3. Provides 99.99% SLA (meets requirement, doesn't need 99.999%).
  4. Lower latency for US users (<10ms since data is in one region, not synchronized across continents).
  5. All users are in the US, so global replication is unnecessary waste of money.
  
- **B (Wrong)**: Multi-Region Spanner is **3x more expensive** and designed for truly global applications requiring:
  - 99.999% SLA (five nines).
  - Users distributed across continents needing local low-latency reads.
  - Surviving total failure of an entire continent.
  The scenario only mentions US users—spending 3x more for global replication is wasteful.

- **C (Wrong)**: The scenario explicitly requires "unlimited horizontal write scaling." Cloud SQL scales writes **vertically** (limited to ~64 vCPUs max). Read replicas don't help write scaling. Cloud SQL cannot handle this requirement.

- **D (Wrong)**: Bigtable is a NoSQL wide-column store, not a relational database. E-commerce applications typically need:
  - Relational schema (products, orders, customers with foreign keys).
  - ACID transactions (e.g., "deduct inventory AND create order" must be atomic).
  - SQL queries (complex joins for reporting).
  Bigtable has none of these (no joins, no SQL, single-row atomicity only).

---

### Question 5: Spanner Hotspotting

**Scenario**: A Cloud Spanner database for a logging system uses a primary key of `timestamp` (incrementing value). The operations team notices that write performance is poor and adding more nodes doesn't help. All writes are going to a single node.

**What is the problem and solution?**

A. Spanner is misconfigured; switch to Multi-Region for better distribution  
B. The sequential primary key causes hotspotting; use UUIDv4 or bit-reverse the timestamp  
C. Enable Spanner autoscaling to dynamically add nodes  
D. Increase node count to 100 to handle the load  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: The configuration (Regional vs Multi-Region) doesn't solve hotspotting. Hotspotting is caused by the **data distribution pattern**, not the geographic configuration. Multi-Region would make the problem worse (more replication overhead) and cost 3x more.

- **B (Correct)**: ✅ Sequential primary keys (like timestamps or auto-incrementing integers) cause all new writes to go to the **same node** (the one responsible for the highest key range). This is called **hotspotting**. Solutions:
  1. **UUIDv4**: Random UUIDs distribute writes evenly across nodes.
  2. **Bit-reverse timestamp**: `2023-12-25-10:00:00` becomes `00:00:01-52-21-3202`, spreading sequential writes.
  3. **Hash prefix**: Add a hash of the timestamp as a prefix (`hash(timestamp)_timestamp`).
  Spanner's performance guide explicitly warns about this anti-pattern.

- **C (Wrong)**: Autoscaling doesn't exist for Spanner (you manually set node/processing unit count). Even if it did, adding more nodes won't help if all writes go to a single node due to poor key design—you're just adding idle nodes that don't receive traffic.

- **D (Wrong)**: This is the same as option C. Adding nodes doesn't help if the data distribution (primary key design) forces all writes to one node. You're wasting money on 99 idle nodes. Fix the root cause (key design), not the symptom.

---

## Section 3: Bigtable

### Question 6: Bigtable vs Firestore

**Scenario**: A mobile gaming company needs to store player profile data (username, level, inventory items) for 100 million players. Players frequently query their own profile (~1,000 reads/sec per player during peak). The data structure is hierarchical (Player → Inventory → Items).

**Which database should they use?**

A. Firestore in Native mode  
B. Cloud Bigtable  
C. Cloud SQL  
D. BigQuery  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ Firestore Native mode is ideal because:
  1. **Document model**: Perfect for hierarchical data (`Player` document → `Inventory` subcollection → `Item` documents).
  2. **Mobile SDKs**: Native SDKs for iOS/Android with built-in caching and offline sync.
  3. **Real-time**: Automatically syncs changes to all connected clients (great for multiplayer games).
  4. **Scalability**: Handles 100M players easily (scales horizontally).
  5. **Query model**: Simple queries like "get profile for player X" are fast.

- **B (Wrong)**: Bigtable is better for:
  - **Analytics** use cases (massive scans, time-series).
  - Data > 1 TB (scenario doesn't mention size).
  - Very high write throughput (millions of writes/sec).
  For reading individual player profiles, Bigtable is overkill and expensive. Firestore is cheaper and simpler for this access pattern.

- **C (Wrong)**: Cloud SQL could technically store this data (relational tables), but:
  - 100 million players would require massive vertical scaling (expensive).
  - Relational joins for hierarchical data (Player → Inventory → Items) are slower than document model.
  - No built-in mobile SDK or offline sync.
  - Overkill for simple key-value lookups.

- **D (Wrong)**: BigQuery is a **data warehouse** for analytics (OLAP), not an operational database (OLTP). It's optimized for:
  - Running complex queries over billions of rows (e.g., "average player level across all players").
- It's terrible for:
  - Point lookups ("get player X's profile") → latency is seconds, not milliseconds.
  - High-frequency individual reads/writes.

---

### Question 7: Bigtable Row Key Design

**Scenario**: A Bigtable table stores sensor data from IoT devices. The row key is currently `device_id#timestamp`. Performance is poor because queries like "get last 24 hours of data for device 12345" require scanning millions of rows.

**How should the row key be redesigned?**

A. Change to `timestamp#device_id` to sort by time  
B. Use `reverse(device_id)#timestamp` to prevent hotspotting  
C. Add a secondary index on `timestamp`  
D. Partition the table by `device_id`  

**Answer: A** ✅

**Explanations**:
- **A (Correct)**: ✅ For time-range queries ("last 24 hours"), you want rows sorted by timestamp. The row key `timestamp#device_id` allows:
  - Efficient range scans: `SCAN from '2025-12-24' to '2025-12-25'`.
  - All rows for a time range are stored together (locality).
  However, this can cause **hotspotting** if all devices write at the same time (all writes go to the latest timestamp range). A better design is `reverse(timestamp)#device_id` to distribute writes, but option A is the best among the given choices for read performance.

- **B (Wrong)**: Reversing the device ID prevents hotspotting but doesn't solve the query problem. The row key `reverse(device_id)#timestamp` still requires scanning all reversed device IDs to find device 12345's data. This doesn't help time-range queries at all.

- **C (Wrong)**: Bigtable does **NOT support secondary indexes**. All queries must use the row key. This is a fundamental limitation of wide-column NoSQL databases (unlike Firestore which auto-indexes all fields).

- **D (Wrong)**: Bigtable doesn't have a "partition table" feature. Splitting data across multiple tables defeats the purpose of Bigtable's horizontal scaling—you'd have to manage which table to query, and cross-table queries are impossible.

---

## Section 4: BigQuery

### Question 8: BigQuery Cost Optimization

**Scenario**: A data analyst runs this query daily on a 10 TB table in BigQuery:
```sql
SELECT * FROM `project.dataset.logs`
WHERE DATE(timestamp) = '2025-12-25'
```
The bill shows $50/day for this single query. How can costs be reduced?

**What is the BEST optimization?**

A. Switch from On-Demand to Flat-Rate pricing  
B. Partition the table by `timestamp` (DATE) and query specific partition  
C. Create a materialized view for DATE = '2025-12-25'  
D. Use BigQuery BI Engine to cache results  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Flat-Rate pricing (paying for reserved slots) only makes sense if you're already running hundreds of expensive queries daily. For a single $50/day query, flat-rate would cost $2,000+/month (minimum commitment), vs $1,500/month on-demand. This is more expensive, not cheaper.

- **B (Correct)**: ✅ Partitioning solves the root cause:
  - **Current problem**: `SELECT *` scans all 10 TB even though filtering by one day.
  - BigQuery charges by **data scanned** (not rows returned).
  - With partitioning by DATE(timestamp):
    - Table is divided into daily partitions (e.g., `2025-12-25`  partition = ~30 GB).
    - Query becomes: `WHERE DATE(timestamp) = '2025-12-25'` → BigQuery scans **only that partition** (30 GB, not 10 TB).
  - Cost drops from $50 ($5/TB × 10 TB) to $0.15 ($5/TB × 0.03 TB). **99% cost reduction!**

- **C (Wrong)**: Materialized views are useful for **aggregations** (e.g., `SELECT COUNT(*), AVG(value) GROUP BY date`), not for daily full-table queries with changing filter values. Creating a new materialized view for each day is impractical and defeats the purpose.

- **D (Wrong)**: BI Engine accelerates **dashboard queries** (repeated queries with sub-second responses), not batch queries. It caches small result sets (GBs, not TBs). A daily `SELECT *` from 30 GB won't benefit from BI Engine.

---

### Question 9: BigQuery vs Bigtable

**Scenario**: A company collects clickstream data from their website (10 billion events/day). They need to:
1. Run complex SQL queries for business intelligence reports (weekly).
2. Serve real-time recommendations (query "last 10 clicks for user X" with < 10ms latency).

**What is the optimal architecture?**

A. Store everything in BigQuery, query for both BI and real-time  
B. Store everything in Bigtable, use BigQuery Federated Queries for BI  
C. Store in Bigtable for real-time lookups, stream to BigQuery for BI  
D. Store in Cloud Storage, query with BigQuery for BI, load into Firestore for real-time  

**Answer: C** ✅

**Explanations**:
- **A (Wrong)**: BigQuery is optimized for **OLAP** (analytical queries over billions of rows), not **OLTP** (operational queries like "get last 10 clicks for user X"). Real-time queries in BigQuery have:
  - High latency (seconds, not milliseconds).
  - High cost (charged by data scanned, even for small results).

- **B (Wrong)**: While BigQuery Federated Queries *can* query Bigtable directly, it's:
  - Slow (network overhead from BQ → Bigtable).
  - Inefficient (Bigtable isn't optimized for complex SQL aggregations and joins).
  - Expensive (BQ charges for compute, Bigtable charges for reads).

- **C (Correct)**: ✅ This follows the **separation of concerns** pattern:
  1. **Bigtable**: Stores hot data (last 30 days) for real-time lookups.
     - Row key: `user_id#reverse(timestamp)` (fast range scans for "last 10 clicks").
     - Millisecond latency for operational queries.
  2. **Pub/Sub → Dataflow → BigQuery**: Stream same data to BigQuery for analytics.
     - BigQuery stores all historical data (years).
     - Weekly BI reports run SQL queries (GROUP BY, JOIN, etc.).
  This is the **Lambda Architecture** pattern Google recommends for this use case.

- **D (Wrong)**: Loading into Firestore for real-time is possible but inefficient:
  - Firestore has soft write limits (~1 write/sec per document). For 10 billion events/day (116K/sec), you'd need complex sharding.
  - Firestore pricing is by operations (reads/writes). Bigtable is cheaper for this high-throughput pattern.

---

## Section 5: CAP Theorem & Database Selection

### Question 10: CAP Theorem Application

**Scenario**: A global social media platform needs a database for user posts. Requirements:
- Users in US, EU, and Asia must be able to post simultaneously without waiting for cross-region replication.
- It's acceptable if a user in Japan sees a post from the US with a 2-second delay.
- The system must remain available even if the US-EU network link fails.

**Which database prioritizes the right CAP properties?**

A. Cloud Spanner (CP - Consistency + Partition Tolerance)  
B. Cassandra/DataStax (AP - Availability + Partition Tolerance)  
C. Cloud SQL (CA - Consistency + Availability)  
D. Bigtable (CP - Consistency + Partition Tolerance)  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Cloud Spanner is **CP** (Consistency + Partition Tolerance). It guarantees strong consistency globally using Paxos and TrueTime. This means:
  - Writes must wait for a quorum (majority) of replicas to commit (adds latency for cross-region writes).
  - During network partition (US-EU link fails), writes might pause until quorum is restored.
  The scenario accepts eventual consistency ("2-second delay acceptable"), so Spanner's strong consistency is unnecessary and adds latency/cost.

- **B (Correct)**: ✅ Cassandra is **AP** (Availability + Partition Tolerance):
  - **Multi-datacenter active-active writes**: Users in US, EU, Asia can all write simultaneously to their local Cassandra datacenter.
  - **Eventual consistency**: Writes replicate asynchronously. A user in Japan might see a 2-second delay for a post from the US (acceptable per scenario).
  - **Partition tolerance**: If US-EU network fails, both datacenters continue accepting writes independently, then sync when the link recovers.
  This matches the scenario's priorities perfectly.

- **C (Wrong)**: Cloud SQL is **CA** (Consistency + Availability) within a single region, but it's **not a distributed database**. It cannot handle "users in US, EU, Asia posting simultaneously" because:
  - Cloud SQL is regional (e.g., `us-central1`).
  - Cross-region read replicas exist but are **async** (read-only). Writes must go to the primary in one region.
  - If the primary region fails, manual failover is required (violates "availability during partition").

- **D (Wrong)**: Bigtable is **CP**, not **AP**. It uses single-master writes (primary cluster in one region). While read replicas exist, they're:
  - Read-only (can't accept writes during partition).
  - Asynchronously replicated (eventual consistency for reads, but writes are still centralized).
  Cassandra's multi-master writes are superior for this use case.

---

## Section 6: Migration & Data Movement

### Question 11: Database Migration Service vs Datastream

**Scenario**: A company has an on-premises Oracle database (5 TB) that stores customer transactions. They want to:
1. Keep Oracle running on-premises for the core application (compliance requirement).
2. Analyze historical transactions in BigQuery using SQL.

**What is the recommended approach?**

A. Use Database Migration Service to migrate Oracle → BigQuery  
B. Use Datastream to replicate Oracle → BigQuery (CDC)  
C. Export Oracle data monthly with `mysqldump` → Cloud Storage → BigQuery  
D. Use BigQuery Federated Queries to query Oracle directly  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Database Migration Service (DMS) is designed for **homogeneous migrations** (e.g., MySQL → MySQL, Postgres → Postgres). While DMS has some heterogeneous features (Oracle → Postgres), it doesn't support Oracle → BigQuery directly. More importantly, DMS is for **"lift and shift"** (moving the database), but the scenario requires keeping Oracle on-premises running.

- **B (Correct)**: ✅ Datastream is purpose-built for this scenario:
  - **Change Data Capture (CDC)**: Reads Oracle's redo logs to capture all changes (inserts/updates/deletes).
  - **Streaming**: Continuously replicates data to BigQuery in near real-time (minutes).
  - **Heterogeneous**: Oracle (on-prem) → BigQuery (cloud).
  - **No disruption**: Oracle keeps running; application is unaffected.
  Datastream acts as a "data pipeline" allowing the operational Oracle database to coexist with the analytical BigQuery warehouse.

- **C (Wrong)**: Monthly exports with `mysqldump` have several problems:
  - **Wrong tool**: `mysqldump` is for MySQL, not Oracle (`expdp` or `datapump` is the Oracle equivalent).
  - **Stale data**: Monthly exports mean analysts work with data that's up to 30 days old.
  - **Downtime**: Large exports can impact Oracle performance.
  - **Manual**: Requires custom scripting and monitoring.
  Datastream automates this with streaming CDC.

- **D (Wrong)**: BigQuery Federated Queries allow querying external sources (Cloud SQL, Bigtable, Cloud Storage), but **Oracle is not a supported source**. Even if it were, querying on-prem databases from BigQuery over the internet would be:
  - Slow (network latency).
  - Expensive (BQ charges for data scanned, Oracle charges for queries).
  - Unreliable (dependent on internet connectivity).

---

### Question 12: MongoDB Migration Decision

**Scenario**: A startup has a 500 GB MongoDB database backing their Node.js application. They want to migrate to Google Cloud. The engineering team has 3 months and wants to minimize code changes.

**What is the recommended migration path?**

A. Refactor the application to use Firestore Native mode  
B. Deploy MongoDB Atlas from Google Cloud Marketplace  
C. Migrate to Cloud Bigtable (both are NoSQL)  
D. Use BigQuery (supports JSON natively)  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Firestore is Google's native document database and is excellent, but:
  - **Different API**: MongoDB uses MongoDB Query Language (MQL: `db.collection.find({})`). Firestore uses its own SDK. This requires rewriting all database queries in the application.
  - **Different data model**: Subtle differences in how documents and subcollections work.
  - **3-month timeline**: Complete rewrite is risky for a startup with limited time.
  While refactoring to Firestore is the long-term "cloud-native" answer, the scenario prioritizes "minimize code changes."

- **B (Correct)**: ✅ MongoDB Atlas on Google Cloud Marketplace is the **lift-and-shift** path:
  - **100% API-compatible**: Application code doesn't change. Same MongoDB drivers, same queries.
  - **Fully managed**: Atlas handles backups, scaling, HA, patching (like Cloud SQL but for MongoDB).
  - **Runs on Google Cloud**: Data stays in GCP regions, integrated billing.
  - **Fast migration**: Export from old MongoDB → import to Atlas (days, not months).
  After the migration, they can optionally refactor to Firestore later (Strangler Fig pattern).

- **C (Wrong)**: Bigtable and MongoDB are both "NoSQL," but that's where similarities end:
  - **Bigtable**: Wide-column store, no secondary indexes, no complex queries, single-row atomicity. Designed for analytics/streaming.
  - **MongoDB**: Document store, rich queries (filters, aggregations, projections), multi-document transactions.
  Migrating MongoDB → Bigtable requires complete application rewrite and loses most MongoDB features.

- **D (Wrong)**: BigQuery supports JSON data type, but it's a **data warehouse**, not an operational database:
  - Optimized for analytical queries over billions of rows (OLAP).
  - High latency for single-document lookups (seconds, not milliseconds).
  - Not designed for transactional workloads.
  You don't run a web app's backend on BigQuery.

### Question 13: Memorystore Scaling

**Scenario**: A high-traffic social media application uses Memorystore for Redis as a session cache. The dataset has grown to 450 GB, and the current instance is experiencing performance degradation and memory pressure.

**What is the most architectural appropriate solution?**

A. Upgrade the instance to the largest possible Basic Tier machine  
B. Migrate to Memorystore for Redis Cluster  
C. Use Cloud Bigtable for session management  
D. Use Memorystore for Memcached for better vertical scaling  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Standalone Memorystore for Redis has a maximum capacity of **300 GB**. Since the dataset is already at 450 GB, vertical scaling is no longer an option.
- **B (Correct)**: ✅ Memorystore for **Redis Cluster** supports horizontal scaling (sharding) and can scale up to **5 TB**. This is the standard choice when a Redis dataset exceeds the 300 GB limit of a standalone instance. It also provides better performance through parallel processing across shards.
- **C (Wrong)**: While Bigtable can store large amounts of data, it is not an in-memory database and has higher latency (~10ms) compared to Redis (<1ms). Session management requires the ultra-low latency that only in-memory stores provide.
- **D (Wrong)**: Memcached is excellent for simple key-value pairs, but it also has a 300 GB limit per node for Memorystore's managed offering. It lacks the advanced data structures (like Hashes or Sets) typically used for complex session data in Redis.

---

### Question 14: BigQuery SQL Orchestration (Dataform)

**Scenario**: A data engineering team is managing hundreds of interconnected SQL scripts in BigQuery. They are struggling with manual execution orders, lack of code versioning, and frequent "bad data" reaching dashboards due to missing validation checks.

**Which Google-native tool should they implement?**

A. Cloud Data Fusion  
B. Dataform  
C. Cloud Composer (Airflow)  
D. BigQuery Scheduled Queries  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Data Fusion is a visual, no-code ETL tool. While it can manage pipelines, the scenario specifically mentions team is already writing SQL scripts and needs versioning. Dataform is better suited for a "SQL-first" engineering team.
- **B (Correct)**: ✅ **Dataform** is the correct answer because:
  1. It is **Git-native** (solves the versioning problem).
  2. It automatically builds a **Dependency Graph (DAG)** (solves the manual execution order).
  3. It includes **Assertions** (solves the "bad data" validation problem).
  4. It uses **SQLX**, allowing for dynamic table references and code reuse.
- **C (Wrong)**: Cloud Composer is a general-purpose orchestrator. While it *could* run these scripts, it requires writing Python DAGs and is managed infrastructure. Dataform is serverless and specifically optimized for BigQuery transformations.
- **D (Wrong)**: Scheduled queries are basic. They don't support complex dependencies, data quality checks, or proper version control through Git.

---

### Question 15: BigQuery Slot Management

**Scenario**: A company's "Executive Dashboard" in BigQuery often fails to load or runs slowly during the end-of-month financial close because the Data Science team is running massive ad-hoc training jobs in the same project.

**How should you solve this "noisy neighbor" problem?**

A. Move to BigQuery Flat-rate pricing and increase the project's slot limit to 5000  
B. Use BigQuery Reservations to create a dedicated slot pool for the Dashboards  
C. Partition the tables used by the Data Science team  
D. Enable BI Engine for all Data Science datasets  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Simply increasing the limit doesn't prevent competition. Both teams would still "fight" for the shared pool of 5000 slots. The ad-hoc jobs could still consume all available capacity.
- **B (Correct)**: ✅ **BigQuery Reservations** (available in Enterprise/Enterprise Plus editions) allow you to:
  1. Buy a pool of slots.
  2. Divide that pool into **Reservations** (e.g., "Finance_Res" with 500 slots, "DS_Res" with 2000 slots).
  3. Assign projects or folders to those reservations. 
  This ensures the Executives always have dedicated compute power that cannot be "stolen" by other teams.
- **C (Wrong)**: Partitioning helps with query efficiency (bytes scanned), but it doesn't solve compute (slot) contention. Even with partitioned tables, a massive scan can still consume all available slots.
- **D (Wrong)**: BI Engine is for accelerating small-result dashboard lookups. It won't help with "massive ad-hoc training jobs" and doesn't solve compute resource isolation.

---

### Question 16: ETL Tool Selection (Data Fusion vs Dataflow)

**Scenario**: An organization needs to build a new ETL pipeline to move data from an on-premises Oracle database to BigQuery. The data team consists primarily of SQL analysts who have no experience with Java or Python. They need to see the "Data Lineage" of all transformations for compliance reasons.

**Which tool should an architect recommend?**

A. Cloud Dataflow  
B. Cloud Data Fusion  
C. Cloud Dataproc  
D. BigQuery Data Transfer Service  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Dataflow requires writing code in Java, Python, or Go using the Apache Beam SDK. The team's lack of coding experience makes this a poor choice.
- **B (Correct)**: ✅ **Cloud Data Fusion** is ideal here because:
  1. It has a **Visual GUI** (No-code) that fits the SQL analysts' skill set.
  2. It contains built-in features for **Data Lineage** (a specific requirement).
  3. It has pre-built connectors for legacy systems like Oracle.
- **C (Wrong)**: Dataproc is for Hadoop/Spark. Use this only if they are migrating existing Spark jobs. Writing new Spark jobs requires Scala/Python coding.
- **D (Wrong)**: DTS is a "pull" service for specific SaaS/Cloud sources. While it supports some third-party databases, it doesn't provide the complex transformation capabilities or visual data lineage tracking required here.

---

### Question 17: Privacy-Safe Data Collaboration

**Scenario**: A major airline and a credit card company want to analyze their shared customers to offer a "Double Points" promotion. Due to strict privacy regulations, neither company is allowed to see the other company's PII (emails, names, or addresses) or individual transaction lists. They only need to see aggregate totals of shared customers.

**What BigQuery feature should they use?**

A. Authorized Views  
B. BigQuery Analytics Hub: Data Exchanges  
C. BigQuery Data Clean Rooms  
D. IAM-based dataset sharing  

**Answer: C** ✅

**Explanations**:
- **A (Wrong)**: Authorized views allow sharing filtered data, but the consumer still sees the raw rows returned by the view. This doesn't prevent one party from seeing another's PII if the query joins on sensitive fields.
- **B (Wrong)**: Data Exchanges are for **finding and subscribing** to data. Once subscribed, you generally have full read access to the shared dataset. It doesn't enforce the "neither party can see raw data" privacy requirement.
- **C (Correct)**: ✅ **BigQuery Data Clean Rooms** are designed exactly for this:
  1. Multiple parties contribute data to a neutral environment.
  2. Parties can run queries that join the data.
  3. **Privacy Policies** enforce aggregation thresholds (e.g., results must contain at least 50 users) and prevent any party from seeing the other's raw rows.
- **D (Wrong)**: Basic IAM sharing gives full access to the shared rows. This is the least secure option for this privacy-critical scenario.

---

### Question 18: File Formats for BigQuery Ingestion

**Scenario**: A company is designing a high-scale data ingestion pipeline. They need to move petabytes of data from Cloud Storage into BigQuery on a daily basis. They are deciding between CSV, JSON, and Avro for the "Raw Landing Zone."

**Which format should they choose for the best ingestion performance and reliability?**

A. Compressed JSON (Gzip)  
B. CSV with headers  
C. Avro  
D. Parquet  

**Answer: C** ✅

**Explanations**:
- **A (Wrong)**: JSON is human-readable but very slow to parse. Compressed (Gzip) files cannot be read in parallel by BigQuery (one worker must decompress the whole file). This is bad for petabyte-scale ingestion.
- **B (Wrong)**: CSV is fast to read but flaky. If a single column contains a comma that isn't escaped correctly, the whole load can fail or data can be corrupted. It also doesn't contain data types.
- **C (Correct)**: ✅ **Avro** is the best choice for **ingestion** because:
  1. It is **Binary** (fast to read).
  2. It is **Row-based** (making it easy to append new events).
  3. It contains the **Schema in the header** (prevents "schema-on-read" errors).
  4. It is **Splittable** (BigQuery can use many slots to read different parts of the same file simultaneously, even if compressed).
- **D (Wrong)**: Parquet is the best for **Analytical Queries** (Columnar), but Avro is traditionally the preferred format for the **Ingestion/Write** phase of a pipeline because row-based binary formats are easier to produce and validate at high velocity.

---

### Question 19: Dashboard Performance Optimization

**Scenario**: A global retail brand has a Looker dashboard that queries a 500 GB "Sales" table in BigQuery. The dashboard is slow, taking 8-10 seconds to load each tile. The underlying data only changes once an hour.

**What is the most cost-effective way to achieve sub-second response times for these dashboard users?**

A. Increase the BigQuery slot reservation count  
B. Enable BigQuery BI Engine with memory reservation  
C. Cluster the table by `store_id` and `date`  
D. Migrate the table to Memorystore for Redis  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: Adding more slots makes the engine work faster, but it still has to scan the disk for every query. This rarely achieves "sub-second" performance for complex dashboard tiles and is more expensive.
- **B (Correct)**: ✅ **BI Engine** is an in-memory analysis service. It caches the relevant table data in RAM. When a dashboard user refreshes a tile, BigQuery reads from memory instead of disk, resulting in **sub-second** latency. It is much cheaper than buying thousands of slots.
- **C (Wrong)**: Clustering helps "prune" data (reading less disk), which reduces cost and improves speed, but it typically gets performance down to the 2-3 second range, not sub-second "instant" feel.
- **D (Wrong)**: BigQuery is a data warehouse; Memorystore is a cache. Moving 500 GB to Memorystore would be extremely expensive (~$30/GB/month) and would require rewriting all the dashboard's SQL to point at a completely different system.

---

### Question 20: Security for Hybrid Data Lakes

**Scenario**: A financial services company stores petabytes of historical transaction files in Cloud Storage (Iceberg and Parquet formats). They want to allow analysts to query this data using SQL in BigQuery, but they need to enforce **Row-level security** so that analysts only see transactions from their authorized region.

**Which technology enables this?**

A. BigQuery Omni  
B. BigLake  
C. Cloud DLP API  
D. Storage Transfer Service  

**Answer: B** ✅

**Explanations**:
- **A (Wrong)**: BigQuery Omni is for querying data across AWS S3 or Azure Blob Storage. It is for **multi-cloud**, not for adding security to GCS files.
- **B (Correct)**: ✅ **BigLake** bridges the gap between GCS (Data Lake) and BigQuery. It allows you to create tables on top of files (like Parquet/Iceberg) and apply **BigQuery-level security** (Row-level and Column-level) to them. Without BigLake, GCS security is "all or nothing" at the bucket/object level.
- **C (Wrong)**: Cloud DLP is for **finding** sensitive data (like masking SSNs). It doesn't enforce database-style row-level access control based on user attributes.
- **D (Wrong)**: Storage Transfer Service is for moving data between buckets/clouds. It has no security enforcement or SQL capabilities.

---

## Answer Key Summary

1. **B** - Cloud SQL vs VM (TCO analysis)
2. **B** - Cloud SQL Auth Proxy for GKE
3. **C** - Cloud SQL scaling limit → Spanner
4. **A** - Spanner Regional (US-only, cost optimization)
5. **B** - Spanner hotspotting (sequential keys)
6. **A** - Firestore for mobile game profiles
7. **A** - Bigtable row key design (time-range queries)
8. **B** - BigQuery partitioning (cost optimization)
9. **C** - Bigtable + BigQuery (Lambda architecture)
10. **B** - Cassandra (AP for social media)
11. **B** - Datastream (Oracle CDC → BigQuery)
12. **B** - MongoDB Atlas (lift and shift)
13. **B** - Memorystore Redis Cluster (>300GB)
14. **B** - Dataform (SQL dependencies/Git)
15. **B** - BigQuery Reservations (Noisy Neighbor)
16. **B** - Cloud Data Fusion (Visual ETL/Lineage)
17. **C** - BigQuery Data Clean Rooms (Privacy)
18. **C** - Avro for high-scale ingestion
19. **B** - BigQuery BI Engine (Dashboard speed)
20. **B** - BigLake (Security for GCS files)

---

## Study Tips

1. **Cloud SQL**: Understand TCO, when NOT to use VMs, connectivity patterns.
2. **Spanner**: Regional vs Multi-Region cost trade-offs, hotspotting, TrueTime/Paxos basics.
3. **Bigtable**: Row key design is 80% of the exam questions, know when it's overkill.
4. **BigQuery**:
   - **Performance**: Partitioning/clustering, BI Engine.
   - **Cost**: Partitioning, Slot Reservations vs On-demand.
   - **Governance**: Dataform (modeling), BigLake (security), Analytics Hub.
5. **CAP Theorem**: Memorize the CP/AP choices for each database.
6. **Migration**: DMS (homogeneous), Datastream (heterogeneous), partner solutions (MongoDB).
7. **Memorystore**: Standalone Redis (300GB) vs Cluster (5TB). 
8. **ETL Tools**: Dataflow (Developer/Scale) vs Data Fusion (Business/Visual).
