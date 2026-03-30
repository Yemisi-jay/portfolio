import urllib.request
import logging
import time

logging.basicConfig(
    filename="ping_heartbeat.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

URL = "https://oluwayemisi.onrender.com"
INTERVAL_SECONDS = 180  # 3 minutes

def ping():
    print(f"Pinging {URL}...")
    try:
        with urllib.request.urlopen(URL, timeout=15) as r:
            status = r.status
            logging.info("PING %s -> %d", URL, status)
            print(f"Success: {URL} -> {status}")
    except Exception as e:
        logging.error("PING %s FAILED: %s", URL, e)
        print(f"Failed: {URL} -> {e}")

if __name__ == "__main__":
    print("Starting ping loop every 3 minutes. Press Ctrl+C to stop.")
    while True:
        ping()
        time.sleep(INTERVAL_SECONDS)