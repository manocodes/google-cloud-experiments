# Cloud Bigtable for PCA

## Fundamentals
- **Service Type**: Fully managed, wide-column NoSQL key-value store. Based on Google's internal BigTable.
- **Protocol**: HBase compatible (Java).
- **Use Cases**: IoT data stream, AdTech (impressions/clicks), Financial Data (market ticks), Time-series requiring high throughput writes/reads.
- **Performance**: Millisecond latency. Designed for **high throughput** (millions of concurrent requests).

## Critical Information
- **Scaling**: Linearly scalable. Add nodes => increase throughput.
- **Schema Key Design**: 
  - **Row Key**: THE most critical design element. Data is sorted lexicographically by Row Key.
  - Correct design prevents "hotspotting" (uneven distribution of traffic).
  - **Anti-patterns**: Domain names (front-heavy), Sequential IDs/Timestamps at start of key.
  - **Patterns**: Reverse domain names, Salting, Hashing, Field promotion.
- **Storage**: Separation of processing (nodes) and storage (Colossus). Resizing Cluster is fast (no data movement needed).

## Traps & "Gotchas"
1. **Not for SQL**: No joins, no complex transactions, no secondary indexes (historically - barely supported now but avoid for exam logic, assume minimal indexing).
2. **Cost**: Minimum node count (usually 1 or 3 for prod) makes it pricey for tiny datasets. Not for storing a "ToDo list" app.
3. **Small Data**: Don't use Bigtable for < 1 TB of data unless you have extremly high throughput requirements. Use Firestore or SQL instead.

## Important Points / Exam Clues
- Keywords: "Hadoop", "HBase", "IoT", "AdTech", "Timeseries", "Low Latency", "High Throughput", "Flat schema", "Wide-column".
- **BigQuery Integration**: You can query Bigtable data directly from BigQuery (Federated Query) for analysis.

## Tips
- Requirement: "Ingest massive sensor data with low latency" -> **Bigtable**.
- Requirement: "Migrate HBase cluster" -> **Bigtable**.
- Tip: Remember that Bigtable learns access patterns to rebalance tablets (shards). It takes time to "warm up" or rebalance.
