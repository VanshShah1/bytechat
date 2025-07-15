import tkinter as tk
from tkinter import scrolledtext, messagebox
import asyncio
from bleak import BleakScanner, BleakClient

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Bluetooth Chat")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.devices_list = tk.Listbox(self)
        self.devices_list.pack(pady=10)

        self.scan_button = tk.Button(self, text="Scan for Devices", command=self.scan_devices)
        self.scan_button.pack(pady=5)

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
            self.devices_list.insert(tk.END, f"{device.name} ({device.address})")

    def send_message(self):
        message = self.message_entry.get()
        if message:
            # Placeholder for sending message
            self.chat_history.config(state='normal')
            self.chat_history.insert(tk.END, f"Me: {message}\n")
            self.chat_history.config(state='disabled')
            self.message_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
