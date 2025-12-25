# Professional Cloud Architect - Official Case Studies Deep Dive

This document provides a technical deep dive into the four official case studies for the Google Cloud Professional Cloud Architect (PCA) certification exam. These scenarios are the basis for a significant portion of the exam questions.

---

## 1. EHR Healthcare
**Scenario:** A leading provider of electronic health records (EHR) software.
**Goal:** Migrate from colocation facilities to Google Cloud to improve scalability, reliability, and developer velocity while maintaining strict HIPAA compliance.

### Key Requirements
*   **Business:** Scale to meet exponential growth, reduce operational costs, accelerate feature velocity (CI/CD), and maintain 99.9% availability.
*   **Technical:** Secure connectivity to legacy on-prem systems (insurance providers), centralized observability, container orchestration, and multi-region disaster recovery.
*   **Compliance:** Strict HIPAA compliance and PII protection.

### Solution Architecture
| Role | Recommended Google Cloud Service | Reasoning |
| :--- | :--- | :--- |
| **Compute / App Hosting** | **Google Kubernetes Engine (GKE)** | Existing apps are already containerized. GKE provides managed scaling and helps standardize environments (Dev, Test, Prod). |
| **Hybrid Connectivity** | **Cloud Interconnect** (Partner or Dedicated) | Application needs high availability and low latency access to on-prem legacy systems. Cloud VPN is a backup. |
| **Database (Relational)** | **Cloud SQL (HA)** | Replaces on-prem MySQL/PostgreSQL. HA configuration ensures 99.9% availability across zones. |
| **Database (NoSQL)** | **Memorystore (Redis)** | For caching user sessions to reduce database load. |
| **Storage** | **Cloud Storage** | Archiving medical images and logs. Lifecycle policies can move old data to Coldline/Archive for cost savings. |
| **Observability** | **Cloud Operations Suite** (Cloud Logging & Monitoring) | Requirements state "centralized view" of logs and metrics across all environments. |

### Exam Watchpoints
*   **Legacy Connectivity:** They connect to external insurance providers. If latency is key, choose **Interconnect**. If cost is key and bandwidth low, choose **VPN**.
*   **Compliance:** Questions often ask how to secure PII. Look for **Cloud DLP** (Data Loss Prevention) to de-identify data before analytics.
*   **Anthos:** If the question mentions "consistent management across on-prem and cloud," **Anthos** is the answer.

---

## 2. Helicopter Racing League (HRL)
**Scenario:** A global sports league hosting races.
**Goal:** Migrate to Google Cloud to enhance real-time predictions, global video streaming, and fan engagement.

### Key Requirements
*   **Business:** Increase season-long viewer engagement, expose data APIs to partners, and minimize latency for global fans.
*   **Technical:** Ingest real-time telemetry from race helicopters, process video streams with low latency, and run AI/ML models for race predictions.
*   **Constraint:** "Truck-mounted mobile data centers" at race tracks with limited connectivity.

### Solution Architecture
| Role | Recommended Google Cloud Service | Reasoning |
| :--- | :--- | :--- |
| **Real-time Ingestion** | **Cloud Pub/Sub** | Decouples telemetry ingestion from processing. Handles traffic spikes during races. |
| **Stream Processing** | **Dataflow** | Processes raw telemetry data in real-time (e.g., calculating leaderboards, filtering noise) before writing to storage. |
| **Video Delivery** | **Media CDN** | Specialized CDN for massive media delivery (based on YouTube's infrastructure). Superior to standard Cloud CDN for streaming. |
| **Prediction Models** | **Vertex AI (TensorFlow)** | For training models on historical data and serving real-time predictions during races. |
| **API Management** | **Apigee** | Requirements mention "exposing data to partners" and "monetization." Apigee handles quotas, billing, and security better than API Gateway. |
| **Data Warehouse** | **BigQuery** | For season-long analytics and historical data querying. |

### Exam Watchpoints
*   **Hybrid Connectivity:** The "truck-mounted data centers" imply a need for robust data transfer. **Transfer Appliance** might be used for moving initial bulk video data if bandwidth is poor.
*   **Latency:** Global video delivery *always* maps to **Cloud CDN** and **Global Load Balancing**.
*   **ML Predictions:** If they need to predict race outcomes in real-time, the model must be served via **Vertex AI Prediction** endpoints.

---

## 3. Mountkirk Games
**Scenario:** A mobile game developer with a hit game "Retro-FPS".
**Goal:** Handle massive, unpredictable global traffic spikes for a new multiplayer game.

### Key Requirements
*   **Business:** "Global footprint," "time-to-market," and handling rapid uptake of users.
*   **Technical:** Real-time global leaderboard, low latency multiplayer, and ability to handle scaling down after peak times (cost optimization).
*   **Data:** Store player profiles and game telemetry.

### Solution Architecture
| Role | Recommended Google Cloud Service | Reasoning |
| :--- | :--- | :--- |
| **Compute Game Server** | **GKE** with **Agones** | GKE is ideal for stateless game servers. **Agones** is the standard open-source K8s game server orchestrator (Exam Keyword). |
| **Global Leaderboard** | **Cloud Memorystore (Redis)** | For sub-millisecond, real-time leaderboard updates. *Note: Use Cloud Spanner if "globally strong consistency" is strictly required, but Redis is standard for gaming speed.* |
| **Database (Transactional)** | **Cloud Spanner** | The specific need for a "global" database scaling to millions of users often points to Spanner over Cloud SQL. |
| **Telemetry Analysis** | **BigQuery** | Ingesting massive amounts of game event logs for analytics (e.g., "Why do players quit level 3?"). |
| **Traffic Routing** | **Global HTTP(S) Load Balancer** | Single Anycast IP to route players to the nearest region. |

### Exam Watchpoints
*   **Why not Cloud SQL?** Cloud SQL is regional. Mountkirk needs a *global* database backend, which favors **Cloud Spanner**.
*   **Rapid Scaling:** Questions often focus on how to handle the "launch day" spike. The answer often involves **pre-warming** load balancers (though now largely automatic) or aggressive **GKE Autoscaling** policies.
*   **NoSQL:** **Firestore** is also a valid choice for player profiles and game state if Spanner is overkill, but Spanner is the classic "Architect" choice for global scale.

---

## 4. TerramEarth
**Scenario:** A heavy industrial manufacturer (mining/agriculture tractors).
**Goal:** Transformation from selling hardware to selling "equipment-as-a-service" using IoT data.

### Key Requirements
*   **Business:** Minimize vehicle downtime (predictive maintenance) and optimize dealer logistics.
*   **Technical:** Two types of vehicles: Connected (cellular) sending real-time data, and Unconnected (no signal) uploading batch data daily via FTP.
*   **Data Volume:** Massive. 2 million vehicles. 9TB/day (connected) + varying batch uploads.

### Solution Architecture
| Role | Recommended Google Cloud Service | Reasoning |
| :--- | :--- | :--- |
| **IoT Ingestion** | **Pub/Sub** (formerly IoT Core) | Ingests the stream from the 200k connected vehicles. |
| **Batch Ingestion** | **Cloud Storage** + **Transfer Service** | For the unplugged vehicles uploading data files daily via FTP/HTTP. |
| **Processing** | **Dataflow** | The "Golden Hammer" for processing both *Streaming* (connected vehicles) and *Batch* (unconnected vehicles) data pipelines using the same code presence. |
| **Analytics/Warehousing** | **BigQuery** | Storing petabytes of sensor data. Partitioned tables (by date/vehicle ID) are critical here for performance. |
| **API Strategy** | **Apigee** | Managing access for dealers and 3rd party developers to build apps on top of the vehicle data. |

### Exam Watchpoints
*   **Dealer API:** Whenever "external partners" or "dealers" need API access, **Apigee** is the answer.
*   **Legacy FTP:** How to handle the text files from unconnected vehicles? Upload to **Cloud Storage** -> Trigger **Cloud Functions** or **Dataflow** to process.
*   **Schema Schema:** TerramEarth has evolving data schemas. **BigQuery** handles schema updates well, or Dataflow can transform data before load.
