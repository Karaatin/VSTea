from typing import List, Dict
from core.plugin_model import Plugin

class PluginMerger:
    def __init__(self):
        self._master_library: Dict[str, Plugin] = {}

    def merge_list(self, new_plugins: List[Plugin]):
        for plugin in new_plugins:
            p_id = plugin.id

            if p_id in self._master_library:
                existing_plugin = self._master_library[p_id]
                existing_plugin.merge_with(plugin)
            else:
                self._master_library[p_id] = plugin

    def get_sorted_library(self) -> List[Plugin]:
        all_plugins = list(self._master_library.values())
        all_plugins.sort(key=lambda x: x.name.lower())
        return all_plugins

    def clear(self):
        self._master_library.clear()