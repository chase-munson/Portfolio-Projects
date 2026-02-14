# =================================================================
# DATA SOURCES & CITATIONS
# RAM History: https://pangoly.com/en/price-trends/ram/32gb-ddr5
# SSD History: https://pangoly.com/en/price-trends/ssd/2tb-pcie-gen4-x4
# Extraction Date: Feb 14, 2026
# =================================================================

import json
import pandas as pd
from datetime import datetime

def process_history(json_filename, component_label):
    """Loads a JSON file and returns a list of dictionaries for Pandas."""
    print(f"Processing {json_filename}...")
    try:
        with open(json_filename, 'r') as f:
            data = json.load(f)
        
        rows = []
        # Pangoly JSON stores data in an 'avg' array of arrays
        for entry in data['avg']:
            timestamp_ms = entry[0]['parsedValue']
            raw_price = entry[1]
            
            # --- NEW SAFETY CHECK ---
            # If the price is a dictionary, grab 'parsedValue'
            if isinstance(raw_price, dict):
                price = float(raw_price['parsedValue'])
            else:
                price = float(raw_price)
            # ------------------------
            
            clean_date = datetime.fromtimestamp(timestamp_ms / 1000.0).strftime('%Y-%m-%d')
            
            rows.append({
                "Date": clean_date,
                "Component": component_label,
                "Avg_Price": price
            })
        return rows
    except FileNotFoundError:
        print(f"❌ Error: {json_filename} not found.")
        return []
    except Exception as e:
        print(f"❌ Error parsing {json_filename}: {e}")
        return []

if __name__ == "__main__":
    # 1. Process both files
    ram_rows = process_history("ram_history.json", "DDR5_32GB_RAM")
    ssd_rows = process_history("ssd_history.json", "2TB_NVME_GEN4")

    # 2. Combine and save
    all_data = ram_rows + ssd_rows
    
    if all_data:
        df = pd.DataFrame(all_data)
        # Drop any potential duplicates and sort by date
        df = df.sort_values(by=["Component", "Date"]).reset_index(drop=True)
        
        # Save the final file
        df.to_csv("ebay_hardware_data.csv", index=False)
        print("\n" + "="*30)
        print("✅ SUCCESS: 'ebay_hardware_data.csv' created.")
        print(f"Total historical data points: {len(df)}")
        print("="*30)
    else:
        print("❌ No data was processed. Check your .json files.")