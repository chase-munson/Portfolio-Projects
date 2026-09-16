#!/usr/bin/env python3
import requests
import os
import json
import subprocess
from datetime import datetime

GTFS_URL   = "https://www.transitchicago.com/downloads/sch_data/google_transit.zip"
GTFS_DIR   = "/home/firehawken/cta_train_tracker/"
GTFS_META  = "/home/firehawken/cta_train_tracker/gtfs_meta.json"
GCS_BUCKET = "gs://cta-train-tracker-data/gtfs_archive/"
LOG_PATH   = "/home/firehawken/cta_train_tracker/gtfs_refresh.log"

def log(msg):
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — {msg}"
    print(line)
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def run():
    try:
        remote = requests.head(GTFS_URL, timeout=10).headers.get("Last-Modified")
        meta   = json.load(open(GTFS_META)) if os.path.exists(GTFS_META) else {}

        if remote == meta.get("last_modified"):
            log(f"GTFS is current ({remote}). No update needed.")
            return

        log(f"New GTFS detected — downloading...")
        date_stamp = datetime.now().strftime("%Y_%m_%d")
        zip_path   = os.path.join(GTFS_DIR, f"google_transit_{date_stamp}.zip")

        with open(zip_path, "wb") as f:
            f.write(requests.get(GTFS_URL, timeout=30).content)
        log("Download complete.")

        log("Uploading to GCS...")
        result = subprocess.run(
            ["/snap/bin/gsutil", "cp", zip_path, GCS_BUCKET + os.path.basename(zip_path)],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log("Upload complete.")
            os.remove(zip_path)
            log("Local zip removed.")
        else:
            log(f"Upload failed: {result.stderr}")

        json.dump({"last_modified": remote, "updated_at": datetime.now().isoformat(),
                   "zip_path": zip_path}, open(GTFS_META, "w"), indent=2)
        log("Done.")

    except Exception as e:
        log(f"Encountered an error: {e}")

if __name__ == "__main__":
    run()