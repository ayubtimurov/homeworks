import sys
import numpy as np
import sympy as sp
from sympy import Symbol
from sympy.solvers import solve
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QLineEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QGridLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from scipy import integrate
      
class GraphingCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphing Calculator")

        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Enter your function")

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_graph)

        self.plot_surface_button = QPushButton("Plot surface")
        self.plot_surface_button.clicked.connect(self.plot_surface)

        self.operations_button = QPushButton("Operations")
        self.operations_button.setCheckable(True)
        self.operations_button.clicked.connect(self.operations_show)

        self.diff_button = QPushButton("Differentiate")
        self.diff_button.setCheckable(True)
        self.diff_button.hide()
        self.diff_button.clicked.connect(self.differentiate)
        self.intg_button = QPushButton("Integrate")
        self.intg_button.hide()
        self.intg_button.clicked.connect(self.integrate)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)

        self.point_a = QLineEdit()
        self.point_a.setPlaceholderText("Enter lower limit")
        #self.point_a.textChanged.connect(self.integrate)
        self.point_a.hide()
        self.point_b = QLineEdit()
        self.point_b.setPlaceholderText("Enter upper limit")
        #self.point_b.textChanged.connect(self.integrate)
        self.point_b.hide()

        self.area_label = QLabel()
        self.area_label.hide()

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, self)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(toolbar)
        toolbar_layout.addWidget(self.clear_button)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_function)
        input_layout.addWidget(self.plot_button)
        input_layout.addWidget(self.plot_surface_button)

        operations_layout = QHBoxLayout()
        operations_layout.addWidget(self.diff_button)
        operations_layout.addWidget(self.intg_button)

        input_limits_layout = QHBoxLayout()
        input_limits_layout.addWidget(self.point_a)
        input_limits_layout.addWidget(self.point_b)


        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addLayout(input_layout)
        layout.addWidget(self.operations_button)
        layout.addLayout(operations_layout)
        layout.addLayout(input_limits_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)

        self.setLayout(layout)

    def plot_graph(self):
        function  = self.input_function.text()
        x = np.linspace(-10, 10, 400) 

        try:
            y = eval(function, {"x": x, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
        ax.plot(x, y, label=f"y = {function}", color='blue')
        ax.grid(True)  
        ax.legend()
        self.canvas.draw()

    def operations_show(self, checked):
        if checked:
            self.diff_button.show()
            self.intg_button.show()
            self.point_a.show()
            self.point_b.show()
            self.area_label.show()
            self.local_min_max.show()
            
        else:
            self.diff_button.hide()
            self.intg_button.hide()
            self.point_a.hide()
            self.point_b.hide()
            self.area_label.hide()
            self.local_min_max.hide()

    def differentiate(self, checked):
        if checked:
            function = self.input_function.text()
            x = np.linspace(-10, 10, 400)

            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
                dfdx = np.gradient(function, x)
            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.plot(dfdx, color='red', label=f"dy/dx = {sp.diff(function, 'x')}")
            ax.grid(True)    
            ax.legend()
            self.canvas.draw()
        else:
            function  = self.input_function.text()
            x = np.linspace(-10, 10, 400) 

            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.plot()
            ax.grid(True)  
            ax.legend()
            self.canvas.draw()

    @Slot()
    def integrate(self):
            function = self.input_function.text()
            a = float(self.point_a.text())
            b = float(self.point_b.text())
            x = np.linspace(-10, 10, 400)
            a_test = str(a)
            b_test = str(b)

            expression = lambda x: eval(function)
            area = integrate.quad(expression, a, b)
            if a_test == "" or b_test == "":
                try:
                    y = eval(function, {"x": x, "np": np, "__builtins__": {}})
                except Exception as e:
                    print("Invalid function:", e)
                    return
            
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, label=f"y = {function}", color='blue')
                ax.grid(True)
                ax.legend()
                self.canvas.draw()
            else:
                try:
                    y = eval(function, {"x": x, "np": np, "__builtins__": {}})
                except Exception as e:
                    print("Invalid function:", e)
                    return
            
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, label=f"y = {function}", color='blue')
                ax.fill_between(
                    x, y, 0,
                    where=(x > a) & (x < b),
                    color='green', alpha=0.5
                                    )
                area1 = area[0]
                self.area_label.setText(f"Area under the curve: {area1:.2f}")
                ax.grid(True)
                ax.legend()
                self.canvas.draw()

    def plot_surface(self):
        z = self.input_function.text()
        a = float(self.point_a.text())
        b = float(self.point_b.text())

        x = np.arange(a, b, 0.1)
        y = np.arange(a, b, 0.1)

        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(z, {"x": x, "y": y, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection="3d")
        self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
        ax.plot_surface(Z, X, Y, label=f"z = {z}", cmap="summer")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        self.canvas.draw()

    def clear(self):
        self.input_function.clear()
        self.diff_button.hide()
        self.intg_button.hide()
        self.point_a.hide()
        self.point_a.clear()
        self.point_b.hide()
        self.point_b.clear()
        self.area_label.hide()
        self.figure.clear()


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingCalculator()
    window.show()
    sys.exit(app.exec())