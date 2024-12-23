import numpy as np
import matplotlib.pyplot as plt

# Data points
class_pos = np.array([[0,0], [0,1], [1,0]])
class_neg = np.array([[1,1], [2,2], [2,0]])

# Create plot
plt.figure(figsize=(8, 6))

# Plot positive class points
plt.scatter(class_pos[:,0], class_pos[:,1], color='blue', label='Class +1', marker='o', s=100)

# Plot negative class points
plt.scatter(class_neg[:,0], class_neg[:,1], color='red', label='Class -1', marker='x', s=100)

# Add labels for each point
for point in class_pos:
    plt.annotate(f'({point[0]},{point[1]})', (point[0], point[1]), xytext=(10,10), textcoords='offset points')
for point in class_neg:
    plt.annotate(f'({point[0]},{point[1]})', (point[0], point[1]), xytext=(10,10), textcoords='offset points')

# Draw a separating line (y = x)
x = np.linspace(-0.5, 2.5, 100)
plt.plot(x, x, '--k', label='Separating Line (y=x)')

plt.grid(True)
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data Points with Separating Line')
plt.axis([-0.5, 2.5, -0.5, 2.5])
plt.show()