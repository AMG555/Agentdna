"""Metadata-only activity monitor. Platform adapters can be added behind get_active_window()."""
import asyncio, platform, time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from .privacy_guard import PrivacyGuard
from .platform import active_window
from ..privacy.redaction import redact
@dataclass
class ActivitySnapshot:
    timestamp: str; app_name: str; window_title: str; duration_seconds: int; switch_from: str|None = None
    def to_dict(self): return asdict(self)
class ActivityMonitor:
    def __init__(self, guard: PrivacyGuard): self.guard=guard; self.snapshots=[]; self.previous=None; self.started=time.monotonic()
    def get_active_window(self):
        return active_window()
    async def run(self):
        while True:
            app, title = self.get_active_window()
            if app and self.guard.can_capture(app):
                now=datetime.now(timezone.utc).isoformat(); switch=self.previous if self.previous and self.previous != app else None
                self.snapshots.append(ActivitySnapshot(now, redact(app), redact(title), 10, redact(switch))); self.snapshots=self.snapshots[-10000:]; self.previous=app
            await asyncio.sleep(10)
    def clear(self): self.snapshots.clear()
