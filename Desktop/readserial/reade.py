#pip3 install pyserial
#pip install pandas

import serial
import time
import json
import pandas as pd
import os
from datetime import datetime

# Replace '/dev/ttyUSB0' with your actual device file
device ='/dev/ttyS0' #'/dev/ttyUSB0' ##
baud_rate = 9600  # Adjust the baud rate according to your device's specifications

# Open the serial port
ser = serial.Serial(device, baud_rate, timeout=1)
current_datetime = datetime.now().strftime('%Y%m%d_%H%M%S')
# Specify the CSV file path with dynamic filename
csv_file  = f"output_{current_datetime}.csv"

# CSV file to save the data

# Check if the CSV file already exists
if not os.path.isfile(csv_file):
    # Create a new CSV file with headers if it doesn't exist
    df = pd.DataFrame(columns=['timestamp', 'json_data'])
    df.to_csv(csv_file, index=False)

try:
    while True:
        if ser.in_waiting > 0:
            # Read a line of data from the serial port
            #line = ser.readline().decode('utf-8').rstrip()
            line = ser.readline().decode('utf-8').rstrip()
            print("Received:", line)
            # Convert the received line to JSON
            try:
                json_data = json.loads(line)
                predition =json_data["output"]
                stime=json_data["stime"]
                etime=time.time()
                latency=etime-stime
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue

            # Create a DataFrame and append to CSV
            df = pd.DataFrame([[str( etime),str( stime),str( latency), str (predition), json_data]], columns=['etime','stime','latency','prediciton', 'json_data'])

            df.to_csv(csv_file, mode='a', header=False, index=False)
            print(df)
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
    
     

