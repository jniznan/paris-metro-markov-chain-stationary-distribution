from __future__ import division
from collections import defaultdict

# Connexions_IDF.csv taken from https://github.com/sandavid/paris-metro-map
f = open("Connexions_IDF.csv")
lines = f.readlines()
f.close()

G = defaultdict(set)
for line in lines:
    if line[0] != "#":
        spl = line.split(";")
        G[spl[1]].add(spl[2])

# H is a graph representing links leading into a node (w/ probabilities)
H = defaultdict(dict)
for st in G:
    for st_ in G[st]:
        H[st_][st] = 1/len(G[st])

ALPHA = 1

pi = {st: 1/len(G) for st in H}
err = float("inf")
it = 0
while err > 1e-10:
    oldpi = pi.copy()
    err = 0
    it += 1
    tmp = sum(oldpi.values()) / len(G)
    for st in pi:
        pi[st] = ALPHA * sum(oldpi[st_]*H[st][st_] for st_ in H[st]) + \
                (1-ALPHA) * tmp
        err += abs(oldpi[st] - pi[st])
    # uncomment the following lines if you want the algorithm to stop 
    # when the order is no longer changing
#    if sorted(pi.keys(), key= lambda x: pi[x], reverse=True) == \
#       sorted(pi.keys(), key= lambda x: oldpi[x], reverse=True):
#        break
        
stations = sorted(pi.keys(), key= lambda x: pi[x], reverse=True)

for st in stations[:10]:
    print st.ljust(25), pi[st]

print "# of iterations:", it