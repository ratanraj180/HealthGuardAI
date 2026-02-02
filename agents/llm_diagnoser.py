from core.models import Diagnosis, Component
import random

class LLMDiagnoserAgent:
    """
    Simulates an LLM-based diagnosis agent.
    In a real scenario, this would call OpenAI/Anthropic/Gemini APIs.
    """
    async def diagnose(self, anomaly, logs):
        # Simulate LLM thinking time
        # In a hackathon, we can pretend the LLM analyzed the data
        root_cause = f"AI analysis indicates {anomaly.component.value} saturation."
        evidence = [log.message for log in logs[-3:]]
        
        recommendation = "Investigate immediately."
        
        if anomaly.component == Component.CPU:
            root_cause = "LLM Analysis: CPU-bound infinite loop detected in 'payment-service' worker thread."
            recommendation = "Restart 'payment-service' and patch loop condition."
        elif anomaly.component == Component.DATABASE:
            root_cause = "LLM Analysis: N+1 query problem detected in 'user-profile' endpoint."
            recommendation = "Cache query results or optimize ORM lookup."
            
        return Diagnosis(
            anomaly_id=anomaly.id,
            root_cause=root_cause,
            confidence=0.92 + random.uniform(-0.05, 0.05),
            evidence=evidence,
            recommendations=[recommendation, "Monitor for recurrence."]
        )
