# CAP Theorem for PCA

The **CAP theorem** is a fundamental principle in distributed systems that explains why different databases make different trade-offs. Understanding it helps you answer "Why use X instead of Y?" questions on the exam.

---

## What is the CAP Theorem?

**CAP Theorem** (also called Brewer's Theorem) states that a distributed database can only guarantee **2 out of 3** of the following properties:

### 1. **C**onsistency
- **Definition**: All nodes see the same data at the same time.
- **Example**: If you write "balance = $100" to the database, every subsequent read (from any node, anywhere in the world) will return "$100" immediately.
- **Strong Consistency**: What Spanner and Bigtable provide.

### 2. **A**vailability
- **Definition**: Every request receives a response (success or failure), even if some nodes are down.
- **Example**: If one datacenter fails, the system continues accepting reads and writes from the other datacenters.
- **Always Online**: What Cassandra prioritizes.

### 3. **P**artition Tolerance
- **Definition**: The system continues to operate despite network partitions (when nodes can't communicate with each other).
- **Example**: If the network cable between US and EU datacenters is cut, both regions continue working independently.
- **Required in Practice**: You **must** choose Partition Tolerance in distributed systems (network failures are inevitable).

---

## The Forced Choice: Pick 2 of 3

Since **Partition Tolerance** is mandatory in distributed systems (networks fail), you're really choosing between:

**Consistency (C) vs Availability (A)**

---

## Google Cloud Database Services on CAP Spectrum

| Database | CAP Choice | What It Means | Trade-Off |
| :--- | :--- | :--- | :--- |
| **Cloud Spanner** | **CP** (Actually "CA" using TrueTime) | Strong global consistency, high availability (but costs more). | Expensive. Uses TrueTime to "cheat" CAP in practice. |
| **Cloud Bigtable** | **CP** | Consistency + Partition Tolerance. Single-master writes. | If the master region fails, writes pause until failover completes. |
| **Cassandra (DataStax)** | **AP** | Availability + Partition Tolerance. Eventual consistency. | You might read stale data for a brief period. |
| **Firestore** | **CP** (with caching) | Strong consistency for writes, but can serve stale cached reads. | Hybrid model. |
| **Cloud SQL** | **CA** (not distributed) | Consistency + Availability within a region. No partition tolerance across regions. | Regional only. Not a distributed database. |

---

## Visual Explanation

```
         Consistency (C)
              /\
             /  \
            /    \
           /  CP  \
          /  (BT)  \
         /  (Span) \
        /___________\
       /             \
      /      CA       \
     /   (Cloud SQL)   \
    /___________________\
   /                     \
  A (Availability)       P (Partition Tolerance)
           \            /
            \   AP    /
             \ (Cass)/
              \     /
               \   /
                \ /
```

---

## How CAP Impacts PCA Exam Decisions

### Scenario 1: "Global Financial System, Zero Tolerance for Inconsistency"
**Requirement**: Strong consistency everywhere.  
**CAP Choice**: **CP** (Consistency + Partition Tolerance).  
**Answer**: **Cloud Spanner** (Globally consistent ACID transactions).

### Scenario 2: "IoT Platform, Must Accept Writes Even if Datacenters Disconnect"
**Requirement**: Always available for writes, even during network partitions.  
**CAP Choice**: **AP** (Availability + Partition Tolerance).  
**Answer**: **Cassandra/DataStax** (Multi-datacenter active-active writes with eventual consistency).

### Scenario 3: "E-commerce Product Catalog, Read-Heavy, Regional"
**Requirement**: Fast reads, strong consistency not critical.  
**CAP Choice**: **CA** (within region).  
**Answer**: **Cloud SQL** + **Read Replicas** (Async replication is acceptable).

---

## Key Exam Patterns

### Pattern 1: "Eventual Consistency" Keyword
If you see **"eventual consistency"** or **"stale reads acceptable"**:
- **Answer**: **Cassandra/DataStax** (AP).
- **Why**: Trades consistency for availability.

### Pattern 2: "Strong Consistency" Keyword
If you see **"strong consistency"** or **"ACID transactions globally"**:
- **Answer**: **Cloud Spanner** (CP, but with high availability via TrueTime).
- **Why**: Refuses to serve stale data even during network issues.

### Pattern 3: "Multi-Region Writes" Keyword
If you see **"accept writes in multiple regions simultaneously"**:
- **Cassandra/DataStax**: AP (eventual consistency, conflicts resolved later).
- **Cloud Spanner**: CP (strong consistency, but writes can go to multiple regions via Paxos quorum).

---

## Common Misconceptions

### Misconception 1: "Cloud Spanner Breaks CAP Theorem"
**Reality**: Spanner doesn't break CAP. It chooses **CP** (Consistency + Partition Tolerance) but uses **TrueTime** to make the availability impact so small it feels like "CA" in practice.

### Misconception 2: "Eventual Consistency Means Data Loss"
**Reality**: Eventual consistency means **temporary inconsistency** (different nodes might return different values for a brief period), not data loss. All nodes will **eventually** converge to the same value.

### Misconception 3: "Bigtable is AP"
**Reality**: Bigtable is **CP**. It has a single-master for writes (strong consistency). Read replicas exist but they're async (for read scaling, not multi-master writes).

---

## The Spanner "Exception" (How It Seems to Violate CAP)

Spanner is often called "CA" because it provides:
- **Strong Consistency** (C)
- **High Availability** (A - 99.999% SLA)

But technically, it's **CP** with extremely good availability due to:
1. **TrueTime**: Reduces uncertainty windows to microseconds.
2. **Paxos Quorum**: Majority of replicas (e.g., 3 of 5) must agree, so it survives some node failures.
3. **Geographic Distribution**: Replicas in multiple zones/regions reduce blast radius of failures.

**Result**: Spanner delivers what feels like "CA" in practice, but it's technically CP (during a network partition, it prioritizes consistency over availability).

---

## Exam Decision Tree Using CAP

```
1. Is the database distributed across multiple regions?
   ├─ NO → Cloud SQL (CA, Regional)
   └─ YES → Continue to 2

2. Must it guarantee strong consistency globally?
   ├─ YES → Cloud Spanner (CP with high availability)
   └─ NO → Continue to 3

3. Is eventual consistency acceptable?
   ├─ YES → Cassandra/DataStax (AP)
   └─ NO → Bigtable (CP, single-master writes)
```

---

## Summary for the Exam

- **CAP Theorem**: You can only pick 2 of 3 (Consistency, Availability, Partition Tolerance).
- **In Practice**: You must choose Partition Tolerance (networks fail), so you're picking between **C** (Consistency) or **A** (Availability).
- **Cloud Spanner**: CP (but feels like CA due to TrueTime).
- **Cassandra/DataStax**: AP (always available, eventual consistency).
- **Bigtable**: CP (strong consistency, single-master writes).
- **Cloud SQL**: CA (not distributed, regional only).

**Exam Tip**: When you see "eventual consistency" → think AP (Cassandra). When you see "strong consistency globally" → think CP (Spanner).
