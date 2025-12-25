# Cloud Spanner for PCA

## Fundamentals
- **Service Type**: Fully managed, **Global**, mission-critical, relational database management system (RDBMS).
- **Key Feature**: Combines the benefits of relational database structure (ACID transactions, schemas) with non-relational horizontal scaling.
- **Use Cases**: Global supply chain, financial trading systems, global inventory, gaming backends, massive scale relational data (> 64 TB).
- **Scaling**: 
  - **Horizontal**: Scales writes and reads by adding nodes. Unlimited scaling.
- **Consistency**: Strong consistency (External Consistency) globally using TrueTime API (keeping clocks synchronized via GPS/Atomic clocks).
- **Consistency**: Strong consistency (External Consistency) globally using TrueTime API (keeping clocks synchronized via GPS/Atomic clocks).

## What does "Global" Mean?
When we say Spanner is "Global", we don't just mean it lives in many places. We mean:
1.  **Single Logical Database**: Your application sees *one* database, even if that database is physically spread across the US, Europe, and Asia. You do not manage "shards" or different connection strings for different regions manually.
2.  **Synchronous Replication**: If you write a transaction in the US, Spanner ensures it is safely replicated to the required voting replicas (potentially across regions) *before* telling you "Success".
3.  **Read Your Writes (Everywhere)**: Because of TrueTime, if you commit a change in New York, a user in Tokyo reading that data milliseconds later is guaranteed to see the update (External Consistency). This is impossible with traditional async replication.

## Critical Information
- **SLA**: Up to 99.999% (5 nines) availability for Multi-Region configurations.
- **Structure**:
  - **Instance**: The container for databases. It defines the **Configuration** (Regional vs Multi-Region) and **Compute Capacity** (Nodes or Processing Units - 1000 PUs = 1 Node).
      - *Note*: You can start small (e.g., 100 PUs) and scale up.
  - **Database**: The actual container for tables, indexes, and data.
  - **Table**: Structure for rows.

## Hierarchy & Organization Strategy (FAQ)
*   **Can I have many databases?**
    *   **Yes**. A single Cloud Spanner Instance can host **multiple databases** (up to 100).
    *   **Shared Resources**: All databases in an instance share the same pool of Compute Nodes (CPU/RAM). If one DB spikes, it can affect neighbors (noisy neighbor problem) unless you monitor carefully.
*   **Should I have "One Global Instance" for my whole Organization?**
    *   **Generally NO**. While technically possible to put everything in one giant Multi-Region instance:
        1.  **Isolation**: You usually want to separate Production from Development/Staging (to avoid accidental deletions or resource starvation).
        2.  **Billing/IAM**: Separation by Google Cloud **Project** is standard for billing attribution and security boundaries. Use different Instances for different Projects.
        3.  **Configuration**: Some apps might only need a *Regional* Spanner (cheaper, lower latency for local users), while others need *Multi-Region* (Global). You cannot mix these configs in a single instance.

## Regional vs Multi-Region Configurations (Cost Control)
Unlocking "Global" capabilities is a configuration choice, not a mandate. You can save massive costs by choosing the right scope.

1.  **Regional Instance (e.g., `us-central1`)**:
    *   **Cost**: Significantly cheaper. (~$0.90/node/hour).
    *   **Availability**: 99.99% SLA.
    *   **Replication**: Data is replicated *within* that one region (typically 3 zones).
    *   **Use Case**: You typically use this if you want Spanner's **unlimited scale** (sharding) but your users are all in one country (e.g., a US-only retail app). You don't need to pay for Global replication.
2.  **Multi-Region Instance (e.g., `nam-eur-asia1`)**:
    *   **Cost**: Expensive. Nodes cost more (~$3.00/node/hour) + higher replication costs.
    *   **Availability**: 99.999% SLA.
    *   **Replication**: Data is replicated across continents (e.g., 1 read-write region in US, 2 read-only regions in EU/Asia, etc.).
    *   **Use Case**: Truly global apps where a user in Tokyo and a user in New York both need low latency reads and survivability if the entire US goes offline.


- **SQL Dialect**: Google Standard SQL (ANSI 2011) and PostgreSQL interface.
- **Interleaved Tables**: Optimization technique where child rows are stored physically next to parent rows. Critical for performance in Spanner.

## Traps & "Gotchas"
1. **Cost**: Spanner is expensive. Don't select it for simple, small regional applications.
2. **"Relational"**: It *is* relational, but migrating from MySQL/Postgres is not always "lift and shift" because you often need to optimize schemas (primary keys, interleaving) to avoid "hotspotting".
3. **Hotspotting**: Storing sequential primary keys (like Timestamp or Incrementing Int) causes all writes to go to one split/node. **BAD**. This defeats the purpose of horizontal scaling. Use Version 4 UUIDs or bit-reversing to distribute writes.
4. **Data Boost**: Serverless, on-demand compute for running analytics queries (e.g. via BigQuery) without impacting the performance of the operational workload.

## Important Points / Exam Clues
- Keywords: "Global", "Strong Consistency", "Horizontal Write Scaling", "Financial", "Scale beyond Cloud SQL", "Multiple regions active-active".
- **TrueTime**: The secret sauce enabling strong global consistency.
- **Federated Queries**: Can seek data in Spanner via BigQuery.

## Tips
- If the requirement says "Relational" AND "Global" -> **Spanner**.
- If the requirement says "Relational" AND "Higher write throughput than a single instance can handle" -> **Spanner**.
- If the requirement says "NoSQL" -> **NOT Spanner** (look at Bigtable/Firestore), although Spanner fits some 'semi-structured' definitions, it's primarily sold as NewSQL/Relational.
