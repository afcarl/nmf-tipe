import numpy as np

class bicluster:
                def __init__(self,vec, n_id = None, left = None, right = None, distance = 0.):
                        self.vec = vec
                        self.id = n_id
                        self.left = left
                        self.right = right
                        self.distance = distance

                def is_endpoint(self):
                        return self.right == None and self.left == None

                def getheight(self):
                        if self.is_endpoint(): return 1
                        return self.right.getheight() + self.left.getheight()


                def getdepth(self):
                        from math import log1p
                        if self.is_endpoint(): return 0
                        return max(self.left.getdepth(), self.right.getdepth()) + log1p(self.distance)

                
                def drawdendrogram(clust,labels, adress='/home/leonard/Bureau/Clusters/c', formPict = '.jpeg'):
                        from PIL import Image, ImageDraw 
                        # height and width
                        h=clust.getheight()*20
                        w=2500
                        depth=clust.getdepth()
                        if depth != 0:
                                # width is fixed, so scale distances accordingly
                                scaling=float(w-150)/depth
                                # Create a new image with a white background
                                img=Image.new('RGB',(w,h),(255,255,255))
                                draw=ImageDraw.Draw(img)
                                draw.line((0,h/2,10,h/2),fill=(255,0,0))
                                # Draw the first node
                                clust.drawnode(draw, 10,(h/2),scaling,labels)
                                print 'ping'
                                img.save(adress+formPict,'JPEG')

                def drawnode(clust, draw, x, y, scaling, labels):
                        from math import log1p
                        if clust.id<0:
                                h1=clust.left.getheight()*20
                                h2=clust.right.getheight()*20
                                top=y-(h1+h2)/2
                                bottom=y+(h1+h2)/2
                                # Line length
                                ll=(log1p(clust.distance))*scaling
                                # Vertical line from this cluster to children
                                draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))
                                # Horizontal line to left item
                                draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))
                                # Horizontal line to right item
                                draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))
                                # Call the function to draw the left and right nodes
                                clust.left.drawnode(draw,x+ll,top+h1/2,scaling,labels)
                                clust.right.drawnode(draw,x+ll,bottom-h2/2,scaling,labels)
                        else:
                                # If this is an endpoint, draw the item label
                                texte = stripAccents(unicode(labels[clust.id]))
                                try:
                                        draw.text((x+5,y-7), texte,(0,0,0))
                                except:
                                        print clust.id
                                        draw.text((x+5,y-7), 'zut',(0,0,0))

def stripAccents(s):
        from unicodedata import normalize, category
        return ''.join((c for c in normalize('NFD', s) if category(c) != 'Mn'))



def pearson(vect1, vect2):
        from math import sqrt
        n = len(vect1)
        sum1 = vect1.sum()
        sum2 = vect2.sum()

        sum1Sq = (vect1**2).sum()
        sum2Sq = (vect2**2).sum()

        pSum = (vect1*vect2).sum()
        return 1. - (pSum-(sum1*sum2)/n)/sqrt((sum1Sq - pow(sum1,2)/n)*(sum2Sq - pow(sum2,2)/n))

def normEucl(vect1, vect2):
        """Return the euclidian distance between to vectors renormalized
        >>> normEucl(np.array([1,0,0]), np.array([0,3,0]))
        2.0
        """
        from math import sqrt
        return ((vect1/sqrt((vect1**2).sum())-vect2/sqrt((vect2**2).sum()))**2).sum()


def hcluster(rows, measure=pearson):
        clust = {}
        for (i,r) in rows:
                clust[i] = bicluster(r, i)
        distances = [((clust[i].id, clust[j].id), measure(clust[i].vec, clust[j].vec)) for i in clust.keys() for j in clust.keys() if i<j]
        distances.sort(None,key = lambda x: x[1])
        return hcluster_aux(clust, distances, -1,measure)

def hcluster_imp(rows, measure = normEucl):
        clust = {}
        clust = dict((i, bicluster(r, i)) for i,r in rows)
        print len(clust)
        distances = [((clust[i].id, clust[j].id), measure(clust[i].vec, clust[j].vec)) for i in clust.keys() for j in clust.keys() if i<j]
        distances.sort(None,key = lambda x: x[1])
        current_id = 0
        b = True
        while len(clust) != 1:
                current_id -= 1
                if len(clust)%50==0: print len(clust)
                (cl1, cl2), closest = distances[0]
                if b: print cl1, cl2, closest
                b = False
                mergevec = (clust[cl1].vec + clust[cl2].vec)/2.
                new_clust = bicluster(mergevec, left = clust[cl1], right = clust[cl2], distance=closest, n_id = current_id)
        
                del clust[cl1]
                del clust[cl2]
                clust[current_id] = new_clust

                distances = newDistances(distances, [((current_id, i), measure(mergevec, clust[i].vec)) for i in clust.keys() if i != current_id], cl1, cl2)
        return clust[clust.keys()[0]]


def hcluster_aux(clust, distances, current_id, measure = normEucl):
        if len(clust) == 1: return clust[clust.keys()[0]]
        
        
        print len(clust)
        (cl1, cl2) , closest = distances[0]

        mergevec = (clust[cl1].vec+clust[cl2].vec)/2.
        new_clust = bicluster(mergevec, left = clust[cl1], right = clust[cl2], distance=closest, n_id = current_id)
        
        del clust[cl1]
        del clust[cl2]
        clust[current_id] = new_clust

        distances = newDistances(distances, [((current_id, i), measure(mergevec, clust[i].vec)) for i in clust.keys() if i != current_id], cl1, cl2)

        return hcluster_aux(clust, distances, current_id-1, measure)


def newDistances(oldDist, toAddDist, delId1, delId2):
        oldDist = [((a,b),m) for ((a,b),m) in oldDist if a not in [delId1, delId2] and b not in [delId1, delId2]]
        toAddDist.sort(None, key = lambda x:x[1])
        oldDist.extend(toAddDist)
        oldDist.sort(None, key = lambda x:x[1])
        return oldDist



def getClusterH(h, words, measure=pearson):
        return hcluster_imp([(i,np.array((h.T)[i])) for i in words])

##def print_cluster(cluster):
##        print_cluster_aux(cluster, 0)
##
##def print_cluster_aux(cluster, deep):
##        if cluster.left == None and cluster.right == None:
##                print deep*'   ' + self.corr_entree[cluster.id]
##        else:
##                print_cluster_aux(cluster.left, deep+1)
##                print_cluster_aux(cluster.right, deep+1)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
