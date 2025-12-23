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

## Step 3: Activate Cloud Identity Free Subscription (Crucial Step!)
By default, you have 0 licenses to add users. You must "buy" the free plan.
1.  In the Admin Console, go to **Billing** > **Get more services**.
    *   *Tip:* If you don't see this, try this direct link: `https://admin.google.com/ac/billing/catalog?appIds=cloud_identity`
2.  Click **Cloud Identity** in the category list.
3.  Find **Cloud Identity Free** (Cost: $0.00).
4.  Click **Get Started** and complete the "checkout".

## Step 4: Create a Managed User (The "Enterprise" Way)
To properly simulate an organization, do not use your personal Gmail. Create a real user.
1.  Go to **Director** > **Users** > **Add new user**.
    *   *If you don't see "Users"*: Type "Add user" in the top search bar.
2.  Name: `Mano` (or your name).
3.  Email: `mano@yourname-cloud-lab.com`.
4.  Copy the temporary password.

## Step 5: Access Google Cloud Console
1.  Log in to [console.cloud.google.com](https://console.cloud.google.com/) using your **new admin account** (`admin@yourname...`) or the new user (`mano@...`).
2.  You will see a "Select Organization" dropdown at the top.
3.  You now have a root **Organization Node**!

## Step 6: Grant Admin Rights & Mix with Personal Gmail (Optional)
If you want to manage this from your personal Gmail:
1.  Log in to Cloud Console as `admin@yourname...`.
2.  Go to **IAM & Admin** > **IAM**.
3.  Make sure the **Organization** is selected in the top dropdown.
4.  Grant access to your personal Gmail (`mano.net@gmail.com`).
5.  **Assign these 3 Roles:**
    *   `Organization Administrator`
    *   `Folder Admin`
    *   `Organization Policy Administrator` (Crucial for editing policies!)
6.  *Troubleshooting*: If you get a "Domain Restricted Sharing" error, go to **Organization Policies**, edit "Domain Restricted Sharing", and set it to **Allow All**.

## Step 7: Test the Hierarchy
1.  **Create a Folder:** Go to "Manage Resources", create a folder named `Production`.
2.  **Create a Project:** Create a project inside `Production`.
3.  **Org Policies:** Go to "IAM & Admin" > "Organization Policies" and try restricting valid regions to `us-central1`.
