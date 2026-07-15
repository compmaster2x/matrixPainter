from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout, QColorDialog
)

from canvas import Canvas
from control_panel import ControlPanel
from serial_manager import SerialManager



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matrix Painter")

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()

        self.canvas = Canvas()
        self.canvas.pixelChanged.connect(self.sendPixel)
        self.panel = ControlPanel()
        self.serial = SerialManager()
        self.loadPorts()
        self.panel.colorButton.clicked.connect(self.chooseColor)
        self.panel.brushButton.clicked.connect(self.selectBrush)
        self.panel.eraserButton.clicked.connect(self.selectEraser)
        self.panel.clearButton.clicked.connect(self.clearCanvas)
        self.panel.connectButton.clicked.connect(self.connectSerial)
        self.panel.disconnectButton.clicked.connect(self.disconnectSerial)

        layout.addWidget(self.canvas, 1)
        layout.addWidget(self.panel)

        central.setLayout(layout)

        self.resize(1000, 700)

    def chooseColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.canvas.setColor(color)

    def selectEraser(self):
        self.canvas.setTool("eraser")

    def selectBrush(self):
        self.canvas.setTool("brush")

    def clearCanvas(self):
            self.canvas.clearCanvas()
            self.serial.clear()

    def loadPorts(self):
        self.panel.portBox.clear()

        ports = self.serial.getPorts()

        self.panel.portBox.addItems(ports)

    def connectSerial(self):

        port = self.panel.portBox.currentText()

        if self.serial.connect(port):
            self.panel.statusLabel.setText(f"🟢 {port}")
        else:
            self.panel.statusLabel.setText("🔴 Ошибка подключения")

    def disconnectSerial(self):

        self.serial.disconnect()

        self.panel.statusLabel.setText("🔴 Не подключено")

    def sendPixel(self, x, y, color):
        self.serial.sendPixel(x, y, color)