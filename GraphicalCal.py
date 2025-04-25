import sys

import numpy as np 
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QMainWindow
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class GraphingCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphing Calculator")
        self.setGeometry(100, 100, 800, 600)

        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Enter function (To plot the graph press Enter)")
        self.input_function.returnPressed.connect(self.plot_graph)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_function)
        #input_layout.addWidget(self.plot_button)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)

    def plot_graph(self):
        try:
            function_str =  self.input_function.text()
            x = np.linspace(-10, 10, 100)
            safe_function_str = function_str.replace("^", "**")
            print(safe_function_str)
            namespace = {
                "x": x, "np": np, "sin": np.sin, "cos": np.cos,
                "tan": np.tan, "log": np.log, "sqrt": np.sqrt
            }
            y = eval(safe_function_str, namespace)

            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {function_str}")
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.grid(True)
            self.canvas.draw()

        except Exception as e:
            print(f"Error: {e}")
            self.input_function.setText("Invalid function")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingCalculator()
    window.show()
    sys.exit(app.exec())