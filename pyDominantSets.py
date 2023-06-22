import numpy as np
import time
import igraph


def repdyn(A, x=None, maxiters=100, epsilon=1e-8):

    if x is None:
        x = np.zeros(A.shape[0])+1./float(A.shape[0])
    
    #distance = epsilon*2.0
    iter = 0
    cohes = 0.0
    while iter < maxiters:
        x = x* A.dot(x)
        cohes = x.sum()
        x = x/ cohes
        iter += 1
    return x, iter, cohes

def getDSs(A, minsize=0, maxiters=1000, eps=1e-6):

    n = A.shape[0]
    V = np.arange(0, n)
    C = []
    W = []
    
    if minsize>0:
        eps = 1./10**(minsize+1)

    while np.sum(A)>0:
        t1 = time.perf_counter()
        x, iter, cohes = repdyn(A, maxiters=maxiters)
        t2 = time.perf_counter()

        idx = np.where(x>=eps)

        C.append(tuple(V[idx]))
        W.append([cohes, (t2 - t1)*1000])

        V = np.delete(V,idx)
        A = np.delete(A, idx, axis=0)
        A = np.delete(A, idx, axis=1)

    if minsize>0:
    
        if minsize==1: # we still have isolated nodes assign each to a separate cluster
            for id in V:
                C.append([id]) 

        for i in enumerate(C):
            if len(i[1])<minsize:
                C.pop(i[0])
                W.pop(i[0])

    #for i in enumerate(C):
    #     for j in enumerate(C):
    #        if i!=j:
    #            if len(np.intersect1d(np.array(i[1]),np.array(j[1])))>0:
    #                print("Errore negli ID")

    

    return C,W


n = 1000
A = np.random.rand(n,n)

A = (A+A.T)/2
A = A*(1-(np.eye(A.shape[0])))

A = np.array(A>0.5, dtype=float)
t1 = time.perf_counter()
C,W = getDSs(A, minsize=3)
t2 = time.perf_counter()
tds = t2-t1
print(f'Search maximal cliques: %.2fms' % ((t2 - t1) * 1000))

graph = igraph.Graph.Adjacency(A.tolist())
graph.to_undirected()
graph.es['weight'] = A[A.nonzero()]
graph.vs['label'] = range(0, A.shape[0])
t1 = time.perf_counter()
macs = graph.maximal_cliques(min=3)
t2 = time.perf_counter()
tbk = t2 - t1
print(f'Search maximal cliques: %.2fms' % ((t2 - t1) * 1000))
print(tds,tbk)