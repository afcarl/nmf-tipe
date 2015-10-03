import re

def splitParagraph(text):
        return text.split('\n\n')        

def cleanXML(text):
        from nltk.util import clean_html
        return clean_html(text)
        
        
def splitWords(text):
        from re import *
        return [w for w in re.split('\W+', text.lower(), flags = re.UNICODE) if w != '']
        
        

def getTitleLanguage(text, language = 'en'):
        """Return the title of the same article in an other language
        >>> getTitleLanguage('Ce texte ne contient aucune langue')
        -1
        >>> getTitleLanguage('texte [[en:test1]] texte [[en:test2]] texte')
        'test2'
        """
        beginId = text.rfind('[['+language)
        if beginId == -1: return -1
        return text[beginId+3 + len(language):text.find(']]', beginId)]

def getLengthIntro(arrPar):
        """Return the length of the intro of an article, ie the number of paragraph before the first '='
        """
        for i in range(len(arrPar)/3):
                a = arrPar[i]
                if len(a)>0 and a[0] == '=': return i
        return 0
        

def treatWiki(title, text, otherLanguage = 'en'):
        """Take an article as its title and its text, and return
        - its name in the original language
        - its name in the foreign language
        - the text, as an array of paragraph, where each paragraph is an array of words
        """
        title2 = getTitleLanguage(text, otherLanguage)
        splitPar = splitParagraph(cleanXML(text))
        lenIntro = getLengthIntro(splitPar)
        if title2 == -1: return None
        return title, title2, [splitWords(x) for x in splitPar][:-1], lenIntro


def printPar(par):
        for w in par: print w,
        print ''



if __name__ == "__main__":
    import doctest
    doctest.testmod()
