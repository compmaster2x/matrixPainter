from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt, QPoint, Signal
import json
import copy


class Canvas(QWidget):
    pixelChanged = Signal(int, int, QColor)

    def __init__(self):
        super().__init__()
        self.history = []
        self.current_color = QColor(255, 0, 0)
        self.brushSize = 1
        self.GRID_SIZE = 16
        self.CELL_SIZE = 35
        self.drawing = False
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

        if event.button() != Qt.LeftButton:
            return

        self.drawing = True
        self.saveState()

        column = int(event.position().x() // self.CELL_SIZE)
        row = int(event.position().y() // self.CELL_SIZE)

        self.paintPixel(column, row)



    def setColor(self, color):
            self.current_color = color

    def setTool(self, tool):
        self.current_tool = tool

    def clearCanvas(self):
        self.saveState()
        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                self.pixels[y][x] = QColor(0, 0, 0)
                

        self.update()

    def mouseMoveEvent(self, event):

        if event.buttons() != Qt.LeftButton:
            return

        x = int(event.position().x() // self.CELL_SIZE)
        y = int(event.position().y() // self.CELL_SIZE)

        self.paintPixel(x, y)

    def paintPixel(self, x, y):

        if x < 0 or x >= self.GRID_SIZE:
            return

        if y < 0 or y >= self.GRID_SIZE:
            return

        if self.current_tool == "fill":
            self.fill(x, y)
            return

        color = self.current_color

        if self.current_tool == "eraser":
            color = QColor(0, 0, 0)

        for dy in range(self.brushSize):
            for dx in range(self.brushSize):

                nx = x + dx
                ny = y + dy

                if nx < 0 or nx >= self.GRID_SIZE:
                    continue

                if ny < 0 or ny >= self.GRID_SIZE:
                    continue

                if self.pixels[ny][nx] == color:
                    continue

                self.pixels[ny][nx] = color
                self.pixelChanged.emit(nx, ny, color)

        self.update()

    def saveToFile(self, fileName):

        data = []

        for y in range(self.GRID_SIZE):

            row = []

            for x in range(self.GRID_SIZE):
                color = self.pixels[y][x]

                row.append([
                    color.red(),
                    color.green(),
                    color.blue()
                ])

            data.append(row)

        with open(fileName, "w") as file:
            json.dump(data, file)

    def loadFromFile(self, fileName):

        with open(fileName, "r") as file:
            data = json.load(file)

        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                r, g, b = data[y][x]

                self.pixels[y][x] = QColor(r, g, b)

                self.pixelChanged.emit(x, y, self.pixels[y][x])

        self.update()

    def fill(self, x, y):
        target = self.pixels[y][x]

        if target == self.current_color:
            return

        stack = [(x, y)]

        while stack:

            x, y = stack.pop()

            if x < 0 or x >= self.GRID_SIZE:
                continue

            if y < 0 or y >= self.GRID_SIZE:
                continue

            if self.pixels[y][x] != target:
                continue

            self.pixels[y][x] = self.current_color
            self.pixelChanged.emit(x, y, self.current_color)

            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

        self.update()

    def saveState(self):
        self.history.append(copy.deepcopy(self.pixels))

        if len(self.history) > 20:
            self.history.pop(0)

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.drawing = False

    def undo(self):

        if not self.history:
            return

        self.pixels = self.history.pop()

        for y in range(self.GRID_SIZE):
            for x in range(self.GRID_SIZE):
                self.pixelChanged.emit(x, y, self.pixels[y][x])

        self.update()
