from enum import Enum

class OSType(Enum):
    WINDOWS = "Windows"
    MACOS = "Darwin"
    LINUX = "Linux"
    UNKNOWN = "Unknown"

class DawID(Enum):
    ABLETON = "Ableton Live"
    BITWIG = "Bitwig Studio"
    CUBASE = "Cubase"
    FL_STUDIO = "FL Studio"
    LOGIC = "Logic Pro"
    REAPER = "Reaper"
    STUDIO_ONE = "Studio One"

class PluginFormat(Enum):
    AU = "AU"
    AAX = "AAX"
    CLAP = "CLAP"
    STOCK = "STOCK"
    UNKNOWN = "UNKNOWN"
    VST2 = "VST2"
    VST3 = "VST3"
