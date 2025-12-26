# Global Multiplayer Game Architecture - Multi-Database Pattern

This document explains a production-grade, multi-database architecture for a global multiplayer game using Google Cloud services.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         GAME CLIENTS                                │
│              (Mobile, Console, PC - Global Users)                   │
└─────────────┬───────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    GLOBAL LOAD BALANCER                             │
│              (Cloud Armor + Cloud CDN for static assets)            │
└─────────────┬───────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      GAME SERVERS (GKE)                             │
│              (Regional clusters in US, EU, Asia)                    │
└──┬────┬────┬────┬────┬──────────────────────────────────────────────┘
   │    │    │    │    │
   │    │    │    │    └──────────────────────────────────────────┐
   │    │    │    │                                               │
   │    │    │    └───────────────────────────────┐               │
   │    │    │                                    │               │
   │    │    └────────────────────┐               │               │
   │    │                         │               │               │
   │    │                         ▼               ▼               ▼
   │    │              ┌──────────────────────────────────────────────┐
   │    │              │    CLOUD FIRESTORE (Document DB)             │
   │    │              │  "Player Profiles, Inventory, Leaderboards"  │
   │    │              └──────────────────────────────────────────────┘
   │    │
   │    │                         ▼               ▼               ▼
   │    │              ┌──────────────────────────────────────────────┐
   │    │              │   MEMORYSTORE (Redis - Regional Cache)       │
   │    │              │  "Session Data, Matchmaking Queue, TTL Data" │
   │    │              └──────────────────────────────────────────────┘
   │    │
   │    │                         ▼               ▼               ▼
   │    │              ┌──────────────────────────────────────────────┐
   │    │              │      CLOUD SPANNER (Relational DB)           │
   │    │              │   "ACID Transactions: Purchases, Trades"     │
   │    │              └──────────────────────────────────────────────┘
   │    │
   │    └─────────────────────────▼
   │                  ┌──────────────────────────────────────────────┐
   │                  │          PUB/SUB TOPICS                      │
   │                  │  "player.events", "game.metrics", "logs"     │
   │                  └─────────┬────────────────────────────────────┘
   │                            │
   │                            ▼
   │                  ┌──────────────────────────────────────────────┐
   │                  │    DATAFLOW (Stream Processing)              │
   │                  │  "Aggregate metrics, Enrich events"          │
   │                  └─────────┬────────────────────────────────────┘
   │                            │
   │                            ▼
   └───────────────────────────▶┌──────────────────────────────────┐
                                │         BIGQUERY                 │
                                │  "Analytics: Daily Active Users, │
                                │   Revenue, Player Behavior"      │
                                └──────────────────────────────────┘
```

---

## Component Analysis Table

| Component | Problem It Solves | Why This Component (vs Alternatives) | Key Benefits | Connection Pattern |
|:----------|:------------------|:-------------------------------------|:-------------|:-------------------|
| **Cloud Firestore (Document DB)** | Store player profiles, inventory, game state with flexible schema and real-time sync | **vs Cloud SQL**: No joins needed for player data (hierarchical: Player → Inventory → Items). Scales horizontally.<br>**vs Bigtable**: Need complex queries (filters, indexes) not just key-value lookups.<br>**vs Spanner**: Player profiles don't need global ACID transactions (eventual consistency acceptable). | • **Mobile SDKs** (offline sync, real-time listeners)<br>• **Flexible schema** (add new item types without ALTER TABLE)<br>• **Serverless** (zero ops, auto-scales)<br>• **Fast reads** (sub-10ms for player profile by ID) | • Game servers read/write player state<br>• Real-time listeners update leaderboards<br>• Inventory changes written here |
| **Memorystore (Redis)** | Sub-millisecond cache for hot data (matchmaking queues, session tokens, TTL data) | **vs Firestore caching**: Need atomic operations (INCR, LPUSH for queues).<br>**vs In-memory cache**: Need shared state across game server instances (not per-instance).<br>**vs Cloud SQL**: Redis is **100x faster** (sub-ms vs 10ms) for simple lookups. | • **Sub-millisecond latency** (0.5-2ms)<br>• **Atomic operations** (leaderboards, counters)<br>• **TTL support** (auto-expire matchmaking tickets after 30 sec)<br>• **Pub/Sub** (notify all servers of match found) | • Game servers check cache before Firestore<br>• Write-through cache (update Redis + Firestore)<br>• Matchmaking queue (LPUSH/RPOP) |
| **Cloud Spanner (Relational DB)** | ACID transactions for financial operations (in-game purchases, player-to-player trades) | **vs Cloud SQL**: Need **global consistency** (player buys item in US, trades it in EU immediately).<br>**vs Firestore**: Need **multi-entity transactions** (deduct currency AND grant item atomically).<br>**vs Manual sharding**: Spanner auto-scales horizontally without app-level sharding logic. | • **Global ACID** (strong consistency across continents)<br>• **Horizontal scaling** (unlimited writes)<br>• **SQL support** (complex queries for fraud detection)<br>• **99.999% SLA** (multi-region) | • Game servers call Spanner for purchases/trades<br>• Read player balance from Spanner<br>• Write transaction logs to Spanner |
| **Cloud Pub/Sub (Event Streaming)** | Decouple game servers from analytics pipeline (async, buffered event delivery) | **vs Direct BigQuery writes**: Game servers shouldn't wait for BigQuery (100ms latency). Pub/Sub buffers events.<br>**vs Cloud Logging**: Need **custom processing** (aggregations, enrichment) before storing in BigQuery.<br>**vs Synchronous API calls**: Pub/Sub guarantees delivery even if downstream fails. | • **Asynchronous** (game servers don't block on analytics)<br>• **At-least-once delivery** (events never lost)<br>• **Buffering** (handles traffic spikes, 1M events/sec)<br>• **Fan-out** (one event → multiple subscribers) | • Game servers publish events to topics<br>• Dataflow subscribes to topics<br>• Cloud Logging also subscribes (for debugging) |
| **Dataflow (Stream Processing)** | Transform and aggregate raw events before loading into BigQuery (ETL pipeline) | **vs Direct Pub/Sub → BigQuery**: Need **windowing** (aggregate metrics per minute, not per event).<br>**vs Cloud Functions**: Dataflow handles **millions of events/sec** with exactly-once semantics.<br>**vs Manual scripts**: Dataflow auto-scales workers based on Pub/Sub backlog. | • **Stream + Batch** processing (Apache Beam)<br>• **Windowing** (tumbling/sliding windows for metrics)<br>• **Auto-scaling** (dynamic worker count)<br>• **Exactly-once** semantics (no duplicate metrics) | • Subscribes to Pub/Sub topics<br>• Aggregates events (e.g., "kills per minute")<br>• Writes to BigQuery tables |
| **BigQuery (Analytics Data Warehouse)** | Historical analytics (daily active users, revenue trends, player behavior) | **vs Firestore**: BigQuery handles **petabytes** and **complex SQL joins** (revenue × player segment).<br>**vs Cloud SQL**: BigQuery scans **terabytes in seconds** (columnar storage).<br>**vs Elasticsearch**: BigQuery is serverless and cheaper for append-only logs. | • **Serverless** (no clusters to manage)<br>• **Petabyte-scale** (years of game logs)<br>• **Standard SQL** (BI tools: Looker, Tableau)<br>• **Cost-effective** (columnar storage, $5/TB scanned) | • Dataflow streams data to BigQuery<br>• Data analysts run SQL queries<br>• Dashboards query BigQuery (Looker Studio) |

---

## Data Flow Examples

### Example 1: Player Logs In

```
1. Client → Game Server: "Login(player_id: 12345, token: xyz)"
2. Game Server → Memorystore: GET session:xyz
   └─ Cache Hit → Return player session (0.5ms)
   └─ Cache Miss:
      └─ Game Server → Firestore: GET players/12345 (8ms)
      └─ Game Server → Memorystore: SET session:xyz (cache for 1 hour)
3. Game Server → Pub/Sub: Publish("player.login", {player_id, timestamp, region})
4. Response to Client: "Welcome back, Player12345!"
```

**Why this pattern?**
- **Memorystore first** (sub-ms latency for active players).
- **Firestore fallback** (source of truth for player data).
- **Pub/Sub async** (analytics doesn't block login).

---

### Example 2: Player Purchases In-Game Currency

```
1. Client → Game Server: "BuyGems(player_id: 12345, gems: 1000, usd: 9.99)"
2. Game Server → Cloud Spanner (TRANSACTION):
   BEGIN;
     -- Check current balance
     SELECT balance FROM player_wallets WHERE player_id = 12345;
     -- Deduct real money (if using wallet)
     UPDATE player_wallets SET balance = balance - 9.99 WHERE player_id = 12345;
     -- Grant gems
     INSERT INTO transactions (player_id, type, amount, timestamp) VALUES (12345, 'purchase', 1000, NOW());
     UPDATE player_wallets SET gems = gems + 1000 WHERE player_id = 12345;
   COMMIT;
3. Game Server → Firestore: UPDATE players/12345 {gems: 1000} (for real-time sync to client)
4. Game Server → Pub/Sub: Publish("revenue.purchase", {player_id, amount, gems, timestamp})
5. Response to Client: "Purchase successful! +1000 gems"
```

**Why Spanner here?**
- **ACID transaction**: All steps succeed or all fail (can't charge money without granting gems).
- **Strong consistency**: If player immediately logs in from different region, they see the gems (no eventual consistency lag).
- **Audit trail**: `transactions` table provides immutable record for fraud detection.

---

### Example 3: Matchmaking

```
1. Client → Game Server: "JoinQueue(player_id: 12345, skill_rating: 1500)"
2. Game Server → Memorystore:
   LPUSH matchmaking:queue:1500 "12345"  ← Add player to queue (skill bucket)
   LLEN matchmaking:queue:1500           ← Check queue length
   
   IF length >= 10:  ← Enough players for a match
     players = RPOP matchmaking:queue:1500 (10 times) ← Pop 10 players
     
     FOR EACH player:
       Publish to Pub/Sub channel "match.found.{player_id}"
       
3. Game Server → Firestore:
   CREATE matches/match_67890 {
     players: [12345, ...],
     status: "in_progress",
     server: "us-central1-a-server-42"
   }
4. Response to Clients: "Match found! Connecting to server..."
```

**Why Memorystore (Redis) here?**
- **List operations** (LPUSH/RPOP) are atomic and fast.
- **Sub-ms latency**: Matchmaking needs to respond in < 10ms.
- **Shared state**: All game servers in a region see the same queue (not per-server).
- **TTL**: If player disconnects, their queue entry expires after 30 seconds (EXPIRE command).

---

### Example 4: Analytics Query (Business Intelligence)

```sql
-- Data Analyst runs this query in BigQuery:

SELECT
  DATE(event_timestamp) AS date,
  region,
  COUNT(DISTINCT player_id) AS daily_active_users,
  SUM(CASE WHEN event_type = 'purchase' THEN revenue ELSE 0 END) AS daily_revenue,
  AVG(session_duration_sec) AS avg_session_duration
FROM
  `game_analytics.player_events`
WHERE
  event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY
  date, region
ORDER BY
  date DESC;
```

**Result**: Scan 30 days of events (100 TB) in **12 seconds**.

**Why BigQuery here?**
- **Columnar storage**: Only reads columns used in query (not entire rows).
- **Distributed execution**: 1,000+ workers scan in parallel.
- **Separation from operational DB**: Spanner/Firestore serve game traffic, BigQuery handles analytics (no resource contention).

---

## Lambda Architecture Pattern Explained

This multiplayer game architecture follows the **Lambda Architecture** pattern, a design approach for handling both real-time and batch data processing.

### What is Lambda Architecture?

**Lambda Architecture** separates data processing into two parallel paths:

```
                    ┌─────────────────────────────────┐
                    │         DATA SOURCE             │
                    │      (Game Events/Actions)      │
                    └───────────┬─────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │                       │
                    ▼                       ▼
        ┌───────────────────┐   ┌───────────────────┐
        │   SPEED LAYER     │   │   BATCH LAYER     │
        │   (Real-Time)     │   │   (Analytics)     │
        │                   │   │                   │
        │ • Memorystore     │   │ • Pub/Sub         │
        │ • Firestore       │   │ • Dataflow        │
        │ • Spanner         │   │ • BigQuery        │
        │                   │   │                   │
        │ Latency: < 10ms   │   │ Latency: minutes  │
        │ Data: Hot (hours) │   │ Data: Cold (years)│
        └───────────────────┘   └───────────────────┘
                    │                       │
                    └───────────┬───────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   SERVING LAYER     │
                    │  (Combined Views)   │
                    │                     │
                    │ • Dashboards        │
                    │ • APIs              │
                    │ • Reports           │
                    └─────────────────────┘
```

### The Two Layers Explained

#### 1. **Speed Layer (Hot Path / Real-Time)**
**Goal**: Serve game requests with minimal latency (< 10ms).

**Components in This Architecture**:
- **Memorystore (Redis)**: Session cache, matchmaking queues.
- **Cloud Firestore**: Player profiles, inventory, leaderboards.
- **Cloud Spanner**: In-game purchases, trades (ACID transactions).

**Characteristics**:
- **Low Latency**: Sub-10ms response time.
- **Hot Data**: Recent data (last 24 hours to 7 days).
- **Optimized for Reads**: 99% of game requests are reads (get player profile, check inventory).
- **Write-Through**: Writes update both cache (Memorystore) and source (Firestore/Spanner).

**Example Flow**:
```
Player Login Request
  └─> Memorystore (0.5ms cache check)
      └─> Cache Miss → Firestore (8ms read player profile)
          └─> Memorystore (update cache for next login)
  └─> Response to Client: 8.5ms total
```

---

#### 2. **Batch Layer (Cold Path / Analytics)**
**Goal**: Process and analyze historical data for business intelligence.

**Components in This Architecture**:
- **Pub/Sub**: Event ingestion buffer (decouples game servers from analytics).
- **Dataflow**: Stream/batch processing (aggregations, transformations).
- **BigQuery**: Data warehouse (stores petabytes of historical events).

**Characteristics**:
- **High Latency**: Acceptable for analytics (minutes to hours).
- **Cold Data**: Historical data (months to years).
- **Optimized for Writes**: Append-only (no updates, only inserts).
- **Async Processing**: Game servers fire-and-forget (don't wait for analytics).

**Example Flow**:
```
Player Purchases Gems
  └─> Spanner (ACID transaction, 50ms)
  └─> Pub/Sub: Publish "revenue.purchase" event (async, 2ms)
      └─> Dataflow: Aggregate "revenue per hour" (5 minutes later)
          └─> BigQuery: Append to revenue_events table
              └─> Dashboard: Shows updated revenue (6 minutes delay is OK)
```

---

### Why Lambda Architecture for Games?

#### Problem 1: **Conflicting Requirements**
- **Game Servers**: Need **sub-10ms latency** (players won't tolerate lag).
- **Analytics**: Need to process **billions of events** (can't run expensive queries on operational DB).

**Without Lambda Architecture**:
- Running analytics queries on Firestore/Spanner **slows down game servers** (resource contention).
- Alternative: Duplicate data manually → expensive, error-prone.

**With Lambda Architecture**:
- **Speed Layer**: Dedicated for game traffic (no analytics interference).
- **Batch Layer**: Dedicated for analytics (runs separately, doesn't impact game).

---

#### Problem 2: **Read vs Write Optimization**
- **Reads** (game requests): Need indexes, caching, low-latency access.
- **Writes** (analytics): Need append-only, columnar storage, batch processing.

**Lambda Architecture Solution**:
- **Speed Layer** (Firestore/Spanner): Optimized for random reads with indexes.
- **Batch Layer** (BigQuery): Optimized for append-only writes with columnar storage.

---

### How Data Flows Between Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                         GAME EVENT                              │
│          "Player 12345 purchased 1000 gems for $9.99"           │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┴──────────────┐
        │                              │
        ▼                              ▼
┌─────────────────┐          ┌─────────────────┐
│  SPEED LAYER    │          │  BATCH LAYER    │
│  (Synchronous)  │          │  (Asynchronous) │
├─────────────────┤          ├─────────────────┤
│ 1. Spanner:     │          │ 1. Pub/Sub:     │
│    BEGIN TRANS  │          │    Publish event│
│    UPDATE wallet│          │    (topic: rev) │
│    INSERT txn   │          │                 │
│    COMMIT       │          │ 2. Dataflow:    │
│    (50ms)       │          │    Read from    │
│                 │          │    Pub/Sub      │
│ 2. Firestore:   │          │    Aggregate    │
│    UPDATE gems  │          │    "revenue/hr" │
│    (10ms)       │          │    (5 min later)│
│                 │          │                 │
│ 3. Response:    │          │ 3. BigQuery:    │
│    "Success!"   │          │    INSERT event │
│    (60ms total) │          │    (6 min later)│
└─────────────────┘          └─────────────────┘
```

**Key Insight**: Speed Layer completes in **60ms** (player sees success). Batch Layer completes in **6 minutes** (analyst sees updated revenue dashboard). Both layers process the **same event** independently.

---

### Lambda Architecture Benefits

| Benefit | Explanation |
|:--------|:------------|
| **Fault Tolerance** | If BigQuery/Dataflow fails, game servers are unaffected (Pub/Sub buffers events until recovery). |
| **Scalability** | Speed Layer scales independently from Batch Layer (add more Firestore capacity without increasing BigQuery costs). |
| **Cost Optimization** | Speed Layer uses expensive, fast storage (Memorystore). Batch Layer uses cheap, slow storage (BigQuery = $0.02/GB/month). |
| **Query Flexibility** | Speed Layer optimized for known queries (get player profile). Batch Layer supports ad-hoc queries (analysts explore data). |
| **Historical Analysis** | Speed Layer keeps hot data (7 days). Batch Layer keeps all data (7 years for compliance). |

---

### Lambda Architecture Trade-Offs

#### Advantages ✅
- **Performance**: Speed Layer serves real-time requests without analytics overhead.
- **Separation of Concerns**: Operational and analytical workloads don't interfere.
- **Flexibility**: Can change analytics logic (Dataflow transformations) without touching game servers.

#### Disadvantages ❌
- **Complexity**: Two separate data pipelines to maintain.
- **Eventual Consistency**: Analytics data lags behind operational data by minutes (acceptable for most use cases).
- **Duplicate Logic**: Sometimes need to implement same business logic in both layers (e.g., revenue calculation in Spanner transaction AND Dataflow aggregation).

---

### Alternative: Kappa Architecture (Simpler, Stream-Only)

**Lambda**: Speed Layer (DB) + Batch Layer (Stream Processing)  
**Kappa**: Everything is a stream (no separate batch layer).

```
Game Events → Pub/Sub → Dataflow → {Firestore, BigQuery}
```

**When to use Kappa**:
- All data can be reprocessed from the stream (no need for separate batch recalculations).
- Lower operational complexity (single pipeline).

**When to use Lambda** (our choice):
- Need **dual optimization** (real-time reads vs batch analytics).
- Game servers can't tolerate stream processing latency.

---

## Key Architectural Principles

### 1. **Polyglot Persistence** (Right Tool for the Job)
- **Firestore**: Document storage (flexible, real-time).
- **Spanner**: Relational + global ACID.
- **Memorystore**: Hot cache (sub-ms latency).
- **BigQuery**: Analytics (petabyte-scale SQL).

**Anti-pattern**: Using one database for everything (e.g., Spanner for both operational and analytics → expensive, slow analytics queries).

---

### 2. **Read Path Optimization** (Cache Hierarchy)
```
Client Request
  └─> Memorystore (sub-ms) ← Cache
      └─> Firestore/Spanner (10ms) ← Source of Truth
          └─> BigQuery (seconds) ← Historical Analytics
```

**99% of reads** hit Memorystore (cheapest, fastest).  
**1% of reads** (cache miss) hit Firestore.  
**Analytics queries** go to BigQuery (separate).

---

### 3. **Write Path Decoupling** (Async Event Streaming)
```
Game Server
  └─> Spanner (synchronous, ACID) ← Critical writes (purchases)
  └─> Firestore (synchronous) ← Player state updates
  └─> Pub/Sub (async, fire-and-forget) ← Analytics events
      └─> Dataflow → BigQuery ← Never blocks game servers
```

**Game servers never wait** for analytics writes (Pub/Sub is asynchronous).

---

### 4. **CAP Theorem Alignment**

| Component | CAP Choice | Why? |
|:----------|:-----------|:-----|
| Spanner | **CP** (Consistency + Partition) | Purchases need strong consistency (no double-spending). |
| Firestore | **CP** (with caching = feels like CA) | Player profiles need consistency, but caching hides latency. |
| Memorystore | **CA** (regional only) | Cache is regional (no cross-region consistency needed). |
| BigQuery | **AP** (eventually consistent ingestion) | Analytics can tolerate 1-2 minute ingestion lag. |

---

## Cost Optimization

| Component | Typical Cost (for 1M daily active users) | Optimization Tips |
|:----------|:------------------------------------------|:------------------|
| Firestore | $500-1,000/month | • Use TTL for temporary data<br>• Minimize document reads (cache in Memorystore) |
| Memorystore | $200-400/month | • Right-size instance (M1 = 5 GB = $30/month)<br>• Use regional (not multi-region) |
| Spanner | $2,000-5,000/month | • Use Regional (not Multi-Region) if possible<br>• Partition tables to avoid hotspots |
| Pub/Sub | $100-200/month | • Use batching (publish 100 events at once)<br>• Set message retention to 1 day (not 7 days) |
| Dataflow | $1,000-2,000/month | • Use batch processing for non-real-time metrics<br>• Auto-scaling (min workers = 1) |
| BigQuery | $500-1,000/month | • Partition tables by date<br>• Use clustering on frequently filtered columns |

**Total**: ~$4,300-9,600/month (for 1M DAU).

---

## When to Add/Remove Components

### Add a Component If:
- **Add Memorystore** if response time > 50ms (cache hot data).
- **Add Spanner** if you need multi-entity ACID transactions (purchases, trades).
- **Add Pub/Sub + Dataflow** if analytics queries slow down operational DB.

### Remove a Component If:
- **Remove Spanner** if you can model purchases as single-document transactions (Firestore handles this).
- **Remove Dataflow** if event volume < 1,000/sec (direct Pub/Sub → BigQuery works).
- **Remove Memorystore** if 99th percentile latency < 10ms (Firestore alone is fast enough).

---

## Exam-Style Decision Framework

**Question**: "Global multiplayer game needs to store player profiles with real-time leaderboards AND process billions of analytics events. Which databases?"

**Answer**:
1. **Firestore**: Player profiles + leaderboards (real-time, document model).
2. **Memorystore**: Cache hot data (leaderboard top 100).
3. **Pub/Sub → Dataflow → BigQuery**: Analytics pipeline (async, decoupled).

**Why NOT just Spanner?**
- Spanner is expensive for high-read, eventual-consistency-tolerant data (player profiles).
- BigQuery is 10x cheaper for analytics (columnar storage).

**Why NOT just BigQuery?**
- BigQuery latency is seconds, not milliseconds (can't serve game requests).

---

## Summary

This multi-database architecture follows the **Lambda Architecture** pattern:

```
Speed Layer (Real-Time):    Memorystore → Firestore/Spanner
Batch Layer (Analytics):    Pub/Sub → Dataflow → BigQuery
```

Each component solves a **specific problem**:
- **Firestore**: Flexible, real-time player data.
- **Memorystore**: Sub-ms cache for hot paths.
- **Spanner**: Global ACID for money.
- **Pub/Sub**: Async decoupling.
- **Dataflow**: Stream processing.
- **BigQuery**: Petabyte analytics.

**Key Takeaway**: Don't use one database for everything. Choose the right tool for each workload.
