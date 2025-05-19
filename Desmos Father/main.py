import sys
import numpy as np
import sympy as sp
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QLineEdit, QPushButton, QWidget, QLabel, QHBoxLayout, QGridLayout
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
import matplotlib.pyplot as plt
from mpl_interactions import ioff, panhandler, zoom_factory
from scipy import integrate

class GraphingCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphing Calculator")

        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Enter your function")

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.plot_graph)

        self.diff_button = QPushButton("Differentiate")
        self.diff_button.setCheckable(True)
        self.diff_button.hide()
        self.diff_button.clicked.connect(self.differentiate)

        self.intg_area_button = QPushButton("Calculate area")
        self.intg_area_button.setCheckable(True)
        self.intg_area_button.hide()
        self.intg_area_button.clicked.connect(self.intg_area)

        self.tangent_line_button = QPushButton("Tangent Line")
        self.tangent_line_button.setCheckable(True)
        self.tangent_line_button.hide()
        self.tangent_line_button.clicked.connect(self.plot_tangent_line)

        self.local_min_max_button = QPushButton("Local Min/Max")
        self.local_min_max_button.setCheckable(True)

        self.x1_2d = QLineEdit()
        self.x1_2d.setPlaceholderText("Enter lower x limit")
        self.x1_2d.hide()
        self.x2_2d = QLineEdit()
        self.x2_2d.setPlaceholderText("Enter upper x limit")
        self.x2_2d.hide()

        self.area_label = QLabel()
        self.area_label.hide()

        self.tangent_line_point = QLineEdit()
        self.tangent_line_point.setPlaceholderText("Tangent line at a point")
        self.tangent_line_point.hide()

        self.plot_surface_button = QPushButton("Plot surface")
        self.plot_surface_button.clicked.connect(self.plot_surface)

        self.intg_volume_button = QPushButton("Calculate Volume")
        self.intg_volume_button.setCheckable(True)
        self.intg_volume_button.hide()
        self.intg_volume_button.clicked.connect(self.intg_volume)

        self.x1_3d = QLineEdit()
        self.x1_3d.hide()
        self.x1_3d.setPlaceholderText("Enter lower x limit")
        self.x2_3d = QLineEdit()
        self.x2_3d.hide()
        self.x2_3d.setPlaceholderText("Enter upper x limit")
        
        self.y1_3d = QLineEdit()
        self.y1_3d.hide()
        self.y1_3d.setPlaceholderText("Enter lower y limit")
        self.y2_3d = QLineEdit()
        self.y2_3d.hide()
        self.y2_3d.setPlaceholderText("Enter upper y limit")

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

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_function)
        input_layout.addWidget(self.plot_button)
        input_layout.addWidget(self.plot_surface_button)

        operations_2d_layout = QHBoxLayout()
        operations_2d_layout.addWidget(self.diff_button)
        operations_2d_layout.addWidget(self.intg_area_button)
        operations_2d_layout.addWidget(self.tangent_line_button)

        limits_layout_2d = QHBoxLayout()
        limits_layout_2d.addWidget(self.x1_2d)
        limits_layout_2d.addWidget(self.x2_2d)
        limits_layout_2d.addWidget(self.tangent_line_point)

        limits_layout_3d = QGridLayout()
        limits_layout_3d.addWidget(self.x1_3d, 0, 0)
        limits_layout_3d.addWidget(self.x2_3d, 1, 0)
        limits_layout_3d.addWidget(self.y1_3d, 0, 1)
        limits_layout_3d.addWidget(self.y2_3d, 1, 1)

        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addLayout(input_layout)
        layout.addLayout(limits_layout_2d)
        layout.addLayout(operations_2d_layout)
        layout.addLayout(limits_layout_3d)
        layout.addWidget(self.intg_volume_button)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)
        layout.addWidget(self.volume_label)

        self.setLayout(layout)

    def plot_graph(self):
        self.diff_button.show()
        self.intg_area_button.show()
        self.tangent_line_button.show()
        self.x1_2d.show()
        self.x2_2d.show()
        self.tangent_line_point.show()
        self.x1_3d.hide()
        self.x2_3d.hide()
        self.y1_3d.hide()
        self.y2_3d.hide()
        self.intg_volume_button.hide()

        function  = self.input_function.text()
        x = np.linspace(-1000, 1000, 100000)

        try:
            y = eval(function, {"x": x, "np": np, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_ylim(-10, 10)
        ax.set_xlim(-10, 10)
        self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
        ax.plot(x, y, label=f"y = {function}", color='blue')
        disconnect_zoom = zoom_factory(ax)
        pan_handler = panhandler(self.figure)
        ax.grid(True)  
        ax.legend()
        self.canvas.draw()

    def plot_tangent_line(self, checked):
        function = self.input_function.text()
        x = np.linspace(-10, 10, 40000)

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
            
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            disconnect_zoom = zoom_factory(ax)
            pan_handler = panhandler(self.figure)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.set_ylim(-10, 10)
            ax.set_xlim(-10, 10)
            ax.plot(x, y, label=f"y = {function}", color="blue")
            if m == 0 and b == 0:
                ax.plot(x, tangent, label=f"Tangent Line: y = 0 ", color="purple")
            elif b == 0:
                ax.plot(x, tangent, label=f"Tangent Line: y = {m:.1f}*x", color="purple")
            elif m == 0:
                ax.plot(x, tangent, label=f"Tangent Line: y = {b:.1f}", color="purple")
            else:
                ax.plot(x, tangent, label=f"Tangent Line: y = {m:.1f}*x {sign} {abs(b):.1f}", color="purple")
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
            disconnect_zoom = zoom_factory(ax)
            pan_handler = panhandler(self.figure)
            ax.set_ylim(-10, 10)
            ax.set_xlim(-10, 10)
            ax.plot(x, y, label=f"y = {function}", color="blue")
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.grid(True)
            self.canvas.draw()

    def differentiate(self, checked):
        function = self.input_function.text()
        x = np.linspace(-1000, 1000, 10000)

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
            disconnect_zoom = zoom_factory(ax)
            pan_handler = panhandler(self.figure)
            ax.set_ylim(-10, 10)
            ax.set_xlim(-10, 10)
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
            disconnect_zoom = zoom_factory(ax)
            pan_handler = panhandler(self.figure)
            ax.set_ylim(-10, 10)
            ax.set_xlim(-10, 10)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.grid(True)
            ax.legend()  
            self.canvas.draw()

    def intg_area(self, checked):
            function = self.input_function.text()
            x1 = float(self.x1_2d.text())
            x2 = float(self.x2_2d.text())
            x = np.linspace(-1000, 1000, 10000)

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
                disconnect_zoom = zoom_factory(ax)
                pan_handler = panhandler(self.figure)
                ax.set_ylim(-10, 10)
                ax.set_xlim(-10, 10)
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
                x = np.linspace(-1000, 1000, 10000) 

                try:
                    y = eval(function, {"x": x, "np": np, "log": np.log,  "__builtins__": {}})
                except Exception as e:
                    print("Invalid function:", e)
                    return

                self.figure.clear()
                ax = self.figure.add_subplot(111)
                disconnect_zoom = zoom_factory(ax)
                pan_handler = panhandler(self.figure)
                ax.set_ylim(-10, 10)
                ax.set_xlim(-10, 10)
                self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
                ax.plot(x, y, label=f"y = {function}", color='blue')
                self.area_label.hide()
                ax.grid(True)  
                ax.legend()
                self.canvas.draw()

                self.x1_2d.clear()
                self.x2_2d.clear()

    def plot_surface(self):
        self.x1_3d.show()
        self.x2_3d.show()
        self.y1_3d.show()
        self.y2_3d.show()
        self.intg_volume_button.show()
        
        z = self.input_function.text()

        x_data = np.arange(-10, 10, 0.1)
        y_data = np.arange(-10, 10, 0.1)

        X, Y = np.meshgrid(x_data, y_data)

        try:
            Z = eval(z, {"x": X, "y": Y, "np": np, "cos": np.cos, "sin": np.sin, "__builtins__": {}})
        except Exception as e:
            print("Invalid function:", e)
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111, projection="3d")
        disconnect_zoom = zoom_factory(ax)
        pan_handler = panhandler(self.figure)
        self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
        ax.plot_surface(X, Y, Z, cmap="summer")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_zlabel("Z Axis")
        self.canvas.draw()

        self.diff_button.hide()
        self.intg_area_button.hide()
        self.x1_2d.hide()
        self.x2_2d.hide()
        self.area_label.hide()
        self.tangent_line_button.hide()
        self.tangent_line_point.hide()
      
    def intg_volume(self, checked):
        z = self.input_function.text()
        x1 = int(self.x1_3d.text())
        x2 = int(self.x2_3d.text())
        y1 = int(self.y1_3d.text())
        y2 = int(self.y2_3d.text())

        x_data = np.arange(-10, 10, 0.1)
        y_data = np.arange(-10, 10, 0.1)

        X, Y = np.meshgrid(x_data, y_data)

        if checked:

            expression = lambda x, y: eval(z)
            volume = integrate.dblquad(expression, x1, x2, y1, y2)

            try:
                Z = eval(z, {"x": X, "y": Y, "np": np, "cos": np.cos, "sin": np.sin, "__builtins__": {}})
            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111, projection="3d")
            disconnect_zoom = zoom_factory(ax)
            pan_handler = panhandler(self.figure)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot_surface(X, Y, Z, cmap="summer")
            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            ax.set_zlabel("Z Axis")
            volume1 = volume[0]
            self.volume_label.show()
            self.volume_label.setText(f"Volume under the surface is: {volume1:.2f}")
            self.diff_button.hide()
            self.intg_area_button.hide()
            self.x1_2d.hide()
            self.x2_2d.hide()
            self.area_label.hide()
            self.canvas.draw()

        else:

            self.x1_3d.clear()
            self.x2_3d.clear()
            self.y1_3d.clear()
            self.y2_3d.clear()

            try:
                Z = eval(z, {"x": X, "y": Y, "np": np, "cos": np.cos, "sin": np.sin, "__builtins__": {}})
            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111, projection="3d")
            disconnect_zoom = zoom_factory(ax)
            pan_handler = panhandler(self.figure)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot_surface(X, Y, Z, cmap="summer")
            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            ax.set_zlabel("Z Axis")
            self.canvas.draw()

        self.diff_button.hide()
        self.intg_area_button.hide()
        self.x1_2d.hide()
        self.x2_2d.hide()
        self.area_label.hide()

    def reset(self):
        self.input_function.clear()
        self.diff_button.hide()
        self.intg_area_button.hide()
        self.tangent_line_button.hide()
        self.x1_2d.hide()
        self.x1_2d.clear()
        self.x2_2d.hide()
        self.x2_2d.clear()
        self.tangent_line_point.hide()
        self.tangent_line_point.clear()
        self.area_label.hide()
        self.x1_3d.hide()
        self.x2_3d.hide()
        self.y1_3d.hide()
        self.y2_3d.hide()
        self.intg_volume_button.hide()
        self.figure.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingCalculator()
    window.show()
    sys.exit(app.exec())