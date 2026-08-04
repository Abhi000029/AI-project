import numpy as np

numbers = [1, 2, 3, 4, 5]
min_value = np.min(numbers)
max_value = np.max(numbers)
mode_value = np.mode(numbers)

print("Minimum value:", min_value)
print("Maximum value:", max_value)
print("Mode value:", mode_value)

#using pandas to create a DataFrame and calculate the mean of a column
import pandas as pd
import numpy as np
data = {
    "numbers": [1, 2, 3, 4, 5]
}
df = pd.DataFrame(data)
mean_value = df["numbers"].mean()   
print("Mean value:", mean_value)
