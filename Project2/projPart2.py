#from AS import *
#from matplotlib import pyplot as plt
#from matplotlib import style
#import numpy as np
import re


def degree(a_s):
  return (len(a_s[0])+len(a_s[1])+len(a_s[2]))



as_exists = []
as_array = []
for i in range(500000):
  as_exists.append(0)
  as_array.append([[],[],[]]) #Provider list, Customer list, Peer list


# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Read from file and create data set
#
# ---------------------------------------------------------
# ---------------------------------------------------------


fp = open('/mnt/c/Users/Tyler Somers/Documents/ece578/project2/Project2/20201001.as-rel2.txt', 'r')

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
node_degree_bins = [0,0,0,0,0,0]
for degree in node_degrees:
  if degree == 0:
    print("***ERORRO*** Should be no degrees equal to 0")
  elif degree == 1:
    node_degree_bins[0] += 1
  elif degree <= 5:
    node_degree_bins[1] += 1
  elif degree <= 100:
    node_degree_bins[2] += 1
  elif degree <= 200:
    node_degree_bins[3] += 1
  elif degree <= 1000:
    node_degree_bins[4] += 1
  else:
    node_degree_bins[5] += 1
    

print("Graph 2 Data:")
print("Bin1 = ",node_degree_bins[0])
print("Bin2 = ",node_degree_bins[1])
print("Bin3 = ",node_degree_bins[2])
print("Bin4 = ",node_degree_bins[3])
print("Bin5 = ",node_degree_bins[4])
print("Bin6 = ",node_degree_bins[5])

#Graph2
x_label = ["1","2-5","5-100","100-200","200-1000",">1000"]
pre_x_data = [node_degree_bins[0],node_degree_bins[1],node_degree_bins[2],node_degree_bins[3],node_degree_bins[4],node_degree_bins[5]]
y_total = 0
for i in range(6):
	y_total += pre_x_data[i]
x_data = []
for i in range(6):
	x_data.append(pre_x_data[i]/y_total)
	#print("x_data[",i, "]= ",x_data[i])

#x_pos = [i for i, _ in enumerate(x_label)]

#plt.bar(x_pos, x_data, color='green')
#plt.xlabel("Bins")
#plt.ylabel("% of Connections")
#plt.title("AS Node Degree Distribution")
#plt.xticks(x_pos, x_label)
#
#plt.savefig('graph_2.png')


# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Graph 3 Data calculations
#
# ---------------------------------------------------------
# ---------------------------------------------------------
ip_counts = []
for i in range(650000):
  ip_counts.append(0)
fp2 = open('/mnt/c/Users/Tyler Somers/Documents/ece578/project2/Project2/routeviews-rv2-20201114-1200.pfx2as', 'r')

line = fp2.readline()
line_cnt = 1
while line :#and line_cnt < 30027:
  line_cnt += 1
  elements = line.split()
  mask = int(elements[1])
  as_set = re.split(',|_',elements[2])
  #print('as_set = ', as_set)
  for a_s in as_set:
    if int(a_s) < 500000:
      #print(' line_Cnt = ', line_cnt,'  a_s = ', a_s)
      ip_counts[int(a_s)] += 2 ** (32-mask)
  line = fp2.readline()



#print('AS[6939] IP Count = ', ip_counts[6939])


ip_list = []
for a_s in as_list:
  ip_list.append([a_s[0],ip_counts[a_s[0]]])


ip_cnt_bins = [0,0,0,0,0,0]
for ip_cnt in ip_list:
  if ip_cnt[1] <= 3000:
    ip_cnt_bins[1] += 1
  elif ip_cnt[1] <= 10000:
    ip_cnt_bins[2] += 1
  elif ip_cnt[1] <= 100000:
    ip_cnt_bins[3] += 1
  elif ip_cnt[1] <= 2000000:
    ip_cnt_bins[4] += 1
  else:
    ip_cnt_bins[5] += 1
    

print("\n\nGraph 3 Data:")
print("Bin1 = ",ip_cnt_bins[0])
print("Bin2 = ",ip_cnt_bins[1])
print("Bin3 = ",ip_cnt_bins[2])
print("Bin4 = ",ip_cnt_bins[3])
print("Bin5 = ",ip_cnt_bins[4])
print("Bin6 = ",ip_cnt_bins[5])


#
#
#ip_sort = []
#for a_s in ip_list:
#  inserted = 0
#  #print('a_s = ', a_s)
#  if len(ip_sort) > 0:
#    for i in range(len(ip_sort)):
#      if a_s[1] >= ip_sort[i][1]:
#        ip_sort.insert(i, a_s)
#        inserted = 1
#        break
#  if inserted == 0:
#    ip_sort.append(a_s)
#  
#    
#for i in range(10):
#  print('AS[',ip_sort[i][0],'] IP Count = ',ip_sort[i][1])




# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Graph 4 Data calculations
#
# ---------------------------------------------------------
# ---------------------------------------------------------

as_entrprs = 0
as_content = 0
as_transit = 0

no_fit = 0

for a_s in as_list:
  if len(a_s[2][1]) == 0 and len(a_s[2][2]) == 0: #Enterprise AS: No customers or Peers
    as_entrprs += 1
  elif len(a_s[2][1]) == 0 and len(a_s[2][2]) > 0: #Content AS: No customers and at least 1 Peer
    as_content += 1
  elif len(a_s[2][1]) > 0: #Transit AS: At least one customer
    as_transit += 1
  else:
    no_fit += 1

print("\n\nGraph 4 Data:")
print("Enterprise ASs: ",as_entrprs)
print("Content ASs: ",as_content)
print("Transit ASs: ",as_transit)

print("no fit ASs = ", no_fit)



def is_connected(asA, asB): #is asA connected to asB (is asA inside one of asB's connection lists)
  #print('is_connected ', asA, '  ', asA[0], '  ', asB[2])
  for a_s in asB[2][0]:
    if asA[0] == a_s:
      return 1
  for a_s in asB[2][1]:
    if asA[0] == a_s:
      return 1
  for a_s in asB[2][2]:
    if asA[0] == a_s:
      return 1
  for a_s in asA[2][0]:
    if asB[0] == a_s:
      return 1
  for a_s in asA[2][1]:
    if asB[0] == a_s:
      return 1
  for a_s in asA[2][2]:
    if asB[0] == a_s:
      return 1
  return 0



# ---------------------------------------------------------
# ---------------------------------------------------------
#
# 2.3 Data calculations
#
# ---------------------------------------------------------
# ---------------------------------------------------------

as_sort = []
for a_s in as_list:
  inserted = 0
  #print('a_s = ', a_s)
  if len(as_sort) > 0:
    for i in range(len(as_sort)):
      if a_s[1] >= as_sort[i][1]:
        as_sort.insert(i, a_s)
        inserted = 1
        break
  if inserted == 0:
    as_sort.append(a_s)
  
    
#for i in range(10):
#  print('AS[',as_sort[i][0],'] Degree = ',as_sort[i][1])



# Inference of T1 Algorithm

S = []
S.append(as_sort.pop(0))
#print('S[0] = ', S[0])
#print('as_sort[0] = ', as_sort[0])
as_sort[0][2][0].append(S[0][0])
#print('S[0] = ', S[0])
#print('as_sort[0] = ', as_sort[0])
#print('s = ', S)
cnt = 0
while len(as_sort) > 0 and len(S) < 10:
  asA = as_sort.pop(0)
  #print('S = ', S)
  connected_to_all = 1
  for asB in S:
    if not is_connected(asA, asB):
      connected_to_all = 0
      break
  if not connected_to_all:
    if cnt<50:
      cnt += 1
    else:
      break
  else:
    S.append(asA)


S_list = []
for a_s in S:
  S_list.append(a_s[0])

print("\n\n2.3 Data:")
print('Clique S = ', S_list)



def get_as(as_id):
  for a_s in as_list:
    if a_s[0] == as_id:
      return a_s
  print('ERROR AS ID ', as_id, ' not found')

as_dict = {}

for a_s in as_list:
  as_dict[a_s[0]] = a_s

def find_customers(a_s):
  new_cust_list = []
  if len(a_s[2][1]) > 0: #if AS has customers
    for cust in a_s[2][1]:
      new_cust_list.extend(find_customers(as_dict[cust]))
  else:
    new_cust_list.append(a_s)
  return new_cust_list




# ---------------------------------------------------------
# ---------------------------------------------------------
#
# 2.4 Data calculations
#
# ---------------------------------------------------------
# ---------------------------------------------------------

#as_cust_cones = {}
#for a_s in as_list:
#  as_cust_cones[a_s[0]] = find_customers(a_s)
#cust_cone1 = find_customers(as_list[0])
#cust_list = []
#for cust in as_cust_cones.get(as_list[0][0]):
#  cust_list.append(cust[0])
#
#print('first cust_cone ', as_cust_cones.get(as_list[0][0]))
#
#top_10_cust_cones = []
#for i in range(10):
#  max_val = 0
#  max_as = []
#  for a_s in as_list:
#    if len(as_cust_cones.get(a_s[0])) > max_val:
#      max_val = len(as_cust_cones.get(a_s[0]))
#      max_as = a_s[0]
#  top_10_cust_cones.append([max_as,max_val])
#  as_cust_cones.pop(max_as)
#
#
#print('Top 10 AS Customer Cones ', top_10_cust_cones)

