import tkinter as tk
import socket
import requests
import serial
import threading
import time

class GameClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote Game Controller")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect(("127.0.0.1", 12345))

        # self.sensor_label = tk.Label(root, text="Sensor Data: ")
        # self.sensor_label.pack()

        # self.serial_label = tk.Label(root, text="Serial Data: ")
        # self.serial_label.pack()

        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        tk.Button(self.control_frame, text="Left", command=lambda: self.send_command("left")).grid(row=1, column=0)
        tk.Button(self.control_frame, text="Right", command=lambda: self.send_command("right")).grid(row=1, column=2)
        tk.Button(self.control_frame, text="Up", command=lambda: self.send_command("up")).grid(row=0, column=1)
        tk.Button(self.control_frame, text="Down", command=lambda: self.send_command("down")).grid(row=2, column=1)

        # self.sensor_thread = threading.Thread(target=self.fetch_sensor_data)
        # self.sensor_thread.start()

        # self.serial_thread = threading.Thread(target=self.read_serial_data)
        # self.serial_thread.start()

    def send_command(self, command):
        self.server_socket.send(command.encode())

    # def fetch_sensor_data(self):
    #     while True:
    #         try:
    #             response = requests.get("https://api.example.com/sensor") #Replace with a real or mock api.
    #             data = response.json()["value"]
    #             self.sensor_label.config(text=f"Sensor Data: {data}")
    #         except Exception as e:
    #             self.sensor_label.config(text=f"Sensor Data: Error - {e}")
    #         time.sleep(1)

    # def read_serial_data(self):
    #     try:
    #         ser = serial.Serial('COM3', 9600)  # Replace 'COM3' with your serial port.
    #         while True:
    #             line = ser.readline().decode('utf-8').strip()
    #             self.serial_label.config(text=f"Serial Data: {line}")
    #             time.sleep(0.1)
    #     except serial.SerialException as e:
    #         self.serial_label.config(text=f"Serial Data: Error - {e}")

root = tk.Tk()
client = GameClient(root)
root.mainloop()