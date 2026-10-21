# Smart Home Monitoring System (IoT + Cloud Computing)

A beginner-friendly BE engineering mini-project built with Python, Flask, SQLite, HTML, CSS, and JavaScript.

## Features
- Simulated temperature and humidity readings every five seconds
- Flask HTTP API receives and stores readings in SQLite
- Environment history chart
- Temperature and humidity alerts
- Software switches for two simulated smart lights
- Responsive dashboard for laptop and mobile browsers
- Health endpoint at `/health`

**Important:** This starter version simulates IoT data and device controls in software. It does not connect to real sensors or switch real electrical equipment.

## Run on Windows 11

1. Install Python 3.11 or newer from https://www.python.org/downloads/ . During installation, tick **Add Python to PATH**.
2. Extract the ZIP file.
3. Open the extracted `smart_home_monitoring_system` folder in File Explorer.
4. Click the address bar, type `powershell`, and press Enter.
5. Run these commands:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, run the install and launch commands without activating the environment:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

6. Open http://127.0.0.1:5000 in your browser.
7. Keep the terminal open while using the application. Stop it with `Ctrl+C`.

## API endpoints
- `GET /api/readings` — latest 20 readings
- `POST /api/readings` — submit JSON such as `{"temperature": 28.5, "humidity": 56}`
- `GET /api/devices` — current simulated device states
- `POST /api/devices/Living%20Room%20Light` — JSON body `{"is_on": false}` or `{"is_on": true}`
- `GET /health` — health check

## Cloud deployment outline

This app includes a `Procfile` for hosts that support Python web services and Gunicorn.

1. Create a GitHub repository and upload the extracted project files.
2. Create a new web service with a Python-capable host (for example Render) and connect the repository.
3. Set the build/install command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app`.
5. Deploy and open the URL supplied by the host.

### Database persistence warning
SQLite is suitable for local demonstration. On many cloud hosts, the local filesystem may be temporary and the database can reset after redeploy/restart. For persistent cloud storage, attach a supported persistent disk and set `DATABASE_PATH` to a file path on that disk, or migrate to a managed PostgreSQL database. Check your host's current plan and storage rules.

## How IoT and cloud connect
In this demo, the browser-side simulator generates readings and sends them to the Flask API using HTTP POST. The Flask server validates and stores the data in SQLite; the browser requests the readings and displays them. To use actual IoT hardware later, replace the simulator with an ESP32 or other device that sends sensor values to the API over Wi-Fi. Secure the endpoint before connecting a device over the public internet.
