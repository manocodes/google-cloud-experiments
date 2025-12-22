import google.cloud.logging
from google.cloud import error_reporting
import time
import random

# 1. Setup Clients
log_client = google.cloud.logging.Client()
logger = log_client.logger("structured-test-logger")
error_client = error_reporting.Client()

def risky_operation(user_id):
    try:
        print(f"User {user_id} is attempting a risky operation...")
        # Simulate a random "Slow" or "Failure" state
        roll = random.random()
        
        if roll < 0.2: # 20% chance of crash
             raise RuntimeError("Database connection timed out!")
        
        duration = random.uniform(0.1, 0.8)
        time.sleep(duration)

        status = "success" if duration < 0.5 else "slow"
        
        # Log structured data
        log_data = {
            "user": user_id,
            "status": status,
            "latency": duration,
            "event": "risky_op_complete"
        }
        
        severity = "INFO" if status == "success" else "WARNING"
        logger.log_struct(log_data, severity=severity)
        print(f"✅ Status: {status} ({duration:.2f}s)")

    except Exception as e:
        print(f"❌ CRASH! Reporting to Error Dashboard...")
        try:
            error_client.report_exception()
        except:
            pass
        
        logger.log_struct({
            "user": user_id,
            "status": "failed",
            "error_msg": str(e)
        }, severity="ERROR")

if __name__ == "__main__":
    print("🚀 Starting continuous simulation (Ctrl+C to stop)...")
    users = ["luke", "leia", "han", "vader", "chewie"]
    
    try:
        while True:
            user = random.choice(users)
            risky_operation(user)
            time.sleep(1.5) 
    except KeyboardInterrupt:
        print("\nSimulation stopped.")