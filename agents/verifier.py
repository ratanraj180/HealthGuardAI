from config.settings import RECOVERY_LIMITS

class VerifierAgent:
    async def verify(self, metrics):
        # Default to healthy
        healthy = True
        details = {}
        
        for m in metrics:
            key = f"{m.component.value}.{m.name}"
            limit = RECOVERY_LIMITS.get(key)
            
            if limit and m.value > limit:
                healthy = False
                details[key] = f"Value {m.value:.2f} exceeds recovery limit {limit}"
        
        return {
            "healthy": healthy,
            "details": details
        }
