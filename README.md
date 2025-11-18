# 🔍 Log Analyzer & Real-Time Monitoring Dashboard

A full **production-grade log monitoring system** built with:

* **Python**
* **Streamlit (real-time dashboard)**
* **Gmail SMTP Alerts (App Password)**
* **Slack Alerts (Webhook)**
* **Log Simulator (generates live logs)**
* **Modular Parser + Analyzer architecture**

This project mimics the responsibilities of a **Supportability / Site Reliability / DevOps Engineer**, making it perfect for:

* Cohesity interviews (Supportability / Support Engineering)
* Production monitoring simulations
* Resume projects
* GitHub portfolio
* Real-time demo deployments

---

## 🚀 Features

✅ **1. Real-Time Streamlit Dashboard**

* Live auto-refresh (1s, 2s, 5s...)
* Dark theme professional UI
* Error trends by hour
* Most repeated errors
* Security alerts (unauthorized attempts)
* Keyword-based filtering
* Raw logs viewer with highlighting

✅ **2. Log Analyzer (Parser + Analyzer)**

* Regex-based structured parsing
* Extracts: timestamp, level, message, stacktrace
* Aggregates errors by level & hour
* Detects repeated patterns
* Keyword detection

✅ **3. Real-Time Alert Engine**

* Watches log file continuously
* Sends alerts for ERROR & CRITICAL logs
* Gmail SMTP alerts (with App Password)
* Optional Slack alerts

✅ **4. Log Simulator (Real-time Log Generator)**

* Generates random logs every second
* Useful for demo & testing
* Feeds dashboard + alert engine

✅ **5. Clean File Structure**

```
log-analyzer/
│​​​── dashboard.py
│​​​── alert.py
│​​​── log_simulator.py
│​​​── log_parser.py
│​​​── analyzer.py
│​​​── utils.py
│​​​── requirements.txt
│​​​── logs/
│​​​     └── sample.log
└── .streamlit/
      └── theme.toml
```

---

## 🛠 Setup Instructions

**1. Clone the Repository**

```
git clone https://github.com/<your-username>/log-analyzer.git
cd log-analyzer
```

**2. Install Dependencies**

```
pip install -r requirements.txt
```

**3. Run the Log Simulator**

```
python log_simulator.py
```

This will create live logs inside `logs/sample.log`.

### **4. Run the Dashboard**

```
streamlit run dashboard.py
```

**5. Run the Alert Engine** (separate terminal)

```
python alert.py
```

---

📧 Gmail SMTP Alert Setup

**Step 1 — Enable 2-Step Verification**

[https://myaccount.google.com/security](https://myaccount.google.com/security)

**Step 2 — Generate App Password**

[https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)

Choose:

* App → Mail
* Device → Windows Computer

Copy the 16-character password.

**Step 3 — Add to alert.py**

```
SENDER = "you@gmail.com"
APP_PASSWORD = "your16charpassword"
RECEIVER = "you@gmail.com"
```

Done — your email alerts will work.

---

🌐 Deploy to Streamlit Cloud

1. Push this project to GitHub
2. Go to: [https://share.streamlit.io](https://share.streamlit.io)
3. Click **New App**
4. Select your repo
5. Choose:

    **Branch**: main
    **File**: dashboard.py
6. Click **Deploy**

Your dashboard will be live online.

---

📊 Screenshots

(Add after deployment)

---

💡 Interview Talking Points

Use these in your interview:

* Built a **real-time monitoring dashboard** similar to internal tools used in production systems.
* Implemented **alerting workflow** using Gmail SMTP (App Password) & Slack Webhooks.
* Engineered a **custom log parser** using regex capturing timestamp, level, message, stacktrace.
* Added **anomaly detection** via repeated error analysis.
* Designed **hourly error aggregation** for trend analysis.
* Implemented **auto-refreshing Streamlit dashboard** with Plotly charts.
* Built a **log simulator** to mimic real production logs.

They will be impressed.

---

📝 Requirements

```
streamlit
plotly
pandas
requests
```

---

⭐ Author

**Aanaya Verma**

If you like this project, ⭐ star the repo!

---

📬 Support

Feel free to raise issues or request enhancements.
