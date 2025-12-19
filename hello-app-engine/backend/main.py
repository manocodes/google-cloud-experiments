from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/data")
def get_data():
    # In a real app, this is where you would query Cloud SQL or Firestore
    return jsonify({
        "message": "Hello from the Secure Backend API!",
        "database_status": "Simulated Connection to Firestore"
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081, debug=True)
