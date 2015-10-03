
# -*- coding: utf-8 -*-
from func import *

def stopw(language = 'french'):
        from nltk.corpus import stopwords
        if language != 'french': return stopwords.words(language)
        return stopwords.words(language) + stopwords.words('english')+['les',unicode('à', 'utf-8'), 'a', 'align', 'date', 'http', 'www', 'formatnum', 'fr',
                                                                       'comme', 'plus', 'left', 'right', 'smn', 'aussi', 'thumb', 'center', 'html', 'text', 'lang', 'isbn', 'org', 'url', 'bar', 'pdf', 'php', 'new', 'id',
                                                                       'background', 'htm', 'i', 'celle', 'x', 'quelques', 'ci', 'svg', 'chaque', 'si', 'h', 'km', 'b', 'elles', 'car', 'ceux', 'afin', 'o', unicode('où', 'utf-8')]

def freq(arr, language = 'french'):
        """Return a dictionnary of the frequency of each word in a paragraph,
        as an array of words
        >>> freq(['test1','test2', 'test3', 'test2'])
        {'test1': 1, 'test3': 1, 'test2': 2}
        """
        return dict((x, arr.count(x)) for x in set(arr))





def lenArticle(article):
        """Return the number of words in an article
        >>> lenArticle([['tata', 'toto', 'titi'],['foo','bar'], ['la', 'grande', 'question']])
        8
        """
        return sum(len(par) for par in article)






def listWord(paragraph, language = 'french'):
        """Return all the words of the paragraph, without the stopwords
        >>> listWord(['Quelle', 'est', 'la', 'grande', 'question', 'sur', 'la', 'vie', 'le', 'bel', 'univers', 'et', 'le', 'reste'])
        ['Quelle', 'grande', 'question', 'vie', 'bel', 'univers', 'reste']
        """
        s = stopw(language)
        return [word for word in paragraph if word not in s]


def listCouple(paragraph, language = 'french'):
        """Return all the couple of words in a text, if these words aren't stop words
        >>> listCouple(['Quelle', 'est', 'la', 'grande', 'question', 'sur', 'la', 'vie', 'le', 'bel', 'univers', 'et', 'le', 'reste'])
        [('grande', 'question'), ('bel', 'univers')]
        """
        s = stopw(language)
        return [(paragraph[i], paragraph[i+1]) for i in range(len(paragraph)-1) if paragraph[i] not in s and paragraph[i+1] not in s]

def listTriple(paragraph, coupleKept, language = 'french'):
        from nltk.corpus import stopwords
        s = stopw(language)
        return [(paragraph[i], paragraph[i+1], paragraph[i+2]) for i in range(len(paragraph)-1) if paragraph[i] not in s and paragraph[i+1] not in s and paragraph[i+2] not in s]


def getPattern(paragraph, smallers, language = 'french'):
        """Return all the pattern of the length given
        If we know the pattern of length (length-1), we give it in smallers
        >>> compareArr(getPattern(['quelle', 'est', 'la', 'grande', 'question', 'sur', 'la', 'vie'], [set(['quelle', 'grande']), set(['grande', 'vie'])]) ,[set(['quelle', 'grande', 'question']), set(['quelle', 'grande', 'vie']), set(['grande', 'vie', 'quelle']), set(['grande', 'vie', 'question'])])
        True
        """
        from nltk.corpus import stopwords
        stopw = stopwords.words(language)
        setParagraph = set(paragraph) - set(stopw)
        return [set([word])|small for small in smallers for word in (setParagraph-small)]

def lenAllArticle(nFile = 4435):
        from ioFiles import loadWiki
        length = []
        for i in range(nFile):
                print i
                length += [lenArticle(art) for art in loadWiki(i)]
        return length


def freqText(text, funcPar, language = 'french', fact = 1, lenIntro = 0):
        """Return the frequences of something in a text, giving 
        """
        if lenIntro == 0: return dict( (key, (fact*value, 1)) for key, value in addDict([freq(funcPar(par, language)) for par in text]).iteritems())
        else: return addDict([freqText(text[:lenIntro], funcPar, language, fact), freqText(text[lenIntro:], funcPar, language)], sumCoupleMax, (0,0))


def freqWordsText(text, factIntro, lenIntro = 0, language = 'french'):
        """Return the frequences of words in a text
        >>> freqWordsText([['quelle', 'est', 'la', 'grande', 'question'], ['sur', 'la', 'vie'], ['c', 'est', 'la', 'grande', 'question']], 1, 0) == {'quelle': (1,1), 'grande': (2,1), 'question': (2,1), 'vie': (1,1)}
        True
        """
        return freqText(text, listWord, language, factIntro, lenIntro)

def freqCouplesText(text, factIntro, lenIntro, language = 'french'):
        """Return the frequences of couples in a text
        ##>>> freqCouplesText([['la', 'grande', 'belle', 'question'], ['une', 'grande', 'belle', 'femme']]) == {('grande', 'belle'): (2,1), ('belle', 'question'): (1, 1), ('belle', 'femme'): (1, 1)}
        ##True
        """
        return freqText(text, listCouple, language, factIntro, lenIntro)


def freqFile(arrArticle, funcText = None, freqArticle = None, language = 'french', factIntro = 1):
        if freqArticle == None:
                freqArticle = [funcText(text, factIntro, l, language) for title, title2, text, l in arrArticle]
        return addDict(freqArticle, sumCouple, (0,0))


def freqWordsFile(arrArticle, freqArticle = None, language = 'french', factIntro = 1):
        """Return the frequence of words in all the file
        >>> freqWordsFile([('title1', 'title2', [['quelle', 'est', 'la', 'grande', 'question'], ['sur', 'la', 'vie'], ['c', 'est', 'la', 'grande', 'question']], 0), ('foo', 'bar', [['question'], ['reponse']], 0)])
        {'vie': (1, 1), 'question': (3, 2), 'reponse': (1, 1), 'quelle': (1, 1), 'grande': (2, 1)}
        """
        return freqFile(arrArticle, freqWordsText, freqArticle, language, factIntro)

def freqCouplesFile(arrArticle, freqArticle = None, language = 'french', factIntro=1):
        """Return the frequence of couples in all the file
        """
        return freqFile(arrArticle, freqCouplesText, freqArticle, language, factIntro)


def freqWiki(nFile, funcText, minFreq, fileName):
        from ioFiles import saveObject, loadWiki
        for i in range(nFile):
                print 'Loading data ...'
                w = loadWiki(i)
                print 'Done'
                print 'Reading data ...'
                f = [funcText((z, l)) for x,y,z,l in w]
                print 'Done'
                saveObject(keepKey([key for key, val in freqFile(w, funcText, f).iteritems() if val>=(minFreq, 0)], f), fileName + str(i))
                print i
                
def freqCouplesWiki(nFile, minFreq = 40, factIntro = 1, fileName = 'Wikipedia/WikiStat/freqCouples/freqCouples', language = 'french'):
        """Save the freqCouplesArray for each text in a new file
        """
        freqWiki(nFile, lambda(text, l): freqCouplesText(text, factIntro, l, language), minFreq, fileName)
        
              
def freqWordsWiki(nFile, minFreq = 70, factIntro = 1, fileName = 'Wikipedia/WikiStat/freqWords/freqWords', language = 'french'):
        """Save the freqWordsText array for each text in a new file
        """
        freqWiki(nFile, lambda(text, l): freqWordsText(text, factIntro, l, language), minFreq, fileName)
                


def findNeighboorWord(word, arrArticle):
        return [(par[max((par.index(word)-5), 0):min((len(par),par.index(word)+5))]) for title1, title2, article in arrArticle for par in article if word in par]



def algNmf(r, arrFreq, nTurn, nameFile):
        from nmf import algorithm, shapeArrDict, algorithm2
        f, corWords = arrFreqtoArrDict(arrFreq)
        m, n = shapeArrDict(f)
        w,h = algorithm(f, randomMatrix(n, r), randomMatrix(r, m), nTurn, nameFile)
        return w,h, corWords


        
def algNmfGram(r, arrFreq, nTurn, nameFile):
        from nmf import algorithmGram, shapeArrDict
        f, corWords = arrFreqtoArrDict(arrFreq)
        h = algorithmGram(f, r, nTurn, nameFile)
        return h
        

def arrFreqtoArrDict(arrFreq):
        index = list(set(sumArrays([x.keys() for x in arrFreq])))
        dictIndex = dict((index[i], i) for i in range(len(index)))
        return  [dict((dictIndex[key], val1) for key, (val1, val2) in x.iteritems()) for x in arrFreq], index


def printW(w, nPrint, corWords):
        n,r = np.shape(w)
        arrW = [dict([[corWords[i], w.item((i,j))] for i in range(n)]) for j in range(r)]
        for j in range(r):
                print 'On affiche le '+ str(j) + 'eme parametre'
                from operator import itemgetter
                l = arrW[j].items()
                l.sort(key=itemgetter(1), reverse=True)
                for k in range(nPrint):
                        print  (l[k][0]) ,
                print ''
        




if __name__ == "__main__":
    import doctest
    doctest.testmod()

