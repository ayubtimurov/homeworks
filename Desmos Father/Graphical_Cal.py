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
        self.plot_button.clicked.connect(self.operations_2d)


        self.diff_button = QPushButton("Differentiate")
        self.diff_button.setCheckable(True)
        self.diff_button.hide()
        self.diff_button.clicked.connect(self.differentiate)

        self.intg_area_button = QPushButton("Calculate area")
        self.intg_area_button.hide()
        self.intg_area_button.clicked.connect(self.integrate)

        self.local_min_max_button = QPushButton("Local Min/Max")
        self.local_min_max_button.setCheckable(True)
        self.local_min_max_button.hide()
        self.local_min_max_button.clicked.connect(self.local_min_max)

        self.x_low_lim_2d = QLineEdit()
        self.x_low_lim_2d.setPlaceholderText("Enter lower x limit")
        self.x_low_lim_2d.hide()
        self.x_upper_lim_2d = QLineEdit()
        self.x_upper_lim_2d.setPlaceholderText("Enter upper x limit")
        self.x_upper_lim_2d.hide()

        self.area_label = QLabel()
        self.area_label.hide()

        self.point_a = QLineEdit()
        self.point_a.setPlaceholderText("Enter limit a")
        self.point_b = QLineEdit()
        self.point_b.setPlaceholderText("Enter limit b")

        self.plot_surface_button = QPushButton("Plot surface")
        self.plot_surface_button.clicked.connect(self.plot_surface)
        self.plot_surface_button.clicked.connect(self.operations_3d)

        self.x_low_lim = QLineEdit()
        self.x_low_lim.setPlaceholderText("Enter lower x limit")
        self.x_low_lim.hide()
        self.y_low_lim = QLineEdit()
        self.y_low_lim.setPlaceholderText("Enter lower y limit")
        self.y_low_lim.hide()
        self.x_upper_lim = QLineEdit()
        self.x_upper_lim.setPlaceholderText("Enter upper x limit")
        self.x_upper_lim.hide()
        self.y_upper_lim = QLineEdit()
        self.y_upper_lim.setPlaceholderText("Enter upper y limit")
        self.y_upper_lim.hide()

        self.intg_volume_button = QPushButton("Calculate volume")
        self.intg_volume_button.setCheckable(True)
        self.intg_volume_button.hide()
        self.intg_volume_button.clicked.connect(self.cal_vol)

        self.volume_label = QLabel()
        self.volume_label.hide()

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)

        self.figure = Figure(figsize=(5, 4))
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, self)

        toolbar_layout = QHBoxLayout()
        toolbar_layout.addWidget(toolbar)
        toolbar_layout.addWidget(self.clear_button)

        a_b_lim_layout = QHBoxLayout()
        a_b_lim_layout.addWidget(self.point_a)
        a_b_lim_layout.addWidget(self.point_b)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_function)
        input_layout.addWidget(self.plot_button)
        input_layout.addWidget(self.plot_surface_button)

        operations_2d_layout = QHBoxLayout()
        operations_2d_layout.addWidget(self.diff_button)
        operations_2d_layout.addWidget(self.intg_area_button)
        operations_2d_layout.addWidget(self.local_min_max_button)

        limits_layout_2d = QHBoxLayout()
        limits_layout_2d.addWidget(self.x_low_lim_2d)
        limits_layout_2d.addWidget(self.x_upper_lim_2d)

        lim_layout_3d = QGridLayout()
        lim_layout_3d.addWidget(self.x_low_lim, 0, 0)
        lim_layout_3d.addWidget(self.x_upper_lim, 1, 0)
        lim_layout_3d.addWidget(self.y_low_lim, 0, 1)
        lim_layout_3d.addWidget(self.y_upper_lim, 1, 1)

        layout = QVBoxLayout()
        layout.addLayout(toolbar_layout)
        layout.addLayout(input_layout)
        layout.addLayout(a_b_lim_layout)
        layout.addLayout(lim_layout_3d)
        layout.addWidget(self.intg_volume_button)
        layout.addLayout(limits_layout_2d)
        layout.addLayout(operations_2d_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.area_label)

        self.setLayout(layout)


    def operations_2d(self):

        self.diff_button.show()
        self.intg_area_button.show()
        self.local_min_max_button.show()
        self.x_low_lim_2d.show()
        self.x_upper_lim_2d.show()
        self.area_label.show()

        self.x_low_lim.hide()
        self.x_upper_lim.hide()
        self.y_low_lim.hide()
        self.y_upper_lim.hide()
        self.intg_volume_button.hide()

    def operations_3d(self):

        self.x_low_lim.show()
        self.x_upper_lim.show()
        self.y_low_lim.show()
        self.y_upper_lim.show()
        self.intg_volume_button.show()

        self.diff_button.hide()
        self.intg_area_button.hide()
        self.local_min_max_button.hide()
        self.x_low_lim_2d.hide()
        self.x_upper_lim_2d.hide()
        self.area_label.hide()

    def plot_graph(self):
        function  = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(point_a, point_b, 400) 

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

    def local_min_max(self, checked):
        function  = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(point_a, point_b, 400) 

        if checked:
            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
                dfdx = sp.lambdify(function)
                f_prime = sp.diff(dfdx, x)
                print(f_prime)
            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.scatter(1, 1, color="black")
            ax.grid(True)  
            ax.legend()
            self.canvas.draw()

    def differentiate(self, checked):
        function = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())
        x = np.linspace(point_a, point_b, 400)

        if checked:
            try:
                y = eval(function, {"x": x, "np": np, "__builtins__": {}})
                dfdx = np.gradient(y, x)

            except Exception as e:
                print("Invalid function:", e)
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True, color='red', linewidth=1)
            ax.plot(x, y, label=f"y = {function}", color='blue')
            ax.plot(x, dfdx, color="red")
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

    def integrate(self):
            function = self.input_function.text()
            point_a = float(self.point_a.text())
            point_b = float(self.point_b.text())
            x_low_lim = float(self.x_low_lim_2d.text())
            x_upper_lim = float(self.x_upper_lim_2d.text())
            x = np.linspace(point_a, point_b, 400)

            expression = lambda x: eval(function)
            area = integrate.quad(expression, x_low_lim, x_upper_lim)

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
                    where=(x > x_low_lim) & (x < x_upper_lim),
                    color='green', alpha=0.5
                            )
            area1 = area[0]
            self.area_label.setText(f"Area under the curve: {area1:.2f}")
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

    def cal_vol(self, checked):
        z = self.input_function.text()
        point_a = float(self.point_a.text())
        point_b = float(self.point_b.text())

        x_data = np.arange(point_a, point_b, 0.1)
        y_data = np.arange(point_a, point_b, 0.1)

        X, Y = np.meshgrid(x_data, y_data)

        if checked:
            x_low_lim = float(self.x_low_lim.text())
            x_upper_lim = float(self.x_upper_lim.text())
            y_low_lim = float(self.y_low_lim.text())
            y_upper_lim = float(self.y_upper_lim.text())

            try:
                Z = eval(z, {"x": X, "y": Y, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function")
                return
            
            self.figure.clear()
            ax = self.figure.add_subplot(111, projection="3d")
            ax.plot_surface(X, Y, Z, cmap="summer")
            cset = ax.contourf(X, Y, Z, zdir="z", offset=-2, cmap="viridis", levels=20, alpha=1)
            ax.set_xlim(x_low_lim, x_upper_lim)
            ax.set_ylim(y_low_lim, y_upper_lim)
            ax.set_zlim(np.min(Z)-2, np.max(Z))
            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            ax.set_zlabel("Z Axis")
            self.canvas.draw()

        else:
            try:
                Z = eval(z, {"x": X, "y": Y, "np": np, "__builtins__": {}})
            except Exception as e:
                print("Invalid function", e)
                return
            self.figure.clear()
            ax = self.figure.add_subplot(111, projection="3d")
            ax.plot_surface(X, Y, Z, cmap="summer")
            ax.set_xlabel("X Axis")
            ax.set_ylabel("Y Axis")
            ax.set_zlabel("Z Axis")
            self.canvas.draw()
            
    def clear(self):
        self.input_function.clear()
        self.point_a.clear()
        self.point_b.clear()
        self.diff_button.hide()
        self.intg_area_button.hide()
        self.intg_volume_button.hide()
        self.x_low_lim_2d.hide()
        self.x_upper_lim_2d.hide()
        self.x_low_lim.hide()
        self.x_upper_lim.hide()
        self.y_low_lim.hide()
        self.y_upper_lim.hide()
        self.area_label.hide()
        self.figure.clear()


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingCalculator()
    window.show()
    sys.exit(app.exec())