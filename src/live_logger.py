import asyncio
import argparse
import csv
from datetime import datetime
from bleak import BleakClient
from src.config import CSV_FILE, NOTIFY_UUID, require_band_address

def clean_hr(value):
    if value is None:
        return None
    if value == 0:
        return None
    if value < 35 or value > 220:
        return None
    return value

def clean_spo2(value):
    if value is None:
        return None
    if value < 70 or value > 100:
        return None
    return value

def notification_handler(sender, data):
    timestamp = datetime.now().isoformat()
    values = list(data)
    raw_hex = data.hex(" ")

    raw_hr = values[21] if len(values) > 21 else None
    raw_spo2 = values[22] if len(values) > 22 else None
    status = values[23] if len(values) > 23 else None

    heart_rate = clean_hr(raw_hr)
    spo2 = clean_spo2(raw_spo2)

    print(
        f"{timestamp} | "
        f"HR {heart_rate if heart_rate is not None else 'invalid'} bpm | "
        f"SpO2 {spo2 if spo2 is not None else 'invalid'}% | "
        f"status {status} | raw HR {raw_hr} | raw SpO2 {raw_spo2}"
    )

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp,
            heart_rate,
            spo2,
            status,
            raw_hr,
            raw_spo2,
            raw_hex
        ])

async def main(duration_minutes: float = 30.0):
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "timestamp",
            "heart_rate",
            "spo2",
            "status",
            "raw_hr",
            "raw_spo2",
            "raw_hex"
        ])

    print("Connecting to JCVital band...")
    print("Turn OFF Bluetooth on your phone first.\n")

    async with BleakClient(require_band_address()) as client:
        print("Connected:", client.is_connected)
        print("Logging live data to:", CSV_FILE)
        print(f"Wear the band. Logging for {duration_minutes:g} minutes...\n")

        await client.start_notify(NOTIFY_UUID, notification_handler)

        await asyncio.sleep(duration_minutes * 60)

        await client.stop_notify(NOTIFY_UUID)
        print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log live BLE packets from a JCVital band.")
    parser.add_argument(
        "--minutes",
        type=float,
        default=30.0,
        help="How long to collect notifications (default: 30).",
    )
    args = parser.parse_args()
    asyncio.run(main(args.minutes))
