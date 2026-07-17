from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPoint, Signal


class Canvas(QWidget):
    pixelChanged = Signal(int, int, QColor)

    def __init__(self):
        super().__init__()

        self.current_color = QColor(255, 0, 0)

        self.GRID_SIZE = 16
        self.CELL_SIZE = 35

        self.pixels = [
            [QColor(0, 0, 0) for _ in range(self.GRID_SIZE)]
            for _ in range(self.GRID_SIZE)
        ]

        self.current_color = QColor(255, 0, 0)

        self.current_tool = "brush"

        self.setFixedSize(
            self.GRID_SIZE * self.CELL_SIZE,
            self.GRID_SIZE * self.CELL_SIZE
        )

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(30, 30, 30))

        painter.setPen(QPen(QColor(80, 80, 80)))

        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                painter.fillRect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.pixels[y][x]
                )

                painter.setPen(QPen(QColor(80, 80, 80)))

                painter.drawRect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE,
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )

    def mousePressEvent(self, event):

        x = event.position().x()
        y = event.position().y()

        column = int(x // self.CELL_SIZE)
        row = int(y // self.CELL_SIZE)

        if self.current_tool == "brush":
            self.pixels[row][column] = self.current_color
        else:
            self.pixels[row][column] = QColor(0, 0, 0)

        self.update()
        self.pixelChanged.emit(column, row, self.pixels[row][column])
        print(f"Нажата клетка: X={column}, Y={row}")

    def setColor(self, color):
            self.current_color = color

    def setTool(self, tool):
        self.current_tool = tool

    def clearCanvas(self):

        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                self.pixels[y][x] = QColor(0, 0, 0)
                

        self.update()