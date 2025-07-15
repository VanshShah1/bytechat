import asyncio
import sys
import logging

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.service import BleakGATTService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# UUIDs for our custom service and characteristic
CHAT_SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAT_CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"

async def chat_server():
    logging.info("Starting chat server...")
    # In a real application, you would advertise a service here.
    # Bleak does not directly support advertising on all platforms, especially macOS.
    # For macOS, you might need to use CoreBluetooth directly or a different library
    # that wraps CoreBluetooth for advertising.
    # For simplicity, this example will assume a client knows the server's address
    # or can discover it through other means (e.g., a pre-shared address or a separate discovery mechanism).
    # This part of the server is a placeholder for receiving messages.

    logging.warning("Bleak does not directly support BLE advertising on macOS. "
                    "You will need to manually provide the server's Bluetooth address to the client, "
                    "or use a different tool/library for advertising on macOS.")

    # Placeholder for server logic to receive messages
    # For a true server, you'd need to set up a GATT server with characteristics
    # that clients can write to. Bleak is primarily a client library.
    # This example will focus on the client side connecting and writing.
    # To make this a functional server, you'd need a peripheral role implementation.
    # For now, this server function will just log that it's waiting.
    logging.info("Server is waiting for a client to connect and send messages (manual connection required for now).")
    while True:
        await asyncio.sleep(1) # Keep the server running

async def chat_client(server_address: str):
    logging.info(f"Starting chat client, connecting to {server_address}...")
    async with BleakClient(server_address) as client:
        if client.is_connected:
            logging.info(f"Connected to {server_address}")
            # Discover services and characteristics
            for service in client.services:
                logging.info(f"Service: {service.uuid}")
                for char in service.characteristics:
                    logging.info(f"  Characteristic: {char.uuid}, Properties: {char.properties}")

            # Find our chat characteristic
            chat_char: BleakGATTCharacteristic = None
            for service in client.services:
                for char in service.characteristics:
                    if char.uuid == CHAT_CHARACTERISTIC_UUID:
                        chat_char = char
                        break
                if chat_char:
                    break

            if not chat_char:
                logging.error(f"Chat characteristic {CHAT_CHARACTERISTIC_UUID} not found.")
                return

            logging.info("Type your message and press Enter to send. Type 'exit' to quit.")
            while True:
                message = await asyncio.to_thread(input, "You: ")
                if message.lower() == 'exit':
                    break
                try:
                    # Write the message to the characteristic
                    await client.write_gatt_char(chat_char, message.encode('utf-8'))
                    logging.info(f"Sent: {message}")
                except Exception as e:
                    logging.error(f"Failed to send message: {e}")
        else:
            logging.error(f"Failed to connect to {server_address}")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python chat_app.py server")
        print("       python chat_app.py client <server_bluetooth_address>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "server":
        await chat_server()
    elif mode == "client":
        if len(sys.argv) < 3:
            print("Usage: python chat_app.py client <server_bluetooth_address>")
            sys.exit(1)
        server_address = sys.argv[2]
        await chat_client(server_address)
    else:
        print("Invalid mode. Use 'server' or 'client'.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
