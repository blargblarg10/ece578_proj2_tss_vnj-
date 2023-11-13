import re
import os
import matplotlib.pyplot as plt
import numpy as np
import math

def degree(a_s):
  return (len(a_s[0])+len(a_s[1])+len(a_s[2]))

# ---------------------------------------------------------
# ---------------------------------------------------------
#
# Read from file and create data set
#
# ---------------------------------------------------------
# ---------------------------------------------------------

as_exists = []
as_array = []
for i in range(500000):
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