import serial, time
class Serial:
    def __init__(self):
        self.PORT = "COM7"
        self.BAUD = 115200
        self.ser = serial.Serial(port=self.PORT, baudrate=self.BAUD, timeout=1, write_timeout=1)
        # tránh reset ESP32 (tuỳ board)
        try:
            self.ser.setDTR(False)
            self.ser.setRTS(False)
        except Exception:
            pass
        time.sleep(0.2)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def send_angle(self, angle):
        angle = max(0, min(180, int(angle)))
        line = f"ANGLE:{angle}\n"
        self.ser.write(line.encode("utf-8"))
        self.ser.flush()
        # chờ phản hồi một dòng
        resp = self.ser.readline().decode("utf-8", errors="ignore").strip()
        return resp
