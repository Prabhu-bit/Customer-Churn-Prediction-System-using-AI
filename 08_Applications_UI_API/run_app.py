"""
UNIVERSAL APP LAUNCHER - Run with: python run_app.py
Handles everything automatically - no manual navigation needed!
"""

import subprocess
import sys
import os
import socket
import re
import time
import webbrowser
import importlib.util

# Get project root
project_root = os.path.dirname(os.path.abspath(__file__))
# Repository root is the parent directory of this Applications_UI_API folder
repo_root = os.path.abspath(os.path.join(project_root, os.pardir))


def get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def wait_for_port(host: str, port: int, timeout_seconds: int = 30) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def get_pids_listening_on_port(port: int) -> set[int]:
    try:
        result = subprocess.run(
            ["netstat", "-ano", "-p", "tcp"],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return set()

    pids: set[int] = set()
    pattern = re.compile(rf"\b(?:TCP|UDP)\b.*:{port}\b.*?(\d+)\s*$", re.IGNORECASE)
    for line in result.stdout.splitlines():
        if f":{port}" not in line:
            continue
        match = pattern.search(line.strip())
        if match:
            try:
                pids.add(int(match.group(1)))
            except ValueError:
                continue
    return pids


def stop_streamlit_process(process: subprocess.Popen) -> None:
    pids_to_stop = {process.pid}
    pids_to_stop.update(get_pids_listening_on_port(8501))

    for pid in sorted(pids_to_stop):
        try:
            subprocess.run(
                ["taskkill", "/PID", str(pid), "/T", "/F"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            continue

    deadline = time.time() + 8
    while time.time() < deadline:
        if not get_pids_listening_on_port(8501):
            return
        time.sleep(0.25)

    try:
        process.terminate()
    except Exception:
        pass


def ensure_streamlit_available() -> None:
    if importlib.util.find_spec("streamlit") is not None:
        return

    print("\n⚠️  Streamlit is not installed in the current Python environment.")
    print("   Attempting automatic install: pip install streamlit")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
        print("✓ Streamlit installed successfully")
    except Exception as install_error:
        print("\n❌ Could not install Streamlit automatically.")
        print("   Run this command and try again:")
        print(f"   {sys.executable} -m pip install streamlit")
        raise RuntimeError("Streamlit is required to run this launcher") from install_error

print("\n" + "="*70)
print("  🚀 CUSTOMER CHURN PREDICTION SYSTEM - UNIVERSAL LAUNCHER")
print("="*70)

# Check if streamlit app exists
app_path = os.path.join(project_root, "streamlit_app.py")
if not os.path.exists(app_path):
    print(f"❌ Streamlit app not found at: {app_path}")
    sys.exit(1)

print("✓ Streamlit app found")

# Check if model exists
model_path = os.path.join(repo_root, "07_Models_Trained", "final_optimized_churn_model_reduced.pkl")
if not os.path.exists(model_path):
    print(f"❌ Model not found at: {model_path}")
    sys.exit(1)

print("✓ Model file found")

ensure_streamlit_available()

internal_url = "http://localhost:8501"
external_url = f"http://{get_local_ip()}:8501"

print("\n" + "-"*70)
print("\n📱 Starting Streamlit App...")
print(f"\n   Internal link: {internal_url}")
print(f"\n   External link: {external_url}")
print("\n   The app will automatically open in your default browser.")
print("\n   Press Enter in this terminal to stop the app.")
print("\n" + "-"*70)

# Change to app directory
app_dir = project_root

# Run streamlit in a child process and keep this launcher alive until the user exits it.
try:
    streamlit_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            app_path,
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--browser.serverAddress=localhost",
            "--logger.level=error",
        ],
        cwd=app_dir,
    )

    if not wait_for_port("127.0.0.1", 8501):
        raise RuntimeError("Streamlit did not start on port 8501 within 30 seconds.")

    print(f"\n   Ready: {internal_url}")
    print(f"   Share this LAN URL: {external_url}")
    webbrowser.open_new_tab(internal_url)

    try:
        input("\nLauncher is running. Press Enter to stop the app... ")
    except KeyboardInterrupt:
        print("\n")

    stop_streamlit_process(streamlit_process)

    print("\n✓ App stopped by user")
except Exception as e:
    print(f"\n❌ Error running app: {e}")
    sys.exit(1)
