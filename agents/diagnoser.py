from core.models import Diagnosis, Component

class DiagnoserAgent:
    async def diagnose(self, anomaly, logs):
        root = "Unknown"
        recs = []
        
        if anomaly.component == Component.CPU:
            root = "CPU-intensive process detected"
            recs = ["Restart service", "Check recent deployments"]
        elif anomaly.component == Component.MEMORY:
            root = "Memory leak suspected"
            recs = ["Restart service", "Increase memory limit"]
        elif anomaly.component == Component.DATABASE:
            root = "Slow queries or connection pool exhaustion"
            recs = ["Clear DB cache", "Optimize queries"]
        elif anomaly.component == Component.API:
            root = "High latency in upstream service"
            recs = ["Check network", "Scale up API"]

        evidence = [log.message for log in logs if log.level == "ERROR"]

        return Diagnosis(
            anomaly_id=anomaly.id,
            root_cause=root,
            confidence=0.85,
            evidence=evidence,
            recommendations=recs
        )
