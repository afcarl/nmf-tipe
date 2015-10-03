import re

def parseWiki(maxSizeFile = 8*1000*1000, finalFiles = 'Wikipedia/WikiCut/wiki', sourcefileName = 'Wikipedia/frwiki-latest-pages-articles.xml', prefix = '{http://www.mediawiki.org/xml/export-0.5/}', minilength = 1500):
        from elementtree.ElementTree import  iterparse
        from treatWiki import treatWiki
        from textStat import lenArticle
        nFile = 0
        arrayArticle = []
        text, title = None, None
        compteur = 0
        size = 0
        nSave = 0
        context = iterparse(sourcefileName, events =('start', 'end'))
        context = iter(context)
        event, root = context.next()


        for event, elem in context:
                if event == 'start':
                        if elem.tag == prefix+'title': title =  elem.text
                        elif elem.tag == prefix+'text': text = elem.text                                  
                elif event == 'end':
                        if title == None and elem.tag == prefix+'title': title = elem.text
                        elif text == None and elem.tag == prefix+'text': text = elem.text
                        elif elem.tag == prefix+'page':
                                compteur += 1
                                if title == None or text == None: print 'CRASH ! : ' + str(compteur)
                                else:
                                        wikiTreated = treatWiki(title, text)
                                        if wikiTreated != None and len(wikiTreated[2]) != 0 and lenArticle(wikiTreated[2]) > minilength:
                                                arrayArticle.append(wikiTreated)
                                                size += lenArticle(wikiTreated[2])
                if size >= maxSizeFile:
                        saveObject(arrayArticle, finalFiles + str(nFile))
                        nFile+=1
                        size = 0
                        nSave += len(arrayArticle)
                        arrayArticle = []
                        root.clear()
                        print str(nSave) + " articles sauvegardes, " + (str(compteur - nSave)) + " mots rejetes."
                elem.clear()
        return nFile

def parseWikiLang(listTitles, maxSizeFile = 200, finalFiles = 'Wikipedia/WikiCutLang/wiki', sourcefileName = 'Wikipedia/enwiki-latest-pages-articles.xml', prefix = '{http://www.mediawiki.org/xml/export-0.5/}'):
        from elementtree.ElementTree import  iterparse
        nFile = 0
        arrayArticle = []
        text, title = None, None
        for event, elem in iterparse(sourcefileName, events=('start', 'end')):
                if event == 'start':
                        if elem.tag == prefix+'title':
                                title =  elem.text
                        elif elem.tag == prefix+'text':
                                text = elem.text                                
                elif event == 'end':
                        if title == None and elem.tag == prefix+'title':
                                title = elem.text
                        elif text == None and elem.tag == prefix+'text':
                                text = elem.text
                        elif elem.tag == prefix+'page' and title in listTitles:
                                arrayArticle.append((title , text))
                                elem.clear()
                if len(arrayArticle) >= maxSizeFile:
                        saveObject(arrayArticle, finalFiles + str(nFile))
                        nFile+=1
                        arrayArticle = []
                        if nFile%100 == 0: print nFile
                elem.clear()
        return nFile

def saveObject(obj, fileName):
        from pickle import dump
        output = open(fileName + '.pkl', 'wb')
        dump(obj, output)
        output.close()

def loadObject(fileName):
        from pickle import load
        pklFile = open(fileName + '.pkl', 'rb')
        obj = load(pklFile)
        pklFile.close()
        return obj

def loadWiki(idFile, directoryName = 'Wikipedia/WikiCut/wiki'):
        return loadObject(directoryName + str(idFile))

def loadFreqWords(idFile, directoryName = 'Wikipedia/WikiStat/freqWords/freqWords'):
        return loadObject(directoryName + str(idFile))

def loadFreqCouples(idFile, directoryName = 'Wikipedia/WikiStat/freqCouples/freqCouples'):
        return loadObject(directoryName + str(idFile))

def loadTitleArticle(nFile):
        return [title for title, title2, text in loadWiki(nFile)]
