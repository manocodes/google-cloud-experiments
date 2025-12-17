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

## 3. Clean Up (Optional)
To stop billing, simply **Shut down** the projects from the Manage Resources page. Folders are free.
