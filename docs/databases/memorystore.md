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
- **Memorystore Offerings** (Engines):
  - **Memorystore for Redis (Standalone)**: Single instance, up to **300 GB**. Default choice for most use cases.
  - **Memorystore for Redis Cluster**: Multi-node (sharded), up to **5 TB**. Use for very large caches (> 300 GB).
  - **Memorystore for Memcached**: Simple key-value, no persistence.
  - **Memorystore for Valkey**: New (2024), API-compatible with Redis. Not tested on PCA yet.
- **High Availability**:

  - **Basic Tier**: No HA (ephemeral).
  - **Standard Tier**: Primary + Replica in different zones. Automatic failover.
- **Networking**: Accessible via **Private IP** (VPC Peering) or Private Service Connect. Not directly public.

## Traps & "Gotchas"
1. **Persistence**: Memorystore for Redis offers optional persistence (RDB snapshots), but it's primarily a cache. If you need a durable *primary* database, don't rely solely on Memorystore. Use Cloud SQL/Spanner as the source of truth.
2. **Maintenance**: Standard Tier instances experience less disruption during maintenance due to failover, but basic tier instances essentially "reboot" (cache clear).
2. **Global**: Memorystore is a **Regional** (or Zonal) service. No built-in global federation like Spanner.

## Important Points / Exam Clues
- Keywords: "Cache", "Sub-millisecond", "Session Store", "Leaderboard", "Reduce database load".
- **Migration**: "Lift and shift existing Redis/Memcached" -> Memorystore.
- **Strategy**: Used often in front of Cloud SQL or Spanner to absorb read traffic.

## Tips
- Requirement: "Reduce latency for frequent database queries" -> **Memorystore**.
- Requirement: "Manage user sessions" -> **Memorystore (Redis)**.
- Difference: If the app needs simple threading/caching -> Memcached. If complex data types/HA -> Redis.

---

## PCA Exam Focus (What to Know vs What to Skip)

### ✅ **Know This** (Tested on Exam)

1. **When to use Memorystore**:
   - Sub-ms latency for caching (reduce database load)
   - Session management (stateless app design)
   - Leaderboards/counters (atomic operations: INCR, ZADD)
   - Matchmaking queues (LPUSH/RPOP for lists)

2. **Redis vs Memcached decision**:
   - **Redis**: Need data structures (lists, sets), persistence, pub/sub, HA → Choose **Redis**
   - **Memcached**: Need simple key-value, multi-threaded performance → Choose **Memcached**

3. **Standalone vs Cluster mode**:
   - **Standalone Redis**: Cache < 300 GB → **Default choice**
   - **Redis Cluster**: Cache > 300 GB → Use cluster mode (sharded, up to 5 TB)

4. **Basic vs Standard Tier**:

   - **Basic**: No HA, cheaper, cache can be lost during maintenance
   - **Standard**: HA with automatic failover, cross-zone replication

4. **Common exam patterns**:
   - "Reduce latency for database queries" → **Memorystore**
   - "Session store for stateless app" → **Memorystore (Redis)**
   - "Real-time leaderboard" → **Memorystore (Redis Sorted Sets)**

### ❌ **Skip This** (NOT Tested on Exam)

- Redis Enterprise cluster architecture (shared-nothing, symmetric architecture)
- Redis Cluster hash slots and CRC16 partitioning algorithms
- Specific Redis commands and Lua scripting syntax
- Redis Enterprise-specific features (Active-Active geo-replication, CRDT)
- Low-level replication protocol details

**Exam Takeaway**: Focus on **"when to use Memorystore"** and **"Redis vs Memcached"** at a high level. Skip internal implementation details.
