"""
API request script to pull data from the CTA Train Tracker API and store it in a SQLite database for
further processing.
"""

# Import required libraries
import requests
import sqlite3
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import os


# Load API key from .env file
load_dotenv()

# Create variables
api_key = os.getenv('API_KEY')

lines = ["Red", "Blue", "Brn", "G", "Org", "P", "Pink", "Y"]

# Setup database and table for long-term storage
def setup_database():
    with sqlite3.connect('cta_train_tracker_data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS train_data (
                timestamp TEXT,
                line TEXT,
                route_number TEXT,
                train_direction INTEGER,
                next_station_id TEXT,
                next_station_name TEXT,
                predicted_time TEXT,
                arrival_time TEXT,
                is_approaching INTEGER,
                is_delayed INTEGER,
                latitude REAL,
                longitude REAL,
                heading INTEGER
            )
        ''')
        conn.commit()

# Create function to pull data from CTA positions from API, write it to SQLite DB.
def pull_otp_api_data():
    with sqlite3.connect('cta_train_tracker_data.db') as conn:
        cursor = conn.cursor()
                
        for line in lines:
            url = f"http://lapi.transitchicago.com/api/1.0/ttpositions.aspx?key={api_key}&rt={line}&outputType=JSON"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                cta_data = response.json()
                trains = cta_data["ctatt"]["route"]
                
                # Handle CTA's variable JSON structure
                if isinstance(trains, dict):
                    trains = trains.get("train", [])
                else:
                    trains = trains[0].get("train", [])
                if isinstance(trains, dict):
                    trains = [trains]
                    
                for train in trains:
                    cursor.execute('''
                        INSERT INTO train_data (
                            timestamp, line, route_number, train_direction, next_station_id,
                            next_station_name, predicted_time, arrival_time, is_approaching, 
                            is_delayed, latitude, longitude, heading
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        datetime.now(timezone.utc).isoformat(),
                        line,
                        train.get("rn"),
                        train.get("trDr"),
                        train.get("nextStaId"),
                        train.get("nextStaNm"),
                        train.get("prdt"),
                        train.get("arrT"),
                        train.get("isApp"),
                        train.get("isDly"),
                        train.get("lat"),
                        train.get("lon"),
                        train.get("heading")
                    ))
            else:
                print(f"Failed for {line}: {response.status_code}")
        
        conn.commit()

# Initialize the database table
setup_database()

# Infinite loop to pull data every 60 seconds.
while True:
    try:
        pull_otp_api_data()
    except Exception as e:
        print(f"Encountered an error: {e}")
    time.sleep(60)