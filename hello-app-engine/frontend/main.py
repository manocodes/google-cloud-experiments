from flask import Flask
import requests
import os

app = Flask(__name__)

# In a real app, you would use a discovery service or environment variable
# For App Engine, services can be reached at https://[service]-dot-[project].appspot.com
BACKEND_URL = os.environ.get('BACKEND_URL', 'https://backend-api-dot-manoyaka-eng-dev.uc.r.appspot.com')

@app.route("/")
def index():
    try:
        # Frontend calling the Backend API
        response = requests.get(f"{BACKEND_URL}/data")
        data = response.json()
        status = "Connected to Backend!"
    except Exception as e:
        data = {"message": "Could not connect to backend"}
        status = f"Error: {str(e)}"

    return f"""
    <h1>Frontend Service</h1>
    <p>Status: <b>{status}</b></p>
    <p>Message from Backend: <i>{data['message']}</i></p>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
