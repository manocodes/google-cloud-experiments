# GCP Operations PCA Practice Questions

This document contains exam-style questions focused on Google Cloud operations, infrastructure management, CI/CD, and reliability, designed to test concepts for the Professional Cloud Architect exam.

---

## Question 1: Infrastructure as Code Rollout
**Scenario:** You need to roll out a standardized GKE cluster configuration across 20 projects with consistent node pools and add-ons. You want auditable, version-controlled definitions with minimal manual steps.

**Options:**
*   A. Use Cloud Deployment Manager templates
*   B. Use Terraform modules applied via a CI/CD pipeline
*   C. Manually create clusters through Cloud Console guided by runbooks
*   D. Execute gcloud commands from Cloud Shell for each project

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Terraform modules:** Provide reusable, version-controlled infrastructure definitions that work seamlessly with CI/CD pipelines, making them ideal for multi-project rollout with full auditability.

**Why others are wrong:**
*   **A:** Cloud Deployment Manager is less commonly used now; Terraform is the industry-standard recommendation for infrastructure as code.
*   **C:** Manual creation via Console does not provide version control or auditability and doesn't scale across 20 projects.
*   **D:** Shell scripts lack the declarative benefits and state management that Terraform provides.
</details>

---

## Question 2: Ephemeral Environment Cleanup
**Scenario:** A team provisions many short-lived test environments in separate projects. They want to avoid orphaned resources and ensure environments auto-clean after 48 hours without manual intervention.

**Options:**
*   A. Use labels and a scheduled script that deletes resources older than 48 hours
*   B. Use project-level deletion scheduled via an internal tool at 48 hours
*   C. Rely on budget alerts to detect unused resources
*   D. Use sustained use discounts to minimize cost

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Project-level deletion:** Creating one project per ephemeral environment and deleting the entire project ensures ALL resources are cleaned up automatically. This aligns with resource hierarchy best practices and simplifies cleanup logic.

**Why others are wrong:**
*   **A:** Label-based cleanup is more complex and error-prone; you risk missing resources without proper labels.
*   **C:** Budget alerts notify but don't enforce deletion.
*   **D:** Sustained use discounts reduce cost but don't clean up resources.
</details>

---

## Question 3: Project Creation Governance
**Scenario:** You want to restrict who can create new projects to maintain governance, but still allow product teams to manage IAM and resources within their own projects.

**Options:**
*   A. Grant Project Creator to all engineers at the organization level
*   B. Grant Project Creator to a small central platform team and delegate Folder Admin and Project IAM roles to product leads
*   C. Give Organization Admin to product leads
*   D. Grant Owner on all existing projects to engineers so they can create new ones

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Separation of duties:** Limiting project creation to a central team while delegating folder and project-level permissions to product leads respects the principle of least privilege and uses the resource hierarchy correctly.

**Why others are wrong:**
*   **A:** Broad Project Creator access undermines governance and creates sprawl.
*   **C:** Organization Admin is far too powerful and violates least privilege.
*   **D:** Project Owner doesn't grant the ability to create new projects; that requires Project Creator at the folder/org level.
</details>

---

## Question 4: Automated Security Baselines
**Scenario:** A team wants to automatically apply security baselines (organization policies, logging sinks, mandatory services) to all new projects under a folder without manual intervention.

**Options:**
*   A. A Cloud Function triggered by Cloud Audit Logs when a new project is created, applying the baseline via APIs
*   B. Manual checklist executed by platform engineers
*   C. Per-project startup script on Compute Engine
*   D. Labels on resources to indicate compliance

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: A**

**Why:**
*   **Event-driven automation:** Using Cloud Audit Logs to detect project creation and triggering a Cloud Function to apply baselines ensures consistent, timely application with minimal manual intervention. This aligns with infrastructure-as-code and governance patterns.

**Why others are wrong:**
*   **B:** Manual checklists don't scale and are prone to human error.
*   **C:** Compute Engine startup scripts only apply to VMs, not project-level configurations.
*   **D:** Labels are metadata; they don't enforce configurations.
</details>

---

## Question 5: CI/CD Pipeline Implementation
**Scenario:** Developers currently deploy directly to production using `gcloud` from their laptops. Outages occur due to unreviewed changes. You need to improve this process.

**Options:**
*   A. Require developers to log deployments in a shared spreadsheet
*   B. Implement a CI/CD pipeline (e.g., Cloud Build + GitHub) with approvals and deploy from the pipeline only
*   C. Allow only senior developers to run `gcloud` in production
*   D. Require VPN but keep the same process

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **CI/CD pipeline:** Centralizes deployment, adds code review and approval gates, provides auditability, and reduces human error. This aligns with PCA expectations for process optimization and governance.

**Why others are wrong:**
*   **A:** Spreadsheets provide logging but don't prevent bad deployments.
*   **C:** Restricting to "senior" developers doesn't fundamentally fix the process; even experienced developers make mistakes.
*   **D:** VPN adds network security but doesn't address the core problem of unreviewed changes.
</details>

---

## Question 6: SLO Monitoring and Alerting
**Scenario:** An operations team wants proactive alerts when an API latency SLO is violated and post-incident reports with clear indicators of service health.

**Options:**
*   A. Only log errors and manually check logs weekly
*   B. Use Cloud Monitoring SLOs, alerting policies on SLI metrics, and dashboards plus incident reports
*   C. Use Stackdriver Debugger only
*   D. Rely on Cloud Audit Logs

<details>
<summary>Click to reveal Answer</summary>

**Correct Answer: B**

**Why:**
*   **Cloud Monitoring SLOs:** Enable defining and monitoring error budgets with alerting when thresholds are breached. Dashboards and incident management support post-incident analysis and continuous improvement.

**Why others are wrong:**
*   **A:** Manual log review is reactive and doesn't provide proactive alerting.
*   **C:** Debugger is for code-level debugging, not operational monitoring.
*   **D:** Audit Logs track who did what, not service performance metrics.
</details>
