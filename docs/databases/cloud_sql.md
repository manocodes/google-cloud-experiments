# Cloud SQL for PCA

## Fundamentals
- **Service Type**: Fully managed relational database service (RDBMS).
- **Engines**: MySQL, PostgreSQL, SQL Server.
- **Use Cases**: General-purpose web frameworks (Django, Rails, etc.), CRM, ERP, eCommerce (uCommerce), current relational database migration to cloud (lift and shift).
- **Scaling**: 
  - **Vertical**: Increase machine type (CPU/RAM). Requires restart.
  - **Horizontal**: Read replicas for read scaling. *Not* for write scaling (creates consistency lag).
- **High Availability (HA)**: Regional (Multi-Zone). Standby instance in a different zone in the same region. Automatic failover.

## Critical Information
- **Storage Limit**: Up to 64 TB (varies by engine, but 64 TB is the general max for Postgres/MySQL).
- **Replication**:
  - **Read Replicas**: For offloading read traffic. Cross-region read replicas supported for disaster recovery (DR) and read-locality.
  - **High Availability**: Synchronous replication to standby.
- **Backups**:
  - **Automated**: Daily, retained for 7 backups (default).
  - **On-demand**: User initiated.
  - **Point-in-Time Recovery (PITR)**: By enabling binary logs (MySQL) or write-ahead logs (Postgres).
- **Maintenance**: Defines a window for OS/database patching. Connection drops during maintenance.

## Traps & "Gotchas"
1. **Write Scaling**: Cloud SQL does **NOT** scale writes horizontally. If you need massive write scaling (millions of QPS), Cloud SQL is the wrong answer. -> Look at **Cloud Spanner**.
2. **Global Reach**: Cloud SQL is a **Regional** resource. If you need a strictly global database with active-active consistency across continents -> Look at **Cloud Spanner**.
3. **Capacity**: If your dataset exceeds 64 TB or requires petabytes -> Look at **Cloud Spanner** or **Bigtable** (if NoSQL).
4. **IAM Auth**: You can use IAM database authentication to log in without a password, but you still need a database user.

## Important Points / Exam Clues
- Keywords: "Relational", "Existing MySQL/Postgres", "Web Framework", "Lift and Shift", "Transactional", "Strong Consistency".
- **Cloud SQL Proxy**: Safe way to connect to Cloud SQL from GKE, Compute Engine, or local without managing SSL certificates or allowing authorized networks (public IP).
- **Private Service Connect / Private IP**: standard way to connect securely within VPC.

## Tips
- Always check if the requirements mention "Global Scale" or "Regional". Regional = Cloud SQL is a contender. Global = Spanner.
- If the exam asks about "migrating an existing PostgreSQL database" with minimal changes -> Cloud SQL for PostgreSQL.
- **Downtime**: Changing machine type (vertical scaling) causes downtime. HA failover causes a brief downtime (seconds).
