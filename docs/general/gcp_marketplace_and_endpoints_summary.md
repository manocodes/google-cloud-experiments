# Google Cloud: Marketplace, Endpoints & Apigee Summary

This document summarizes the key concepts discussed regarding Google Cloud Marketplace, API management with Endpoints, and the transition to Apigee.

## 1. Google Cloud Marketplace vs. Workspace

There are two distinct marketplaces:

### Google Cloud Marketplace
*   **Target Audience**: Developers, DevOps, IT Ops.
*   **Purpose**: To find and deploy software *on* the Google Cloud Platform infrastructure.
*   **Key Use Cases**:
    *   **Click-to-Deploy VMs**: Launch credentials-ready stacks (e.g., LAMP, Deep Learning VM with NVIDIA drivers) in minutes, avoiding manual configuration ("Driver Hell").
    *   **Managed Services (SaaS)**: Subscribe to third-party services like **MongoDB Atlas** or **Redis Enterprise**. The vendor manages the infrastructure (backups, patches), while users manage the data.
    *   **Security Appliances**: Deploy virtual firewalls (e.g., Palo Alto Networks) into your VPC.
*   **Benefits**: Speed (pre-configured), Consolidated Billing (one GCP invoice), and Vetted Security.

### Google Workspace Marketplace
*   **Target Audience**: End-users of Office tools.
*   **Purpose**: Add-ons for Gmail, Docs, Sheets (e.g., DocuSign for Gmail).

---

## 2. Google Cloud Endpoints (Serverless API Management)

**Endpoints** acts as a "Reception Desk" or "Doorman" for your APIs. It is not the server running the code, but a gateway that sits in front of it.

### Core Functions
*   **Authentication**: Verifies user identity (Firebase, Auth0, etc.).
*   **Monitoring**: Logs requests and errors.
*   **Quotas**: Prevents abuse by limiting calls per user.
*   **Protocol**: Handles transcoding (HTTP/JSON to gRPC).

### The "Facade Pattern"
Endpoints allows you to hide multiple backend resources behind a single public URL (e.g., `api.myapp.com`).
*   `GET /users` -> Routes to **Cloud Run**.
*   `POST /process` -> Routes to **Cloud Functions**.
*   `GET /legacy` -> Routes to **App Engine**.
*   **Benefit**: Users see one unified API, while you can mix, match, and refactor backends invisibly.

---

## 3. Apigee vs. Endpoints

Both offer API Management, but they serve different scales and business goals.

| Feature | Google Cloud Endpoints | Apigee |
| :--- | :--- | :--- |
| **Analogy** | **Office Receptionist** | **International Airport** |
| **Primary Goal** | Protect & Monitor APIs. | **Monetize** & Manage APIs as Products. |
| **Target User** | Internal Developers / Microservices. | Enterprises selling to Partners/Public. |
| **Key Features** | Auth, Quotas, Logging. | Billing/Monetization, Developer Portals, Advanced Analytics, Legacy Transformation. |
| **Cost** | Pay-as-you-go (Low/Free tier). | Enterprise Pricing (High). |

### The Evolution Path
A common growth strategy for APIs:
1.  **Stage 1 (Internal)**: Direct calls to a microservice.
2.  **Stage 2 (Public Protocol)**: Add **Endpoints** to secure it, handle auth, and protect against spam (Quotas).
3.  **Stage 3 (Product)**: As demand grows, place **Apigee** in front (or replace Endpoints) to handle billing ("Gold Tier" plans), partner onboarding, and advanced business logic.
