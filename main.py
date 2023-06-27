import pyDominantSets as DS
import numpy as np
import time


# create a random graph
n = 100
A = np.random.rand(n,n)

A = (A+A.T)/2
A = A*(1-(np.eye(A.shape[0])))

A = np.array(A>0.8, dtype=float)  # this can be also weighted

# run DominantSet on the Affinity matrix... and check time
t1 = time.perf_counter()
C,W = DS.getDSs(A, minsize=2)
t2 = time.perf_counter()
tds = t2-t1
print(f'Search maximal cliques DS: %.2fms' % (tds * 1000))
print(f'Number of cliques DS: %.2f' % (len(C)))
print(C)
print(W)
print("\n")
