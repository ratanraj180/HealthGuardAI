import time
import hashlib
from config.settings import THRESHOLDS
from core.models import Anomaly, Severity

class DetectorAgent:
    async def detect(self, metrics):
        anomalies = []

        for m in metrics:
            key = f"{m.component.value}.{m.name}"
            threshold = THRESHOLDS.get(key)
            
            if threshold and m.value > threshold:
                aid = hashlib.md5(f"{key}{time.time()}".encode()).hexdigest()[:8]
                
                # Determine severity
                severity = Severity.HIGH
                if m.value > threshold * 1.5:
                    severity = Severity.CRITICAL
                elif m.value < threshold * 1.1:
                    severity = Severity.MEDIUM
                
                anomalies.append(
                    Anomaly(
                        id=aid,
                        component=m.component,
                        metric=m.name,
                        value=m.value,
                        threshold=threshold,
                        severity=severity,
                        confidence=0.85, # Static for rule-based, could be dynamic
                        timestamp=m.timestamp
                    )
                )
        return anomalies
