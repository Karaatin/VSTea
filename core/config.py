import json
from core.environment import Environment

class ConfigManager:
    def __init__(self):
        sys_info = Environment.detect()
        self.config_dir = sys_info.config_path / "VSTea"

        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "config.json"

        self.settings = {
            "theme": "matcha",
            "auto_updates": True
        }

        self.load()

    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self.settings.update(loaded_data)
            except Exception as e:
                print(f"[WARNING] Could not read config: {e}")

    def save(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"[ERROR] Could not save config: {e}")

    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value):
        self.settings[key] = value
        self.save()