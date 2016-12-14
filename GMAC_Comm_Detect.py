import networkx as nx
import matplotlib .pyplot as plt

#Zachary's karate graph
G=nx.karate_club_graph()			
pos = nx.spring_layout(G)
labels = {}
sp_u = []
sp_v = []
q = []
s = []
a = []
w = []
quo = []
num = []
denom = []
neigh = []
neigh1 = []
list_is_a = []
list_es_a = []
k = 0

#Finding the shortest path with d=1 from
#two selected nodes
def find_sp(u):
    q = []
    for n in G:
        labels[n] = n
        sp_u =  nx.shortest_path(G,u,n)
            
        if len(sp_u) == 2:
            q.append(n)
    
    return q

q = find_sp(17)
s = find_sp(3)

#Selecting nodes common to both the selected nodes
for i in range(len(q)):
    for j in range(len(s)):
        if q[i] == s[j]:
            a.append(q[i])
			
#Creating a sub set of nodes common between 17 and 3
for i in range(len(a)):
    if i == 0:   
        x = find_sp(a[i]) 
    else:
        y = find_sp(a[i]) 
     
#Elements connected to the subgraph created [17,3,0,1]
def find_sp_from_i(k, w):
    q = []
    for i in w:
        sp_u =  nx.shortest_path(G,k,i)
        
        if len(sp_u) == 2:
           q.append(i)
    
    return q

#Elements connected to the community 
first_iter_1 = find_sp_from_i(1, x)
second_iter_1 = find_sp_from_i(1, s)

first_iter_0 = find_sp_from_i(0, y)
second_iter_0 = find_sp_from_i(0, s)

first_iter_3 = find_sp_from_i(3, x)
second_iter_3 = find_sp_from_i(3, y)

first_iter_17 = find_sp_from_i(17, x)
second_iter_17 = find_sp_from_i(17, y)
third_iter_17 = find_sp_from_i(17, s)

# Finding phi value between 1 and 0
def phi(ele1,ele2,inter):
    quo = float(float(len(inter))/float((len(ele1)) + float(len(ele2)) - float(len(inter))))
    return quo

phi_1_to_0 = phi(y, x, first_iter_1)
phi_1_to_3 = phi(y, s, second_iter_1)
phi_0_to_1 = phi(x, y, first_iter_0)
phi_0_to_3 = phi(x, s, second_iter_0)
phi_3_to_0 = phi(s, x, first_iter_3)
phi_3_to_1 = phi(s, y, second_iter_3)
phi_17_to_0 = phi(q, x, first_iter_17)
phi_17_to_1 = phi(q, y, second_iter_17)
phi_17_to_3 = phi(q, s, third_iter_17)

# Denominator to find CI
sum_of_all_phis = phi_1_to_0 + phi_1_to_3 + phi_0_to_1 + phi_0_to_3 + phi_3_to_0 + phi_3_to_1 + phi_17_to_0 + phi_17_to_1 + phi_17_to_3

# numerator of find CI
sum_of_num_phis = phi_17_to_0 + phi_17_to_1 + phi_17_to_3 + phi_1_to_0 +  phi_3_to_1 + phi_0_to_3

#Compactness Isolation of the community
CI = float(float(sum_of_num_phis) / float((1 + sum_of_all_phis)))
print "CI value is: " , CI

#Compute the neighbour set of the community
comm = [17, 0, 1, 3]
neigh = first_iter_1 + second_iter_17 + third_iter_17 + second_iter_0 +  second_iter_1 +  first_iter_17
neigh = set(neigh) - set(comm)
neigh = list(neigh)

#Computation of the IS value   
for ele1 in neigh:
    sum_phi_is = 0
    for ele in comm:
        sp_x_is =  nx.shortest_path(G,ele1,ele)
        sum_phi_is = sum_phi_is + float(float(len(sp_x_is))/float(len(find_sp(ele1)) + float(len(find_sp(ele)))- float(len(sp_x_is))))
    list_is_a.append(sum_phi_is)

#Computation of the ES value
for ele1 in neigh:
    sum_phi_es = 0
    for ele in neigh:
        if ele1 != ele:
            sp_x_es =  nx.shortest_path(G,ele1,ele)
            sum_phi_es = sum_phi_is + float(float(len(sp_x_es))/float(len(find_sp(ele1)) + float(len(find_sp(ele)))- float(len(sp_x_es))))
    list_es_a.append(sum_phi_es)

num = list_is_a

#Compute the value IS/(IS-ES)
denom.append([list_es_a - list_is_a for list_es_a, list_is_a in zip(list_es_a,list_is_a)])
denom = denom.pop(0) # to get the list out of a list

quo.append([(num/denom) for num, denom in zip(num,denom)])
quo = quo.pop(0)
print "\nIS(a) / ES(a) - IS(a) = " , quo

#Comparison of IS/(IS-ES) and CI
for ele in quo:
    if ele > CI:
        comm.append(neigh[quo.index(ele)])
        
print "\nCommunity found after the addition of new nodes:"
print comm





