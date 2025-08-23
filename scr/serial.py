import serial
import time

# Khởi tạo serial (anh chỉnh lại /dev/ttyUSB0 cho đúng với cổng ESP32 của anh)
ser = serial.Serial(
    port="/dev/ttyUSB0",  # trên Windows có thể là "COM3"
    baudrate=115200,
    timeout=1
)

# Chờ ESP32 reset xong
time.sleep(2)

def send_message(speed: int, angle: int):
    """
    Gửi lệnh điều khiển tới ESP32 qua Serial USB.
    speed : int   -> giá trị tốc độ (-100 .. 100)
    angle : int   -> góc bẻ lái (10 .. 170)
    """
    message = f"s{speed}a{angle}\n"
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message.strip()}")

# Ví dụ sử dụng
if __name__ == "__main__":
    send_message(50, 120)   # speed=50, angle=120
    time.sleep(1)
    send_message(-30, 90)   # speed=-30, angle=90
