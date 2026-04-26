# Coffee Vending Machine Sales Automation

## What it does
An automated ETL pipeline designed to streamline sales reporting for coffee vending operations. The system monitors incoming logs, processes large-scale transaction data, and delivers multi-tabbed analytical reports to stakeholders via email autonomously.

## Features
- **Data Integration:** Aggregates and synchronizes transaction logs from multiple vending units into a unified dataset.
- **Advanced Processing:** Cleanses and validates 3,800+ rows of raw sales data to ensure high-integrity reporting.
- **Automated Reporting:** Generates a comprehensive 7-tab Excel workbook with granular categorical insights.
- **Event-Driven Ingestion:** Utilizes a file-system observer to detect and ingest new CSV exports in real-time.
- **Scheduled Dispatch:** Features an integrated task scheduler for consistent daily email report delivery.

## Built with
- **Python** (Core Logic)
- **Pandas** (Data Manipulation)
- **Openpyxl** (Excel Engine)
- **Watchdog** (File System Monitoring)
- **APScheduler** (Task Scheduling)

## How to run
1. **Clone the repo:**
   `git clone https://github.com/yourusername/coffee-sales-automation.git`
2. **Install dependencies:**
   `pip install -r requirements.txt`
3. **Configure environment:**
   Create a `.env` file in the root directory with your SMTP email credentials.
4. **Run the watcher:**
   `python watcher.py`