from debugpy import connect
import serial, time

PORT = "COM7"          # hoặc "/dev/ttyUSB0"
BAUD = 115200
class Connect:
    def __init__(self):
        self.ser = serial.Serial(port=PORT, baudrate=BAUD, timeout=1, write_timeout=1)
        # tránh reset ESP32 (tuỳ board)
        try:
            self.ser.setDTR(False)
            self.ser.setRTS(False)
        except Exception:
            pass
        time.sleep(0.2)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
    def send_message(self,angle):
        angle = max(0, min(180, int(angle)))
        line = f"ANGLE:{angle}\n"
        self.ser.write(line.encode("utf-8"))
        self.ser.flush()
        # chờ phản hồi một dòng
        resp = self.ser.readline().decode("utf-8", errors="ignore").strip()
        
def interactive():
    connect = Connect()
    ser = connect.ser
    print("Connected:", ser.port)
    # đọc các dòng khởi động (nếu có)
    time.sleep(0.2)
    while ser.in_waiting:
        print("ESP32:", ser.readline().decode(errors="ignore").strip())

    try:
        while True:
            s = input("Nhap goc (0..180) hoac 'SWEEP'/'q': ").strip()
            if s.lower() == 'q':
                break
            if s.upper() == "SWEEP":
                ser.write(b"SWEEP\n")
            else:
                try:
                    angle = int(s)
                    if 0 <= angle <= 180:
                        pass
                    else:
                        print("Goc ngoai 0..180, se clamp.")
                    resp = connect.send_message(angle)
                    print("ESP32:", resp)
                    continue
                except ValueError:
                    print("Nhap so nguyen 0..180 hoac 'SWEEP'")
                    continue
            # đọc phản hồi
            resp = ser.readline().decode("utf-8", errors="ignore").strip()
            print("ESP32:", resp)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

if __name__ == "__main__":
    interactive()
