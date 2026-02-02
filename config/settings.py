# All system configuration in ONE place

THRESHOLDS = {
    "cpu.usage": 0.85,
    "memory.usage": 0.85,
    "database.latency": 300,
    "api.latency": 400
}

RECOVERY_LIMITS = {
    "cpu.usage": 0.75,
    "memory.usage": 0.75,
    "database.latency": 200,
    "api.latency": 250
}

SIMULATION = True # Set to False for real production use
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/FAKE/WEBHOOK/URL" # Replace with real URL
