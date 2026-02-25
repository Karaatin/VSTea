import sqlite3
from pathlib import Path
from typing import List, Callable, Optional

from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class AbletonParser(BaseParser):

    def is_valid(self) -> bool:
        if not self.config_path or not self.config_path.exists():
            return False

        return self._get_target_db() is not None

    def _get_target_db(self) -> Optional[Path]:
        if not self.config_path or not self.config_path.exists():
            return None

        plugin_dbs = list(self.config_path.glob("Live-plugins-*.db"))
        if plugin_dbs:
            plugin_dbs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return plugin_dbs[0]

        file_dbs = list(self.config_path.glob("Live-files-*.db"))
        if file_dbs:
            file_dbs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return file_dbs[0]

        return None

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        if not self.is_valid():
            return []

        db_file = self._get_target_db()
        plugins = []

        if progress_callback:
            progress_callback(f"Reading Ableton Database: {db_file.name}...")

        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='plugins';")
            if not cursor.fetchone():
                conn.close()
                return []

            cursor.execute("SELECT dev_identifier, name, vendor FROM plugins WHERE name IS NOT NULL;")
            rows = cursor.fetchall()

            for row in rows:
                data = dict(row)

                plugin_name = data.get("name")
                vendor = data.get("vendor")
                dev_id = str(data.get("dev_identifier", "")).lower()

                if not vendor or str(vendor).strip() == "":
                    vendor = "Unknown"

                fmt_str = PluginFormat.UNKNOWN.value

                if ":vst3:" in dev_id:
                    fmt_str = PluginFormat.VST3.value
                elif ":vst:" in dev_id or ":vst2:" in dev_id:
                    fmt_str = PluginFormat.VST2.value
                elif ":au:" in dev_id or "audiounit" in dev_id:
                    fmt_str = PluginFormat.AU.value
                elif ":clap:" in dev_id:
                    fmt_str = PluginFormat.CLAP.value

                p = Plugin(
                    name=str(plugin_name),
                    vendor=str(vendor),
                    formats={fmt_str},
                    detected_by={"Ableton Live"},
                    instances=[{"daw": "Ableton Live", "format": fmt_str, "path": "Internal Ableton DB"}]
                )
                plugins.append(p)

            conn.close()

        except Exception as e:
            print(f"[Ableton Parser] Error reading DB: {e}")

        return plugins