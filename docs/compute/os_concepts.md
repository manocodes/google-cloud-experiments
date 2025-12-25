# Compute Engine & OS Concepts: The "No-CLI" Guide

> **Target Audience:** Architects and Technical Leads who need to understand *system behavior* without memorizing *system administration commands*.

## The Golden Rule
**You are designing the house, not plumbing the sink.**
The exam asks about **OS concepts** only when they affect **architecture**, **scalability**, **reliability**, or **security**.

---

## 1. The "Black Box" Problem (Memory Visibility)

### The Concept
Imagine you rent a storage unit (The VM) to a tenant (The OS).
- You (GCP) can see if the tenant is entering/leaving often (Network I/O).
- You can see how much electricity they use (CPU Usage).
- **You CANNOT see how full their boxes are (RAM Usage).**

From the outside, GCP has no idea if the OS is using 1% or 99% of its RAM. This is a privacy/architecture boundary.

### The Exam "Trap"
**Scenario:** "You need to autoscaling a Managed Instance Group based on **Memory/RAM utilization**."
**Solution:** You CANNOT do this out of the box. You **must** install the **Ops Agent** (formerly Stackdriver Agent).
- **Without Agent:** GCP sees CPU, Disk I/O, Network.
- **With Agent:** GCP sees Memory, Disk Space (User-level).

> **Key Takeaway:** If the requirement mentions scaling or monitoring "Memory" or "Disk Space" (not Disk I/O), the answer MUST involve installing an Agent.
> **Exam Tip:** Look for the metric `agent.googleapis.com/memory/percent_used`. Standard metrics are `compute.googleapis.com/...`.

---

## 2. Bootstrapping: Scripts vs. Images

### The Dilemma
You need to launch 1,000 servers that run your application. How do they get the code?

### Option A: Startup Scripts (The "To-Do List")
You give the VM a list of instructions to run *every time it boots*.
- `apt-get update`
- `apt-get install python`
- `git clone my-app`
- `run app`

**Implementation:** You set this in the **Metadata** of the instance using the key `startup-script` or `startup-script-url`.

**Pros:** Flexible. easy to change code (just update the repo).
**Cons:** Slow boot time (has to install everything every time). If the repo is down, the server fails to start.

### Option B: Custom Images (The "Frozen Dinner")
You set up one server perfectly, "bake" it into an image, and launch 1,000 copies.
- The app is already installed.
- The dependencies are already there.

**Pros:** Fast boot time. Reliable (no external downloads at boot).
**Cons:** "Immutable". To change the code, you must build a new image and redeploy.

> **Key Takeaway:**
> - Need **fast scaling**? Use **Custom Images**.
> - Need **frequent, minor config updates**? Use **Startup Scripts**.
> - Best Practice? **Hybrid**. Bake the heavy stuff (Python, Java) into the Image. Use Startup Script for the last-mile config (Environment variables, grabbing the latest jar).

---

## 3. SSH & Access: The "Key" Problem

### The Old Way: SSH Keys
Manually copying a text file (public key) to the server.
**Risk:** Who has the key? Did the ex-employee keep it? It's a "Shared Secret" nightmare.

### The Google Way: OS Login
Connects the Linux User system directly to **Google Cloud IAM**.
- If `alice@company.com` leaves the company (and loses IAM access), she distinctly loses SSH access to the servers.
- No keys to manage.
- Complete audit trail of who logged in.

> **Key Takeaway:** The answer for "Secure Management of SSH" is almost always **enable OS Login**.
> **Implementation:** Set the project-wide (or instance-level) metadata key: `enable-oslogin = TRUE`.

---

## 4. The "Emergency Door": Serial Console

### The Concept
What happens if you mess up the firewall and block port 22 (SSH)? You locked yourself out of the house.

### The Solution
The **Serial Console** is like walking into the datacenter and plugging a monitor and keyboard directly into the server. It bypasses the network.
- You can see the kernel "panic" (crash) logs.
- You can log in via text-only mode to fix the firewall.

> **Key Takeaway:** If an instance is "unreachable via the network," the debugging step is "Check the Serial Console output."
> **Note:** To interact with the serial console (login), you need the `serial-port-enable=TRUE` metadata.

---


## 5. Memory Management: What actually happens when you run out?

### The Concept (OOM Killer)
If you fill a physical warehouse efficiently, you just stop accepting new boxes.
If you fill a Server's RAM 100%, the OS kernel panics. It needs RAM just to keep running.
To survive, the Linux Kernel summons the **OOM (Out of Memory) Killer**.
- It looks for the "most expensive" tenant (usually your main application).
- It **kills the process immediately** to free up RAM.

**Risk:** Your server didn't "slow down"; it crashed. The application process just vanished.

### Swap Memory (The Fake RAM)
You can configure a portion of the Hard Disk (Disk) to act like RAM.
- **Pros:** Prevents OOM crashes.
- **Cons:** Disks are 10,000x slower than RAM. If your app starts using Swap, performance falls off a cliff.
- **Cloud Reality:** In many Cloud architectures, **Swap is disabled/discouraged** because it makes performance unpredictable. It's better to crash and restart (fail fast) than to run at 1% speed.

### "Free" Memory is a Lie
Linux hates wasted space. If you have 10GB of RAM and your app only uses 2GB, Linux will use the other 8GB to **cache** files upon the disk.
- **Active Memory:** Actually used by your app.
- **Cached/Buffered:** Used by the OS to speed up disk access, but *instantly available* if the app needs it.

> **Key Takeaway:**
> - If you see "99% Memory Usage" in a tool, check if it's **Active** or **Cached**. 99% Cached is *good*. 99% Active is *danger*.
> - If an instance mysteriously restarts or the app process disappears, check the logs for **"OOM Killer"**.

---
## 6. Linux Terminology Cheat Sheet

| Tech Term | Conceptual Translation | Exam Context |
| :--- | :--- | :--- |
| **User Data / Metadata** | **Global Variables** | Passing config (DB URL, API Key) to the instance without hardcoding it. |
| **fstab** | **Disk Mounting List** | If you detach a disk but forget to remove it from here, the server might refuse to boot. |
| **Preemptible / Spot** | **Clearance Sale** | 80% cheaper, but Google can take it back anytime. Use for "stateless" batch jobs (processing queues), NOT databases. |
| **Shielded VM** | **Tamper-Proof Seal** | Ensures the OS hasn't been infected by a rootkit (bootloader security). |
