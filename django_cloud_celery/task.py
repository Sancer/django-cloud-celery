from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from google.protobuf import timestamp_pb2


@dataclass
class Task:
    task_name: str
    url: str
    id: str | None = field(default_factory=lambda: str(uuid4()))
    payload: dict | None = None
    eta: datetime | None = None

    def payload_to_json(self):
        return json.dumps(self.payload)

    def eta_to_timestamp_pb2(self) -> timestamp_pb2.Timestamp:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(self.eta)
        return timestamp
