import os
import json
from pathlib import Path
from typing import List, Callable, Optional

from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class BitwigParser(BaseParser):
    def is_valid(self) -> bool:
        if not self.config_path.is_dir():
            return False

        scan_path = self.config_path
        if "AppData" in str(scan_path) or "Library/Application Support" in str(scan_path):
            from pathlib import Path
            docs_lib = Path.home() / "Documents" / "Bitwig Studio" / "Library"
            if docs_lib.exists():
                return True

        return "Bitwig Studio" in str(scan_path) or (scan_path / "Presets").exists()

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        if not self.is_valid(): return []

        plugins = []
        scan_path = self.config_path

        if "AppData" in str(scan_path) or "Library/Application Support" in str(scan_path):
            user_home = Path.home()
            docs_lib = user_home / "Documents" / "Bitwig Studio" / "Library"
            if docs_lib.exists():
                scan_path = docs_lib

        if progress_callback:
            progress_callback(f"Scanning Library...")

        for root, dirs, files in os.walk(scan_path):
            for file in files:
                if file.endswith(".bwpreset"):
                    full_path = Path(root) / file
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            data = json.load(f)
                            meta = data.get("meta_data", {})

                            plugin_name = meta.get("plugin_name")
                            vendor = meta.get("vendor", "Bitwig")

                            if not plugin_name:
                                plugin_name = file.rsplit('.', 1)[0]

                            data_str = str(data).lower()

                            if "clap" in data_str:
                                fmt = PluginFormat.CLAP.value
                            elif "vst3" in data_str:
                                fmt = PluginFormat.VST3.value
                            elif "vst" in data_str:
                                fmt = PluginFormat.VST2.value
                            else:
                                fmt = PluginFormat.STOCK.value

                            p = Plugin(
                                name=plugin_name,
                                vendor=vendor,
                                category="Bitwig Preset",
                                formats={fmt},
                                detected_by={"Bitwig Studio"},
                                instances=[{"daw": "Bitwig", "format": fmt, "path": str(full_path)}]
                            )
                            plugins.append(p)
                    except Exception:
                        pass

        return plugins