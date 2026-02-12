# 📈 AI-Hardware Market Intelligence Tracker (MVP)

## Project Overview
This project is a high-reliability backend data pipeline designed to monitor and record price volatility for high-end hardware components. It currently tracks **DDR5 32GB RAM** and **2TB NVMe SSDs**, specifically configured to handle the 2026 market surge for premium Gen5 and AI-capable hardware.

## 🛠️ Implementation Audit (Feb 12, 2026)

### 1. Data Extraction Engine (`tracker.py`)
* **Resilient Scraping:** Utilizes a **Regex-based extraction engine** to pull currency values directly from raw HTML, bypassing fragile CSS selectors that frequently change.
* **Bot-Detection Mitigation:** Implements a "Human Fingerprint" strategy using modern browser headers, Google referrers, and polite connection delays to prevent 403 Forbidden errors.
* **Dynamic Outlier Filtering:**
    * **RAM:** Captures listings between **$50 – $500**.
    * **SSD:** Captures listings between **$50 – $1,000** (Expanded to include premium Gen5 2TB NVMe drives).

### 2. Data Storage Layer (`ebay_hardware_data.csv`)
* **Schema:** `Date`, `Component`, `Avg_Price`, `Count`
* **Integrity:** Uses **Append-Only logic** (`mode='a'`) to preserve historical data.
* **Categorization:** Implements component tagging to allow for granular analysis of different hardware classes within a single dataset.

### 3. Environment & Stack
* **Language:** Python 3.x (Anaconda Instance)
* **Key Libraries:** `Pandas` (Data Structures), `BeautifulSoup4` (HTML Parsing), `Requests` (HTTP Client), `Re` (Regex).

---

## 🚀 Next Steps (Cloud Migration)
The local implementation is complete and "Headless-Ready." The next phase of the project involves:
1.  **AWS Lambda Deployment:** Porting the `tracker.py` logic to a serverless environment to bypass local IP flagging.
2.  **Amazon S3 Integration:** Moving the CSV storage to a cloud "Data Lake" for permanent persistence.
3.  **Automation:** Scheduling daily runs via **Amazon EventBridge**.