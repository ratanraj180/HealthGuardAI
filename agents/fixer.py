from core.models import Fix, Component
import asyncio

class FixerAgent:
    async def fix(self, diagnosis):
        action = "notify_only"
        params = {}
        safe = True

        root_cause_lower = diagnosis.root_cause.lower()

        if "cpu" in root_cause_lower:
            action = "restart_service"
            params = {"service": "api-worker"}
        elif "database" in root_cause_lower:
            action = "clear_db_cache"
            params = {"scope": "global"}
        elif "memory" in root_cause_lower:
            action = "restart_service"
            params = {"service": "memory-hog-service"}
        elif "api" in root_cause_lower:
            action = "scale_up"
            params = {"replicas": 3}

        # Simulate fix execution time
        await asyncio.sleep(1)

        return Fix(action, params, safe)
