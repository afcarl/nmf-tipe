# -*- coding: utf-8 -*-
from ioFiles import *
from textStat import *
from clustering import *
from func import *
from nmf import *

#parseWiki()
#lenArt = [lenArticle(a[2])  for i in range(40) for a in loadWiki(i)]


###APPLIQUE NMF A UN SOUS ENSEMBLE D'ARTICLE
data = [(x, lenArticle(z)) for (x,y,z,l) in loadWiki(1)]
fw = loadFreqWords(1)
fc = loadFreqCouples(1)
v = [addDict([fw[i], fc[i]], sumCouple, (0,0)) for i in range(len(fw))]
w,h = loadObject('Wikipedia/WikiResult/results3')
data = [(x, lenArticle(z)) for (x,y,z,l) in loadWiki(1)]
titles = [x for x, length in data]


print 'donnes chargees'

index = np.argsort(np.array([z for x, z in data])).tolist()
index.reverse()
index = index[:10]
f, corWords = arrFreqtoArrDict(v)
print 'pingoo saute sur la banquise'

m,n = shapeArrDict(f)
r = h.shape[0]
indicesDeleted = nRandom(n/3, n)
halfArticles = delKey(indicesDeleted , [f[i] for i in index])
from random import uniform
hHalf = randomMatrix(r, len(index))
print 'tableaux construits'


factorizeSparse(transArrDict(halfArticles), hHalf.T, w.T)
print 'nmf a fonctionne'

v2 = w*hHalf
completed = [np.array(x)[0] for x in v2.T]
variance = np.array(var(f, True))


for i in range(len(completed)):
        t = [abs(f[index[i]].get(word, 0) - completed[i].item(word)) for word in indicesDeleted if f[index[i]].get(word, 0) != 0]#/(f[index[i]].get(word, 0)) for word in indicesDeleted if f[index[i]].get(word, 0) != 0]
        s = sum(t)
        l = len(t)
        print s/l
##for  i in range(len(index)):
##        print titles[index[i]]
##        order = np.argsort((completed[i])/mean(f)).tolist()
##        order.reverse()
##        for j in order[:50]:
##                print corWords[j],
##                print ' : ',
##                print completed[i][j]
##        print ''
##        print ''
        

##
##h2Half = [np.array(x)[0] for x in hHalf.T]
##h2 = [np.array(x)[0] for x in h.T]
##neighboorHalf = [
##        (index[j], sorted((i for i in range(len(h2))), key = lambda i: normEucl(h2Half[j], h2[i])))
##        for j in range(len(h2Half))]
##
##
##print 'tout est fini'
# DESSINE LE GRAPHE
##data =[(x, lenArticle(z)) for (x,y,z,l) in loadWiki(0)]
##w,h = loadObject('Wikipedia/WikiResult/results2')
##h2 = [np.array(x)[0] for x in h.T]
##print 'data loaded'
##
##
##titles = [x for x, length in data]
##print data[1081], titles[1081]
##
##data = [(i,)+data[i]+(h2[i],) for i in range(len(data))]
##data.sort(None, key=lambda(x,y,z,t): z, reverse = True)
##data = data[:600]
##
##table = dict((y, t) for x,y,z,t in data)
##print 'loaded'
##g = makeGraph(table)
##
##import networkx as nx
##import matplotlib.pyplot as plt
###nx.draw_spring(g)
##
##connex = nx.connected_component_subgraphs(g)
##for x in connex:
##        nx.draw_spring(x)
##        plt.show()


## PARSE LES FICHIERS WIKI
##parseWiki()
##
#freqWordsWiki(40, 200, 10)
#freqCouplesWiki(40, 150, 10)


##for i in range(40):
##        print 'pingoo est parti en voyage avec babar et mange ' + str(i) + ' papillons'
##        f = loadFreqCouples(i)
##        saveObject(keepKey([key for key, val in freqCouplesFile([], f).iteritems() if val>=(150, 0)], f), 'Wikipedia/WikiStat/freqWords/freqCouples' + str(i))

##FAIT NMF
##fw = loadFreqWords(1)
##fc = loadFreqCouples(1)

##v = [addDict([fw[i], fc[i]], sumCouple, (0,0)) for i in range(len(fw))]
##w,h = algNmf(200, v, 200, 'Wikipedia/WikiResult/resultstest')
##
###FAIT UN DENDROGRAMME
##data = [(x, lenArticle(z)) for (x,y,z,l) in loadWiki(1)]
##titles = [x for x, z in data]
##print 'data loaded'
##
##
##data = [(i,)+data[i] for i in range(len(data))]
##data.sort(None, key=lambda(x,y,z): z)
##data.reverse()
##data = data[:800]
##
##print 'data preparated'
##
##w,h = loadObject('Wikipedia/WikiResult/resultstest')
##c = getClusterH(h, [i for i,j,k in data])
##
##c.drawdendrogram(titles, 'Wikipedia/WikiResult/Clusters/cluster3_1')
