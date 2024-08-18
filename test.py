import numpy as np

b1 = np.array([1, 0])
b2 = np.array([0.2, 1])

t = np.array([0.5, 0.5])

c1 = b1 * (np.dot(b1, t)) / np.linalg.norm(b1)**2
c2 = b2 * (np.dot(b2, t)) / np.linalg.norm(b2)**2

print(c1 + c2)