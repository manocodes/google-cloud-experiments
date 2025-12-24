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

| Feature | Cloud SQL | Spanner | Bigtable | Firestore | BigQuery |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Type** | RDBMS (Regional) | RDBMS (Global) | Wide-Column NoSQL | Document NoSQL | Data Warehouse |
| **Ideal For** | Web Backends, CRM, ERP, General Purpose | Global Trading, Supply Chain, Critical Consistency | IoT, AdTech, High Throughput, Timeseries | Mobile/Web Apps, User Profiles, CMS | Analytics, BI, Reporting |
| **Scaling** | Vertical (Read Horizontal) | Horizontal (Read/Write) | Horizontal (Linear) | Horizontal (scales to 0) | Serverless |
| **Transactions**| ACID (Local) | ACID (Global) | Single-Row (mostly) | ACID (Multi-document) | N/A (Atomic loads) |
| **SQL?** | Yes | Yes (Standard/PG) | No (HBase) | No (SQL-like syntax) | Yes (Standard) |

## Summary of "Traps"
-   **"Hadoop Migration"**: Often implies **Bigtable** (HBase) or **Dataproc**.
-   **"Lift and Shift Oracle"**: **Bare Metal Solution** (if preserving license/hardware reqs) or refactor to **Spanner/Cloud SQL**.
-   **"Global User Base"**: If read-heavy, Cloud SQL + Read Replicas *might* work. If write-heavy everywhere, **Spanner**.
-   **"JSON"**: Firestore is the default "JSON" store. BigQuery also handles JSON natively now, but for analytics.
