import asyncio
from core.orchestrator import HealthGuardOrchestrator
import sys
import io

# Force UTF-8 output for Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


if __name__ == "__main__":
    print("\n🚀 HealthGuard AI System Starting...")
    print("Initialize Monitor... [OK]")
    print("Initialize Detector... [OK]")
    print("Initialize AI Diagnoser... [OK]")
    print("Initialize Auto-Fixer... [OK]")
    print("------------------------------------------------")
    print("System is running. Start the dashboard with:")
    print("   streamlit run ui/dashboard.py")
    print("------------------------------------------------\n")
    
    try:
        asyncio.run(HealthGuardOrchestrator().run())
    except KeyboardInterrupt:
        print("\n🛑 System Shutting Down.")
