import logging
import os
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

def run_experiment(use_cloud_logging=False):
    print(f"\n--- Starting Experiment (Cloud Logging: {use_cloud_logging}) ---")

    if use_cloud_logging:
        # This setup connects Python's logging to GCP
        client = google.cloud.logging.Client()
        client.setup_logging()
        print("✅ Cloud Logging initialized. Logs will go to the Cloud Console!")
    else:
        # Standard local-only logging
        logging.basicConfig(level=logging.DEBUG, force=True)
        print("💻 Local logging only. Logs will only appear in this terminal.")

    # 🟢 Level 1: Standard Print
    print("[PRINT] This is a standard print statement.")

    # 🟡 Level 2: Python Logging Levels
    logging.debug("[DEBUG] Fine details for developers.")
    logging.info("[INFO] Something notable happened.")
    logging.warning("[WARNING] This might be a problem.")
    logging.error("[ERROR] This is definitely a problem!")

    # 🔴 Level 3: Structured Logging
    # Note: 'extra' fields only show up as searchable metadata in the Cloud Console
    logging.info("Task completed", extra={
        "json_fields": {
            "task_id": "12345",
            "user": "developer_test",
            "status": "success"
        }
    })

    # 💥 The Exception Trap
    try:
        result = 10 / 0
    except Exception as e:
        # logging.exception is the "Golden Ruler" of debugging
        logging.exception("An unexpected error occurred during math operations!")

if __name__ == "__main__":
    # Change this to True if you want to test sending logs to your GCP project
    # (Requires being logged in via: gcloud auth application-default login)
    run_experiment(use_cloud_logging=False)
