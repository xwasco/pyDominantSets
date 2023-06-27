import numpy as np


def repdyn(A, x=None, maxiters=100, epsilon=1e-8):

    if x is None:
        x = np.zeros(A.shape[0])+1./float(A.shape[0])
    
    distance = epsilon*2.0
    iter = 0
    cohes = 0.0
    while iter < maxiters and distance > epsilon:
        x_old = np.copy(x)
        x = x* A.dot(x)
        cohes = x.sum()
        x = x/ cohes
        distance = np.sqrt(np.sum((x-x_old)**2))
        iter += 1
    return x, iter, cohes



def getDSs(A, minsize=1, maxiters=1000, eps=1e-6):

    n = A.shape[0]
    V = np.arange(0, n)
    C = []
    W = []

    while np.sum(A)>0:
        x, iters, cohes = repdyn(A, maxiters=maxiters)

        idx = np.where(x>=eps)

        C.append(tuple(V[idx]))
        W.append([cohes, iters])

        V = np.delete(V,idx)
        A = np.delete(A, idx, axis=0)
        A = np.delete(A, idx, axis=1)

    if minsize>0:
    
        if minsize==1:
            for id in V:
                C.append(tuple([id])) 
        else:
            for i in enumerate(C):
                if len(i[1])<minsize:
                    C.pop(i[0])
                    W.pop(i[0])

    return C,W
