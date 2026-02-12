import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import os
import time

def run_tracker():
    # 1. SETUP - Tracking multiple components now
    components = {
        "DDR5_32GB_RAM": "DDR5+32GB+RAM",
        "2TB_NVME_SSD": "2TB+NVME+SSD"
    }
    filename = "ebay_hardware_data.csv"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for label, search_term in components.items():
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_term}&LH_BIN=1"
        print(f"--- Scanning: {label} ---")
        
        try:
            time.sleep(2) # Be polite to avoid bot detection
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract prices using Regex
            matches = re.findall(r'\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', soup.get_text())
            
            # Dynamic Filter: RAM prices are expected to keep climbing, SSDs to a lesser extent.
            price_limit = 600 if "SSD" in label else 1000
            prices = [float(m.replace(',', '')) for m in matches if 50 < float(m.replace(',', '')) < price_limit]

            if prices:
                avg_p = round(sum(prices) / len(prices), 2)
                new_row = pd.DataFrame({
                    "Date": [datetime.now().strftime("%Y-%m-%d")],
                    "Component": [label], # Key addition: Category tagging
                    "Avg_Price": [avg_p],
                    "Count": [len(prices)]
                })

                file_exists = os.path.isfile(filename)
                new_row.to_csv(filename, mode='a', index=False, header=not file_exists)
                print(f"SUCCESS: {label} Average: ${avg_p}")
            else:
                print(f"No valid prices found for {label}.")

        except Exception as e:
            print(f"Error scanning {label}: {e}")

if __name__ == "__main__":
    run_tracker()
