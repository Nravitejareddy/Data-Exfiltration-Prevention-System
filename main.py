import threading
import time
import random
import queue
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import numpy as np
    import pandas as pd
    from sklearn.ensemble import IsolationForest
    import joblib
except Exception as e:
    print("Missing packages. Install with:\n pip install numpy pandas scikit-learn joblib")
    raise e


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model_deps_iforest.pkl"
DATA_PATH = BASE_DIR / "deps_sample_traffic.csv"

APP_BG = "#F3F4F6"
CARD_BG = "#FFFFFF"
STAT_CARD_BG = "#EFF6FF"
STAT_CARD_BORDER = "#BFDBFE"

HEADER_BG = "#1E3A8A"
HEADER_TEXT = "#FFFFFF"

TEXT = "#1F2937"
MUTED = "#6B7280"
ACCENT = "#2563EB"
DANGER = "#DC2626"
SUCCESS = "#16A34A"

ALT_ROW = "#F9FAFB"
TABLE_HEADER = "#EAF2FF"
TABLE_SELECTED = "#DBEAFE"

PROTO_MAP = {"tcp": 0, "udp": 1, "icmp": 2}

NUM_FEATURES = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "pkts",
    "conn_rate",
    "failed_logins",
]

ALL_FEATURES = ["protocol"] + NUM_FEATURES


def encode_protocol(proto: str) -> int:
    return PROTO_MAP.get(str(proto).lower(), 0)


def row_to_features(row: dict) -> np.ndarray:
    vals = [
        float(row.get("duration", 0)),
        float(row.get("src_bytes", 0)),
        float(row.get("dst_bytes", 0)),
        float(row.get("pkts", 0)),
        float(row.get("conn_rate", 0)),
        float(row.get("failed_logins", 0)),
    ]
    return np.array([encode_protocol(row.get("protocol", "tcp"))] + vals, dtype=float).reshape(1, -1)


def random_packet(exfiltration=False):
    proto = random.choice(list(PROTO_MAP.keys()))

    if not exfiltration:
        return {
            "protocol": proto,
            "duration": max(0.0, random.gauss(0.8, 0.5)),
            "src_bytes": abs(int(random.gauss(4000, 1200))),
            "dst_bytes": abs(int(random.gauss(3800, 1100))),
            "pkts": max(1, int(random.gauss(8, 3))),
            "conn_rate": max(0.01, random.gauss(2.5, 0.7)),
            "failed_logins": max(0, int(abs(random.gauss(0.1, 0.4)))),
        }

    return {
        "protocol": proto,
        "duration": max(0.0, random.gauss(12, 6)),
        "src_bytes": abs(int(random.gauss(180000, 70000))),
        "dst_bytes": abs(int(random.gauss(220000, 90000))),
        "pkts": max(1, int(random.gauss(300, 100))),
        "conn_rate": max(0.01, random.gauss(30, 12)),
        "failed_logins": max(1, int(abs(random.gauss(8, 4)))),
    }


def generate_synthetic_csv(path: Path, n_normal=3000, n_exfil=300):
    rows = [random_packet(False) for _ in range(n_normal)]
    rows += [random_packet(True) for _ in range(n_exfil)]
    random.shuffle(rows)

    df = pd.DataFrame(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

    print(f"DEPS sample traffic dataset saved to {path}")


def train_and_save_model(data_path: Path, model_path: Path):
    print("Training DEPS ML model...")

    if not data_path.exists():
        print("Traffic dataset missing. Generating synthetic DEPS data...")
        generate_synthetic_csv(data_path)

    df = pd.read_csv(data_path)

    for col in ALL_FEATURES:
        if col not in df.columns:
            df[col] = "tcp" if col == "protocol" else 0.0

    df["protocol"] = (
        df["protocol"].astype(str).str.lower().map(PROTO_MAP).fillna(0).astype(int)
    )

    for col in NUM_FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    X = df[["protocol"] + NUM_FEATURES].values

    model = IsolationForest(
        n_estimators=200,
        max_samples="auto",
        contamination=0.08,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X)
    joblib.dump(model, model_path)

    print("DEPS ML model trained and saved to", model_path)
    return model


class DEPSApp(tk.Tk):
    def __init__(self, model):
        super().__init__()

        self.title("DEPS - Data Exfiltration Prevention System")
        self.geometry("1200x720")
        self.minsize(1100, 650)
        self.configure(bg=APP_BG)

        self.model = model
        self.running = False
        self.total_count = 0
        self.risk_count = 0
        self.last_scan_time = "--:--:--"
        self.row_index = 0
        self.q = queue.Queue(maxsize=200)

        self._build_ui()
        self.after(200, self._consume_queue)

    def _build_ui(self):
        header = tk.Frame(self, bg=HEADER_BG)
        header.pack(fill="x")

        title_block = tk.Frame(header, bg=HEADER_BG)
        title_block.pack(side="left", padx=22, pady=6)

        title = tk.Label(
            title_block,
            text="Data Exfiltration Prevention System",
            bg=HEADER_BG,
            fg=HEADER_TEXT,
            font=("Segoe UI", 18, "bold"),
        )
        title.pack(anchor="w")

        subtitle = tk.Label(
            title_block,
            text="Machine Learning Based Network Traffic Monitoring",
            bg=HEADER_BG,
            fg="#DBEAFE",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w")

        self.badge = tk.Label(
            header,
            text="● SYSTEM ONLINE",
            bg="#DCFCE7",
            fg="#15803D",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3,
        )
        self.badge.pack(side="right", padx=24)

        panel = tk.Frame(self, bg=APP_BG)
        panel.pack(fill="x", padx=20, pady=10)
        panel.columnconfigure(6, weight=1)

        self.start_btn = tk.Button(
            panel,
            text="▶ Start Monitoring",
            command=self.start_monitor,
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=12,
            pady=4,
        )

        self.stop_btn = tk.Button(
            panel,
            text="■ Stop Monitoring",
            command=self.stop_monitor,
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=12,
            pady=4,
        )

        self.clear_btn = tk.Button(
            panel,
            text="🗑 Clear Logs",
            command=self.clear_table,
            bg="#6B7280",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padx=12,
            pady=4,
        )

        self.start_btn.grid(row=0, column=0, padx=(0, 8), sticky="w")
        self.stop_btn.grid(row=0, column=1, padx=8, sticky="w")
        self.clear_btn.grid(row=0, column=2, padx=8, sticky="w")

        self.total_value = self._stat_card(panel, "Total Traffic", "0", 3)
        self.alert_value = self._stat_card(panel, "Threat Alerts", "0", 4)
        self.rate_value = self._stat_card(panel, "Risk Rate", "0.00%", 5)

        container = tk.Frame(
            self,
            bg=CARD_BG,
            highlightbackground="#D1D5DB",
            highlightthickness=1,
        )
        container.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground=TEXT,
            rowheight=32,
            borderwidth=0,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Treeview.Heading",
            background=TABLE_HEADER,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )

        style.map(
            "Treeview",
            background=[("selected", TABLE_SELECTED)],
            foreground=[("selected", TEXT)],
        )

        cols = (
            "time",
            "protocol",
            "duration",
            "out_bytes",
            "in_bytes",
            "packets",
            "conn_rate",
            "failed_logins",
            "threat_score",
            "status",
        )

        self.tree = ttk.Treeview(
            container,
            columns=cols,
            show="headings",
            selectmode="none",
        )

        headings = {
            "time": "TIME",
            "protocol": "PROTOCOL",
            "duration": "DURATION",
            "out_bytes": "OUT BYTES",
            "in_bytes": "IN BYTES",
            "packets": "PACKETS",
            "conn_rate": "CONN RATE",
            "failed_logins": "FAILED LOGINS",
            "threat_score": "THREAT SCORE",
            "status": "STATUS",
        }

        for c in cols:
            self.tree.heading(c, text=headings[c])
            self.tree.column(c, anchor="center", width=105)

        self.tree.column("time", width=90)
        self.tree.column("protocol", width=95)
        self.tree.column("status", width=270)

        self.tree.tag_configure("safe_even", foreground="#1F2937", background="#FFFFFF")
        self.tree.tag_configure("safe_odd", foreground="#1F2937", background=ALT_ROW)

        self.tree.tag_configure("risk_even", foreground="#DC2626", background="#FEF2F2")
        self.tree.tag_configure("risk_odd", foreground="#DC2626", background="#FEF2F2")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        vsb.grid(row=0, column=1, sticky="ns", pady=10)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        footer = tk.Frame(
            self,
            bg=CARD_BG,
            highlightbackground="#D1D5DB",
            highlightthickness=1,
        )
        footer.pack(fill="x", padx=20, pady=(0, 12))

        footer_inner = tk.Frame(footer, bg=CARD_BG)
        footer_inner.pack(side="left", padx=12, pady=7)

        self.footer_monitoring = tk.Label(
            footer_inner,
            text="Ready",
            bg=CARD_BG,
            fg=MUTED,
            font=("Segoe UI", 10, "bold"),
        )
        self.footer_monitoring.pack(side="left")

        self.footer_sep1 = tk.Label(
            footer_inner,
            text="  │  ",
            bg=CARD_BG,
            fg="#CBD5E1",
            font=("Segoe UI", 10, "bold"),
        )
        self.footer_sep1.pack(side="left")

        self.footer_model = tk.Label(
            footer_inner,
            text="Isolation Forest Standby",
            bg=CARD_BG,
            fg=ACCENT,
            font=("Segoe UI", 10, "bold"),
        )
        self.footer_model.pack(side="left")

        self.footer_sep2 = tk.Label(
            footer_inner,
            text="  │  ",
            bg=CARD_BG,
            fg="#CBD5E1",
            font=("Segoe UI", 10, "bold"),
        )
        self.footer_sep2.pack(side="left")

        self.footer_scan = tk.Label(
            footer_inner,
            text="Last Scan: --:--:--",
            bg=CARD_BG,
            fg=MUTED,
            font=("Segoe UI", 10, "bold"),
        )
        self.footer_scan.pack(side="left")

    def _stat_card(self, parent, title, value, col):
        card = tk.Frame(
            parent,
            bg=STAT_CARD_BG,
            highlightbackground=STAT_CARD_BORDER,
            highlightthickness=1,
            width=135,
            height=62,
        )
        card.grid(row=0, column=col, padx=8, sticky="e")
        card.grid_propagate(False)

        label = tk.Label(
            card,
            text=title,
            bg=STAT_CARD_BG,
            fg=MUTED,
            font=("Segoe UI", 9, "bold"),
        )
        label.pack(pady=(4, 0))

        value_label = tk.Label(
            card,
            text=value,
            bg=STAT_CARD_BG,
            fg="#1E3A8A",
            font=("Segoe UI", 18, "bold"),
        )
        value_label.pack(pady=(0, 4))

        return value_label

    def _update_footer(self, state_text, state_color, model_text, scan_time):
        self.footer_monitoring.config(text=state_text, fg=state_color)
        self.footer_model.config(text=model_text, fg=ACCENT)
        self.footer_scan.config(text=f"Last Scan: {scan_time}", fg=MUTED)

    def start_monitor(self):
        if self.model is None:
            messagebox.showerror("Error", "DEPS model missing. Train model first.")
            return

        if self.running:
            return

        self.running = True
        self.badge.config(text="● PROTECTED")

        self._update_footer(
            "● Monitoring",
            SUCCESS,
            "Isolation Forest Active",
            self.last_scan_time,
        )

        self.thread = threading.Thread(target=self._producer_loop, daemon=True)
        self.thread.start()

    def stop_monitor(self):
        self.running = False
        self.badge.config(text="● SYSTEM ONLINE")

        self._update_footer(
            "Stopped",
            MUTED,
            "Isolation Forest Standby",
            self.last_scan_time,
        )

    def clear_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        self.total_count = 0
        self.risk_count = 0
        self.row_index = 0
        self.last_scan_time = "--:--:--"

        self._update_stats()
        self._update_footer(
            "Logs Cleared",
            MUTED,
            "Isolation Forest Standby",
            "--:--:--",
        )

    def _update_stats(self):
        self.total_value.config(text=str(self.total_count))
        self.alert_value.config(text=str(self.risk_count))

        rate = 0 if self.total_count == 0 else (self.risk_count / self.total_count) * 100
        self.rate_value.config(text=f"{rate:.2f}%")

    def _producer_loop(self):
        while self.running:
            is_exfiltration = random.random() < 0.12
            pkt = random_packet(exfiltration=is_exfiltration)
            features = row_to_features(pkt)

            try:
                score = float(self.model.decision_function(features)[0])
                pred = int(self.model.predict(features)[0])
            except Exception:
                score = 0.0
                pred = 1

            label = "POSSIBLE DATA EXFILTRATION" if pred == -1 else "SAFE TRAFFIC"
            self.q.put((pkt, score, label))

            time.sleep(0.6)

    def _consume_queue(self):
        try:
            while True:
                pkt, score, label = self.q.get_nowait()
                self._insert_row(pkt, score, label)
        except queue.Empty:
            pass
        finally:
            self.after(200, self._consume_queue)

    def _insert_row(self, pkt, score, label):
        self.total_count += 1
        self.row_index += 1
        self.last_scan_time = datetime.now().strftime("%H:%M:%S")

        if label == "POSSIBLE DATA EXFILTRATION":
            self.risk_count += 1
            status = "🔴 Possible Data Exfiltration"
            risk_tag = "risk"
        else:
            status = "🟢 Safe Traffic"
            risk_tag = "safe"

        proto = pkt["protocol"].upper()

        if proto == "TCP":
            proto_text = "🔵 TCP"
        elif proto == "UDP":
            proto_text = "🟠 UDP"
        else:
            proto_text = "🟣 ICMP"

        values = (
            self.last_scan_time,
            proto_text,
            f"{pkt['duration']:.2f}",
            pkt["src_bytes"],
            pkt["dst_bytes"],
            pkt["pkts"],
            f"{pkt['conn_rate']:.2f}",
            pkt["failed_logins"],
            f"{score:.3f}",
            status,
        )

        row_style = "even" if self.row_index % 2 == 0 else "odd"
        tag = f"{risk_tag}_{row_style}"

        iid = self.tree.insert("", "end", values=values, tags=(tag,))

        if len(self.tree.get_children()) > 200:
            self.tree.delete(self.tree.get_children()[0])

        self.tree.see(iid)
        self.tree.yview_moveto(1)

        self._update_stats()

        if self.running:
            self._update_footer(
                "● Monitoring",
                SUCCESS,
                "Isolation Forest Active",
                self.last_scan_time,
            )


def main():
    if MODEL_PATH.exists():
        try:
            model = joblib.load(MODEL_PATH)
            print("Loaded DEPS model from", MODEL_PATH)
        except Exception as e:
            print("Failed to load DEPS model. Will retrain:", e)
            model = train_and_save_model(DATA_PATH, MODEL_PATH)
    else:
        model = train_and_save_model(DATA_PATH, MODEL_PATH)

    app = DEPSApp(model)
    app.mainloop()


if __name__ == "__main__":
    main()