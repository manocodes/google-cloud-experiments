# Google Cloud Functions Study Guide (PCA Exam)

## 1. Overview
Google Cloud Functions (GCF) is a **Function-as-a-Service (FaaS)** offering. It is fully serverless, meaning you only provide code, and Google handles the underlying infrastructure, scaling, and security.

### Key Characteristics
- **Event-driven**: Executes in response to events (e.g., file upload, message in a queue).
- **Stateless**: Functions should not store state locally as the environment can be recycled.
- **Automatic Scaling**: Scales from zero to thousands of instances and back to zero.
- **Pay-per-use**: Billed only for the duration of execution and resources consumed.

---

## 2. Generations: 1st Gen vs. 2nd Gen
The PCA exam frequently tests the transition between generations. **2nd Gen** is built on top of **Cloud Run** and **Eventarc**, offering more features.

| Feature | 1st Generation | 2nd Generation |
| :--- | :--- | :--- |
| **Max Request Time** | HTTP: 9 mins, Event: 9 mins | HTTP: 60 mins, Event: 9 mins |
| **Max Instance Size** | 8 GB RAM, 2 vCPUs | 32 GB RAM, 8 vCPUs |
| **Concurrency** | 1 request per instance | Up to 1000 requests per instance |
| **Traffic Splitting** | Not natively supported | Supported (via Cloud Run integration) |
| **Underlying Tech** | Proprietary | Cloud Run + Eventarc |

---

## 3. Triggers and Events
Functions are triggered by events. For PCA, know which service triggers what.

### HTTP Triggers
- Standard RESTful API calls.
- Provides a URL to invoke the function.

### Event-driven Triggers (Pub/Sub & Storage)
- **Pub/Sub**: Triggered when a message is published to a specific topic.
- **Cloud Storage**: Triggered on object creation, deletion, or metadata update (Finalize, Delete, Archive, Metadata Update).
- **Firestore/Firebase**: Triggered by database changes.

### Eventarc (2nd Gen)
- Allows triggering functions from **over 90+ Google Cloud sources** and custom sources via Pub/Sub.

---

## 4. Resource Management & Networking
### Performance & Scaling
- **Cold Starts**: The delay when a function starts from zero instances. 
  - *Mitigation*: Use **Min instances** to keep warm instances ready.
- **Max instances**: Limit scaling to prevent overwhelming downstream databases or controlling costs.

### Networking
- **Ingress**: Control who can call the function (e.g., Internal only vs. Allow all).
- **Egress**: To access resources in a VPC (like a Cloud SQL private IP or a GCE VM), you **must** use a **Serverless VPC Access Connector**.

---

## 5. Security (Identity & Access Management)
- **Service Account**: Each function runs as a service account. By default, it's the `App Engine default service account`, but for PCA, you should **always use a dedicated, least-privileged service account**.
- **Roles**:
  - `roles/cloudfunctions.invoker`: Required to call the function.
  - `roles/cloudfunctions.developer`: Required to create/edit functions.
- **Secrets Management**:
  - **Do NOT** store API keys in environment variables (they are visible in the console/logs).
  - **Use Secret Manager**: Mount secrets as environment variables or volumes securely. Key exam pattern.

---

## 6. PCA Decision Matrix: Why Choose Cloud Functions?
Compare with other compute options:

- **VS. Cloud Run**: Use Cloud Run if you need a container, longer timeouts, or specific libraries not in GCF runtimes. Use GCF for simple, single-purpose snippets or native Eventarc integration.
- **VS. App Engine**: Use App Engine for full web applications with multiple routes and stateful sessions. Use GCF for backend tasks triggered by events.
- **VS. Compute Engine**: Use GCE only if you need OS-level control or legacy software that cannot be containerized.

---

## 8. Knative & Portability (The "Trigger" Word)
Knative is the open-source foundation for Cloud Run (and thus GCF 2nd Gen).

### Why it matters for PCA:
- **Anthos/Hybrid**: If you need "Cloud Run" on-premises, you are running Knative on GKE Enterprise (Anthos).
- **Portability**: Because GCF 2nd Gen and Cloud Run follow the Knative spec, you can move your workloads to any Kubernetes cluster running Knative with minimal changes.
- **Scale-to-Zero**: Knative is what allows Kubernetes-based workloads to scale to zero when idle.

---

## 9. Common Exam Scenarios
1. **Scenario**: You need to resize images uploaded to GCS.
   - **Answer**: Use a Cloud Function triggered by `google.storage.object.finalize`.
2. **Scenario**: You want to process millions of messages from a queue with minimal latency.
   - **Answer**: Use Cloud Functions with Pub/Sub triggers and set **Min instances** to avoid cold starts.
3. **Scenario**: A function needs to access a private Cloud SQL instance.
   - **Answer**: Configure a **Serverless VPC Access Connector**.
