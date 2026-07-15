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



        layout.addStretch()

        self.setLayout(layout)
        self.setFixedWidth(220)