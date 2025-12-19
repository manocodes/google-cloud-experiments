# Google Cloud Resource Hierarchy Lab

This guide walks you through creating a standard enterprise hierarchy.

## 1. The Structure
We are building a nested hierarchy (Depth = 3), which is standard for large enterprises.
```text
Organization (manoyaka.com)
└── Folder: Engineering (Department)
    ├── Folder: Production
    │   └── Project: manoyaka-eng-prod
    ├── Folder: Staging
    │   └── Project: manoyaka-eng-stage
    └── Folder: Development
        └── Project: manoyaka-eng-dev
```

## 2. Execution Steps

### Step A: Create the Department Folder
1.  Go to **Manage Resources**.
2.  Select Organization (`manoyaka.com`).
3.  Click **Create Folder**.
    *   **Name:** `Engineering`
    *   **Create**.

### Step B: Create Environment Folders (Nested)
1.  Click on the new `Engineering` folder to enter it.
2.  Click **Create Folder** *inside* Engineering.
    *   **Name:** `Development`
3.  Repeat to create `Staging` and `Production` *inside* Engineering.

### Step C: Create Projects
1.  Enter the `Development` folder (Path: `manoyaka.com > Engineering > Development`).
2.  Click **Create Project**.
    *   **Name:** `manoyaka-eng-dev`
    *   **Location:** Ensure it shows the `Development` folder path.
3.  Repeat for Staging and Prod projects in their respective folders.

### Step D: Why this matters (Exam Tip)
This structure allows you to:
*   Grant "Department Head" access at the `Engineering` level.
*   Grant "Junior Dev" access ONLY at the `Development` folder level.
*   Set strict Org Policies (e.g., "No Public IPs") at the `Production` folder level.


### Step C: Verify Inheritance (The Exam Question)
1.  Go to **IAM & Admin** > **IAM**.
2.  Select the **Development** folder in the top dropdown.
3.  Grant `Storage Object Viewer` to one of your users.
4.  Switch the top dropdown to the `manoyaka-dev-app` **Project**.
5.  **Check:** Does that user appear in the list?
    *   *Result:* They should appear with the role `Inherited from folder Development`.

### Step E: Setting an Organization Policy (Guardrails)
Policies are different from IAM. IAM says *WHO*, Policies say *WHAT*.
*Goal:* We want to block Public IP creation in the `Staging` environment to save money and improve security.

1.  **Navigate:** Go to **IAM & Admin** > **Organization Policies**.
2.  **Select Scope:** Click the top Project Selector and choose the **Staging** folder (`manoyaka.com > Engineering > Staging`).
3.  **Search Policy:** Filter for "external IPs".
4.  **Click:** `Define allowed external IPs for VM instances` (compute.vmExternalIpAccess).
5.  **Edit:**
    *   Click **Manage Policy** (or Edit).
    *   Select **Override parent's policy**.
    *   **Rule:** Select **Deny All**.
    *   Click **Set Policy**.

**Verification:**
*   If you now try to create a VM in `manoyaka-eng-stage` and give it a Public IP, it will fail with an error.
*   *Exam Note:* This is how you enforce compliance (e.g., HIPAA/PCI) without micromanaging every developer.

## 3. Clean Up (Optional)
To stop billing, simply **Shut down** the projects from the Manage Resources page. Folders are free.

