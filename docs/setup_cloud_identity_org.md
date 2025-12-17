# Setting Up a Free Google Cloud Organization

This guide outlines the steps to create a Google Cloud Organization for personal learning and testing without purchasing a Google Workspace subscription.

## Prerequisites
*   A personal Gmail account.
*   A credit card (for domain purchase).
*   ~15-30 minutes.

## Step 1: Buy a Domain Name
You need a domain name (e.g., `yourname-cloud-lab.com`) to prove ownership to Google.
*   **Cost:** ~$10 - $15 / year.
*   **Registrars:** Namecheap, Cloudflare, or Google Domains (now Squarespace) are good options.
*   **Tip:** Choose one that is cheap. The name doesn't matter much as long as you own it.
*   **Action:** Go to [Namecheap](https://www.namecheap.com/) or another registrar and buy a cheap domain.

## Step 2: Sign Up for Cloud Identity Free Edition
This is the "trick" to get an Organization resource for free.
*   **Link:** [Cloud Identity Free Signup](https://workspace.google.com/gcpidentity/signup?sku=identitybasic)
*   **Important:** Use the link above. Standard Workspace signup pages will try to sell you a monthly subscription.
*   **Process:**
    1.  Enter your Name (e.g., "John Doe") and "Business Name" (e.g., "Mano Cloud Lab").
    2.  Select "Just You" for the number of employees.
    3.  **Current Email Address:** Use your current personal Gmail (e.g., `mano.net@gmail.com`).
    4.  **Business Domain:** Enter the domain you just bought in Step 1.
    5.  **Username:** Create a new admin user (e.g., `admin@yourname-cloud-lab.com`). *Remember this password!*

## Step 3: Verify Your Domain
Google needs to know you actually own the domain.
1.  After signup, the Google Admin Console will ask you to verify.
2.  Select "Add a TXT record to my DNS".
3.  **Copy** the `google-site-verification` code provided.
4.  **Go to your Domain Registrar** (where you bought the domain):
    *   Find "DNS Settings" or "Advanced DNS".
    *   Add a new Record:
        *   **Type:** `TXT`
        *   **Host/Name:** `@`
        *   **Value:** Paste the code from Google.
        *   **TTL:** Set to 1 min or Automatic.
5.  Go back to Google Admin Console and click "Verify". It might take a few minutes.

## Step 4: Access Google Cloud Console
Once verified:
1.  Log in to [console.cloud.google.com](https://console.cloud.google.com/) using your **new admin account** (`admin@yourname...`), NOT your personal Gmail.
2.  You will see a "Select Organization" dropdown at the top.
3.  You now have a root **Organization Node**!

## Step 5: Invite Your Personal User (Optional but Recommended)
To keep using your personal Gmail for daily work:
1.  In the Console (logged in as `admin`), go to **IAM & Admin** > **IAM**.
2.  Click **Grant Access**.
3.  Add your personal Gmail (`mano.net@gmail.com`).
4.  Assign roles:
    *   `Organization Administrator` (or "Organization Admin")
    *   `Folder Admin` (Use the filter to search for "Folder Admin")
    *   `Project Creator` (If not found, search for the role ID: `roles/resourcemanager.projectCreator`. Note: "Organization Admin" usually includes permissions to create projects, but adding this role is safe.)
5.  Now you can log back in as yourself and manage the new Organization.

## Step 6: Test the Hierarchy
1.  **Create a Folder:** Go to "Manage Resources", create a folder named `Production`.
2.  **Create a Project:** Create a project inside `Production`.
3.  **Org Policies:** Go to "IAM & Admin" > "Organization Policies" and try restricting valid regions to `us-central1`.
