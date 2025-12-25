# Cloud Firestore for PCA

## Fundamentals
- **Service Type**: Fully managed, serverless, document-oriented NoSQL database.
- **Successor to**: Cloud Datastore (Datastore mode is available on Firestore backend).
- **Use Cases**: Mobile backend, Web apps, User profiles, Game state, Real-time synchronization (chat apps), Offline support.
- **Data Model**: Collections of Documents. Data is JSON-like.

## Critical Information
- **Modes**:
  - **Native Mode**: Supports real-time updates, client libraries for mobile/web, offline sync.
  - **Datastore Mode**: For backward compatibility with Datastore, high write throughput, no real-time client features.
- **ACID**: Firestore supports cross-document ACID transactions! (Unlike legacy NoSQL).
- **Indexing**: Automatic indexing of all fields by default (makes writes slightly heavier, reads super fast).
- **Multi-region**: Automatic multi-region replication available for 99.999% SLA.

## Traps & "Gotchas"
1. **Write Limits**: Native mode has soft limits on write rates to a *single document* (~1 write/sec) to maintain index consistency. Not for high-frequency counters (use distributed counters or Bigtable/Memorystore).
2. **Queries**: Very specific query limitations. "No sorting by field A and filtering by field B without a composite index."
3. **Selectivity**: Firestore pricing is predominantly **Read/Write Operations**, not just storage. A query returning 1 million documents costs 1 million reads.
4. **Mode Selection**: You choose **Native** or **Datastore** mode at project creation. **You cannot change this later**. Choosing wrong is a fatal project error requiring migration.

## Important Points / Exam Clues
- Keywords: "Mobile", "Offline sync", "JSON", "Documents", "Real-time updates", "Serverless".
- **Firestore vs Bigtable**: Bigtable for heavy analytic/ingestion throughput (machine-generated). Firestore for app-serving/user-generated hierarchical data.

## Tips
- Requirement: "Mobile app with offline capability" -> **Firestore**.
- Requirement: "Fast application development with flexible schema" -> **Firestore**.
- Requirement: "Legacy application using Datastore API" -> **Firestore in Datastore Mode**.
- Exam Trick: "Datastore" is often the answer for older "NoSQL transactional" questions, which effectively means Firestore now.

## Comparison: Cloud Firestore vs Firebase Realtime Database
*   **Yes, they are different!** Both are part of the Firebase suite, but:
    1.  **Cloud Firestore**: The newer, flagship database.
        *   **Data Model**: Distributed, document-oriented (Collections -> Documents).
        *   **Querying**: Richer, more powerful queries.
        *   **Scaling**: Scales automatically.
        *   **Use this for**: 99% of new applications.
    2.  **Firebase Realtime Database**: The original legacy product.
        *   **Data Model**: One giant JSON tree.
        *   **Querying**: Very limited (no complex filtering).
        *   **Scaling**: Limited (requires sharding manually if you get too big).
        *   **Use this for**: Simple presence systems (online/offline status) or very low-latency simple syncing.

