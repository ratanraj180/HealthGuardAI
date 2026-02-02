from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional

class Component(Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DATABASE = "database"
    API = "api"

class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(Enum):
    DETECTED = "detected"
    DIAGNOSING = "diagnosing"
    FIXED = "fixed"
    VERIFYING = "verifying"
    RESOLVED = "resolved"
    FAILED = "failed"

@dataclass
class Metric:
    component: Component
    name: str
    value: float
    timestamp: datetime

@dataclass
class Log:
    level: str
    message: str
    timestamp: datetime

@dataclass
class Anomaly:
    id: str
    component: Component
    metric: str
    value: float
    threshold: float
    severity: Severity
    confidence: float
    timestamp: datetime

@dataclass
class Diagnosis:
    anomaly_id: str
    root_cause: str
    confidence: float
    evidence: List[str]
    recommendations: List[str]

@dataclass
class Fix:
    action: str
    parameters: Dict[str, Any]
    safe: bool

@dataclass
class IncidentReport:
    id: str
    anomaly: Anomaly
    diagnosis: Diagnosis
    fix: Fix
    verification: Dict[str, Any]
    duration: float
    status: IncidentStatus
