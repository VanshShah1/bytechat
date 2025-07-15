import tkinter as tk
from tkinter import scrolledtext, messagebox
import asyncio
from bleak import BleakScanner, BleakClient

# Custom UUID for the chat service
CHAT_SERVICE_UUID = "00001101-0000-1000-8000-00805f9b34fb"

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Bluetooth Chat")
        self.pack()
        self.create_widgets()
        self.client = None

    def create_widgets(self):
        self.devices_list = tk.Listbox(self)
        self.devices_list.pack(pady=10)

        self.scan_button = tk.Button(self, text="Scan for Devices", command=self.scan_devices)
        self.scan_button.pack(pady=5)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_to_device)
        self.connect_button.pack(pady=5)

        self.chat_history = scrolledtext.ScrolledText(self, state='disabled')
        self.chat_history.pack(pady=10)

        self.message_entry = tk.Entry(self)
        self.message_entry.pack(pady=5)

        self.send_button = tk.Button(self, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

    def scan_devices(self):
        asyncio.run(self.discover_devices())

    async def discover_devices(self):
        self.devices_list.delete(0, tk.END)
        devices = await BleakScanner.discover()
        for device in devices:
            device_name = device.name if device.name else "Unknown Device"
            self.devices_list.insert(tk.END, f"{device_name} ({device.address})")

    def connect_to_device(self):
        selected_device = self.devices_list.get(self.devices_list.curselection())
        if selected_device:
            device_address = selected_device.split("(")[1].split(")")[0]
            asyncio.run(self.connect(device_address))

    async def connect(self, address):
        try:
            self.client = BleakClient(address)
            await self.client.connect()
            self.chat_history.config(state='normal')
            self.chat_history.insert(tk.END, f"Connected to {address}\n")
            self.chat_history.config(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {e}")

    def send_message(self):
        message = self.message_entry.get()
        if message and self.client:
            # Placeholder for sending message
            self.chat_history.config(state='normal')
            self.chat_history.insert(tk.END, f"Me: {message}\n")
            self.chat_history.config(state='disabled')
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
