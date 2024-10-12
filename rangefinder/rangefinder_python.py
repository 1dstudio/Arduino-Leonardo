# source myenv/bin/activate

import tkinter as tk
import threading
import serial
import time

# Replace with your actual port
arduino_port = '/dev/cu.usbmodem1101'  # e.g., '/dev/ttyACM0' for Linux/Mac, 'COM3' for Windows
baud_rate = 9600

# Flag to control reading state
reading = False

# Function to start reading from the Arduino
def start_reading():
    global reading
    reading = True
    # Create a new thread for reading to avoid freezing the GUI
    threading.Thread(target=read_sensor_data, daemon=True).start()

# Function to stop reading from the Arduino
def stop_reading():
    global reading
    reading = False

# Function to read sensor data
def read_sensor_data():
    global reading
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Allow time for the connection to be established
    
    while reading:
        if ser.in_waiting > 0:
            distance = ser.readline().decode('utf-8').strip()
            distance_label.config(text=f"Distance: {distance} cm")
        time.sleep(0.1)  # Slight delay to avoid overwhelming the serial connection
    
    ser.close()  # Close the serial connection when stopped

# Create the GUI window
window = tk.Tk()
window.title("Ultrasonic Sensor Reader")

# Create and position the label to display distance
distance_label = tk.Label(window, text="Distance: N/A cm", font=("Arial", 14))
distance_label.pack(pady=20)

# Create and position the "Start" button
start_button = tk.Button(window, text="Start Reading", command=start_reading, font=("Arial", 12))
start_button.pack(pady=10)

# Create and position the "Stop" button
stop_button = tk.Button(window, text="Stop Reading", command=stop_reading, font=("Arial", 12))
stop_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()