import sys
import os
import json
import urllib.request
from typing import Tuple, Optional

from core.constants import APP_VERSION

def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def check_for_updates() -> Tuple[bool, Optional[str], Optional[str]]:
    github_api_url = "https://api.github.com/repos/Karaatin/VSTea/releases/latest"

    try:
        req = urllib.request.Request(github_api_url, headers={'User-Agent': 'VSTea-App'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))

            latest_version = data.get("tag_name", "")
            release_url = data.get("html_url", "")

            if not latest_version:
                return False, None, None

            clean_latest = latest_version.lstrip('v')
            clean_current = APP_VERSION.lstrip('v')

            latest_parts = [int(x) for x in clean_latest.split('.')]
            current_parts = [int(x) for x in clean_current.split('.')]

            if latest_parts > current_parts:
                return True, latest_version, release_url

    except Exception as e:
        pass

    return False, None, None