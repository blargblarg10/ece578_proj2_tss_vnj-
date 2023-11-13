import re
import matplotlib.pyplot as plt
import math

# ---------------------------------------------------------
# Graph 3 Data calculations
# ---------------------------------------------------------

# Initialize the dictionary for IP counts
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
                ip_counts[as_number] = ip_counts.get(as_number, 0) + 2 ** (128 - mask)

# Function to determine the logarithmic bin index with a lower bound
def get_log_bin_index(ip_count, lower_bound=24, upper_bound=30):
    if ip_count == 0:
        return 0
    bin_index = int(math.log10(ip_count))
    return min(max(bin_index, lower_bound), upper_bound)  # Ensure bin index is not below the lower bound

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
