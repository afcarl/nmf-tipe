import numpy as np

def compareArr(arr1, arr2):
        """Compare if two arrays have the same length, and the same elements
        >>> compareArr([0,1,2], [0, 2,1])
        True
        >>> compareArr([1,2,3], [1,2,4])
        False
        """
        return len(arr1) == len(arr2) and reduce(lambda x,y: x and y, [x in arr2 for x in arr1])


def inSorted(l, x):
        """Return if x is in l, where l is a sorted list
        >>> inSorted([2,3,5,7,11,13,17], 16)
        False
        >>> inSorted([2,3,5,7,11,13,17], 13)
        True
        >>> inSorted(['avion', 'babar', 'xylophone', 'zebre'], 'avion')
        True
        """
        from bisect import bisect_left
        i = bisect_left(l,x)
        return i != len(l) and l[i] == x

def positionSorted(l,x):
        """Return the position where would have to be inserted an element
        in a sorted list
        >>> positionSorted([1,4,5], 4)
        1
        """
        from bisect import bisect_left
        return bisect_left(l,x)

def sumCouple((x1, y1), (x2, y2)):
        return (x1+x2, y1+y2)

def sumCoupleMax((x1, y1), (x2, y2)):
        return (x1+x2, max(y1, y2))


def addDict(arrDict, fsum = None, zero = 0):
        """Return the sum of the two dictionnary.
        If they have the same key, it sums the two values.
        Else, it take the only value
        >>> addDict([{1: 1, 2: 2, 3: 3}, {1: 42, 5:7, 4: 2}])
        {1: 43, 2: 2, 3: 3, 4: 2, 5: 7}
        >>> addDict([{1: (1, 2), 2: (2, 4), 3: (3, 6)}, {1: (42, 84), 5:(7, 14), 4: (2, 4)}], sumCouple, (0,0))
        {1: (43, 86), 2: (2, 4), 3: (3, 6), 4: (2, 4), 5: (7, 14)}
        """
        nDict = dict.fromkeys(set(sumArrays(x.keys() for x in arrDict)), zero)
        for d in arrDict:
                for key, value in d.iteritems():
                        if fsum == None: nDict[key] += value
                        else: nDict[key] = fsum(nDict[key], value)
        return nDict
                
def sumArrays(arrArr):
        """ Return the sum of a few arrays
        >>> sumArrays([[0,1,2,3],['toto', 'tata'], [42, 1729]])
        [0, 1, 2, 3, 'toto', 'tata', 42, 1729]
        """
        return [x for y in arrArr for x in y]


def delKey(arrWord, arr):
        """Return the same array of  dict array, but all without the key word
        >>> delKey(['word'], [{'maison': 1, 'patate': 17, 'word': 22}, {'toto':1, 'tata': 0}, {'question': 0, 'word': 26, 'reponse': 42}]) == [{'patate': 17, 'maison': 1}, {'toto': 1, 'tata': 0}, {'question': 0, 'reponse': 42}] 
        True
        """
        a = sorted(arrWord)
        return [dict((key, value) for key, value in d.iteritems() if not inSorted(a, key)) for d in arr]

def keepKey(arrWord, arr, isSorted = False):
        """Return the same array of dict array, but all only with the key given
        >>> keepKey(['maison', 'toto', 'tata', 'question'], [{'maison': 1, 'patate': 17, 'word': 22}, {'toto':1, 'tata': 0}, {'question': 0, 'word': 26, 'reponse': 42}])
        [{'maison': 1}, {'toto': 1, 'tata': 0}, {'question': 0}]
        """
        a = sorted(arrWord)
        return [dict((key, value) for key, value in d.iteritems() if inSorted(a, key)) for d in arr]


def drawhistogram(data, nRect, delNoise = False):
        """
        This example shows how to use a path patch to draw a bunch of
        rectangles.  The technique of using lots of Rectangle instances, or
        the faster method of using PolyCollections, were implemented before we
        had proper paths with moveto/lineto, closepoly etc in mpl.  Now that
        we have them, we can draw collections of regularly shaped objects with
        homogeous properties more efficiently with a PathCollection.  This
        example makes a histogram -- its more work to set up the vertex arrays
        at the outset, but it should be much faster for large numbers of
        objects
        """

        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import matplotlib.path as path

        fig = plt.figure()
        ax = fig.add_subplot(111)

        # histogram our data with numpy
        l = len(data)
        data.sort()
        if delNoise: data = data[:l-(l/10)]
        n, bins = np.histogram(data, nRect)

        # get the corners of the rectangles for the histogram
        left = np.array(bins[:-1])
        right = np.array(bins[1:])
        bottom = np.zeros(len(left))
        top = bottom + n


        # we need a (numrects x numsides x 2) numpy array for the path helper
        # function to build a compound path
        XY = np.array([[left,left,right,right], [bottom,top,top,bottom]]).T

        # get the Path object
        barpath = path.Path.make_compound_path_from_polys(XY)

        # make a patch out of it
        patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='gray', alpha=0.8)
        ax.add_patch(patch)

        # update the view limits
        ax.set_xlim(left[0], right[-1])
        ax.set_ylim(bottom.min(), top.max())

        plt.show()


def allDist(v, arrVect):
        """Return the array of inverse of dist from vect of arrVect to v, where v is
        an np.array and arrVect an array of np.array
        """
        from clustering import normEucl
        return [normEucl(v, a) for a in arrVect]

def getNeighboor(v, arrVect, aDist = None):
        """Return the sorted list of the neighboor of v in arrVect
        """
        if aDist == None: aDist = allDist(v, arrVect)
        return sorted([(i, aDist[i]) for i in range(len(aDist))], key=lambda(x,y): y)


        
def makeGraph(table, tolerance = 1.01):
        """Create a graph from a dict of np.array, where the keys are labels and
        the array the coo
        """
        import networkx as nx
        g = nx.Graph()
        g.add_nodes_from(table.keys())
        edges = []
        for i in range(len(table)-1):
                d = allDist(table[table.keys()[i]], [table[k] for k in table.keys() if k != i])
                d = sorted([(j, d[j]) for j in range(len(d))], key = lambda(x,y): y)
                mini = d[1][1]
                pos = positionSorted([a for k,a in d], mini*tolerance) + 1
                edges.extend([(min(i,k), max(i,k), a) for k, a in d[:pos]])

        edges.sort()
        print len(edges)
        k = len(edges)-1
        while k>0:
                i1,j1,a1, i2, j2, a2 = edges[k] + edges[k-1]
                if i1 == i2 and j1 == j2:
                        edges.pop(k-1)
                else: k = k-1
        print len(edges)
        print edges[:20]
        #print len(table), min([i for i, j, a in edges]), max([j for i,j,a in edges])
        g.add_edges_from([(table.keys()[i],table.keys()[j], {'weight': d}) for i,j,d in edges])
        return g
                
def randomInt(maxi, mini = 0):
        from random import random
        return int(random()*(maxi-mini)+mini)

def nRandom(length, maxi, mini = 0):
        l = []
        x = randomInt(maxi, mini)
        for i in range(length):              
                while x in l: x  = randomInt(maxi, mini)
                l.append(x)
        return l

def randomMatrix(n, m, mini = 0.1, maxi = 1.):
        """Return a random matrix which shape is (n,m)
        >>> (randomMatrix(10, 14)).shape
        (10, 14)
        """
        from random import uniform
        return np.matrix([  [uniform(mini, maxi) for y in range(m)] for x in range(n)])
        
                
if __name__ == "__main__":
    import doctest
    doctest.testmod()

