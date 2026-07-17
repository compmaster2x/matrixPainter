from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QColorDialog,
    QComboBox
)


class ControlPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Подключение"))

        self.portBox = QComboBox()
        layout.addWidget(self.portBox)

        self.connectButton = QPushButton("Подключить")
        layout.addWidget(self.connectButton)

        self.disconnectButton = QPushButton("Отключить")
        layout.addWidget(self.disconnectButton)

        self.statusLabel = QLabel("🔴 Не подключено")
        layout.addWidget(self.statusLabel)

        layout.addSpacing(20)

        layout.addWidget(QLabel("Инструменты"))

        self.brushButton = QPushButton("Кисть")
        layout.addWidget(self.brushButton)

        self.colorButton = QPushButton("Цвет")
        layout.addWidget(self.colorButton)

        self.eraserButton = QPushButton("Ластик")
        layout.addWidget(self.eraserButton)

        self.clearButton = QPushButton("Очистить")
        layout.addWidget(self.clearButton)

        self.fillButton = QPushButton("Заливка")
        layout.addWidget(self.fillButton)

        self.saveButton = QPushButton("Сохранить")
        layout.addWidget(self.saveButton)

        self.loadButton = QPushButton("Загрузить")
        layout.addWidget(self.loadButton)

        self.brushSize = QComboBox()

        self.brushSize.addItem("1x1")
        self.brushSize.addItem("2x2")
        self.brushSize.addItem("3x3")

        layout.addWidget(self.brushSize)


        layout.addStretch()

        self.setLayout(layout)
        self.setFixedWidth(220)
