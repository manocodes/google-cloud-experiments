# Cloud Memorystore for PCA

## Fundamentals
- **Service Type**: Fully managed in-memory data store service.
- **Engines**: Redis, Memcached.
- **Use Cases**: Caching (database/session), Gaming leaderboards, Real-time analytics, Pub/Sub (Redis), Message queues.
- **Performance**: Sub-millisecond latency.

## Critical Information
- **Redis vs Memcached**:
  - **Redis**: Advanced data structures (Sets, Sorted Sets, Lists), Persistence (RDB/AOF), Pub/Sub, High Availability (Replication).
  - **Memcached**: Simple Key-Value, Multi-threaded (better vertical scaling on single node for pure KV), No persistence.
- **High Availability**:
  - **Basic Tier**: No HA (ephemeral).
  - **Standard Tier**: Primary + Replica in different zones. Automatic failover.
- **Networking**: Accessible via **Private IP** (VPC Peering) or Private Service Connect. Not directly public.

## Traps & "Gotchas"
1. **Persistence**: Memorystore for Redis offers optional persistence (RDB snapshots), but it's primarily a cache. If you need a durable *primary* database, don't rely solely on Memorystore.
2. **Global**: Memorystore is a **Regional** (or Zonal) service. No built-in global federation like Spanner.

## Important Points / Exam Clues
- Keywords: "Cache", "Sub-millisecond", "Session Store", "Leaderboard", "Reduce database load".
- **Migration**: "Lift and shift existing Redis/Memcached" -> Memorystore.
- **Strategy**: Used often in front of Cloud SQL or Spanner to absorb read traffic.

## Tips
- Requirement: "Reduce latency for frequent database queries" -> **Memorystore**.
- Requirement: "Manage user sessions" -> **Memorystore (Redis)**.
- Difference: If the app needs simple threading/caching -> Memcached. If complex data types/HA -> Redis.
