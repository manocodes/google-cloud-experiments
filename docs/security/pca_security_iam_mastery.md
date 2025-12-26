# PCA Security: IAM Authorization Mastery

Identity and Access Management (IAM) is the backbone of Google Cloud security. This guide covers the *Authorization* aspect (Permission logic), complementing the *Authentication* (ADC) guide.

## 1. The Resource Hierarchy & Policy Inheritance

Policies are attached to resources. The hierarchy flows:
**Organization** -> **Folders** -> **Projects** -> **Resources** (Buckets, VMs).

### The Golden Rule: Union of Permissions
*   **Result:** Permissions are **ADDITIVE**.
*   **Permissions:** You cannot "block" a permission at a lower level that was granted at a higher level using standard Allow policies.
*   **Example:**
    *   User is granted `Storage Admin` at the **Organization** level.
    *   You try to give them only `Storage Viewer` at the **Project** level.
    *   **Effective Permission:** `Storage Admin` (The higher (broader) permission wins).
    *   *Exam Trap:* "How do I restrict a specific user in a sub-project?" -> You **CANNOT** override a parent Allow policy. You must remove the parent policy and re-apply narrower permissions at lower levels.

### Deep Dive: Deny Policies (IAM Deny)
*   Google recently introduced **Deny Policies**.
*   **Logic:** `DENY` overrides `ALLOW`.
*   **Use Case:** "Ensure NO ONE, not even Org Admins, can delete this specific compliance log bucket."
*   **Exam Relevance:** Be careful. Standard IAM is additive. "IAM Deny" is a specific advanced feature for guardrails.

---

## 2. Roles: The Three Types

| Role Type | Description | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Basic (Primitive)** | `Owner`, `Editor`, `Viewer`. Pre-date IAM. | Simple. | **Too broad.** `Editor` can delete almost anything. **Violates Least Privilege.** |
| **Predefined** | Managed by Google (e.g., `Storage Object Viewer`). | granular. Maintained by Google (updated automatically). | Might logically group permissions you don't want combined. |
| **Custom** | You pick specific permissions (e.g., `storage.buckets.get`). | **Perfect Least Privilege.** | **High Maintenance.** If Google adds a new beta feature, your role won't have the permission until you update it manually. |

*   *Exam Tip:* Always prefer **Predefined Roles** for operational ease unless strictly required to use **Custom Roles** for compliance/least privilege. **Never** use Basic roles in production.

---

## 3. IAM Conditions (Conditional Access)

You can add a "Condition" to a Role Binding. The role is only active if the condition is TRUE.

### Common Conditions
1.  **Time-Based (JIT Access):**
    *   "Grant `Compute Admin` to Alice expires at 5:00 PM today."
    *   *Syntax:* `request.time < timestamp("2023-12-31T17:00:00Z")`
2.  **Resource-Based:**
    *   "Grant `Storage Admin` ONLY for buckets that start with `dev-`."
    *   *Syntax:* `resource.name.startsWith(...)`
3.  **Access Levels:**
    *   "Grant access only if IP is corporate VPN."

*   *Exam Scenario:* "Contractors need access to reset VMs only between 9 AM and 5 PM on weekdays." -> **Use IAM Conditions.**

---

## 4. Service Account Best Practices

Service Accounts (SAs) are identities for resources.

1.  **One SA per Application/Function:** Don't share the default Compute Engine SA. Create a dedicated SA (e.g., `app-backend-sa`).
2.  **No Keys (if possible):** As covered in the Authentication guide, rely on attached identities.
3.  **Scopes vs. IAM:**
    *   Legacy Access Scopes (Metadata) exist on VMs.
    *   **Rule:** Set Access Scopes to `Allow Full Access to all Cloud APIs` and manage permissions strictly via **IAM Roles**. This decouples the network authorization from the identity authorization.

---

## 5. Organizational Policies (Guardrails)

Do not confuse IAM (Who can do what) with Org Policies (What can be done).

*   **IAM:** "Alice can create VMs."
*   **Org Policy:** "No VMs can be created with Public IPs."
*   **Result:** Alice tries to create a VM with Public IP -> **Failed** (Forbidden by Org Policy).

### Common Org Policies for Exam:
*   `constraints/compute.vmExternalIpAccess`: Block Public IPs.
*   `constraints/iam.allowedPolicyMemberDomains`: "Only allow users from `company.com` to be added to IAM." (Prevents adding personal @gmail.com accounts).
*   `constraints/gcp.resourceLocations`: "Restrict resource creation to `europe-west1` only."

---

## 6. Exam Scenarios Recap

| Scenario | Solution |
| :--- | :--- |
| "Prevent developers from creating external Load Balancers." | **Org Policy** constraint. |
| "Ensure developers can only restart VMs, not delete them." | **Custom IAM Role** with `compute.instances.reset`. |
| "Developer needs access to a bucket for 4 hours." | **IAM Condition** (Time-based). |
| "You accidentially granted Owner at Org Level. How to restrict for one project?" | **Remove** the User from Org Level. Add them to specific projects individually. (Or use Deny Policy if option provided). |
