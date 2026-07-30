"""The mandatory gate before any observer access."""
from datetime import datetime, timedelta

DEFAULT_BLOCKED = {"1password", "bitwarden", "lastpass", "keepass", "banking", "incognito", "private browsing"}
class PrivacyGuard:
    def __init__(self):
        self.monitoring_enabled = False  # explicit opt-in: safe default
        self.allowed_apps: set[str] = set()
        self.blocked_apps = set(DEFAULT_BLOCKED)
    def pause(self): self.monitoring_enabled = False
    def resume(self): self.monitoring_enabled = True
    def allow(self, app_name: str): self.allowed_apps.add(app_name.lower())
    def can_capture(self, app_name: str) -> bool:
        name = app_name.lower()
        return self.monitoring_enabled and any(x in name for x in self.allowed_apps) and not any(x in name for x in self.blocked_apps)
    def to_dict(self): return {"monitoring_enabled": self.monitoring_enabled, "allowed_apps": sorted(self.allowed_apps), "blocked_apps": sorted(self.blocked_apps)}
