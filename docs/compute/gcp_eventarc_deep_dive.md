# Eventarc Deep Dive (PCA Exam)

## 1. What is Eventarc?
Eventarc is a fully managed service that lets you route events from Google Cloud services, SaaS, and your own apps to diverse destinations. It standardizes event delivery using the **CloudEvents** format.

## 2. Key Concepts
- **Triggers**: Filters that define which events to capture (e.g., "Any file deleted in bucket X").
- **Providers**: The source of the event (Cloud Storage, Pub/Sub, Cloud Audit Logs, etc.).
- **Destinations**: Where the event is sent (Cloud Functions 2nd Gen, Cloud Run, GKE, Workflows).
- **Transport**: Most events use **Pub/Sub** as the underlying transport layer, but this is managed for you.

## 3. The "Swiss Army Knife": Cloud Audit Logs
One of the most powerful features for the PCA exam is using **Cloud Audit Logs as an event source**.
- This allows you to trigger actions based on **administrative changes** (e.g., a new VM is created, a Firewall rule is modified).
- It turns "logs" into "actions."

## 4. PCA Comparison: Eventarc vs. Pub/Sub
| Feature | Eventarc | Pub/Sub |
| :--- | :--- | :--- |
| **Purpose** | Event Routing & Filtering | Message Queuing & Delivery |
| **Standard** | CloudEvents (standardized) | Arbitrary data (raw bytes) |
| **Philosophy** | "Something happened" (Event-driven) | "Please do this" or "Here is data" |
| **Sources** | 90+ GCP Services natively | Manual integration required |

## 5. Exam Tips
- Whenever you see **"respond to changes in [GCP Service X] that doesn't have a native trigger,"** the answer is likely **Eventarc via Audit Logs**.
- Eventarc is the backbone of **Cloud Functions 2nd Gen**.
- Use Eventarc to trigger **Workflows** for complex, multi-step orchestration.
