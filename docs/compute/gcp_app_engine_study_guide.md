# Google App Engine (GAE) Study Guide

Google App Engine is a **Platform-as-a-Service (PaaS)** that allows developers to build and deploy applications without managing the underlying infrastructure. For the PCA exam, it is the classic "Serverless" compute option for web applications.

## 1. Core Concepts
*   **Fully Managed**: No OS to patch, no servers to scale manually.
*   **Code-First**: You focus on the code; Google handles the rest.
*   **Traffic Splitting**: Easily move traffic between versions (Canary deployments, A/B testing).
*   **The Singleton Rule**: You can only have **exactly one** App Engine application per GCP Project.
    *   **Constraint**: Once created, you **cannot** change the region.
    *   **Multi-Region**: If you need a second App Engine app in a different region, you **must create a new GCP Project**.
*   **Services**: To run multiple components (e.g., Frontend and Backend) in one project, use multiple **Services** within the single application.
    *   **How to add**: Create a new folder with its own `app.yaml`.
    *   **Key setting**: The `app.yaml` MUST contain `service: [name]`.
    *   **The Default Rule**: Every app must have a service named `default` before other services can be added.

### The "Sandbox" (Standard Environment Only)
To achieve "Scale to Zero" and sub-second startup, GAE Standard uses a restricted sandbox:
*   **No Disk Writes**: You cannot write to the local file system (except `/tmp`). You must use **Cloud Storage** for files.
*   **No OS Access**: You cannot SSH into the instance or install OS-level packages.
*   **White-listed Libraries**: Only specific runtimes and libraries are supported.
*   **Request Timeouts**: Typically 60 seconds (HTTP) up to 10 minutes (Task Queues).
*   **Strictly Stateless**: Instances are ephemeral. Local storage (`/tmp`) is wiped on restart. You **cannot** attach Persistent Disks.

---

## 2. Standard vs. Flexible Environment
This is the **most tested** comparison for GAE.

| Feature | **Standard Environment** | **Flexible Environment** |
| :--- | :--- | :--- |
| **Underlying Tech** | **Proprietary Sandbox** (Not GCE). | **Compute Engine VMs** (Managed GCE). |
| **Startup Time** | Seconds (fast). | Minutes (slow). |
| **Scaling** | Scales to **Zero**. | Scales to **Minimum 1 instance**. |
| **Runtime** | Specific versions (Python, Java, Node, etc.). | Any language (runs in a Docker container). |
| **Custom Libraries** | No (restricted to runtime). | Yes (full control over the container). |
| **VPC Access** | Via Serverless VPC Access connector. | Native access to VPC via Compute Engine. |
| **Price** | Pay-per-request (mostly). | Pay for provisioned VM resources. |
| **Best For** | Spiky traffic, cost-to-zero, fast startup. | Consistent traffic, custom OS dependencies. |

### Custom Runtimes (The "Flex" Superpower)
In GAE Flexible, you use a **Custom Runtime** by providing a `Dockerfile`.
*   **Configuration**: You can `RUN apt-get install` anything.
*   **Binaries**: You can run C++, Haskell, or even proprietary COBOL binaries if they fit in a container.
*   **Resource Control**: Explicitly set CPU/RAM in `app.yaml`.
*   **Note**: While you control the container, Google still manages the **Host OS** security patches.

---

## 3. Key Architectural Features
*   **Traffic Splitting**: Use the Console or `gcloud` to split traffic based on IP address or Cookies (useful for A/B testing).
*   **Versions**: You can have multiple versions of a service running. Turning off a version doesn't delete it, but it stops billing for its instances.

### 3.1 Security & Networking
*   **Public URL**: By default, every app gets a public `*.appspot.com` URL.
*   **Identity-Aware Proxy (IAP)**: The primary way to restrict access to specific IAM users/groups without a VPN.
*   **Ingress Settings**: You can set an app to "Internal Only" so it only accepts traffic from your VPC or a Load Balancer.

### 3.2 URL Routing & Targeting
App Engine URLs follow a strict hierarchy that allows you to target specific layers:
*   **Project Level**: `https://[PROJECT_ID].appspot.com` (Goes to the `default` service).
*   **Service Level**: `https://[SERVICE]-dot-[PROJECT_ID].appspot.com`.
*   **Version Level**: `https://[VERSION]-dot-[SERVICE]-dot-[PROJECT_ID].appspot.com` (Crucial for testing a new version before shifting traffic).

---

## 4. Database & Storage Integrations
App Engine is stateless, so it **must** offload data to external services.

### 4.1 Recommended Databases
*   **Firestore (Datastore Mode)**: The "Native" NoSQL choice. Best for seamless integration and massive scaling.
*   **Cloud SQL**: The standard choice for relational data (MySQL/Postgres). Requires a **Serverless VPC Access Connector** to connect to private IPs from GAE Standard.
*   **Cloud Spanner**: Use only for massive, global, distributed transactional needs.

### 4.2 Storage & Caching
*   **Cloud Storage (GCS)**: The only way to store files/blobs. GAE local disk is read-only (except `/tmp`).
*   **Cloud Memorystore (Redis)**: Used for low-latency session state or caching. Also requires a VPC Access Connector.

---

### Choose GAE Standard IF:
*   You need to **Scale to Zero** to save costs during idle periods.
*   Your application is a standard web app (Python, Java, Go, PHP, Ruby, Node).
*   You want the absolute minimum operational overhead.

### Choose GAE Flexible IF:
*   Your app requires **custom OS libraries** or C-libraries not in the Standard runtime.
*   You need to write to the local file system (though persistent storage should still be external).
*   Your traffic is steady and predictable (making "scale to zero" less valuable).

### Choose Cloud Run INSTEAD of GAE IF:
*   The application is already **containerized** (Docker).
*   You want to use any language/library with "Scale to Zero" capability.
*   (On the modern exam, Cloud Run is often the "newer" preferred answer for stateless containers).

---

## 6. GAE Flexible vs. Cloud Run (The "Container" Confusion)
Both use containers, but their behavior is different:

| Key Difference | App Engine Flexible | Cloud Run |
| :--- | :--- | :--- |
| **Scaling** | Min 1 instance (No Scale-to-Zero). | Scales to **Zero** (Pay $0 when idle). |
| **Startup** | Minutes (Provisions VMs). | Seconds (Knative managed). |
| **Cost** | Fixed per VM hour. | Pay-per-request (Granular). |
| **Use Case** | Legacy apps requiring dedicated VMs. | Modern, portable, stateless containers. |

---

## 7. Tips & Distractors

### ✅ Tips
*   **Zero to Hero**: GAE Standard is the *only* compute option that scales to zero for non-containerized code.
*   **App Engine Regionality**: An App Engine application is **regional**. Once you pick a region for your project, you **cannot change it**.
*   **IAP**: If the question asks how to secure an internal App Engine app without a VPN, the answer is **Identity-Aware Proxy (IAP)**.
*   **Memcache**: GAE has a built-in Memcache (Standard only), but for modern designs, use **Cloud Memorystore (Redis)**.

### ❌ Distractors (Common Wrong Answers)
*   **"Install App Engine on-premises"**: Wrong. GAE is a proprietary Google service. Use **GKE (Anthos)** for hybrid/on-prem serverless.
*   **"Use GAE Standard for long-running batch jobs"**: Wrong. GAE Standard has request timeouts (usually 60 seconds - 10 minutes). Use Compute Engine or Dataflow for long jobs.
*   **"SSH into GAE Standard"**: Impossible. You cannot SSH into Standard instances. You can only debug via logs.
*   **"Update the OS on GAE"**: Wrong. Google manages the OS. If you need OS control, use GCE.

---

## 8. Modern Perspective: App Engine vs. Cloud Run
In modern architecture, **Cloud Run** is generally preferred over App Engine. Here is how they are viewed on the exam:

*   **App Engine (The "Stable" Option)**: Choose this for **legacy code migration** (non-containerized) or when using deeply integrated features like the built-in Task Queues.
*   **Cloud Run (The "Modern" Option)**: Choose this for **all new development**, containerized microservices, and when you need a "Clean" separation from the proprietary App Engine ecosystem.

**If the question mentions "Docker" or "Containerized" and "Serverless" in the same sentence, the answer is almost always Cloud Run.**

---

## 9. Deployment Patterns for the PCA Exam

| Pattern | **Multi-Service (One Project)** | **Multi-Project (Distributed)** |
| :--- | :--- | :--- |
| **Logic** | Multiple services in one App Engine app. | Separate App Engine apps in separate projects. |
| **Region** | Stuck in **One Region**. | Can be in **Different Regions**. |
| **Database** | Native/Shared (Easy). | Cross-Project Shared (Requires IAM). |
| **Best For** | Internal Microservices. | Global High Availability / DR. |
| **Exam Trigger** | "Simplified microservice management." | "Multi-region disaster recovery." |

---

## 10. Traffic Operations
*   **Traffic Migration**: Switches 100% of traffic to a new version.
*   **Traffic Splitting**: Shards traffic between versions (e.g., 90/10).

### 10.1 Splitting Methods (High Yield for PCA)
| Method | Use Case | Mechanic |
| :--- | :--- | :--- |
| **IP Address** | Simple stateless splitting. | Uses a hash of the IP to assign a version. (Multiple users behind a proxy go to the same version). |
| **Cookie** (Sticky) | **A/B Testing / Consistent UX**. | Uses the `GOOGAPPUID` cookie to keep a user on one version. (Managed by Google infrastructure; no code changes required). |
| **Random** | Absolute unbiased testing. | No stickiness. User may switch versions between every request. |

## 11. Custom Routing (`dispatch.yaml`)
By default, services have separate subdomains. Use `dispatch.yaml` to route based on path:
*   Example: `manoyaka.com/api/*` -> routes to `backend-api` service.
*   Example: `manoyaka.com/static/*` -> routes to `default` service.

## 12. Background Tasks & Cron
*   **Cron (`cron.yaml`)**: Built-in scheduler for periodic tasks.
*   **Cloud Tasks (formerly App Engine Task Queues)**: Used for asynchronous processing.
    *   **Push Queues**: App Engine pushes tasks to a worker.
    *   **Pull Queues**: Workers pull tasks from the queue (deprecated in favor of Pub/Sub).

---

## 13. Tips & Distractors

### ✅ Tips
*   **Zero to Hero**: GAE Standard is the *only* compute option that scales to zero for non-containerized code.
*   **App Engine Regionality**: An App Engine application is **regional**. Once you pick a region for your project, you **cannot change it**.
*   **IAP**: If the question asks how to secure an internal App Engine app without a VPN, the answer is **Identity-Aware Proxy (IAP)**.
*   **Memcache**: GAE has a built-in Memcache (Standard only), but for modern designs, use **Cloud Memorystore (Redis)**.

### ❌ Distractors (Common Wrong Answers)
*   **"Install App Engine on-premises"**: Wrong. GAE is a proprietary Google service. Use **GKE (Anthos)** for hybrid/on-prem serverless.
*   **"Use GAE Standard for long-running batch jobs"**: Wrong. GAE Standard has request timeouts (usually 60 seconds - 10 minutes). Use Compute Engine or Dataflow for long jobs.
*   **"SSH into GAE Standard"**: Impossible. You cannot SSH into Standard instances. You can only debug via logs.
*   **"Update the OS on GAE"**: Wrong. Google manages the OS. If you need OS control, use GCE.

---

## 14. Cost Optimization & Cleanup
Architects must manage "Zombie" resources to prevent waste.
*   **Scale to Zero**: GAE Standard does this by default (0 traffic = 0 compute cost).
*   **Disabling an App**: The only way to stop a GAE app without deleting the project. Use `gcloud app update --noserving-status`.
*   **Cleaning Deployment Artifacts**: `gcloud app deploy` leaves code in **Cloud Storage** buckets and images in **Artifact Registry**. These must be manually cleaned to avoid storage costs.
*   **Deleting Versions**: Keep only the necessary versions; delete old ones to save on storage and metadata overhead.
