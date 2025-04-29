
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x = np.linspace(-10, 10, 100)
y1 = np.log(x)
y2 = np.sin(x)
y3 = x**3

ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])

plt.plot(x, y1, label="y = log(x)")
plt.plot(x, y2, label="y = sin(x)")
plt.plot(x, y3, label="y = x^3")
plt.xlabel("x")
plt.ylabel("y", rotation= 0)
plt.title("Multiple Graphs")
plt.grid(True)
plt.legend()

plt.show()