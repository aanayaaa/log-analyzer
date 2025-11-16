"# log-analyzer" 
# 🔍 Log Analyzer & Email Alert System (Python Automation)

A production-style log monitoring and alerting system that:
- Reads and parses system log files  
- Detects errors, warnings, and security issues  
- Generates summaries and analytics  
- Sends email alerts when critical events occur  
- Can run automatically via Windows Task Scheduler  

This project is designed similar to real supportability tools used in companies like Cohesity, where log analysis, automation, and monitoring are core workflows.

---

## 🚀 Features

### ✔ Log Reader  
Reads `.log` files line-by-line and supports large log files.

### ✔ Log Parser (Regex + Multiline Support)
Extracts:
- Timestamp  
- Log Level (INFO, WARNING, ERROR, CRITICAL)  
- Message  

Supports **multiline stack traces**, grouping them under one log entry.

### ✔ Log Analyzer
Generates:
- Severity count  
- Most repeated errors  
- Errors grouped by hour  
- Keyword-based search (e.g., unauthorized access)

### ✔ Email Alert System (SMTP)
Automatically sends alerts when:
- `CRITICAL` logs occur  
- `ERROR` count exceeds threshold  
- Security keyword appears (e.g., “unauthorized”)  

### ✔ Automation using Windows Task Scheduler
Runs automatically:
- Every 5 minutes  
- Hourly  
- Daily  
- At system startup  

---

## 🏗 Project Structure

log-analyzer/
│
├── main.py # Main controller
├── parser.py # Log reading + regex parsing
├── analyzer.py # Summaries + analytics
├── alert.py # Email alert system
├── run_log_analyzer.bat # Automation batch script
│
└── logs/
└── sample.log # Example log file


---

## 🛠 Tech Stack

- Python 3.12  
- Regex (`re`)  
- Collections (`Counter`, `defaultdict`)  
- SMTP (email automation)  
- Windows Batch  
- Windows Task Scheduler  

---

## 📊 Example Output

### Log Summary
Total Entries: 53
Log Level Counts: Counter({'ERROR': 21, 'INFO': 18, 'WARNING': 11, 'CRITICAL': 3})


### Top Errors
2x - Database connection failed: timeout after 30s
1x - Unauthorized access attempt from IP 192.168.1.45


### Email Alert
=== SENDING EMAIL ALERT ===
[ALERT] Email sent successfully

---

## 📩 Email Alert Trigger Conditions

An email is sent when:
- A CRITICAL log appears  
- Total ERROR logs exceed threshold  
- Log contains keywords like `"unauthorized"`  

The email contains:
- Severity  
- Timestamp  
- Error message  
- Summary  

---

## ⚙ Automation Setup (Windows Task Scheduler)

### 1. Create `run_log_analyzer.bat` with:

@echo off
cd /d "C:\Users\HP\Desktop\log-analyzer"
"C:\Users\HP\AppData\Local\Programs\Python\Python312\python.exe" main.py
pause

### 2. Open Task Scheduler  
Press `Win + R` → type `taskschd.msc`

### 3. Create Basic Task  
→ Name: **Log Analyzer Automation**

### 4. Set Trigger  
Choose: Daily / Every 5 minutes / Hourly / At Startup

### 5. Action → Start Program  
Browse → select `run_log_analyzer.bat`

Now the system runs automatically.

---

## 📐 Architecture Diagram

pgsql
Copy code
            ┌──────────────────────────┐
            │        sample.log         │
            └───────────────┬──────────┘
                            │
                   read_log_file()
                            │
                            ▼
            ┌──────────────────────────┐
            │        parser.py         │
            │  Regex + stack trace     │
            └───────────────┬──────────┘
                            │
                            ▼
               Parsed log entries (dict)
                            │
                            ▼
            ┌──────────────────────────┐
            │       analyzer.py        │
            │ Counts | Trends | Alerts │
            └───────────────┬──────────┘
                            │
                            ▼
                    Summary output
                            │
                            ▼
            ┌──────────────────────────┐
            │        alert.py          │
            │    Email notifications   │
            └──────────────────────────┘
yaml
Copy code

---

## 🧪 How to Run

### Manual:
python main.py

shell
Copy code

### Automated:
run_log_analyzer.bat

yaml
Copy code
or scheduled via Task Scheduler.

---

## 🎯 Future Enhancements

- Power BI/Tableau dashboard  
- Flask web dashboard  
- Multi-log directory monitoring  
- Rate-limited email alerts  
- Snowflake / SQL storage  

---

## ⭐ Why This Project is Valuable

This project showcases skills in:
- Log parsing  
- Automation  
- Monitoring systems  
- Regex  
- Email alerts  
- OS-level scheduling  
- Debugging  
- System thinking  

Perfect for roles such as:
- Supportability Engineer  
- SRE  
- DevOps Engineer  
- Cloud/Backend Engineer  
- Automation Engineer  

---

