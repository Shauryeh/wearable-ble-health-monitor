import asyncio
from bleak import BleakClient
from src.config import require_band_address

async def main():
    print("Connecting to JCVital band...")
    print("Make sure the JCVital app is fully closed on your phone.\n")

    async with BleakClient(require_band_address()) as client:
        print("Connected:", client.is_connected)
        print("\nListing Bluetooth services and characteristics...\n")

        # For newer Bleak versions
        services = client.services

        for service in services:
            print(f"Service: {service.uuid}")
            print(f"Description: {service.description}")

            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")
                print(f"  Description: {char.description}")
                print(f"  Properties: {char.properties}")

            print()

if __name__ == "__main__":
    asyncio.run(main())
