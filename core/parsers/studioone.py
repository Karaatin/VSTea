import xml.etree.ElementTree as ET
from typing import List, Callable, Optional
from .base_parser import BaseParser
from core.plugin_model import Plugin
from core.enums import PluginFormat

class StudioOneParser(BaseParser):
    def is_valid(self) -> bool:
        if not self.config_path.is_dir():
            return False

        possible_files = [
            self.config_path / "x64" / "Vstplugins.settings",
            self.config_path / "Vstplugins.settings",
            self.config_path / "x64" / "PlugInInfos.settings"
        ]

        return any(f.exists() for f in possible_files)

    def parse(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[Plugin]:
        if not self.is_valid():
            return []

        plugins = []
        possible_files = [
            self.config_path / "x64" / "Vstplugins.settings",
            self.config_path / "Vstplugins.settings",
            self.config_path / "x64" / "PlugInInfos.settings"
        ]

        for xml_file in possible_files:
            if not xml_file.exists():
                continue

            if progress_callback:
                progress_callback(f"Reading {xml_file.name}...")

            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()

                for elem in root.iter():
                    if "path" in elem.attrib and "name" in elem.attrib:
                        path_str = elem.attrib["path"]
                        name = elem.attrib["name"]
                        vendor = elem.attrib.get("vendor", "Unknown")

                        fmt = PluginFormat.UNKNOWN.value
                        if ".vst3" in path_str.lower():
                            fmt = PluginFormat.VST3.value
                        elif ".dll" in path_str.lower() or ".vst" in path_str.lower():
                            fmt = PluginFormat.VST2.value
                        elif ".component" in path_str.lower():
                            fmt = PluginFormat.AU.value

                        subCategory = elem.attrib.get("subCategory", "Uncategorized")

                        p = Plugin(
                            name=name,
                            vendor=vendor,
                            category=subCategory,
                            formats={fmt},
                            detected_by={"Studio One"},
                            instances=[{"daw": "Studio One", "format": fmt, "path": path_str}]
                        )
                        plugins.append(p)
            except Exception as e:
                print(f"Error parsing Studio One XML: {e}")

        return plugins