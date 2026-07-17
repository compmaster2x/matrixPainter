from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout, QColorDialog, QFileDialog
)

from canvas import Canvas
from control_panel import ControlPanel
from serial_manager import SerialManager
from PySide6.QtGui import QShortcut, QKeySequence


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
        self.panel.saveButton.clicked.connect(self.saveImage)
        self.panel.loadButton.clicked.connect(self.loadImage)
        self.panel.fillButton.clicked.connect(self.selectFill)
        self.panel.brushSize.currentIndexChanged.connect(self.changeBrushSize)
        self.undoShortcut = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.undoShortcut.activated.connect(self.undo)
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
            self.serial.clear()
            self.canvas.clearCanvas()
        else:
            self.panel.statusLabel.setText("🔴 Ошибка подключения")

    def disconnectSerial(self):

        self.serial.disconnect()

        self.panel.statusLabel.setText("🔴 Не подключено")

    def sendPixel(self, x, y, color):
        self.serial.sendPixel(x, y, color)

    def saveImage(self):

        fileName, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить",
            "",
            "JSON (*.json)"
        )

        if not fileName:
            return

        self.canvas.saveToFile(fileName)

    def loadImage(self):

        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть",
            "",
            "JSON (*.json)"
        )

        if not fileName:
            return

        self.canvas.loadFromFile(fileName)

    def selectFill(self):
        self.canvas.setTool("fill")

    def changeBrushSize(self, index):
        self.canvas.brushSize = index + 1
        print(self.canvas.brushSize)

    def undo(self):
        self.canvas.undo()

