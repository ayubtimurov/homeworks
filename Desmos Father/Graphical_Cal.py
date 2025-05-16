import sys
import numpy as np
import sympy as sp
import sympy
from sympy import *
from sympy import Symbol
from sympy.solvers import solve
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QLineEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QSlider
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

        self.range_label = QLabel("Set range for graph: [")
        self.range_label_middle = QLabel(":")
        self.range_label_end = QLabel("]")

        self.diff_button = QPushButton("Differentiate")
        self.diff_button.setCheckable(True)
        self.diff_button.hide()
        self.diff_button.clicked.connect(self.differentiate)

        self.intg_area_button = QPushButton("Calculate area")
        self.intg_area_button.setCheckable(True)
        self.intg_area_button.hide()
        self.intg_area_button.clicked.connect(self.integrate)

        self.local_min_max_button = QPushButton("Local Min/Max")
        self.local_min_max_button.setCheckable(True)
        self.local_min_max_button.hide()
        self.local_min_max_button.clicked.connect(self.local_min_max)

        self.tangent_line_button = QPushButton("Tangent Line")
        self.tangent_line_button.setCheckable(True)
        self.tangent_line_button.hide()
        self.tangent_line_button.clicked.connect(self.plot_tangent_line)

        self.x_low_lim_2d = QLineEdit()
        self.x_low_lim_2d.setPlaceholderText("Enter lower x limit")
        self.x_low_lim_2d.hide()
        self.x_upper_lim_2d = QLineEdit()
        self.x_upper_lim_2d.setPlaceholderText("Enter upper x limit")
        self.x_upper_lim_2d.hide()

        self.tangent_line_point = QLineEdit()
        self.tangent_line_point.setPlaceholderText("Tangent line at a point")
        self.tangent_line_point.hide()

        self.tangent_line_point_slider = QSlider(Qt.Horizontal)
        #self.tangent_line_point_slider.hide()
        self.tangent_line_point_slider.setMinimum(-10)
        self.tangent_line_point_slider.setMaximum(10)
        self.tangent_line_point_slider.setTickInterval(1)
        self.tangent_line_point_slider.setTickPosition(QSlider.TicksBelow)
        self.tangent_line_point_slider.valueChanged.connect(self.plot_tangent_line)

        self.area_label = QLabel()
        self.area_label.hide()

        self.point_a = QLineEdit()
        self.point_a.setFixedWidth(30)
        self.point_b = QLineEdit()
        self.point_b.setFixedWidth(30)

        self.taylor_series_at_point = QLineEdit()
        self.taylor_series_at_point.setPlaceholderText("Taylot series at a point")

        self.number_of_terms = QLineEdit()
        self.number_of_terms.setPlaceholderText("Number of terms")

        self.plot_taylor_series = QPushButton("Taylor series")
        self.plot_taylor_series.clicked.connect(self.taylor_series_plot)

        self.plot_surface_button = QPushButton("Plot surface")
        self.plot_surface_button.clicked.connect(self.plot_surface)

        self.volume_label = QLabel()
        self.volume_label.hide()

        self.clear_button = QPushButton("Reset")
        self.clear_button.clicked.connect(self.reset)

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, self)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(toolbar)
        toolbar_layout.addWidget(self.clear_button)

        range_layout = QHBoxLayout()
        range_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        range_layout.addWidget(self.range_label)
        range_layout.addWidget(self.point_a)
        range_layout.addWidget(self.range_label_middle)
        range_layout.addWidget(self.point_b)
        range_layout.addWidget(self.range_label_end)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_function)
        input_layout.addWidget(self.plot_button)
        input_layout.addWidget(self.plot_surface_button)

        operations_2d_layout = QHBoxLayout()
        operations_2d_layout.addWidget(self.diff_button)
        operations_2d_layout.addWidget(self.intg_area_button)
        operations_2d_layout.addWidget(self.local_min_max_button)
        operations_2d_layout.addWidget(self.tangent_line_button)
        operations_2d_layout.addWidget(self.plot_taylor_series)

        limits_layout_2d = QHBoxLayout()
        limits_layout_2d.addWidget(self.x_low_lim_2d)
        limits_layout_2d.addWidget(self.x_upper_lim_2d)
        limits_layout_2d.addWidget(self.tangent_line_point)
        limits_layout_2d.addWidget(self.taylor_series_at_point)
        limits_layout_2d.addWidget(self.number_of_terms)

        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addLayout(input_layout)
        layout.addLayout(range_layout)
        layout.addLayout(limits_layout_2d)
        layout.addLayout(operations_2d_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)

        self.setLayout(layout)

    def plot_graph(self):
        self.diff_button.show()
        self.intg_area_button.show()
        self.local_min_max_button.show()
        self.tangent_line_button.show()
        self.x_low_lim_2d.show()
        self.x_upper_lim_2d.show()
        self.tangent_line_point.show()

        function  = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(point_a, point_b, 400) 

        try:
            y = eval(function, {"x": x, "np": np, "log": np.log,  "__builtins__": {}})
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

    def local_min_max(self, checked):
        function  = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x_val = np.linspace(point_a, point_b, 400) 

        if checked:
            try:
                y = eval(function, {"x": x_val, "np": np, "__builtins__": {}})

                x = sp.Symbol("x")
                expression = sp.sympify(function)
                f_prime = sp.diff(expression, x) 
                print(f_prime)
                roots = solve(f_prime, x, dict=True)
                print(roots)
            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot(x_val, y, label=f"y = {function}", color='blue')
            ax.grid(True)  
            ax.legend()
            self.canvas.draw()

    def plot_tangent_line(self, checked):
        function = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(point_a, point_b, 1000)

        if checked:
            f = lambda x: eval(function)
 
            a = float(self.tangent_line_point.text())
            h = 1e-8

            m = (f(a+h) - f(a)) / h
            b = f(a) - m * a
            sign = "-" if b < 0 else "+"

            tangent = f(a) + m * (x-a)

            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function", e)
                return
            
            if m == 0 and b == 0:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, label=f"y = {function}", color="blue")
                ax.plot(x, tangent, label=f"Tangent Line: y = 0 ", color="black")
                self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
                ax.grid(True)
                ax.legend()
                self.canvas.draw()
            else:
                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, label=f"y = {function}", color="blue")
                ax.plot(x, tangent, label=f"Tangent Line: y = {m:.1f}*x {sign} {abs(b):.1f} ", color="black")
                self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
                ax.grid(True)
                ax.legend()
                self.canvas.draw()
        else:
            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function", e)
                return
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, label=f"y = {function}", color="blue")
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.grid(True)
            self.canvas.draw()

    def differentiate(self, checked):
        function = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(point_a, point_b, 1000)

        if checked:
            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
                dfdx = np.gradient(y, x)
                f_prime = sp.diff(function)

            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.plot(x, dfdx, label=f"y = {f_prime}", color="red")
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
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.grid(True)
            ax.legend()  
            self.canvas.draw()

    def integrate(self, checked):
            function = self.input_function.text()
            point_a = float(self.point_a.text())
            point_b = float(self.point_b.text())
            x1 = float(self.x_low_lim_2d.text())
            x2 = float(self.x_upper_lim_2d.text())
            x = np.linspace(point_a, point_b, 400)

            if checked:
                expression = lambda x: eval(function)
                area = integrate.quad(expression, x1, x2)

                try:
                    y = eval(function)
                except Exception as e:
                    print("Invalid function", e)
                    return

                self.figure.clear()
                ax = self.figure.add_subplot(111)
                ax.plot(x, y, label=f"y = {function}", color='blue')
                ax.fill_between(
                    x, y, 0,
                    where=(x > x1) & (x < x2),
                    color='green', alpha=0.5
                            )
                area1 = area[0]
                self.area_label.show()
                self.area_label.setText(f"Area under the curve: {area1:.2f}")
                ax.grid(True)
                ax.legend()
                self.canvas.draw()
            else:
                function  = self.input_function.text()
                point_a = float(self.point_a.text())
                point_b = float(self.point_b.text())
                x = np.linspace(point_a, point_b, 400) 

                try:
                    y = eval(function, {"x": x, "np": np, "log": np.log,  "__builtins__": {}})
                except Exception as e:
                    print("Invalid function:", e)
                    return

                self.figure.clear()
                ax = self.figure.add_subplot(111)
                self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
                ax.plot(x, y, label=f"y = {function}", color='blue')
                self.area_label.hide()
                ax.grid(True)  
                ax.legend()
                self.canvas.draw()

                self.x_low_lim_2d.clear()
                self.x_upper_lim_2d.clear()

    def taylor_series_plot(self):
        
        def taylor_series(function, variable, a, n):

            i = 0
            taylor = 0
            while i <= n:
                p = (function.diff(variable, i).subs(variable, a) / sp.factorial(i)) * (variable - a)**i
                taylor += p
                i += 1
            return
    
        x = Symbol("x")
        expression = self.input_function.text()
        function = lambda x: eval(expression)
        a = float(self.taylor_series_at_point.text())
        n = int(self.number_of_terms.text())
        taylor_expansion = taylor_series(function, x, a, n)
        print(taylor_expansion)

        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x_vals = np.linspace(point_a, point_b, 400)

        try:
            y = eval(function, {"x": x, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Value Error", e)
            return
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x_vals, y, label=f"y = {function}", color="blue")
        ax.grid(True)
        ax.legend()
        self.canvas.draw()

    def plot_surface(self):
        z = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())

        x_data = np.arange(point_a, point_b, 0.1)
        y_data = np.arange(point_a, point_b, 0.1)

        X, Y = np.meshgrid(x_data, y_data)

        try:
            Z = eval(z, {"x": X, "y": Y, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111, projection="3d")
        self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
        ax.plot_surface(X, Y, Z, cmap="summer")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        self.canvas.draw()

        self.diff_button.hide()
        self.intg_area_button.hide()
        self.local_min_max_button.hide()
        self.x_low_lim_2d.hide()
        self.x_upper_lim_2d.hide()
        self.area_label.hide()
       
    def reset(self):
        self.input_function.clear()
        self.point_a.clear()
        self.point_b.clear()
        self.diff_button.hide()
        self.intg_area_button.hide()
        self.local_min_max_button.hide()
        self.tangent_line_button.hide()
        self.x_low_lim_2d.hide()
        self.x_low_lim_2d.clear()
        self.x_upper_lim_2d.hide()
        self.x_upper_lim_2d.clear()
        self.tangent_line_point.hide()
        self.tangent_line_point.clear()
        self.area_label.hide()
        self.figure.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingCalculator()
    window.show()
    sys.exit(app.exec())