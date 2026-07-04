<div align="center">

# 🛡️ Data Exfiltration Prevention System (DEPS)

### Machine Learning Based Network Traffic Monitoring & Threat Detection

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-0F4C81)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-IsolationForest-F7931E?logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.x-013243?logo=numpy&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

*A desktop cybersecurity application that monitors simulated outbound network traffic and detects potential data exfiltration attempts using Machine Learning.*

</div>

---

# 📖 Overview

The **Data Exfiltration Prevention System (DEPS)** is a desktop-based cybersecurity application built with **Python**, **Tkinter**, and **Scikit-learn**.

The application continuously analyzes simulated outbound network traffic using the **Isolation Forest** anomaly detection algorithm to identify suspicious behavior that may indicate data exfiltration.

An enterprise-inspired dashboard provides live monitoring, traffic statistics, protocol visualization, timestamped logs, and real-time threat alerts.

---

# 🚀 Project Highlights

- 🛡️ Real-Time Network Traffic Monitoring
- 🤖 Machine Learning-Based Threat Detection
- 📊 Enterprise Dashboard Interface
- ⚠️ Live Threat Alert Detection
- 📈 Traffic Statistics Cards
- ⏱️ Timestamped Monitoring Logs
- 🔵 TCP / 🟠 UDP / 🟣 ICMP Visualization
- 🔄 Auto-Scrolling Live Monitoring Table
- 🎨 Professional Enterprise UI Design
- 🧠 Isolation Forest Anomaly Detection

---

# 🖥️ Dashboard Preview

## System Offline

<p align="center">
<img src="screenshots/dashboard_off.png" width="95%">
</p>

---

## System Monitoring

<p align="center">
<img src="screenshots/dashboard_on.png" width="95%">
</p>

---

# ✨ Features

| Feature | Description |
|----------|-------------|
| Live Monitoring | Continuously monitors simulated outbound traffic |
| ML Detection | Detects anomalous traffic using Isolation Forest |
| Threat Alerts | Highlights suspicious network activity |
| Statistics Dashboard | Displays Total Traffic, Threat Alerts and Risk Rate |
| Protocol Visualization | Color-coded TCP, UDP and ICMP packets |
| Timestamp Logging | Records packet arrival time |
| Enterprise UI | Professional dashboard with status cards and monitoring footer |
| Auto Scroll | Automatically follows the newest traffic entries |

---

# 🧠 Machine Learning

## Algorithm

**Isolation Forest**

Isolation Forest identifies anomalous observations by isolating data points that significantly differ from normal network behavior.

### Input Features

- Protocol
- Duration
- Outbound Bytes
- Inbound Bytes
- Packet Count
- Connection Rate
- Failed Login Attempts

### Output Classes

- 🟢 Safe Traffic
- 🔴 Possible Data Exfiltration

---

# ⚙️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming |
| Tkinter | Desktop GUI |
| NumPy | Numerical Computing |
| Pandas | Data Processing |
| Scikit-Learn | Machine Learning |
| Isolation Forest | Anomaly Detection |
| Joblib | Model Serialization |

---

# 📊 Dashboard Components

- Enterprise Header
- System Status Indicator
- Monitoring Controls
- Statistics Cards
- Live Traffic Table
- Threat Highlighting
- Timestamped Logs
- Professional Status Footer

---

# 🏗️ Project Architecture

```
Network Traffic
        │
        ▼
Feature Extraction
        │
        ▼
Isolation Forest Model
        │
        ▼
Threat Prediction
        │
        ▼
Enterprise Dashboard
```

---

# 📂 Project Structure

```
DEPS/
│
├── screenshots/
│   ├── dashboard_off.png
│   └── dashboard_on.png
│
├── main.py
├── model_deps_iforest.pkl
├── deps_sample_traffic.csv
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DEPS.git
```

Navigate to the project directory

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

Or install manually:

```bash
pip install numpy pandas scikit-learn joblib
```

---

# 🔍 Workflow

```
Generate Network Traffic
        │
        ▼
Extract Features
        │
        ▼
Isolation Forest Prediction
        │
        ▼
Threat Classification
        │
        ▼
Dashboard Update
        │
        ▼
Live Monitoring & Alerts
```

---

# 🎯 Future Improvements

- Live Packet Capture using Scapy
- Real Network Interface Monitoring
- SIEM Integration
- Email Notifications
- PDF Report Generation
- User Authentication
- Dark Mode
- Historical Analytics Dashboard
- Database Logging
- CSV / PDF Export

---

# 👨‍💻 Author

**Ravi Teja Reddy N**

Computer Science Engineering Graduate

**Skills**

- Python
- Machine Learning
- Cybersecurity
- Java
- SQL
- Full Stack Development

---

<div align="center">

### ⭐ If you found this project useful, please consider giving it a star!

</div>
