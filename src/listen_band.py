import asyncio
from datetime import datetime
from bleak import BleakClient
from src.config import require_band_address

NOTIFY_CHARACTERISTICS = [
    "0000fff7-0000-1000-8000-00805f9b34fb",
    "00000003-0000-1000-8000-00805f9b34fb",
    "00000005-0000-1000-8000-00805f9b34fb",
    "a6ed0402-d344-460a-8075-b9e8ec90d71b",
]

def notification_handler(sender, data):
    timestamp = datetime.now().strftime("%H:%M:%S")
    hex_data = data.hex(" ")
    int_data = list(data)

    print("\n--- Notification received ---")
    print("Time:", timestamp)
    print("From:", sender)
    print("HEX:", hex_data)
    print("INT:", int_data)

async def main():
    print("Connecting to JCVital band...")
    print("Turn OFF Bluetooth on your phone first.\n")

    async with BleakClient(require_band_address()) as client:
        print("Connected:", client.is_connected)

        for uuid in NOTIFY_CHARACTERISTICS:
            try:
                await client.start_notify(uuid, notification_handler)
                print("Listening on:", uuid)
            except Exception as e:
                print("Could not listen on:", uuid)
                print("Reason:", e)

        print("\nNow wear the band, move around, press the band button, or trigger a measurement if possible.")
        print("Listening for 2 minutes...\n")

        await asyncio.sleep(120)

        for uuid in NOTIFY_CHARACTERISTICS:
            try:
                await client.stop_notify(uuid)
            except Exception:
                pass

        print("Done listening.")

if __name__ == "__main__":
    asyncio.run(main())
