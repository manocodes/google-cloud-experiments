# Google Cloud Logging: A Solid Foundation

Logging is the "black box" of your cloud applications. It's the primary way to understand what's happening inside your code when it's running in the cloud.

---

## 🟢 Level 1: Standard Output (`print`)
The simplest way to log. Anything you `print()` is automatically captured by Cloud Logging.

- **Pros:** Fast, zero setup.
- **Cons:** 
    - **No Severity:** Everything is marked as "DEFAULT" or "INFO". You can't filter for errors.
    - **Fragmentation:** Multi-line prints (like stack traces) are broken into multiple separate log entries.
    - **No Metadata:** You don't get extras like `user_id` or `request_id` attached automatically.
- **Use Case:** Local debugging and quick scripts.

> **💡 The "Gotcha":** In the Cloud Console, if you filter for `Severity: ERROR`, you will **NOT** see your `print()` statements, even if they say "ERROR" in the text!

```python
print("Processing file: image.jpg")
```

---

## 🟡 Level 2: Professional Logging (`logging` module)
Using Python's built-in `logging` module allows you to assign **Severity**.

### Severity Levels
| Level | Color (GCP) | Use Case |
| :--- | :--- | :--- |
| `DEBUG` | Gray | Fine-grained info (e.g., "Entering loop") |
| `INFO` | Blue | Standard milestones (e.g., "Started processing") |
| `WARNING` | Yellow | Unusual but non-critical (e.g., "Retry 1/3") |
| `ERROR` | Red | Something failed (e.g., "File not found") |
| `EXCEPTION`| Red + Trace | Includes the **Full Stack Trace** automatically. |

### Implementation
```python
import logging
logging.basicConfig(level=logging.INFO)

logging.info("Everything is fine")
logging.error("Something went wrong")

try:
    1 / 0
except Exception as e:
    logging.exception("Math is hard") # Captures the traceback!
```

---

## 🔴 Level 3: Structured Logging (JSON)
The "Pro" way. Instead of logging a string, you log a **dictionary**. This turns your logs into a searchable database.

### Why Structured?
If you have 10,000 logs, searching for a specific filename in a text string is slow and prone to errors. With structured logging, you can query fields directly.

### Implementation
Requires `google-cloud-logging` library.

```python
import google.cloud.logging
import logging

client = google.cloud.logging.Client()
client.setup_logging()

# Log with extra data
logging.info("File copy successful", extra={
    "json_fields": {
        "file_name": "invoice_1.pdf",
        "user_id": 12345,
        "latency_ms": 450
    }
})
```
---

## 🧭 Mastering the Log Explorer UI

The Log Explorer is a database, not a text file. Use these features to find bugs fast:

### 1. The "Cheat" Method (Add to Query)
Don't type queries manually. Expand any log entry, click on a field value (like a `user_id` or `status`), and select **Show matching entries**. Google will write the code for you.

### 2. The Time Histogram
The bar chart at the top shows frequency.
- **Blue bars:** Info/Success
- **Red bars:** Errors
- **Action:** Click and drag over a cluster of red bars to "Zoom in" on a specific crash event.

### 3. "Hide Matching" (Anti-Spam)
If a specific log (like a health check) is cluttering your view:
- Expand the log.
- Click the annoying field.
- Select **Hide matching entries**.
- This adds `NOT` to your query, clearing the noise.

### 4. Direct JSON Querying
In **Editor** mode, you can query nested fields directly:
```sql
jsonPayload.performance.duration_sec > 0.5
severity = ERROR
```

---

## 🛠 Pro Tips for Debugging

### 1. The Power of `logging.exception`
Never just `print(e)` in an exception block. Always use `logging.exception("Context message")`. It automatically captures the line number and the error type, saving you hours of hunting for the source of a crash.

### 2. Log Explorer Queries
In the Google Cloud Console, you can query your structured logs like this:
- **Search for a field:** `jsonPayload.file_name = "invoice_1.pdf"`
- **Filter by severity:** `severity >= ERROR`
- **Time range:** Select from the dropdown to focus on a 5-minute window around a crash.

### 3. Correlation (Trace IDs)
Always include a unique identifier (like an `event_id` or `request_id`) in your structured logs. This allows you to follow the "story" of a single request as it traverses multiple services.

---

## 🛠 Level 4: Error Reporting (The Bug Task-List)

While Log Explorer is for *history*, Error Reporting is for *action*. It treats crashes as tasks to be solved.

### 1. Grouping: One Entry vs. 1,000 Logs
If your code fails 50 times on the same line, Error Reporting shows **one single entry** with a count of 50. This saves you from "Log Fatigue."

### 2. The "Fixed" Lifecycle
This is the most powerful feature for developers:
- **Open:** The bug is active.
- **Acknowledged:** You are currently debugging it.
- **Fixed:** You've pushed a fix. 
- **Automatic Re-opening:** If the bug happens again *after* you marked it "Fixed," Google sends you an alert saying: "Hey, your fix didn't work! The error just returned."

### 3. Linking to Logs
In the Error Dashboard, every crash has a **"View Logs"** link. This takes you back to the Log Explorer, but it automatically filters for the exact milliseconds before the crash happened, so you can see the "context" (what the user was doing right before it blew up).

---

## 📈 Level 5: Log-based Metrics & Alerts (The Watchman)

Don't watch the logs; let the logs watch the app.

### 1. What are Log-based Metrics?
They turn text matches into a numeric stream. 
- **Example:** Match `jsonPayload.status="failed"` -> Counter increments.
- **Example:** Extract `jsonPayload.latency` -> Average/Distribution chart.

### 2. Creating an Alert (The Golden Signal)
Once you have a metric, you can create a **Notification Channel**.
- **The Rule:** "If the Failure Counter > 5 in any 1-minute window, send an email to the team."
- **Why this matters:** You catch "Silent Failures" (cases where the code doesn't crash, but it's not working correctly) before your users report them.

### 3. Log Sinks (Forwarding)
For the PCA exam, remember that logs disappear after 30 days unless you create a **Log Sink**:
- **BigQuery:** For long-term SQL analysis of your logs.
- **Cloud Storage:** For cheap, multi-year compliance storage.
- **Pub/Sub:** To trigger *other* code whenever a specific log happens.

## ⚙️ Log Router & Cost Management

*   **Log Router**: The engine that checks every log against rules.
*   **Log Sink**: The rule itself ("If text matches 'ERROR', send to BigQuery").
*   **Exclusion Filters**: **Money Saver**.
    *   *Scenario*: Your load balancer logs 200 OK health checks 10 times a second. You pay for that ingestion.
    *   *Solution*: Create an Exclusion Filter in Log Router to **drop** 200 OK logs from `HTTP Load Balancer`. They never hit storage, so you pay $0.

## 🔐 Audit Logs (Data Access)
*   **Admin Activity**: (On by Default). "Who created the bucket?" - Free.
*   **Data Access**: (Off by Default). "Who read file.txt?" - High volume, costs money. Must enable explicitly.
