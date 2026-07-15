import serial
import serial.tools.list_ports


class SerialManager:

    def __init__(self):
        self.serial = None

    def getPorts(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]

    def connect(self, port, baudrate=9600):

        try:
            self.serial = serial.Serial(port, baudrate)
            return True
        except:
            self.serial = None
            return False

    def disconnect(self):

        if self.serial and self.serial.is_open:
            self.serial.close()

        self.serial = None

    def isConnected(self):

        return (
            self.serial is not None
            and
            self.serial.is_open
        )

    def sendPixel(self, x, y, color):

        if not self.isConnected():
            return

        r = color.red()
        g = color.green()
        b = color.blue()

        message = f"PX,{x},{y},{r},{g},{b}\n"

        self.serial.write(message.encode())

    def clear(self):

        if not self.isConnected():
            return

        self.serial.write(b"CLEAR\n")