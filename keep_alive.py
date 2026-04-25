"""
Keep-alive script to prevent Render instance from spinning down
Makes periodic HTTP requests to keep the application active
"""

import requests
import threading
import time
import os

# Get the application URL from environment or use localhost
APP_URL = os.environ.get('APP_URL', 'http://localhost:8050')
KEEP_ALIVE_INTERVAL = 30  # seconds


def keep_alive():
    """Make periodic requests to keep the server active"""
    while True:
        try:
            time.sleep(KEEP_ALIVE_INTERVAL)
            response = requests.get(f'{APP_URL}/', timeout=5)
            print(f"[KEEP-ALIVE] ✓ Ping to {APP_URL} - Status: {response.status_code} - {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"[KEEP-ALIVE] ⚠ Error pinging {APP_URL}: {str(e)} - {time.strftime('%H:%M:%S')}")


def start_keep_alive_daemon():
    """Start keep-alive in a background daemon thread"""
    daemon = threading.Thread(target=keep_alive, daemon=True)
    daemon.start()
    print("[KEEP-ALIVE] Daemon started - will ping every 30 seconds")
    return daemon


if __name__ == '__main__':
    print("Starting keep-alive service...")
    start_keep_alive_daemon()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[KEEP-ALIVE] Shutting down...")
