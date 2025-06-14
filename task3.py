import configparser
import json
import os
import sqlite3
from flask import Flask, jsonify

# Constants
CONFIG_FILE = "config.ini"
DB_FILE = "config_data.db"
TABLE_NAME = "configurations"

# Flask app
app = Flask(__name__)

# Function to parse config file
def parse_config(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

    config = configparser.ConfigParser()
    config.read(file_path)

    data = {}
    for section in config.sections():
        data[section] = {}
        for key in config[section]:
            data[section][key] = config[section][key]
    return data

# Save JSON data into SQLite
def save_to_database(json_data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    ''')

    json_string = json.dumps(json_data)
    c.execute(f"INSERT INTO {TABLE_NAME} (data) VALUES (?)", (json_string,))
    conn.commit()
    conn.close()

# Fetch latest config from database
def fetch_config():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(f"SELECT data FROM {TABLE_NAME} ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return json.loads(row[0]) if row else {}

# Flask route
@app.route("/config", methods=["GET"])
def get_config():
    try:
        config_data = fetch_config()
        return jsonify(config_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main function
if __name__ == "__main__":
    try:
        parsed_data = parse_config(CONFIG_FILE)
        save_to_database(parsed_data)
        print(" Configuration parsed and saved to database.")
    except Exception as e:
        print(f" Error: {e}")

    # Run Flask API
    app.run(debug=True, port=8080)
