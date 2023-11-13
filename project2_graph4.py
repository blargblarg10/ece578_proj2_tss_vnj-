import re
import os
import matplotlib.pyplot as plt
import numpy as np
import math

file_list = {
  "2021": {"file":'/mnt/c/Users/Tyler Somers/Documents/ece578/ece578_proj2_tss_vnj/20210401.as2types.txt'}
  }

data_per_class = {}

for year, file_info in file_list.items():
    file_path = file_info["file"]

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"ERROR: File {file_path} does not exist")
        continue

    with open(file_path, 'r') as fp:
        data = {}
        for line in fp:
            if line.startswith('#'):
                continue
            elements = line.split('|')
            ASes = elements[1].strip()
            classes = elements[2].strip()

            # Initialize the nested dictionary for 'classes' if it doesn't exist
            if classes not in data:
                data[classes] = {}

            # Increment the count for 'ASes' under the specific 'classes'
            data[classes][ASes] = data[classes].get(ASes, 0) + 1

data_per_class = data

# Calculating total counts for each year
total_counts_per_class = {classes: sum(data.values()) for classes, data in data_per_class.items()}

# Calculating percentages
percentages_per_class = {}
for classes in data_per_class:
    total = total_counts_per_class[classes]
    percentages_per_class[classes] = {ASes: (count / total) * 100 for ASes, count in data_per_class[classes].items()}

# Number of years and ASes
num_classes = len(percentages_per_class)
num_ases = len(set(ases for data in data_per_class.values() for ases in data))

# Width of a bar
bar_width = 0.8 / num_ases  # Adjust the width as needed

# X locations for the groups
indices = np.arange(num_classes)

# Plotting
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

for i, ASes in enumerate(set(ases for data in data_per_class.values() for ases in data)):
    # Offset each ASes bar
    offset = (i - num_ases / 2) * bar_width + bar_width / 2
    ases_percentages = [class_data.get(ASes, 0) for class_data in percentages_per_class.values()]
    bars = plt.bar(indices + offset, ases_percentages, bar_width, label=ASes)

    # Adding text labels above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

# Setting x-ticks and labels
plt.xticks(indices, percentages_per_class.keys())
plt.xlabel('classes')
plt.ylabel('Percentage of ASes')
plt.title('Percentage of ASes per classes')
plt.legend()

plt.tight_layout()
plt.show()
pass