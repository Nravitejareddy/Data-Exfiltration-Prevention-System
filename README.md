<div align="center">

# 🛡️ Data Exfiltration Prevention System

### Machine Learning Based Network Traffic Monitoring & Threat Detection

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-0F4C81)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-IsolationForest-F7931E?logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

*A modern enterprise-inspired cybersecurity dashboard that detects suspicious outbound network traffic using Machine Learning.*

</div>

---

# 📖 Overview

The **Data Exfiltration Prevention System (DEPS)** is a desktop cybersecurity application developed in **Python** using **Tkinter** and **Isolation Forest Machine Learning**.

The application continuously monitors simulated outbound network traffic, analyzes packets in real time, and detects anomalous behavior that may indicate **data exfiltration attempts**.

It provides an enterprise-style dashboard with live monitoring, traffic statistics, threat alerts, protocol visualization, and real-time machine learning predictions.

---

# ✨ Features

- 🛡️ Real-time Network Traffic Monitoring
- 🤖 Machine Learning Threat Detection
- 📊 Enterprise Dashboard UI
- ⚠️ Live Threat Alerts
- 📈 Total Traffic Statistics
- 🚨 Threat Alert Counter
- 📉 Risk Rate Calculation
- ⏱️ Timestamped Traffic Logs
- 🔵 TCP / 🟠 UDP / 🟣 ICMP Visualization
- 🔄 Auto-scrolling Live Table
- 🎨 Professional Enterprise Theme
- 🧠 Isolation Forest Anomaly Detection

---

# 🖥️ Dashboard Preview

## System Offline

> Replace with your screenshot

<p align="center">
<img src="screenshots/dashboard_off.png" width="95%">
</p>

---

## System Monitoring

> Replace with your screenshot

<p align="center">
<img src="screenshots/dashboard_on.png" width="95%">
</p>

---

# ⚙️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Tkinter | Desktop GUI |
| NumPy | Numerical Computing |
| Pandas | Dataset Processing |
| Scikit-Learn | Machine Learning |
| Isolation Forest | Anomaly Detection |
| Joblib | Model Serialization |

---

# 🧠 Machine Learning Model

The application uses the **Isolation Forest** algorithm to detect anomalous outbound traffic.

### Input Features

- Protocol
- Duration
- Outbound Bytes
- Inbound Bytes
- Packet Count
- Connection Rate
- Failed Logins

### Output

- 🟢 Safe Traffic
- 🔴 Possible Data Exfiltration

---

# 📊 Dashboard Components

- Enterprise Header
- System Status Badge
- Monitoring Controls
- Live Statistics Cards
- Network Traffic Table
- Threat Highlighting
- Auto Scrolling Logs
- Colored Footer Status

---

# 📂 Project Structure

```
DEPS/
│
├── main.py
├── model_deps_iforest.pkl
├── deps_sample_traffic.csv
├── requirements.txt
├── README.md
│
├── screenshots/
│   ├── dashboard_off.png
│   └── dashboard_on.png
│
└── venv/
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DEPS.git
```

Go to project directory

```bash
cd DEPS
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python main.py
```

---

# 📋 Requirements

```
numpy
pandas
scikit-learn
joblib
```

or

```bash
pip install numpy pandas scikit-learn joblib
```

---

# 🔍 Workflow

```
Generate Network Traffic
            │
            ▼
Feature Extraction
            │
            ▼
Isolation Forest Model
            │
            ▼
Anomaly Prediction
            │
            ▼
Update Enterprise Dashboard
            │
            ▼
Threat Alert (if detected)
```

---

# 🎯 Future Improvements

- Deep Learning Based Detection
- Live Packet Capture using Scapy
- SIEM Integration
- Email Alert Notifications
- PDF Report Generation
- User Authentication
- Dark Mode
- Database Logging
- Threat History Analytics
- Export Logs to CSV/PDF

---

# 👨‍💻 Author

**Ravi Teja Reddy N**

Computer Science Engineer

Python • Machine Learning • Cybersecurity • Java • Full Stack Development

---

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>
