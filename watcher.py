import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

# -- Config --
load_dotenv()
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
WATCH_DIR      = os.path.join(BASE_DIR, "raw_data")
EMAIL_SENDER   = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


# -- Send Email --
def send_email(mode="daily"):
    report_path = os.path.join(BASE_DIR, "coffee_report.xlsx")

    msg = MIMEMultipart()
    msg["From"]    = EMAIL_SENDER
    msg["To"]      = EMAIL_RECEIVER
    msg["Subject"] = f"☕ Coffee Vending Machine - {'Daily' if mode == 'daily' else 'Weekly'} Report"

    body = f"""Hi,

Your {'daily' if mode == 'daily' else 'weekly'} Coffee Vending Machine report is ready!

{"- Daily Revenue, Top Coffees, Best Hours" if mode == 'daily' else "- Full 7 tab report included"}

— Coffee Automation Bot"""

    msg.attach(MIMEText(body, "plain"))

    with open(report_path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=coffee_report.xlsx")
        msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

    print(f"{'Daily' if mode == 'daily' else 'Weekly'} report emailed successfully.")


# -- Weekly Email Function --
def send_weekly_report():
    print("Running weekly analysis...")
    os.system(f'python "{os.path.join(BASE_DIR, "coffee.py")}" weekly')
    send_email("weekly")
    print("Weekly report done.")


# -- File Watcher --
class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.src_path.endswith(".csv"):
            print(f"New file detected: {event.src_path}")
            time.sleep(2)
            os.system(f'python "{os.path.join(BASE_DIR, "coffee.py")}" daily')
            print("Daily analysis complete.")
            send_email("daily")


# -- Observer --
observer = Observer()
observer.schedule(CSVHandler(), path=WATCH_DIR, recursive=False)
observer.start()

print(f"Watching folder: {WATCH_DIR}")
print("Drop a CSV file in raw_data to trigger the analysis...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()