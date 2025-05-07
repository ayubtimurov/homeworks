import sys
import numpy as np
import sympy as sp
from PySide6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from scipy import integrate
from PySide6.QtWidgets import QSpinBox
import matplotlib.pyplot as plt

class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wolfram Father")

        self.input = QLineEdit()
        self.input.setPlaceholderText("enter function...")
        self.point_a = QLineEdit()
        self.point_a.setPlaceholderText("enter limit a...")
        self.point_b = QLineEdit()
        self.point_b.setPlaceholderText("enter limit b...")
        self.area_label = QLabel("integral equals to...")
        self.button = QPushButton("PLOT")
        self.button_surface = QPushButton("PLOT SURFACE")

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.input)

        point_inputs = QHBoxLayout()
        point_inputs.addWidget(self.point_a)
        point_inputs.addWidget(self.point_b)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.button)
        buttons_layout.addWidget(self.button_surface)

        layout.addLayout(point_inputs)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)
        layout.addWidget(toolbar)

        self.setLayout(layout)
        self.init_style()

        self.button.clicked.connect(self.plot)
        self.button_surface.clicked.connect(self.plot_surface)

    def plot(self):
        expression = self.input.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(-10, 10, 400)

        try:
            y = eval(expression, {"x": x, "np": np, "__builtins__": {}})
            dfdx = np.gradient(y, x)
            
            function = lambda x: eval(expression)
            area, _ = integrate.quad(function, point_a, point_b)
        except Exception as e:
            print("Invalid function:", e)
            return

        self.figure.clear()
        axes = self.figure.add_subplot(111)
        axes.plot(x, y, color="yellow")
        axes.plot(x, dfdx, color="red")

        axes.grid(True)
        axes.legend()
        axes.set_title(f"y = {expression}")
        self.canvas.draw()
    
    def plot_surface(self):
        expression = self.input.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())

        x_data = np.arange(point_a, point_b, 0.1)
        y_data = np.arange(point_a, point_b, 0.1)

        X, Y = np.meshgrid(x_data, y_data)

        try:
            Z = eval(expression, {"x": X, "y": Y, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return

        self.figure.clear()
        axes = self.figure.add_subplot(111, projection="3d")
        axes.plot_surface(X, Y, Z, cmap="summer")
        axes.set_title(f"y = {expression}")
        self.canvas.draw()

    def init_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #dcdcdc;
            } 
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 18px; 
                font-family: "Arial", sans-serif; 
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
            }
            QPushButton::pressed {
                background-color: #005a9e;
                color: white;
                border: 2px solid #ffcc00;
            }
            QLineEdit {
                font-size: 18px;
                font-family: "Courier New", monospace;
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLabel {
                font-size: 18px;
                font-family: "Arial", sans-serif;
                color: #333333;
                padding: 5px;
                text-align: center;
            }
        """)


        
app = QApplication(sys.argv)
window = PlotWindow()
window.show()
sys.exit(app.exec())