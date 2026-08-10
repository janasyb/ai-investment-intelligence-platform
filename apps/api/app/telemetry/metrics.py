from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass
class ApplicationMetrics:
    requests_total: int = 0
    responses_5xx_total: int = 0
    _lock: Lock = field(default_factory=Lock, repr=False)

    def record_request(self) -> None:
        with self._lock:
            self.requests_total += 1

    def record_5xx_response(self) -> None:
        with self._lock:
            self.responses_5xx_total += 1

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return {
                "requests_total": self.requests_total,
                "responses_5xx_total": self.responses_5xx_total,
            }


metrics = ApplicationMetrics()
