import numpy as np
#import matplotlib.pyplot as plt
from scipy.spatial import KDTree

size = 1000

def circle(radius):
    center = size // 2
    y, x = np.ogrid[:size, :size]
    distance_center = np.sqrt((x - center) ** 2 + (y - center) ** 2)
    mask = abs(distance_center - radius) <= 2
    matrix = np.zeros((size, size), dtype=int)
    matrix[mask] = 1
    return matrix

class Track:
    def __init__(self, matrix):
        self.matrix = matrix
        self.points = np.argwhere(matrix == 1)
        self.tree = KDTree(self.points)

    def nearest(self, point):
        distance, index = self.tree.query(point)
        return (distance, self.points[index])

if __name__ == "__main__":
    track = Track(circle(400))
    print(track.nearest((145,278)))

'''
plt.imshow(circle(400), cmap='gray')
plt.title("1000x1000 Matrix with a Circle of Ones")
plt.show()
'''