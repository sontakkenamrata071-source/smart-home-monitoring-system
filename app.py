from flask import Flask, render_template, jsonify, request
from datetime import datetime, timezone
import sqlite3
import os
import random

app = Flask(__name__)
DB_PATH = os.environ.get("DATABASE_PATH", "smart_home.db")

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                name TEXT PRIMARY KEY,
                is_on INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.execute("INSERT OR IGNORE INTO devices (name, is_on) VALUES ('Living Room Light', 1)")
        conn.execute("INSERT OR IGNORE INTO devices (name, is_on) VALUES ('Bedroom Light', 0)")
        conn.commit()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/readings", methods=["GET"])
def get_readings():
    with connect_db() as conn:
        rows = conn.execute(
            "SELECT temperature, humidity, created_at FROM readings ORDER BY id DESC LIMIT 20"
        ).fetchall()
    return jsonify([dict(row) for row in reversed(rows)])

@app.route("/api/readings", methods=["POST"])
def add_reading():
    data = request.get_json(silent=True) or {}
    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        if not (-20 <= temperature <= 80 and 0 <= humidity <= 100):
            raise ValueError("Sensor values are outside the accepted range.")
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Send valid temperature (-20 to 80) and humidity (0 to 100)."}), 400

    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    with connect_db() as conn:
        conn.execute(
            "INSERT INTO readings (temperature, humidity, created_at) VALUES (?, ?, ?)",
            (temperature, humidity, timestamp)
        )
        conn.commit()
    return jsonify({"temperature": temperature, "humidity": humidity, "created_at": timestamp}), 201

@app.route("/api/devices", methods=["GET"])
def get_devices():
    with connect_db() as conn:
        rows = conn.execute("SELECT name, is_on FROM devices ORDER BY name").fetchall()
    return jsonify([{"name": row["name"], "is_on": bool(row["is_on"])} for row in rows])

@app.route("/api/devices/<path:name>", methods=["POST"])
def toggle_device(name):
    data = request.get_json(silent=True) or {}
    if not isinstance(data.get("is_on"), bool):
        return jsonify({"error": "Provide is_on as true or false."}), 400
    with connect_db() as conn:
        cur = conn.execute("UPDATE devices SET is_on = ? WHERE name = ?", (int(data["is_on"]), name))
        conn.commit()
        if cur.rowcount == 0:
            return jsonify({"error": "Device not found."}), 404
    return jsonify({"name": name, "is_on": data["is_on"]})

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
