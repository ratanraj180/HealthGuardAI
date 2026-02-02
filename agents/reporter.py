from datetime import datetime

class ReporterAgent:
    def generate(self, report):
        status_icon = "✅" if report.verification['healthy'] else "❌"
        
        return f"""
====================================================
HEALTHGUARD AI – INCIDENT REPORT
====================================================
Incident ID : {report.id}
Timestamp   : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Status      : {report.status.value.upper()} {status_icon}
Duration    : {report.duration:.2f}s

--- ANOMALY ---
Component   : {report.anomaly.component.value}
Metric      : {report.anomaly.metric}
Value       : {report.anomaly.value:.2f}
Severity    : {report.anomaly.severity.value}

--- DIAGNOSIS (AI Powered) ---
Root Cause  : {report.diagnosis.root_cause}
Confidence  : {report.diagnosis.confidence:.2f}
Evidence    : {report.diagnosis.evidence}

--- AUTOMATED ACTION ---
Fix Action  : {report.fix.action}
Parameters  : {report.fix.parameters}

--- VERIFICATION ---
Result      : {"Success" if report.verification['healthy'] else "Failed"}
Details     : {report.verification.get('details', 'N/A')}

====================================================
"""
