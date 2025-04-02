import platform
from flask import Flask, jsonify, render_template,send_from_directory
from flask_cors import CORS
import webbrowser
import os
import json
import threading
import requests
from werkzeug.serving import run_simple  # Import run_simple
import time
import signal

app = Flask(__name__,static_folder='.')
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# ✅ Default path for local execution
DEFAULT_PATH = os.path.join(os.getcwd(), "../", "telemetry_data")

# ✅ Default path for local execution in Windows systems
# DEFAULT_PATH ="C:\\TTS_HOME\\bin\\invest\\src\\Results" 

# ✅ Use environment variable if set, otherwise fallback to DEFAULT_PATH
TELEMETRY_DATA_PATH = os.getenv("TELEMETRY_DATA_PATH", DEFAULT_PATH)


def get_latest_folders(limit=3):
    """Get the latest 'limit' folders sorted by latest update time (only folders with results.json)."""
    folders = []

    if not os.path.exists(TELEMETRY_DATA_PATH):
        return []  # Return an empty list if directory doesn't exist

    for folder in os.listdir(TELEMETRY_DATA_PATH):
        folder_path = os.path.join(TELEMETRY_DATA_PATH, folder)
        results_file = os.path.join(folder_path, "results.json")

        if os.path.isdir(folder_path) and os.path.exists(results_file):  # ✅ Check if results.json exists
            creation_time = os.path.getctime(folder_path)  
            modification_time = os.path.getmtime(folder_path)  

            file_modification_time = os.path.getmtime(results_file)
            modification_time = max(modification_time, file_modification_time)

            latest_time = max(creation_time, modification_time)
            folders.append((folder, latest_time))

    latest_folders = sorted(folders, key=lambda x: x[1], reverse=True)[:limit]
    return [folder[0] for folder in latest_folders]


def get_telemetry_data():
    """Fetch telemetry data from latest valid folders (folders with results.json)."""
    result = {}
    latest_folders = get_latest_folders()

    for folder in latest_folders:
        file_path = os.path.join(TELEMETRY_DATA_PATH, folder, "results.json")

        if os.path.exists(file_path):  # ✅ Check again before reading
            with open(file_path, "r") as file:
                result[folder] = json.load(file)

    return {"folders": list(result.keys()), "data": result}  # ✅ Return only folders that have data



@app.route("/api/telemetry", methods=["GET"])
def telemetry_api():
    response = jsonify(get_telemetry_data())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/")
def serve_html():
    """Serves the report_with_graph.html file."""
    return send_from_directory(os.getcwd(), "report_with_graph.html")

@app.route("/hotwire_logo.png")
def serve_logo():
    return send_from_directory(os.getcwd(), "hotwire_logo.png")

def run_server():
    """Start the Flask server."""
    run_simple('localhost', 5001, app, use_reloader=False)  # Remove shutdown_with_keyboard_interrupt

def is_server_ready(url):
    """Checks if the Flask server is ready."""
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    server_url = "http://127.0.0.1:5001/api/telemetry"
    while not is_server_ready(server_url):
        time.sleep(0.1)

    report_file = os.path.abspath("report_with_graph.html")
    webbrowser.open("file://" + report_file)

    try:
        server_thread.join()  # Wait for the server thread to finish
    except KeyboardInterrupt:
        print("Server termination requested.")
        if platform.system() == "Windows":
            os.kill(os.getpid(), signal.CTRL_C_EVENT)  # Simulate Ctrl+C on Windows
        else:
            os.kill(os.getpid(), signal.SIGTERM)  # Terminate on other platforms



