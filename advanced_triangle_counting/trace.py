import networkx as nx
import numpy as np
import concurrent.futures
 
def TraceTriangleN(graph, gamma = 1, parallel = False):
    T = []
    A = nx.adjacency_matrix(graph)
    n = A.shape[0]
    M = np.ceil(gamma*np.log(n)**2)
    if (parallel == True):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = [executor.submit(core,A,n,1) for _ in range(0,int(M)) ]
            for f in concurrent.futures.as_completed(res):
                T.append(f.result())
    else:
        for i in range(0,int(M)):
            x = np.array(np.random.normal(size = n))
            y = A*np.matrix(x).transpose()
            T.append((y.T * A * y)/6)
    delta = sum(T)/len(T)
    return delta

def TraceTriangleR(graph, gamma = 1, parallel = False):
    T= []
    A = nx.adjacency_matrix(graph)
    n = A.shape[0]
    M = np.ceil(gamma*np.log(n)**2)
    if (parallel == True):
        with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
            res = [executor.submit(core,A,n,2) for _ in range(0,int(M)) ]
            for f in concurrent.futures.as_completed(res):
                T.append(f.result())
    else:
        for i in range(0,int(M)):
            x = np.array(rademacher(size = n))
            y = A*np.matrix(x).transpose()
            T.append((y.T * A * y)/6)
    delta = sum(T)/len(T)
    return delta

def TraceTriangleM(graph, gamma = 1, parallel = False):
    T = []
    A = nx.adjacency_matrix(graph)
    n = A.shape[0]
    D = np.matrix(np.zeros((n, n), int))
    diag = list(map(lambda a: 1 if a>0.5  else -1, np.random.uniform(size = n)))
    np.fill_diagonal(D, diag)
    M = np.ceil(gamma*np.log(n)**2)
    if (parallel == True):
        with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
            res = [executor.submit(core, A, n, D, 3) for _ in range(0, int(M)) ]
            for f in concurrent.futures.as_completed(res):
                T.append(f.result())
    else:
        for i in range(0,int(M)):
            j = int(np.random.uniform(1, n))
            x = [np.sqrt(1/n) if j == 1 else np.sqrt(2/n)*np.cos(np.pi*(k+0.5)*j/n) for k in range(n)]
            y = A*D*np.matrix(x).transpose()
            T.append(n*(y.T * A * y)/6)
    delta = np.sum(T)/len(T)
    return delta


def rademacher(size=1):
    a = np.random.uniform(size = size)
    b = list(map(lambda a: 1 if a>0.5  else -1,a))
    return b

def core(Adjacency, n, D=None, mode=1):
    if mode == 2:
        x = np.array(rademacher(size = n))
        y = Adjacency*np.matrix(x).transpose()
        T = ((y.T * Adjacency * y)/6)
    elif mode == 1:
        x = np.array(np.random.normal(size = n))
        y = Adjacency*np.matrix(x).transpose()
        T = ((y.T * Adjacency * y)/6)
    else:
        j = int(np.random.uniform(1,n))
        x = [np.sqrt(1/n) if j == 1 else np.sqrt(2/n)*np.cos(np.pi*(k+0.5)*j/n)  for k in range(n)]
        y = Adjacency*D*np.matrix(x).transpose()
        T = (n*(y.T * Adjacency * y)/6)
    return T
