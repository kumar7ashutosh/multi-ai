import os
import sys
import time
import subprocess
import socket
from dotenv import load_dotenv

load_dotenv()

HOST = "127.0.0.1"
PORT = 9999


def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def wait_for_backend(host, port, timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        if is_port_open(host, port):
            return True
        time.sleep(0.5)
    return False


def get_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def start_backend(root):
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.backend.api:app", "--host", HOST, "--port", str(PORT)],
        cwd=root
    )


def start_frontend(root):
    env = os.environ.copy()
    env["PYTHONPATH"] = root

    return subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app/frontend/ui.py"],
        cwd=root,
        env=env
    )


def main():
    root = get_root()

    backend = None
    if not is_port_open(HOST, PORT):
        backend = start_backend(root)
        if not wait_for_backend(HOST, PORT):
            print("Backend failed")
            return

    frontend = start_frontend(root)

    try:
        frontend.wait()
    except KeyboardInterrupt:
        pass
    finally:
        if frontend:
            frontend.terminate()
        if backend:
            backend.terminate()


if __name__ == "__main__":
    main()