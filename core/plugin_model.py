from dataclasses import dataclass, field
from typing import List, Set, Dict

@dataclass
class Plugin:
    name: str
    vendor: str = "Unknown"
    category: str = "Uncategorized"

    formats: Set[str] = field(default_factory=set)
    detected_by: Set[str] = field(default_factory=set)

    instances: List[Dict[str, str]] = field(default_factory=list)

    @property
    def id(self) -> str:
        return self.name.lower().strip()

    def merge_with(self, other: 'Plugin'):
        self.formats.update(other.formats)
        self.detected_by.update(other.detected_by)

        for instance in other.instances:
            if instance not in self.instances:
                self.instances.append(instance)

        if self.category == "Uncategorized" and other.category != "Uncategorized":
            self.category = other.category

    def to_dict(self):
        return {
            "name": self.name,
            "vendor": self.vendor,
            "category": self.category,
            "formats": list(sorted(self.formats)),
            "detected_by": list(sorted(self.detected_by)),
            "instances": self.instances
        }