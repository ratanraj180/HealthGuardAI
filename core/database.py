import sqlite3
import json
from datetime import datetime
import os

DB_FILE = "healthguard.db"

class DatabaseManager:
    def __init__(self):
        # Connect to DB (creates it if not exists)
        # check_same_thread=False is needed for Streamlit + Asyncio concurrency
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Metrics Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                component TEXT,
                name TEXT,
                value REAL
            )
        ''')

        # Incidents Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                status TEXT,
                anomaly_component TEXT,
                root_cause TEXT,
                fix_action TEXT,
                full_report TEXT
            )
        ''')
        self.conn.commit()

    def log_metric(self, component, name, value):
        try:
            cursor = self.conn.cursor()
            timestamp = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO metrics (timestamp, component, name, value)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, component, name, value))
            self.conn.commit()
        except Exception as e:
            print(f"DB Error (log_metric): {e}")

    def log_incident(self, report, full_report_str):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO incidents (id, timestamp, status, anomaly_component, root_cause, fix_action, full_report)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                report.id,
                datetime.now().isoformat(),
                report.status.value,
                report.anomaly.component.value,
                report.diagnosis.root_cause,
                report.fix.action,
                full_report_str
            ))
            self.conn.commit()
        except Exception as e:
            print(f"DB Error (log_incident): {e}")
    
    def get_latest_metrics(self, limit=100):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM metrics ORDER BY id DESC LIMIT ?', (limit,))
            return cursor.fetchall()
        except Exception:
            return []
        
    def get_incidents(self, limit=10):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT * FROM incidents ORDER BY timestamp DESC LIMIT ?', (limit,))
            return cursor.fetchall()
        except Exception:
            return []
