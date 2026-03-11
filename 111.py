import serial
import serial.tools.list_ports
import dotenv
import os
dotenv.load_dotenv()
ser = serial.Serial(port=os.getenv('COM'),timeout=5)
