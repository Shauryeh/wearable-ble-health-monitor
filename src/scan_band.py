import asyncio
from bleak import BleakScanner

async def main():
    print("Scanning for Bluetooth devices for 15 seconds...")
    print("Make sure your JCVital app is closed on your phone.\n")

    results = await BleakScanner.discover(
        timeout=15,
        return_adv=True
    )

    if not results:
        print("No Bluetooth devices found.")
        return

    for i, (address, data) in enumerate(results.items()):
        device, adv = data
        name = device.name or adv.local_name or "Unknown"
        rssi = adv.rssi if hasattr(adv, "rssi") else "N/A"

        print(f"{i}: name={name}, address={address}, rssi={rssi}")

if __name__ == "__main__":
    asyncio.run(main())
