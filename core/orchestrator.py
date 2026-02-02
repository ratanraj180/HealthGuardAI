import time
import asyncio
import json
import os
from agents.monitor import MonitorAgent
from agents.detector import DetectorAgent
from agents.diagnoser import DiagnoserAgent
from agents.llm_diagnoser import LLMDiagnoserAgent
from agents.fixer import FixerAgent
from agents.verifier import VerifierAgent
from agents.reporter import ReporterAgent
from core.models import IncidentStatus, IncidentReport
from integrations.slack_alert import send_slack_alert

from core.database import DatabaseManager

class HealthGuardOrchestrator:
    def __init__(self):
        self.monitor = MonitorAgent()
        self.detector = DetectorAgent()
        self.diagnoser = DiagnoserAgent()
        self.llm_diagnoser = LLMDiagnoserAgent() # The "Brain"
        self.fixer = FixerAgent()
        self.verifier = VerifierAgent()
        self.reporter = ReporterAgent()
        
        # State
        self.metrics_history = []
        self.incidents = []
        
        # Database
        self.db = DatabaseManager()

    async def run(self):
        print("HealthGuard AI Orchestrator Running...")
        
        while True:
            # 1. Monitor
            metrics, logs = await self.monitor.collect()
            
            # Log metrics to DB
            for m in metrics:
                self.db.log_metric(m.component.value, m.name, m.value)
            
            # 2. Detect
            anomalies = await self.detector.detect(metrics)
            
            if anomalies:
                print(f"⚠️ Detected {len(anomalies)} anomalies. Starting resolution pipeline...")
                send_slack_alert(f"⚠️ Anomaly Detected! Count: {len(anomalies)}")
                
                for anomaly in anomalies:
                    # 3. Diagnose (Combine Standard + LLM)
                    diagnosis = await self.llm_diagnoser.diagnose(anomaly, logs)
                    print(f"🧠 Diagnosis: {diagnosis.root_cause}")
                    
                    # 4. Fix
                    fix = await self.fixer.fix(diagnosis)
                    print(f"🛠️ Applying Fix: {fix.action}")
                    
                    # 5. Verify
                    await asyncio.sleep(2) 
                    new_metrics, _ = await self.monitor.collect()
                    verification = await self.verifier.verify(new_metrics)
                    
                    # 6. Report
                    incident_id = f"INC-{int(time.time())}"
                    status = IncidentStatus.RESOLVED if verification["healthy"] else IncidentStatus.FAILED
                    
                    report = IncidentReport(
                        id=incident_id,
                        anomaly=anomaly,
                        diagnosis=diagnosis,
                        fix=fix,
                        verification=verification,
                        duration=0.0, 
                        status=status
                    )
                    
                    report_str = self.reporter.generate(report)
                    print(report_str)
                    
                    # Add to history and DB
                    self.incidents.append(report)
                    self.db.log_incident(report, report_str)
                    
                    # Notify Slack
                    if verification["healthy"]:
                        send_slack_alert(f"✅ Incident {incident_id} Resolved! Cause: {diagnosis.root_cause}")
                    else:
                        send_slack_alert(f"❌ Incident {incident_id} Failed to resolve.")

            # Sleep before next cycle
            await asyncio.sleep(5)

