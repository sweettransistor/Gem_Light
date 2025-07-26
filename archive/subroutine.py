import sys
import asyncio
import subprocess
from bleak import BleakClient, BleakScanner

UUID_NUS = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"


async def connect_device(device_name):
    # async with BleakClient(device_name) as client:
    await client.connect()
    if client.is_connected:
        print(f"Connected to {device_name}")

    else:
        print(f"Failed to connect to {device_name}")
        # value = await client.read_gatt_char(received_var)
        # print(f"Value: {value}")

async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == received_var:
            return device
    
async def main():
    device1 = await scan()
    global client
    client = BleakClient(device1)
    await connect_device(device1)
    string_to_send = sys.argv[2]
    bytes_ts = string_to_send.encode("utf-8")
    
    await client.write_gatt_char(UUID_NUS, bytes_ts)
    print(f"Sent: {bytes_ts.decode('utf-8')}")
    await client.disconnect()
    return 0

if __name__ == '__main__':
    received_var = sys.argv[1]
    asyncio.run(main())


