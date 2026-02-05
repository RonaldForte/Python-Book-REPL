import json
from datetime import datetime
from domain.circulation import Circulation


class CirculationRepository:
    def __init__(self, filepath: str = "checkout_logs.json"):
        self.filepath = filepath

    def log_circulation(self, circulation: Circulation) -> bool:
        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(json.dumps(circulation.to_dict()) + "\n")
            return True
        except Exception:
            return False

    def get_all_logs(self) -> list[Circulation]:
        try:
            logs = []
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    timestamp = datetime.fromisoformat(data["timestamp"])
                    data = {k: v for k, v in data.items() if k != "timestamp"}
                    logs.append(Circulation(**data, timestamp=timestamp))
            return logs
        except FileNotFoundError:
            return []
