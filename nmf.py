import numpy as np
import scipy.sparse as ssp
import cProfile

def transArrDict(arrDict):
        """Return the arrDict.T, as if it was a matrix
        >>> transArrDict([{2: 7, 5: 3}, {1: 1, 2: 2, 5: 1}, {0: -1, 3: 5}, {4: 1}, {0: 42, 4: 2}])
        [{2: -1, 4: 42}, {1: 1}, {0: 7, 1: 2}, {2: 5}, {3: 1, 4: 2}, {0: 3, 1: 1}]
        """
        shapeX, shapeY = shapeArrDict(arrDict)
        return [dict((j, arrDict[j].get(i, None)) for j in range(shapeX) if arrDict[j].get(i, None) != None)   for i in range(shapeY)]

def shapeArrDict(arrDict):
        """Return the shape of an array of dict, where the first is the len of the array,
        and the second is the max of dict keys
        >>> shapeArrDict([{2: 7, 5: 3}, {}, {1: 1, 2: 2, 5: 1}, {0: -1, 3: 5}, {4: 1}, {0: 42, 4: 2}])
        (6, 6)
        """
        return len(arrDict), max(max(y) for y in (x.keys() for x in arrDict if len(x) != 0 ))+1


def factorizeSparse(v2, w, h):
        """One turn of the nmf alg, for w
        if you want to get h, just do : factorize(transArrDict(arrV), h.T, w.T)
        """
        
        sumhLine = h.sum(1)
        r = w.shape[1]
        wh = w*h
        v = transArrDict(v2)
        n,m = shapeArrDict(v)
        print n, m, r, h.shape, w.shape

        for j in range(r):
                fact = np.array([1. for i in range(n)])
                for i in range(n):
                        keys = v[i].keys()
                        wh_iReduced = wh[i].take(keys)
                        vReduced = np.array(v[i].values())
                        hReduced = np.array(h[j]).take(keys)
                        fact[i] = ((hReduced*vReduced)/wh_iReduced).sum()
                fact = fact/(sumhLine.item(j))
                oldValues = (w.T)[j]
                (w.T)[j] = np.array((w.T)[j])*fact
                wh += (((w.T)[j] - oldValues).T)*(h[j])

       

                             
def factorize(v, w, h):
        from time import time
        sumhLine = h.sum(1)
        m,n = np.shape(v)
        r = np.shape(w)[1]
        wh = w*h
        for j in range(r):                
                fact = np.array(h[j]*(v/wh))/sumhLine.item(j)
                oldValues = (w.T)[j]
                (w.T)[j] = np.array((w.T)[j])*fact
                wh += (((w.T)[j] - oldValues).T)*(h[j])
                
                

def algorithm(arrV, w, h, nTurn, nameFile = '/home/leonard/Travail/Wikipedia/WikiResult/results'):
        from ioFiles import saveObject
        from time import time
        m,n = shapeArrDict(arrV)
        arrVT = transArrDict(arrV)
        for i in range(nTurn):
                print 'Round '+ str(i) + ' !'
                factorizeSparse(arrV, w, h)
                factorizeSparse(arrVT, h.T, w.T)
                saveObject((w,h), nameFile)
        return w,h

def algorithm2(arrV, r, nTurn, nameFile = '/home/leonard/Travail/Wikipedia/WikiResult/results'):
        from ioFiles import saveObject
        from random import uniform
        from time import time
        m,n = shapeArrDict(arrV)
        h = np.matrix([  [uniform(0.4,0.6) for y in range(m)] for x in range(r)])
        w = np.matrix([  [uniform(0.4,0.6) for y in range(r) ] for x in range(n)])
        vCoo = arrVtoCoo(arrV)
        v = vCoo.tocsc()
        vT = (v.T).tocsc()
        for i in range(nTurn):
                print 'Round '+ str(i) + ' !'
                debut = time()
                factorizeSparse2(vT, w, h)
                print time()-debut
                factorizeSparse2(v, h.T, w.T)
                saveObject((w,h), nameFile)
        return w,h

def algorithmGram(arrV, r, nTurn, nameFile = '/home/leonard/Travail/Wikipedia/WikiResult/resultsGram'):
        from ioFiles import saveObject
        from random import uniform
        import scipy.sparse as ssp

        m,n = shapeArrDict(arrV)
        va = np.array(var(arrV, True))
        ps = cscDiago(va)
        v = gram(arrV, ps)+0.000000001
        
        h = np.matrix([  [uniform(0.4,0.6) for y in range(m)] for x in range(r)])
        w = (h.T).copy()
        for i in range(nTurn):
                print 'Round '+ str(i) + ' !'
                factorize(v, w, h)
                saveObject(h, nameFile)
                h = (w.T).copy()
        return h
                
        
def gram(arrV, ps = None):
        """Return the gram matrix of the given vectors as an array of dict
        >>> gram([{1: 3, 2: 4}, {0: 1, 2: 6}])
        matrix([[25, 24],
                [24, 37]])
        >>> gram([{1: 3, 2: 4}, {0: 1, 2: 6}], ssp.csc_matrix(np.matrix([[1, 0, 0], [0, -1, 0], [0, 0, 2]])))
        matrix([[23, 48],
                [48, 73]])
        """
        import scipy.sparse as ssp
        m,n = shapeArrDict(arrV)
        indptr = np.cumsum(np.array([0 if i == 0 else len(arrV[i-1]) for i in range(m+1)]))
        indices = np.array([key for col in arrV for key in col.keys()])
        data = np.array([v for col in arrV for v in col.values()])
        v1 = ssp.csc_matrix((data, indices, indptr), shape = (n,m))
        v2 = v1.transpose()
        if ps == None: v = (v2*v1).todense()
        else: v = (v2*ps*v1).todense()
        return v
        
def var(arrV, norm = False):
        """Return an array of the variance along the lines of arrV
        >>> var([{1: 3, 2: 4}, {0: 1, 2: 6}])
        [0.25, 2.25, 1.0]
        >>> var([{1: 3, 2: 4}, {0: 1, 2: 6}], True)
        [1.0, 1.0, 0.03999999999999998]
        """
        m,n = shapeArrDict(arrV)
        if norm: return [var_aux(np.array([arrV[j].get(i, 0) for j in range(m)])) for i in range(n)]
        return [(np.array([arrV[j].get(i, 0) for j in range(m)])).var() for i in range(n)]

def mean(arrV):
        """Return an array of the variance along the lines of arrV
        >>> mean([{1: 3, 2: 4}, {0: 1, 2: 6}])
        [0.5, 1.5, 5.0]
        """
        m,n = shapeArrDict(arrV)
        return [(np.array([arrV[j].get(i, 0) for j in range(m)])).mean() for i in range(n)]

def var_aux(tab):
        m = tab.mean()
        return (tab/m).var()


def arrVtoCoo(arrV):
        """Return a coo sparse matrix from an array of dict
        >>> arrVtoCoo([{1: 3, 2: 4}, {0: 1, 2: 6}]).todense()
        matrix([[0, 1],
                [3, 0],
                [4, 6]])
        """
        m,n = shapeArrDict(arrV)
        col = [j for j in range(len(arrV)) for elem in arrV[j]]
        row = [i for d in arrV for i in d.keys()]
        data = [elem for d in arrV for elem in d.values()]
        return ssp.coo_matrix((data, (row, col)), shape = (n,m))
        

def cscDiago(arr):
        """Return the diagonal sparse matrix with the given element
        >>> cscDiago([-1, 1, 2]).todense()
        matrix([[-1,  0,  0],
                [ 0,  1,  0],
                [ 0,  0,  2]])"""
        import scipy.sparse as ssp
        n = len(arr)
        return ssp.csc_matrix((np.array(arr), np.array([i for i in range(n)]), np.array([i for i in range(n+1)])), (n,n))
        








                
                
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()

