# BigQuery for PCA

## Fundamentals
- **Service Type**: Serverless, highly scalable, and cost-effective multi-cloud data warehouse.
- **Architecture**: Separates Compute (slots) from Storage (Colossus).
- **Use Cases**: Analytics, Data Warehousing, Business Intelligence (BI), ML (BigQuery ML), Geospatial analysis (GIS).
- **Interface**: Standard SQL (ANSI).

---

## 3. Architecture Deep Dive: "Slots" vs. "Colossus"
*The "Separation of Compute and Storage" explained*

### The Old World (Coupled)
In a traditional database (like Oracle or PostgreSQL on a VM), **Compute and Storage are glued together**.
- If you need to store 10PB of data, you need thousands of hard drives.
- To attach those drives, you need hundreds of servers (CPUs).
- **The Problem:** Even if you aren't running any queries, you are paying for those hundreds of CPUs just to keep the hard drives online. You pay for "idle" capacity.

### The BigQuery Way (Decoupled)
BigQuery chops the database in half with a machete.

#### 1. The Storage (Colossus) - "The Bookshelf"
- Your data lives in **Colossus** (Google's global file system).
- It is cheap, durable, and infinitely expandable.
- It has **zero CPU power**. It's just a dead disk sitting in a rack.
- **Cost:** You pay only for GBs stored (very cheap).

#### 2. The Compute (Borg) - "The Readers"
- When you run `SELECT *`, BigQuery wakes up a massive cluster of CPUs (called **Slots**) from Google's shared pool (Borg).
- These 1,000+ Slots connect to the Storage over Google's "Jupiter" network (which is incredibly fast, 1 Petabit/sec).
- They read the data, process it, give you the answer, and **then they vanish**.
- **Cost:** You pay *only* for the seconds those CPUs were working (or for the bytes they processed).

### Why this matters to an Architect?
1.  **True Serverless:** You don't manage "Instances". There are no servers to patch or resize.
2.  **Scale to Zero:** If you run no queries at night, your compute cost is $0.
3.  **Burst Performance:** You can summon 2,000 slots for a massive query for just 60 seconds. In the old world, you'd have to buy 2,000 servers permanently to have that power available.

---

## 4. Critical Information
- **Storage**:
  - **Active**: Modified in last 90 days.
  - **Long-term**: No modification for 90 days (Price drops ~50%).
- **Slots**: The unit of computational capacity tailored for SQL execution.
  - **On-demand**: Pay per TB processed.
  - **Capacity (Editions)**: Pay for slot duration (Standard/Enterprise/Enterprise Plus). Requires reservation.
  - **Autoscaling**: Slots can autoscale to handle spikes.
- **Caching**: Queries are cached per user. If the same query runs again (and data hasn't changed), the result is free/instant.
- **BI Engine**: An in-memory analysis service. Sits "on top" of BigQuery. Makes dashboards (Looker, Data Studio) fly with **sub-second response times** by caching table data in RAM.
- **Data Transfer Service (DTS)**: Automated, managed service to "pull" data from Google SaaS (AdWords, YouTube), AWS S3, or cross-project BigQuery transfers on a schedule.

---

## 5. Security & Governance (Mission Critical)
*Common "Who gets access?" exam scenarios*

### 1. Data Sharing (Least Privilege)
- **Authorized Views:** Give a user access to a "View" (virtual table) that filters out sensitive data. The user **does not** need access to the raw table.
- **Authorized Functions:** Similar to views, but shares results of a SQL function without exposing raw data.

### 2. Fine-Grained Auditing
- **Row-level Security:** Filters which rows a user can see based on SQL conditions (e.g., `WHERE region = 'US'`).
- **Column-level Security:** Uses **Policy Tags** (Dataplex) to mask or block specific columns (e.g., `SSN`).

### 3. BigLake
- Provides a unified interface for data lakes (GCS) and warehouses (BQ).
- Allows you to apply **BigQuery-level security** (Row/Column) to files sitting in Cloud Storage (Parquet, Avro, etc.).

---

## 5. Slot Management: "On-Demand" vs. "Reservations"
*This is the core of your architectural control.*

### Path A: On-Demand (Default)
- **Concept:** You don't manage anything. You pay for "Bytes Scanned" (typically $6.25/TB).
- **Control:** None. BigQuery gives you a maximum soft limit of **2,000 slots** across your whole project.
- **Simultaneous Usage:** If two people run massive queries, they "fight" for those 2,000 slots. You cannot prioritize one over the other. 
- **The PCA Answer:** Choose this for **variable, unpredictable workloads** or when you want **zero management**.

### Path B: BigQuery Editions (Slot Management)
If you want to **manage** slots, you must use **Reservations** (available in **Enterprise** and **Enterprise Plus** editions).

1.  **Reservations:** You "buy" a dedicated pool of slots (e.g., 2,000 slots).
2.  **Assignments:** You divide that pool into smaller pieces (Reservations) and assign them to specific projects, folders, or departments.
    - *Example:* "Reserve 1,500 slots for 'Production' and 500 for 'Dev'."
3.  **Noisy Neighbors:** This prevents a developer's accidental `SELECT *` from slowing down your critical production dashboards.
4.  **Idle Slots:** If the 'Dev' reservation isn't being used, those 500 slots aren't wasted—they are "borrowed" by 'Production' automatically until 'Dev' needs them again.

### BigQuery Editions Comparison
| Feature | **Standard** | **Enterprise** | **Enterprise Plus** |
| :--- | :--- | :--- | :--- |
| **Pricing** | Pay-as-you-go slots | Dedicated/Autoscale slots | Dedicated/Autoscale slots |
| **Reservations** | ❌ None | ✅ Yes (Management!) | ✅ Yes (Management!) |
| **SLA** | 99.9% | 99.99% | 99.99% |
| **Security**| Basic | ✅ VPC SC, CMEK | ✅ Column/Row security |
| **Data Governance** | No | ✅ Dataplex | ✅ Advanced Governance |

---

## 6. Data Ingestion Best Practices
*How to get data into BigQuery effectively*

### 1. The Standard Path: GCS → BigQuery
- **Recommended for:** Large files, production pipelines, scheduled loads.
- **Benefit:** Reliable (resumable), high-speed (Google internal network), data staging (raw file audit).
- **Tool:** Use `bq load` or **Data Transfer Service (DTS)**.

### 2. Streaming Ingestion
- **Recommended for:** Real-time analytics, dashboards that need immediate data.
- **Technology:** BigQuery Storage Write API (replaces legacy Streaming API).
- **Note:** Incurs an ingestion cost ($0.05/GB). Data is queryable in seconds.

### 3. External Tables (Federated Queries)
- **Recommended for:** Querying data "in-place" without loading it. 
- **Sources:** Cloud Storage (CSV, Parquet), Bigtable, Google Drive, Spanner.
- **Pros:** No storage cost in BQ; instant access.
- **Cons:** Slower query performance than native BigQuery tables.

### 4. Direct Upload (Console)
- **Limit:** **10MB per file**. 
- **Note:** Use only for tiny one-off tests. Not for production.

---

## 7. Traps & "Gotchas"

1. **Not a Transactional Store**: BQ is OLAP (Online Analytical Processing), not OLTP. Do not use for "web app backend" serving low-latency point lookups or frequent single-row updates (streaming inserts exist but are for ingestion, not typical DB CRUD).
2. **SELECT * **: Deadly for cost! BQ charges by *columns read*. Selecting all columns parses the full table. **ALWAYS** select only needed columns.
3. **Partitioning & Clustering**: Use these to prune usage.
   - **Partitioning**: Divide table by Date/Time or Integer range. (Reduces cost by scanning fewer partitions).
   - **Clustering**: Sort data within partitions (Improves performance/cost for filters).
21. **Streaming Buffer**: Data inserted via Streaming API is available instantly but might be in the specifically optimized "streaming buffer" for a bit. It is fully queryable.
22. **Storage API**: Use the BigQuery Storage Read API for high-throughput capability to read data (e.g., for ML training or Spark jobs). Don't just `SELECT *` into a pandas dataframe for massive data.

## 6. Important Points / Exam Clues
- Keywords: "Data Warehouse", "SQL Analytics", "Petabyte scale", "Serverless", "Looker", "BI".
- **BigQuery ML**: Create ML models directly using SQL (`CREATE MODEL`). Good for "Democratizing ML" or "Analyst team needs ML".
- **BigQuery Omni**: Analyze data across GCP, AWS, and Azure (Anthos under the hood, but transparent).
- **Connected Sheets**: Use Google Sheets to query billions of rows in BigQuery without needing to know SQL or move data.
- **External Tables**: Query data directly in GCS, Bigtable, Drive without importing. (Federated queries).
- **Materialized Views**: Pre-compute complex queries. BQ automatically uses them to speed up related queries and save costs. Zero maintenance (auto-refresh).

---

## 8. Cross-Organization Sharing: Analytics Hub
*How to share data without copying it*

### 1. Data Exchanges
- **What:** A private or public "portal" for discovering datasets.
- **Logic:** Providers publish "listings"; Consumers subscribe to them.
- **Key Benefit**: Centralized discovery. No manual IAM management for every user; you manage access at the Exchange level.
- **Where to find it (BigQuery Studio)**: Left-hand navigation -> **Analytics Hub** -> **Search Listings**.

### 2. Data Clean Rooms (Privacy-Safe)
- **What:** A secure environment for multi-party collaboration.
- **Logic:** Allows joining two datasets (e.g., Brand + Retailer) **without** either party seeing the other's raw data.
- **Privacy Policy:** Enforces "Aggregation Thresholds"—results are only shown if they represent a large enough group (e.g., >50 people) to prevent identifying individuals.
- **PCA Exam Answer:** Choose this for **"Privacy-compliant collaboration between third parties."**

---

## 9. Tips
- Requirement: "Analyze historical data" -> **BigQuery**.
- Requirement: "Cost-effective storage of logs for regulatory analysis" -> **BigQuery** (Long-term storage pricing is cheap).
- Requirement: "Ad-hoc SQL queries on petabytes" -> **BigQuery**.
- If minimizing cost is key: "Partition tables", "Use 'Limit' does NOT reduce cost (only reduces output), select specific columns".
