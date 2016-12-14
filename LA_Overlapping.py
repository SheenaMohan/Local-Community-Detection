import networkx as nx
import matplotlib .pyplot as plt

G=nx.karate_club_graph()
pos = nx.spring_layout(G)
labels = {}
rank_int = []
c = []
rank = []
w_int = []
j = 0
k = []
popped = []
inter = []
inter_sum1 = []
fc = []
prev_rank = []
prev_c = []
sum_rank = 0

#Community set
c = [0, 3, 33, 12, 29, 5, 19, 7]
print "Community under test : ", c
def find_sp(u):
    q = []
    for n in G:
        labels[n] = n
        sp_u =  nx.shortest_path(G,u,n)
            
        if len(sp_u) == 2:
            q.append(n)
    return q

#Computing distance of all nodes connected to the community
for i in c:
    rank_int.append(find_sp(i))
    rank.append(len(find_sp(i)))

#Computing the summation of distances
for i in rank:
    sum_rank = sum_rank + i

#Computing the distance of nodes within the community
for i in c:
    c.pop(rank.index(max(rank)))
    rank_int.pop(rank.index(max(rank)))
    rank.pop(rank.index(max(rank)))    
    inter_sum = 0
    w_int = []    
    for list in rank_int:
        count = 0
        for num in list:
            for m in c:
                if num == m:
                    count = count + 1
        inter_sum = inter_sum + count       
        w_int.append(count)
    inter_sum1.append(inter_sum)
    inter.append(w_int)

# Computing the lamda value
for i in inter_sum1:
    fc.append(float(i) / float(sum_rank))
print "\nFitness function value = ", fc