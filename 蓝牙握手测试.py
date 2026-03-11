import serial
import time

# 改成你的传出COM口（比如COM5、COM7等）
BLUETOOTH_PORT = 'COM5'  # <--- 改成传出端口
BAUD_RATE = 9600

try:
    print(f"正在连接传出端口 {BLUETOOTH_PORT}...")
    ser = serial.Serial(BLUETOOTH_PORT, BAUD_RATE, timeout=5)
    time.sleep(2)
    
    print("发送连接请求...")
    ser.write(b'H')
    
    print("等待回复...")
    response = ser.readline().decode().strip()
    
    if response:
        print(f"收到: {response}")
        if response == "连接成功":
            print("✓ 蓝牙连接测试成功！")
    else:
        print("✗ 没有收到回复")
    
    ser.close()
    
except serial.SerialException as e:
    print(f"连接失败: {e}")
    print("请确认使用的是传出COM口")