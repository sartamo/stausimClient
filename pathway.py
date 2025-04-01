import numpy as np
import matplotlib.pyplot as plt

size = 1000

def circle(radius):
    center = size // 2
    y, x = np.ogrid[:size, :size]
    distance_center = np.sqrt((x - center) ** 2 + (y - center) ** 2)
    mask = abs(distance_center - radius) <= 1
    matrix = np.zeros((size, size), dtype=int)
    matrix[mask] = 1
    return matrix

plt.imshow(circle(400), cmap='gray')
plt.title("1000x1000 Matrix with a Circle of Ones")
plt.show()