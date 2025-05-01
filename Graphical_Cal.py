import sys
import numpy as np
import sympy as sp
from sympy import Symbol
from sympy.solvers import solve
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
        self.input_function.setPlaceholderText("Enter function (To plot the graph press Enter)")

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_graph)

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

        self.point_a = QLineEdit()
        self.point_a.setPlaceholderText("Enter lower limit")
        self.point_a.hide()
        self.point_b = QLineEdit()
        self.point_b.setPlaceholderText("Enter upper limit")
        self.point_b.hide()

        self.area_label = QLabel()
        self.area_label.hide()

        self.local_min_max = QPushButton("Local Min/Max")
        self.local_min_max.hide()
        self.local_min_max.clicked.connect(self.local_min_max1)

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        toolbar = NavigationToolbar(self.canvas, self)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_function)
        input_layout.addWidget(self.plot_button)

        operations_layout = QHBoxLayout()
        operations_layout.addWidget(self.diff_button)
        operations_layout.addWidget(self.intg_button)
        operations_layout.addWidget(self.local_min_max)

        input_limits_layout = QHBoxLayout()
        input_limits_layout.addWidget(self.point_a)
        input_limits_layout.addWidget(self.point_b)

        self.cursor = Cursor(self.ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
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
        
        self.ax.clear() 
        self.ax.plot(x, y, label=f"y = {function}", color='blue')
        self.ax.grid(True)  
        self.ax.legend()
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
                dfdx = np.gradient(y, x)
            except Exception as e:
                print("Invalid function:", e)
                return

            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {function}", color='blue')
            self.ax.plot(dfdx, color='red', label=f"dy/dx = {sp.diff(function, 'x')}")
            self.ax.grid(True)    
            self.ax.legend()
            self.canvas.draw()
        else:
            function  = self.input_function.text()
            x = np.linspace(-10, 10, 400) 

            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function:", e)
                return
        
            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {function}", color='blue')
            self.ax.plot()
            self.ax.grid(True)  
            self.ax.legend()
            self.canvas.draw()

    def integrate(self):
            function = self.input_function.text()
            a = float(self.point_a.text())
            b = float(self.point_b.text())
            x = np.linspace(-10, 10, 400)

            expression = lambda x: eval(function)
            area = integrate.quad(expression, a, b)
            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function:", e)
                return
            
            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {function}", color='blue')
            self.ax.fill_between(
                x, y, 0,
                where=(x > a) & (x < b),
                color='green', alpha=0.5
            )
            area1 = area[0]
            self.area_label.setText(f"Area under the curve: {area1:.2f}")
            self.ax.grid(True)
            self.ax.legend()
            self.canvas.draw()

    def local_min_max1(self):
        function  = self.input_function.text()
        x = np.linspace(-10, 10, 400)

        x = Symbol('x', 'sin')
        diff = solve(sp.diff(function, x))
        input = round(float(diff[0]), 2)
        def eval_func(function, x):
            safe_globals = {"x": x, "np": np, "__builtins__": {}}

            try:
                answer = eval(function, safe_globals)
                return answer
            except Exception as e:
                print("Invalid function:", e)
                return f"Error: {e}"
            
        output = round(eval_func(function, input),2)

        x_min = [input]
        y_min = [output]
        print(x_min, y_min)

        try:
            y = eval(function, {"x": x, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return
        
        self.ax.clear()
        #self.ax.plot(x, y, label=f"y = {function}", color='blue' )
        self.ax.plot(x_min, y_min, 'ro')
        self.ax.grid(True)
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingCalculator()
    window.show()
    sys.exit(app.exec())