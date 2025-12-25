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
- **BI Engine**: An in-memory analysis service. Sits "on top" of BigQuery. Makes dashboards (Looker, Data Studio) fly with sub-second response times.

## 5. Traps & "Gotchas"
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
- **External Tables**: Query data directly in GCS, Bigtable, Drive without importing. (Federated queries).
- **Materialized Views**: Pre-compute complex queries. BQ automatically uses them to speed up related queries and save costs. Zero maintenance (auto-refresh).

## 7. Tips
- Requirement: "Analyze historical data" -> **BigQuery**.
- Requirement: "Cost-effective storage of logs for regulatory analysis" -> **BigQuery** (Long-term storage pricing is cheap).
- Requirement: "Ad-hoc SQL queries on petabytes" -> **BigQuery**.
- If minimizing cost is key: "Partition tables", "Use 'Limit' does NOT reduce cost (only reduces output), select specific columns".
