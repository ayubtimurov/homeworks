import sys

import numpy as np
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QLabel
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Graph(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        

    def plot_graph(self):
        try:
            function_str = self.input_function.text()
            x = np.linspace(-10, 10, 100)
            namespace = {
                "x": x, "np": np, "sin": np.sin, "cos": np.cos,
                "tan": np.tan, "log": np.log, "sqrt": np.sqrt
            }
            y = eval(function_str, namespace)

            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {function_str}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.grid(True)
            self.ax.legend()
            self.draw()
        except Exception as e:
            print(f"Error: {e}")
            self.input_function.setText("Invalid function")

class GraphicalCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphing Calculator")
        self.setGeometry(100, 100, 800, 600)

        widget = QWidget()
        layout = QVBoxLayout()

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphicalCalculator()
    window.show()
    sys.exit(app.exec())     