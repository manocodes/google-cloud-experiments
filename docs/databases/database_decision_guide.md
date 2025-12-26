# GCP Database Decision Guide for PCA

This guide simplifies the decision-making process for choosing a database service, a critical skill for the PCA exam.

## Decision Flowchart (Mental Model)

### 1. Is the data Relational (SQL) or Non-Relational (NoSQL)?

**IF RELATIONAL (SQL):**
1.  **Do you need Global Scalability (Horizontal Write Scaling, Multi-Region Active-Active)?**
    -   **YES** -> **Cloud Spanner** (The "Global" answer).
    -   **NO** (Regional is fine):
        -   **Is it an existing MS SQL Server or MySQL application?** -> **Cloud SQL**.
        -   **Is it PostgreSQL?**
            -   Standard Requirements? -> **Cloud SQL for PostgreSQL**.
            -   High Performance / HTAP / Enterprise grade needed? -> **AlloyDB**.
        -   **Is it for Analytics/Warehousing (OLAP)?** -> **BigQuery** (Not for transaction processing!).

**IF NON-RELATIONAL (NoSQL):**
1.  **Is it for Analytics / Heavy Writes / IoT / Time Series / > 1TB?**
    -   **YES** -> **Cloud Bigtable** (HBase compatible, flat schema).
2.  **Is it for Mobile / Web Apps / Hierarchical Data / < 1TB (typically)?**
    -   **YES** -> **Firestore** (Documents, Flexible schema).
3.  **Is it a temporary cache / Session store?**
    -   **YES** -> **Memorystore** (Redis/Memcached).

## Comparison Matrix

| **Feature** | **Cloud SQL** | **AlloyDB** | **Spanner** | **Bigtable** | **Firestore** | **BigQuery** |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Type** | RDBMS (Regional) | RDBMS (Regional++ ) | RDBMS (Global) | Wide-Column NoSQL | Document NoSQL | Data Warehouse |
| **Ideal For** | Web Backends, CRM, ERP | High-End Postgres, HTAP, Legacy Migration | Global Trading, Supply Chain, Critical Consistency | IoT, AdTech, High Throughput, Timeseries | Mobile/Web Apps, User Profiles, CMS | Analytics, BI, Reporting |
| **Scaling** | Vertical | Vertical (Write) / Horizontal (Read) | Horizontal (Read/Write) | Horizontal (Linear) | Horizontal (scales to 0) | Serverless |
| **Transactions**| ACID (Local) | ACID (Local) | ACID (Global) | Single-Row (mostly) | ACID (Multi-document) | N/A (Atomic loads) |
| **SQL?** | Yes | Yes (Postgres) | Yes (Standard/PG) | No (HBase) | No (SQL-like syntax) | Yes (Standard) |

## Summary of "Traps"
-   **"Hadoop Migration"**: Often implies **Bigtable** (HBase) or **Dataproc**.
-   **"Lift and Shift Oracle"**: **Bare Metal Solution** (if preserving license/hardware reqs) or refactor to **Spanner/Cloud SQL**.
-   **"Global User Base"**: If read-heavy, Cloud SQL + Read Replicas *might* work. If write-heavy everywhere, **Spanner**.
-   **"JSON"**: Firestore is the default "JSON" store. BigQuery also handles JSON natively now, but for analytics.

## Partner & Specialized Database Solutions

Google Cloud's native databases are **excellent for 80% of use cases**. But the PCA exam tests whether you know when to recommend a **specialized tool** for the remaining 20%.

### The Strategic Rule
> "If the use case explicitly requires a specialized capability that no native GCP database offers, the answer is a **Marketplace Partner Solution**."

### Common Specialized Database Partners

#### 1. **Neo4j** (Graph Database)
*   **Native Alternative**: None. (Spanner has *some* graph-like queries, but it's not a true graph DB).
*   **Use Case**: Social networks ("Friends of Friends"), Fraud detection (relationship patterns), Knowledge graphs, Recommendation engines.
*   **Exam Keyword**: "Graph", "Relationships", "Traversal", "Shortest Path".
*   **Why Partner?**: Google Cloud has no native managed graph database. Neo4j is the industry standard.

#### 2. **DataStax (Apache Cassandra)**
*   **Native Alternative**: Bigtable (similar wide-column NoSQL).
*   **Use Case**: When you need **multi-datacenter active-active writes** with tunable consistency (Cassandra's specialty).
*   **Exam Keyword**: "Cassandra", "Multi-datacenter writes", "Tunable consistency" (AP vs CP in CAP theorem).
*   **Why Partner?**: Bigtable is single-master for writes (read replicas exist but are async). Cassandra allows writes in multiple datacenters simultaneously with eventual consistency.

#### 3. **Elastic (Elasticsearch)**
*   **Native Alternative**: BigQuery (for analytics), Firestore (for search), or Vertex AI Search.
*   **Use Case**: Full-text search, Log analytics (ELK stack), Real-time search with fuzzy matching.
*   **Exam Keyword**: "Elasticsearch", "ELK Stack", "Kibana", "Full-text search".
*   **Why Partner?**: If the requirement says "Existing Elasticsearch stack" or "Advanced search ranking algorithms", use Elastic Cloud on GCP.

#### 4. **MongoDB Atlas**
*   **Native Alternative**: Firestore.
*   **Use Case**: Existing MongoDB application, "No code changes" constraint.
*   **Exam Keyword**: "MongoDB", "Document DB", "No refactoring".
*   **Why Partner?**: 100% API compatibility.

#### 5. **Redis Enterprise (vs Memorystore)**
*   **Native Alternative**: Memorystore for Redis.
*   **Use Case**: When you need Redis features that Memorystore doesn't support (e.g., Active-Active Geo-Distribution, RedisJSON, RedisGraph).
*   **Exam Keyword**: "Advanced Redis Modules", "Multi-region Redis writes".
*   **Why Partner?**: Memorystore for Redis is excellent but doesn't support all Redis modules or active-active writes across regions.

#### 6. **InfluxDB**
*   **Native Alternative**: Bigtable (can store time-series but requires custom schema design).
*   **Use Case**: Specialized time-series database with built-in downsampling, retention policies.
*   **Exam Keyword**: "Time-series", "Metrics", "InfluxDB".
*   **Why Partner?**: If the scenario says "Existing InfluxDB" or requires specific InfluxQL features.

---

### Exam Decision Framework
```
Does the requirement mention a SPECIFIC technology by name (e.g., "Neo4j", "Cassandra")?
├─ YES: Use the Marketplace Partner version.
└─ NO: Does the use case require a specialized capability?
    ├─ Graph Relationships → Neo4j
    ├─ Multi-DC Active Writes (NoSQL) → DataStax
    ├─ Advanced Full-Text Search → Elastic
    └─ Everything Else → Default to Google Native (Spanner/Bigtable/Firestore/BigQuery)
```

---

## Key Performance Terminology for Exam

Understanding these metrics is vital for choosing between Cloud SQL, Spanner, and Bigtable.

1.  **QPS (Queries Per Second)**:
    *   **Definition**: A measure of **Throughput**. How many requests the database handles every second.
    *   **Scale**:
        *   **Cloud SQL**: Thousands to tens of thousands.
        *   **Cloud Spanner**: Millions (Horizontal scaling).
        *   **Bigtable**: Millions (Linear scaling).
2.  **Latency**:
    *   **Definition**: The time it takes for a *single* query to return.
    *   **Scale**:
        *   **Memorystore**: Microseconds (Fastest).
        *   **Bigtable/Cloud SQL/Spanner**: Milliseconds.
        *   **BigQuery**: Seconds (or minutes for huge jobs).
3.  **TPS (Transactions Per Second)**:
    *   Similar to QPS but specifically for write transactions (INSERT/UPDATE/DELETE) that require ACID guarantees.

## ACID Transactions Explained
ACID is the set of properties that guarantee database transactions are processed reliably. Most critical for Financial/Inventory apps.

*   **A - Atomicity**: "All or Nothing". If one part of the transaction fails, the entire transaction fails. (e.g., Money leaves Account A AND enters Account B. It never just leaves A and disappears).
*   **C - Consistency**: Database goes from one valid state to another. All data constraints (like "Foreign Keys" or "Not Null") are respected.
*   **I - Isolation**: Concurrent transactions don't interfere with each other. (e.g., Two users trying to buy the last ticket at the exact same millisecond; only one succeeds).
*   **D - Durability**: Once the database says "Success" (Committed), the data is saved forever, even if the power plug is pulled 1ms later.

**Exam Rule of Thumb**:
*   **Cloud SQL / Spanner**: Full ACID support. (Spanner = Global ACID).
*   **Firestore**: ACID support (even across multiple documents).
*   **Bigtable**: **No** multi-row ACID. Only single-row atomicity.

## Scaling Explained: Vertical vs Horizontal

This is a **fundamental** concept for the exam. You must know which DB uses which strategy.

### 1. Vertical Scaling ("Scale Up")
*   **Concept**: Making the *single* machine bigger. Adding more CPU, more RAM, or more Disk to the existing instance.
*   **Analogy**: You have a small car that can't carry enough luggage. You buy a bigger truck. It's still one vehicle.
*   **Pros**: Simple connection logic (app connects to one IP).
*   **Cons**:
    *   **Downtime**: Usually requires a restart to change size (Cloud SQL).
    *   **Ceiling**: You eventually hit the limit of the biggest machine available (e.g., 96 CPUs). You cannot go higher.
*   **GCP Example**: **Cloud SQL** and **Memorystore**.
    *   *Tip*: If Cloud SQL CPU is high, you change the machine type from `db-n1-standard-4` to `db-n1-standard-16`.

### 2. Horizontal Scaling ("Scale Out")
*   **Concept**: Adding *more* machines (nodes) to the pool. The data and load are distributed across them.
*   **Analogy**: You have a small car that can't carry enough people. You buy 10 more cars. Now you have a fleet.
*   **Pros**:
    *   **Unlimited Scale**: Just keep adding nodes.
    *   **No Downtime**: You can add nodes while the database is running (Live scaling).
*   **Cons**: Complex app logic (unless the DB manages it for you, like Spanner does).
*   **GCP Example**: **Cloud Spanner**, **Bigtable**, and **Firestore**.
    *   *Tip*: If Spanner CPU is high, you increase the `Processing Units` (Nodes) count.

### Summary Table for Exam
| Database | Write Scaling Strategy | Read Scaling Strategy |
| :--- | :--- | :--- |
| **Cloud SQL** | **Vertical** (Limit: Max machine size) | **Horizontal** (Read Replicas) |
| **Spanner** | **Horizontal** (Unlimited) | **Horizontal** (Unlimited) |
| **Bigtable** | **Horizontal** (Unlimited) | **Horizontal** (Unlimited) |
| **Firestore** | **Horizontal** (Automatic) | **Horizontal** (Automatic) |


