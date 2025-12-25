# Database Migration & Replication for PCA

Migration strategies are massive on the PCA exam. You need to distinguish between "Moving the database" and "Streaming the data for analysis".

## 1. Database Migration Service (DMS)
**"The Lift-and-Shift Tool"**

*   **Fundamantals**: A fully managed, serverless service designed primarily for **homogeneous** migrations (SameDB -> SameDB) to Cloud SQL or AlloyDB.
*   **Primary Use Cases**:
    *   Migrating on-prem MySQL -> Cloud SQL for MySQL.
    *   Migrating AWS RDS PostgreSQL -> Cloud SQL for PostgreSQL / AlloyDB.
    *   Lift and shift with minimal downtime.
*   **Critical Info**:
    *   Uses native replication tools under the hood (e.g., MySQL binlog replication, PostgreSQL logical replication) but automates the setup.
    *   **Continuous Replication**: Keeps source and destination in sync for a window of time to allow a minimal-downtime cutover.
*   **Exam Tip**: If the scenario is "Migrate an existing MySQL database to Google Cloud with minimal downtime and minimal setup complexity," the answer is **DMS**.

## 2. Datastream
**"The Change Data Capture (CDC) Pipeline"**

*   **Fundamentals**: Serverless Change Data Capture (CDC) and replication service.
*   **Primary Use Cases**:
    *   **Heterogeneous** data movement.
    *   Streaming real-time changes from Oracle/MySQL/PostgreSQL to **BigQuery** for analytics.
    *   Streaming data to **Cloud Storage** for data lake archival.
    - Replicating data to **Cloud Spanner**.
    - **Heterogeneous Migrations**: Oracle to PostgreSQL (AlloyDB/Cloud SQL) - often used when standard DMS doesn't cover complexity or custom transforms are needed.
*   **Critical Info**:
    *   It reads the transaction logs (redo logs, binlogs) of the source database.
    *   It is often used in conjunction with **Dataflow** for transformation before landing in the destination.
*   **Exam Tip**: If the scenario is "Real-time analytics on data living in an operational Oracle database," the answer is **Datastream -> BigQuery**.

## 3. Comparison / Decision Matrix

| Feature | Database Migration Service (DMS) | Datastream |
| :--- | :--- | :--- |
| **Goal** | **Migrate** the database (Lift & Shift). | **Replicate/Stream** data for use elsewhere. |
| **Source/Dest** | Homogeneous (MySQL->MySQL, PG->PG). | Heterogeneous (Oracle->BigQuery, MySQL->GCS). |
| **Duration** | Temporary (runs until cutover). | Indefinite (runs continuously for pipelines). |
| **Typical Target** | Cloud SQL, AlloyDB. | BigQuery, Cloud Storage, Spanner. |
| **Logic** | Database-to-Database replication (Binlog). | Change Data Capture (CDC). |

## 4. Other Migration Tools (Context)
*   **pg_dump / mysqldump**: Valid for small databases or where downtime is acceptable. Manual, harder to manage.
*   **BigQuery Data Transfer Service**: Specifically for moving data *into* BigQuery (from SaaS apps like Google Ads, or other cloud warehouses like Redshift/Teradata).
*   **Transfer Appliance**: For physically moving petabytes of data (too big for network).

## Exam Traps
1.  **DMS for Analytics?** No. Do not use DMS to feed a data warehouse. Use Datastream.
2.  **Datastream for Migration?** You *could*, but it typically requires more setup (schema conversion, etc.) than DMS for a straight lift-and-shift. Datastream is better for "I want to keep my Oracle DB on-prem but run queries in BQ".
3.  **Oracle to Cloud SQL?** DMS supports Oracle to Cloud SQL for PostgreSQL in some capacities (schema conversion with conversion workspace), but for the exam, usually stick to:
    *   **Bare Metal Solution** (Keep Oracle).
    *   **Datastream** (Replicate Oracle).
