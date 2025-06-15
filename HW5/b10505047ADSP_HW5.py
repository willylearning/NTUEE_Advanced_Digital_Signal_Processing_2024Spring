import numpy as np
# input example: 
# if you want x = [1, 2, 3], then enter 1 2 3
# if you want y = [4, 5, 6], then enter 4 5 6
x_input = input("Please enter the first N-point real signal : ")
y_input = input("Please enter the second N-point real signal : ")

x = np.array([float(val) for val in x_input.split()])
y = np.array([float(val) for val in y_input.split()])

x = np.array(x).flatten()
y = np.array(y).flatten()

# Step 1
z = x + 1j * y

# Step 2
Fz = np.fft.fft(z)

# Step 3
Fx = (Fz + np.conj(np.roll(Fz[::-1], 1))) / 2        # even sequence
Fy = (Fz - np.conj(np.roll(Fz[::-1], 1))) / (2j)     # odd sequence

print("Fx = ", Fx)
print("Fy = ", Fy)