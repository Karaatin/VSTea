import os
from pathlib import Path
from typing import List, Dict, Callable, Optional

from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class FLStudioParser(BaseParser):

    def is_valid(self) -> bool:
        if not self.config_path.exists():
            return False
        return (self.config_path / "Effects").exists() or (self.config_path / "Generators").exists()

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        if not self.is_valid():
            return []

        plugins = []
        categories = ["Effects", "Generators"]

        for cat in categories:
            cat_path = self.config_path / cat
            if not cat_path.exists():
                continue

            if progress_callback:
                progress_callback(f"Scanning FL {cat}...")

            for root, dirs, files in os.walk(cat_path):
                root_path = Path(root)

                upper_parts = [p.upper() for p in root_path.parts]

                for file in files:
                    if file.lower().endswith(".fst"):
                        fst_path = root_path / file
                        nfo_path = fst_path.with_suffix(".nfo")

                        nfo_data = self._parse_nfo(nfo_path)

                        plugin_name = nfo_data.get("ps_name")

                        if not plugin_name:
                            for k, v in nfo_data.items():
                                if "file_name" in k:
                                    plugin_name = v
                                    break

                        if not plugin_name:
                            plugin_name = file[:-4]

                        vendor = nfo_data.get("vendor") or nfo_data.get("vendor name", "Unknown")

                        if vendor == "Unknown":
                            for k, v in nfo_data.items():
                                if "vendorname" in k:
                                    vendor = v
                                    break

                        fmt_str = PluginFormat.UNKNOWN.value

                        if "VST3" in upper_parts:
                            fmt_str = PluginFormat.VST3.value
                        elif "VST2" in upper_parts or "VST" in upper_parts:
                            fmt_str = PluginFormat.VST2.value
                        elif "CLAP" in upper_parts:
                            fmt_str = PluginFormat.CLAP.value
                            # FIX: Wir prüfen auf "AU" und auf "AUDIOUNIT" im Ordnernamen!
                        elif "AU" in upper_parts or "AUDIOUNIT" in upper_parts:
                            fmt_str = PluginFormat.AU.value
                        elif "FRUITY" in upper_parts:
                            fmt_str = PluginFormat.STOCK.value
                            vendor = "Image-Line"

                        if fmt_str == PluginFormat.UNKNOWN.value:
                            for k, v in nfo_data.items():
                                if "file_filename" in k:
                                    v_lower = v.lower()
                                    if ".vst3" in v_lower:
                                        fmt_str = PluginFormat.VST3.value
                                    elif ".dll" in v_lower or ".vst" in v_lower:
                                        fmt_str = PluginFormat.VST2.value
                                    elif ".clap" in v_lower:
                                        fmt_str = PluginFormat.CLAP.value
                                    elif ".component" in v_lower or "audiounit" in v_lower:
                                        fmt_str = PluginFormat.AU.value

                                    if fmt_str != PluginFormat.UNKNOWN.value:
                                        break

                        if fmt_str == PluginFormat.AU.value and vendor == "Unknown" and plugin_name.startswith("AU"):
                            vendor = "Apple"

                        if vendor.lower() in ["apple", "image-line"]:
                            fmt_str = PluginFormat.STOCK.value

                        instance_data = {
                            "daw": "FL Studio",
                            "format": fmt_str,
                            "path": str(fst_path)
                        }

                        p = Plugin(
                            name=plugin_name,
                            vendor=vendor,
                            category=cat,
                            formats={fmt_str},
                            detected_by={"FL Studio"},
                            instances=[instance_data]
                        )
                        plugins.append(p)

        return plugins

    def _parse_nfo(self, path: Path) -> Dict[str, str]:
        data = {}
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "=" in line:
                        key, val = line.split("=", 1)
                        data[key.strip().lower()] = val.strip()
        except Exception:
            pass
        return data