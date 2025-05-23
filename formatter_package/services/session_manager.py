import json
import time
from pathlib import Path

SESSION_FILE = Path("sessions/.session.json")
SESSION_TIMEOUT_SECONDS = 3600  # 1 hour

class SessionManager:
    @staticmethod
    def save_session(username: str, role: str):
        with open(SESSION_FILE, "w") as f:
            json.dump({
                "username": username,
                "role": role,
                "timestamp": int(time.time())
            }, f)

    @staticmethod
    def load_session():
        if SESSION_FILE.exists():
            with open(SESSION_FILE, "r") as f:
                session_data = json.load(f)
            if time.time() - session_data.get("timestamp", 0) > SESSION_TIMEOUT_SECONDS:
                SESSION_FILE.unlink()
                return None
            SessionManager.save_session(
                session_data["username"],
                session_data["role"]
            )
            return session_data
        return None

    @staticmethod
    def clear_session():
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()