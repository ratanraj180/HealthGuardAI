import random
from datetime import datetime
from core.models import Metric, Log, Component

class MonitorAgent:
    def __init__(self):
        # Simulation baselines
        self.cpu_baseline = 0.4
        self.memory_baseline = 0.5
        self.db_latency_baseline = 100
        self.api_latency_baseline = 150

    async def collect(self):
        now = datetime.now()
        
        # Simulate some fluctuation
        cpu = max(0.0, min(1.0, self.cpu_baseline + random.uniform(-0.1, 0.4)))
        # Occasional spike
        if random.random() < 0.1:
            cpu = random.uniform(0.8, 1.0)
            
        memory = max(0.0, min(1.0, self.memory_baseline + random.uniform(-0.05, 0.1)))
        
        db_latency = max(10, self.db_latency_baseline + random.uniform(-20, 100))
        # Occasional latency spike
        if random.random() < 0.05:
            db_latency = random.uniform(300, 600)
            
        api_latency = max(10, self.api_latency_baseline + random.uniform(-30, 150))

        metrics = [
            Metric(Component.CPU, "usage", cpu, now),
            Metric(Component.MEMORY, "usage", memory, now),
            Metric(Component.DATABASE, "latency", db_latency, now),
            Metric(Component.API, "latency", api_latency, now),
        ]

        logs = []
        if cpu > 0.85:
            logs.append(Log("ERROR", "High CPU usage detected", now))
        if db_latency > 300:
            logs.append(Log("WARN", "Database query slow", now))

        return metrics, logs
