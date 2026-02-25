from typing import List, Callable, Optional

from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class ReaperParser(BaseParser):
    def is_valid(self) -> bool:
        if not self.config_path.is_dir():
            return False

        ini_files = [
            self.config_path / "reaper-vstplugins64.ini",
            self.config_path / "reaper-vstplugins.ini",
            self.config_path / "reaper-auplugins64.ini",
        ]
        return any(f.exists() for f in ini_files)

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        if not self.is_valid(): return []

        plugins = []
        ini_files = [
            self.config_path / "reaper-vstplugins64.ini",
            self.config_path / "reaper-vstplugins.ini",
            self.config_path / "reaper-auplugins64.ini",
        ]

        for ini_path in ini_files:
            if not ini_path.exists(): continue

            if progress_callback:
                progress_callback(f"Reading {ini_path.name}...")

            try:
                with open(ini_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()

                for line in lines:
                    if "=" not in line or line.startswith("["): continue

                    parts = line.split("=", 1)
                    file_path_str = parts[0].strip()
                    value_part = parts[1].strip()

                    details = value_part.split(",", 1)
                    if len(details) < 2: continue

                    raw_name = details[1]
                    fmt = PluginFormat.UNKNOWN.value

                    if ini_path.name.startswith("reaper-au"):
                        fmt = PluginFormat.AU.value
                    elif ".vst3" in file_path_str.lower():
                        fmt = PluginFormat.VST3.value
                    elif ".dll" in file_path_str.lower():
                        fmt = PluginFormat.VST2.value
                    elif ".clap" in file_path_str.lower():
                        fmt = PluginFormat.CLAP.value
                    elif ".vst" in file_path_str.lower():
                        fmt = PluginFormat.VST2.value

                    name = raw_name
                    vendor = "Unknown"

                    if "!!!" in name: name = name.split("!!!")[0]

                    if "(" in name and name.endswith(")"):
                        try:
                            last_open = name.rfind("(")
                            vendor = name[last_open + 1:-1]
                            name = name[:last_open].strip()
                        except:
                            pass

                    p = Plugin(
                        name=name.strip(),
                        vendor=vendor.strip(),
                        category="Uncategorized",
                        formats={fmt},
                        detected_by={"Reaper"},
                        instances=[{"daw": "Reaper", "format": fmt, "path": file_path_str}]
                    )
                    plugins.append(p)

            except Exception as e:
                print(f"Error reading Reaper INI {ini_path}: {e}")

        return plugins