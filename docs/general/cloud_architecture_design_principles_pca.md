# Cloud Architecture Design Principles for PCA

This guide covers the **design principles and patterns** that the PCA exam tests. Understanding these helps you make the right architectural decisions.

---

## 1. The 12-Factor App Methodology

The **12-Factor App** is a methodology for building cloud-native applications. **Expect 1-3 questions** on the exam testing whether you know how Google Cloud implements these principles.

### Factor I: Codebase
**Principle**: One codebase tracked in version control, many deploys.

**Google Cloud Implementation**:
- **Cloud Source Repositories**: Git hosting.
- **Cloud Build**: CI/CD from single repo → multiple environments (dev/staging/prod).

### Factor II: Dependencies
**Principle**: Explicitly declare and isolate dependencies.

**Google Cloud Implementation**:
- **Containers**: Docker images bundle all dependencies.
- **Cloud Build**: `requirements.txt` (Python), `package.json` (Node.js) → reproducible builds.

### Factor III: Config ✅ **HIGH PRIORITY**
**Principle**: Store config in the **environment**, not in code.

**Google Cloud Implementation**:
- **Secret Manager**: Secrets (API keys, passwords).
- **Runtime Configurator / Firestore**: Non-secret config.
- **Environment Variables**: In Cloud Run, Cloud Functions, GKE.

**Exam Trap**: Never hardcode credentials in code. Never store them in Git.

### Factor IV: Backing Services
**Principle**: Treat databases, queues, caches as **attached resources** (swap them via URL change).

**Google Cloud Implementation**:
- Databases: Cloud SQL, Spanner, Firestore (accessed via connection string).
- Message Queue: Pub/Sub.
- Cache: Memorystore.

### Factor V: Build, Release, Run
**Principle**: Strictly separate build and run stages.

**Google Cloud Implementation**:
- **Build**: Cloud Build creates container image.
- **Release**: Push image to Artifact Registry, tag with version.
- **Run**: Deploy to Cloud Run / GKE.

### Factor VI: Processes ✅ **HIGH PRIORITY**
**Principle**: Execute the app as **stateless processes**. Store state in backing services, not in memory.

**Google Cloud Implementation**:
- **Cloud Run**: Stateless by design. Instances can be killed anytime.
- **Cloud Functions**: Stateless by design.
- **GKE**: Design pods to be stateless (use Persistent Volumes for state).

**Exam Question Pattern**: "An app stores user sessions in memory. What's wrong?"  
**Answer**: Violates Factor VI. Use **Memorystore (Redis)** for sessions.

### Factor VII: Port Binding
**Principle**: Export services via port binding (self-contained).

**Google Cloud Implementation**:
- Cloud Run listens on `PORT` environment variable (e.g., 8080).
- GKE services expose ports.

### Factor VIII: Concurrency
**Principle**: Scale out via the process model (horizontal scaling).

**Google Cloud Implementation**:
- **Cloud Run**: Automatically scales instances based on traffic.
- **GKE Autoscaling**: Horizontal Pod Autoscaler (HPA).

### Factor IX: Disposability ✅ **HIGH PRIORITY**
**Principle**: Maximize robustness with **fast startup and graceful shutdown**.

**Google Cloud Implementation**:
- **Cloud Run**: Starts in < 1 second (container image cached).
- **GKE**: Kubernetes handles SIGTERM for graceful shutdown.

**Exam Trap**: Apps that take 5 minutes to start are bad for autoscaling.

### Factor X: Dev/Prod Parity
**Principle**: Keep development, staging, and production as similar as possible.

**Google Cloud Implementation**:
- Use same services in all envs (dev uses Cloud SQL, prod uses Cloud SQL).
- **Infrastructure as Code**: Terraform/Deployment Manager for reproducibility.

### Factor XI: Logs ✅ **HIGH PRIORITY**
**Principle**: Treat logs as **event streams**. Write to `stdout`, not to files.

**Google Cloud Implementation**:
- **Cloud Logging**: Automatically captures stdout from Cloud Run, GKE, Cloud Functions.
- **Log Router**: Routes logs to BigQuery, Cloud Storage, Pub/Sub.

**Exam Pattern**: "How to centralize logs from 100 microservices?"  
**Answer**: Write to `stdout`, Cloud Logging aggregates automatically.

### Factor XII: Admin Processes
**Principle**: Run admin tasks (migrations, one-off scripts) as one-off processes.

**Google Cloud Implementation**:
- **Cloud Run Jobs**: Run one-off tasks (e.g., database migration).
- **GKE Jobs / CronJobs**: Kubernetes native.

---

## 2. Google Cloud Well-Architected Framework

Google's version of best practices, organized into **pillars**.

### Pillar 1: Operational Excellence
**Goal**: Run and monitor systems to deliver business value.

**Key Practices**:
- **Monitoring**: Cloud Monitoring (metrics), Cloud Logging (logs), Error Reporting.
- **CI/CD**: Cloud Build, Artifact Registry.
- **IaC**: Terraform, Deployment Manager.

**Exam Pattern**: "How to detect performance degradation?"  
**Answer**: Set up **Cloud Monitoring alerts** on latency SLIs.

### Pillar 2: Security
**Goal**: Protect data and systems.

**Key Practices**:
- **IAM**: Least privilege, service accounts, Workload Identity Federation.
- **Encryption**: Data at rest (CMEK), data in transit (TLS).
- **Network Security**: VPC Service Controls, Cloud Armor, Binary Authorization.

**Exam Pattern**: "Prevent data exfiltration from BigQuery?"  
**Answer**: **VPC Service Controls** (creates security perimeter).

### Pillar 3: Reliability
**Goal**: System performs intended function correctly and consistently.

**Key Practices**:
- **High Availability**: Multi-zone (Cloud SQL HA), Multi-region (Spanner).
- **Disaster Recovery**: Regular backups, cross-region replication.
- **Fault Tolerance**: Retry logic, circuit breakers, graceful degradation.

**Exam Pattern**: "Ensure database survives zone failure?"  
**Answer**: Enable **Cloud SQL HA** (synchronous standby in different zone).

### Pillar 4: Performance Efficiency
**Goal**: Use resources efficiently to meet requirements.

**Key Practices**:
- **Right-Sizing**: Committed Use Discounts, Sustained Use Discounts.
- **Caching**: CDN (Cloud CDN), Memorystore.
- **Autoscaling**: Cloud Run, GKE HPA/VPA.

**Exam Pattern**: "Reduce latency for global users accessing static content?"  
**Answer**: **Cloud CDN** (cache at edge locations).

### Pillar 5: Cost Optimization
**Goal**: Avoid unnecessary costs.

**Key Practices**:
- **Preemptible/Spot VMs**: 60-91% discount for fault-tolerant workloads.
- **Lifecycle Policies**: Move Cloud Storage objects to Nearline/Coldline.
- **BigQuery**: Partition tables, select only needed columns.

**Exam Pattern**: "Reduce cost for batch processing?"  
**Answer**: Use **Preemptible VMs** (can be interrupted, but dirt cheap).

---

## 3. SRE Principles (SLI, SLO, SLA)

**Site Reliability Engineering (SRE)** is Google's approach to operations. The PCA exam tests your understanding of reliability metrics.

### SLI (Service Level Indicator)
**Definition**: A **quantifiable measure** of service behavior.

**Examples**:
- Latency: "99th percentile response time < 100ms"
- Availability: "Percentage of successful HTTP 200 responses"
- Throughput: "Requests per second handled"

**Google Cloud Tools**: Cloud Monitoring (custom metrics).

### SLO (Service Level Objective)
**Definition**: The **target** for an SLI. "We aim for 99.9% availability."

**Example**:
- SLI: HTTP 200 response rate
- SLO: 99.9% of requests return HTTP 200 (over 30 days)

**Implication**: 0.1% can fail. That's your **error budget**.

### SLA (Service Level Agreement)
**Definition**: A **contract** with penalties if SLO is not met.

**Example**:
- BigQuery SLA: 99.99% monthly uptime.
- If violated, Google issues service credits.

**Google Cloud SLAs**: Each service publishes SLA (e.g., Spanner Multi-Region = 99.999%).

### Error Budget
**Definition**: The amount of downtime you can afford before violating SLO.

**Example**:
- SLO: 99.9% availability.
- Error Budget: 0.1% downtime = **43 minutes/month**.

**Philosophy**: If error budget is exhausted, stop new features and fix reliability.

---

## 4. Microservices Design Patterns

### Pattern 1: API Gateway
**Problem**: Clients don't want to call 20 different microservices.

**Solution**: Single entry point that routes to backends.

**Google Cloud Implementation**:
- **Cloud Endpoints**: API management for REST/gRPC.
- **Apigee**: Enterprise API management (rate limiting, analytics).

### Pattern 2: Service Mesh
**Problem**: Service-to-service communication is complex (retries, circuit breakers, observability).

**Solution**: Sidecar proxy handles all communication logic.

**Google Cloud Implementation**:
- **Istio on GKE**: Traffic management, security, observability.
- **Cloud Service Mesh**: Managed Istio.

### Pattern 3: Event-Driven Architecture
**Problem**: Tight coupling between services.

**Solution**: Services communicate via events (async, decoupled).

**Google Cloud Implementation**:
- **Pub/Sub**: Publish events to topics, subscribers process them.

**Exam Pattern**: "Decouple order service from inventory service?"  
**Answer**: Order service publishes "OrderPlaced" event to **Pub/Sub**. Inventory service subscribes and updates stock.

### Pattern 4: Strangler Fig (Legacy Migration)
**Problem**: Can't rewrite entire monolith at once.

**Solution**: Gradually replace pieces of the monolith with microservices.

**Google Cloud Implementation**:
- **Cloud Load Balancer**: Route `/api/v1/*` to legacy app, `/api/v2/*` to new microservice.
- **Apigee**: Route based on headers/paths.

---

## 5. Cloud-Native Principles Summary

| Principle | What It Means | Google Cloud Service |
| :--- | :--- | :--- |
| **Stateless** | Don't store state in app instances | Cloud Run, Cloud Functions |
| **Immutable Infrastructure** | Don't patch servers, replace them | Containers, GKE |
| **Declarative Config** | Describe desired state, system converges to it | Kubernetes YAML, Terraform |
| **Ephemeral Compute** | Instances come and go | Cloud Run (scales to zero) |
| **Cattle, not Pets** | Treat instances as replaceable, not unique | Managed Instance Groups |

---

## 6. Exam Decision Framework

### Question: "App stores user sessions in memory. Users lose sessions when app restarts. Fix this."
**12-Factor Violation**: Factor VI (Processes - stateless).  
**Answer**: Store sessions in **Memorystore (Redis)** or **Firestore**.

### Question: "How to ensure database credentials are not in Git?"
**12-Factor Violation**: Factor III (Config).  
**Answer**: Store in **Secret Manager**, inject via environment variables.

### Question: "App takes 10 minutes to start. Autoscaling doesn't work well."
**12-Factor Violation**: Factor IX (Disposability).  
**Answer**: Optimize startup (use lighter base image, cache dependencies).

### Question: "Need to ensure 99.95% uptime for web app. What do you do?"
**SRE Question**: Define SLI, SLO, implement HA.  
**Answer**: 
1. Set SLI (e.g., HTTP 200 rate).
2. Set SLO (99.95%).
3. Deploy to **multiple zones** (GKE multi-zone cluster or Cloud Run in multiple regions).
4. Monitor with **Cloud Monitoring**, alert if SLO at risk.

---

## 7. Common Exam Traps

### Trap 1: "Storing Secrets in Environment Variables"
**Looks Right**: 12-Factor says "config in environment."  
**Actually Wrong**: Secrets should be in **Secret Manager**, not plain environment variables (which are logged).

### Trap 2: "Pets, Not Cattle"
**Scenario**: "SSH into the server to manually fix an issue."  
**Why Wrong**: Violates immutability. Should replace the instance, not patch it.

### Trap 3: "Skipping Dev/Prod Parity"
**Scenario**: "Dev uses SQLite, Prod uses Cloud SQL."  
**Why Wrong**: Violates Factor X. Use Cloud SQL in both (or at least Postgres locally).

---

## Summary for the Exam

- **12-Factor App**: Know Factors III (Config), VI (Stateless), IX (Disposability), XI (Logs).
- **Well-Architected**: Understand the 5 pillars (Ops, Security, Reliability, Performance, Cost).
- **SRE**: Know the difference between SLI (metric), SLO (target), SLA (contract).
- **Microservices**: API Gateway, Service Mesh (Istio), Event-Driven (Pub/Sub).

**Exam Tip**: When you see "violates best practices," think 12-Factor App or Well-Architected Framework.
