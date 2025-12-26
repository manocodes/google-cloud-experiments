# GCP Databases Master Cram Sheet for PCA

This sheet acts as the central hub for your database study. It summarizes the key discriminators and links to the comprehensive deep-dive files.

## 🔗 Deep Dive Guides
*   [Decision Guide (Start Here)](./database_decision_guide.md) - **Critical**: How to choose the right DB.
*   [Cloud SQL (MySQL/PG/SQL Server)](./cloud_sql.md) - Regional, relational, lift-and-shift.
*   [Cloud Spanner (Global relational)](./cloud_spanner.md) - Global, infinite scale, expensive.
*   [Bigtable (Wide-Column NoSQL)](./bigtable.md) - IoT, high-throughput, flat data.
*   [Firestore (Document NoSQL)](./firestore.md) - Mobile, web, hierarchy, offline sync.
*   [Memorystore (Redis/Memcached)](./memorystore.md) - Caching, sub-ms latency.
*   [BigQuery (Warehouse)](./bigquery.md) - Analytics, SQL, Petabytes.
*   [AlloyDB (PG on Steroids)](./alloydb.md) - High perf PostgreSQL for enterprise.

## ⚡ Quick Decision Matrix (The "Cheat Code")

| Keyword in Question | Likely Answer | Why? |
| :--- | :--- | :--- |
| **"Global", "Horizontal Write Scaling", "Strong Consistency"** | **Cloud Spanner** | The only global relational DB with ACID. |
| **"Lift and Shift", "MySQL", "Postgres", "Standard"** | **Cloud SQL** | Default choice for standard RDBMS. |
| **"Postgres Performance", "HTAP", "Enterprise", "Oracle migration"** | **AlloyDB** | "Postgres on Steroids". Faster for analytics. |
| **"IoT", "Sensor Data", "AdTech", "Millions QPS", "10TB+"** | **Bigtable** | throughput monster. |
| **"Mobile App", "User Profile", "Offline Support"** | **Firestore** | Built for app developers. |
| **"Cache", "Session Store", "Sub-millisecond"** | **Memorystore** | Standard caching layer. |
| **"Analytics", "Warehouse", "History", "Business Intelligence"** | **BigQuery** | OLAP engine. |
| **"Oracle Migration", "Strict Latency"** | **Bare Metal Solution** | If you can't refactor. |
| **"MongoDB", "No Code Changes", "Marketplace"** | **MongoDB Atlas** | Managed Partner solution. |
| **"Graph", "Relationships", "Neo4j"** | **Neo4j** | The only managed graph database option. |
| **"Cassandra", "Multi-DC Writes"** | **DataStax (Cassandra)** | Active-active writes across datacenters. |
| **"Elasticsearch", "ELK", "Full-text Search"** | **Elastic Cloud** | Advanced search capabilities. |

## ⚙️ Migration Patterns

1.  **Homogeneous (MySQL -> MySQL)**:
    *   Use **Database Migration Service (DMS)**.
2.  **Heterogeneous (Oracle -> BigQuery)**:
    *   Use **Datastream** (Change Data Capture).
3.  **On-Prem -> Cloud Storage**:
    *   **Transfer Appliance** (if PBs of data and slow network).
    *   **Storage Transfer Service** (if data is in AWS S3 or generic HTTP).
    *   **gsutil** (if small scale).

## ⚠️ Top Exam Traps

1.  **Don't use BigQuery for a Web App Backend**. It's too slow (latency).
2.  **Don't use Cloud SQL for Global Writes**. It will fail. Use Spanner.
3.  **Don't use Bigtable for "SQL Queries"**. It doesn't speak SQL. (BigQuery *can* query Bigtable, but Bigtable itself is NoSQL).
4.  **Don't confuse "Multi-Region" with "Global"**.
    *   Cloud SQL HA is *Regional* (Zone A + Zone B).
    *   Spanner is *Global* (US + EU + Asia).
