import numpy as np

# Example 2D array
arr = np.loadtxt('test3.txt')

print(arr)
# Find the maximum value in each row
max_values_rows = np.max(arr, axis=1)
print(max_values_rows)
# Calculate the mean of these maximum values
mean_of_max_values = np.mean(max_values_rows)

print(f"Mean of the maximum values in each row: {mean_of_max_values}")
