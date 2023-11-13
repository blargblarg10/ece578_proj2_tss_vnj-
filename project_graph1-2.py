import re
import os
import matplotlib.pyplot as plt
import numpy as np
import math

def degree(a_s):
  return (len(a_s[0])+len(a_s[1])+len(a_s[2]))



# as_exists = []
# as_array = []
# for i in range(500000):
#   as_exists.append(0)
#   as_array.append([[],[],[]]) #Provider list, Customer list, Peer list


# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Read from file and create data set
#
# ---------------------------------------------------------
# ---------------------------------------------------------

file_list = {
  "2015": {"file":'/mnt/c/Users/Tyler Somers/Documents/ece578/ece578_proj2_tss_vnj/20150801.as2types.txt'}, 
  "2021": {"file":'/mnt/c/Users/Tyler Somers/Documents/ece578/ece578_proj2_tss_vnj/20210401.as2types.txt'}
  }

data_per_year = {}

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
            data[ASes] = data.get(ASes, 0) + 1

        data_per_year[year] = data

    print("Year:", year)
    print("Data:", data)

# ...

# Calculating total counts for each year
total_counts_per_year = {year: sum(data.values()) for year, data in data_per_year.items()}

# Calculating percentages
percentages_per_year = {}
for year in data_per_year:
    total = total_counts_per_year[year]
    percentages_per_year[year] = {ASes: (count / total) * 100 for ASes, count in data_per_year[year].items()}

# Number of years and ASes
num_years = len(percentages_per_year)
num_ases = len(set(ases for data in data_per_year.values() for ases in data))

# Width of a bar
bar_width = 0.8 / num_ases  # Adjust the width as needed

# X locations for the groups
indices = np.arange(num_years)

# Plotting
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

for i, ASes in enumerate(set(ases for data in data_per_year.values() for ases in data)):
    # Offset each ASes bar
    offset = (i - num_ases / 2) * bar_width + bar_width / 2
    ases_percentages = [year_data.get(ASes, 0) for year_data in percentages_per_year.values()]
    bars = plt.bar(indices + offset, ases_percentages, bar_width, label=ASes)

    # Adding text labels above each bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

# Setting x-ticks and labels
plt.xticks(indices, percentages_per_year.keys())
plt.xlabel('Year')
plt.ylabel('Percentage of ASes')
plt.title('Percentage of ASes per Year')
plt.legend()

plt.tight_layout()
plt.show()

# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Read from file and create data set
#
# ---------------------------------------------------------
# ---------------------------------------------------------

as_exists = []
as_array = []
for i in range(506306):
  as_exists.append(0)
  as_array.append([[],[],[]]) #Provider list, Customer list, Peer list

fp = open('/mnt/c/Users/Tyler Somers/Documents/ece578/ece578_proj2_tss_vnj/2023.AS-rel.txt', 'r')

line = fp.readline()
line_cnt = 1
while line :#and line_cnt < 200:
    line_cnt += 1
    if line[0] != '#':
        elements = line.split('|')
        asA = int(elements[0])
        asB = int(elements[1])

        type = int(elements[2])
        #print('A = ', asA, 'B = ', asB, 'Type = ',type)
        if as_exists[asA] != 1:
          as_exists[asA] = 1
          #print(as_array[asA])
        if as_exists[asB] != 1:
          as_exists[asB] = 1
        
        if type == -1:
          if asB not in as_array[asA][1]:
            as_array[asA][1].append(asB)
          if asA not in as_array[asB][0]:
            as_array[asB][0].append(asA) 
        elif type == 0:
          if asB not in as_array[asA][2]:
            as_array[asA][2].append(asB)
          if asA not in as_array[asB][2]:
            as_array[asB][2].append(asA) 
   
       # print(elements)
        #print("Line {}: {}".format(line_cnt, line.split('|')))
    line = fp.readline()

as_list = []  #[number, degree, [[Provider set], [Customer set], [Peer set]]]
count = 0

for i in range(len(as_exists)):
  if as_exists[i]:
    count += 1
    as_list.append([i,degree(as_array[i]),as_array[i]])

print('Number of elements = ', count)
print('Number of elements = ', len(as_list))

print('item 0 = ',as_list[0])
print('item 1 = ',as_list[1])


# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Graph 2 Data calculations
#
# ---------------------------------------------------------
# ---------------------------------------------------------

node_degrees = []

#Calculat node degrees for each AS
for i in range(len(as_exists)):
  if as_exists[i]:
    node_degrees.append((len(as_array[i][0])+len(as_array[i][1])+len(as_array[i][2])))
print('node_degree 1 = ',node_degrees[0])
bins = [0] * 7
for degree in node_degrees:
  if degree == 0:
    bins[0] += 1
  elif degree == 1:
    bins[1] += 1
  elif degree <= 5:
    bins[2] += 1
  elif degree <= 100:
    bins[3] += 1
  elif degree <= 200:
    bins[4] += 1
  elif degree <= 1000:
    bins[5] += 1
  else:
    bins[6] += 1
    
    
    

print("Graph 2 Data:")
print("Bin1 = ",bins[0])
print("Bin2 = ",bins[1])
print("Bin3 = ",bins[2])
print("Bin4 = ",bins[3])
print("Bin5 = ",bins[4])
print("Bin6 = ",bins[5])
print("Bin7 = ",bins[6])

# Plotting
x_label = ["0", "1", "2-5", "6-100", "101-200", "201-1000", ">1000"]
x_pos = range(len(bins))

plt.bar(x_pos, bins, color='green')
plt.xlabel("Degree Bins")
plt.ylabel("Number of AS")
plt.title("AS Node Degree Distribution")
plt.xticks(x_pos, x_label)

plt.show()


# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Graph 3 Data calculations
#
# ---------------------------------------------------------
# ---------------------------------------------------------
# Initialize the list for IP counts
ip_counts = {}

# Open the data file
with open('/mnt/c/Users/Tyler Somers/Documents/ece578/ece578_proj2_tss_vnj/routeviews-rv6-20231105-1200.pfx2as.txt', 'r') as fp2:
    for line in fp2:
        elements = line.split()
        mask = int(elements[1])
        as_set = re.split(',|_', elements[2])
        for a_s in as_set:
            as_number = int(a_s)
            if as_number < 500000:
                ip_counts[as_number] = ip_counts.get(as_number, 0) + 2 ** (32 - mask)

# Function to determine the logarithmic bin index
def get_log_bin_index(ip_count):
    if ip_count == 0:
        return 0
    return int(math.log10(ip_count))

# Create a dictionary for logarithmic bin counts
log_bin_counts = {}

for count in ip_counts.values():
    if count > 0:
        bin_index = get_log_bin_index(count)
        log_bin_counts[bin_index] = log_bin_counts.get(bin_index, 0) + 1

# Prepare data for plotting
bins = sorted(log_bin_counts.keys())
counts = [log_bin_counts[bin_index] for bin_index in bins]

# Plotting
plt.bar(bins, counts, width=0.4, color='blue', align='center')
plt.xlabel('Logarithmic Bin (10^x)')
plt.ylabel('Number of ASes')
plt.title('Histogram of IP Space Size Assigned to Each AS')
plt.xticks(bins, [f"10^{i}" for i in bins])  # Set x-axis labels as 10^bin_index
plt.show()
pass