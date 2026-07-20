"""Runtime configuration loaded from environment variables."""

import os
from pathlib import Path


BAND_ADDRESS = os.getenv("JCVITAL_BAND_ADDRESS", "")
NOTIFY_UUID = os.getenv(
    "JCVITAL_NOTIFY_UUID",
    "0000fff7-0000-1000-8000-00805f9b34fb",
)
CSV_FILE = Path(os.getenv("JCVITAL_CSV_FILE", "data/jcvital_live_data.csv"))


def require_band_address() -> str:
    """Return the configured BLE address or raise an actionable error."""
    if not BAND_ADDRESS:
        raise RuntimeError(
            "Set JCVITAL_BAND_ADDRESS before connecting. "
            "Run `python -m src.scan_band` to discover nearby devices."
        )
    return BAND_ADDRESS
