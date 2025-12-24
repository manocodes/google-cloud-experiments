# Cloud Spanner for PCA

## Fundamentals
- **Service Type**: Fully managed, **Global**, mission-critical, relational database management system (RDBMS).
- **Key Feature**: Combines the benefits of relational database structure (ACID transactions, schemas) with non-relational horizontal scaling.
- **Use Cases**: Global supply chain, financial trading systems, global inventory, gaming backends, massive scale relational data (> 64 TB).
- **Scaling**: 
  - **Horizontal**: Scales writes and reads by adding nodes. Unlimited scaling.
- **Consistency**: Strong consistency (External Consistency) globally using TrueTime API (keeping clocks synchronized via GPS/Atomic clocks).

## Critical Information
- **SLA**: Up to 99.999% (5 nines) availability for Multi-Region configurations.
- **Structure**:
  - **Instance**: Global or Regional control plane.
  - **Nodes/Processing Units**: Unit of compute/storage capacity.
  - **Database**: The actual container for tables.
- **SQL Dialect**: Google Standard SQL (ANSI 2011) and PostgreSQL interface.
- **Interleaved Tables**: Optimization technique where child rows are stored physically next to parent rows. Critical for performance in Spanner.

## Traps & "Gotchas"
1. **Cost**: Spanner is expensive. Don't select it for simple, small regional applications.
2. **"Relational"**: It *is* relational, but migrating from MySQL/Postgres is not always "lift and shift" because you often need to optimize schemas (primary keys, interleaving) to avoid "hotspotting".
3. **Hotspotting**: Storing sequential primary keys (like Timestamp or Incrementing Int) causes all writes to go to one split/node. **BAD**. Use Version 4 UUIDs or bit-reversing.

## Important Points / Exam Clues
- Keywords: "Global", "Strong Consistency", "Horizontal Write Scaling", "Financial", "Scale beyond Cloud SQL", "Multiple regions active-active".
- **TrueTime**: The secret sauce enabling strong global consistency.
- **Federated Queries**: Can seek data in Spanner via BigQuery.

## Tips
- If the requirement says "Relational" AND "Global" -> **Spanner**.
- If the requirement says "Relational" AND "Higher write throughput than a single instance can handle" -> **Spanner**.
- If the requirement says "NoSQL" -> **NOT Spanner** (look at Bigtable/Firestore), although Spanner fits some 'semi-structured' definitions, it's primarily sold as NewSQL/Relational.
