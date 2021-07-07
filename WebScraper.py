import wikipediaapi
from wikipedia2vec import Wikipedia2Vec
from bs4 import BeautifulSoup
import urllib 
import copy
import random
from sklearn.metrics.pairwise import cosine_similarity
import re


class WebScraper:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia('en')
        self.wiki2vec = Wikipedia2Vec.load("enwiki_20180420_win10_100d.pkl")
        #self.gensim2vec = api.load('glove-wiki-gigaword-50')


    def getWikiPageAndInput(self):
        pageInput, page = None, None
        http404 = True
        while http404 == True:
            try:
                print("Enter start term:")
                pageInput = input()
                pageInput = pageInput.replace(" ", "_")
                page = self.wiki.page(pageInput)
                http404 = False
            except:
                print("No page exists for that term, try again:")
                http404 = True
        return page


    def getUserInput(self):
        startPage = self.getWikiPageAndInput();
        endPage = self.getWikiPageAndInput();
        return startPage, endPage


    def getRandomPage(self):
        page = urllib.request.urlopen("https://en.wikipedia.org/wiki/Special:Random").read().decode("utf-8")
        name = BeautifulSoup(page, features="html.parser").select("#firstHeading")[0].text
        name = name.replace(" ", "_")
        page = self.wiki.page(name)
        return page


    def getStartEndPair(self, depth):
        startPage = self.getRandomPage()
        tempPage = copy.deepcopy(startPage)
        name = ""

        for i in range(depth):
            try:
                links = self.filterLinks(list(tempPage.links.keys()))
                link = links[random.randrange(0, len(links))]
                name = link.replace(" ", "_")
                tempPage = self.wiki.page(name)
            except:
                #print(tempPage.title)
                #traceback.print_exc()
                i = i - 1
        name = name.replace("_", " ")
        return startPage, tempPage


    def filterLinks(self, links):
        negSearch = 'Media:|Special:|User:|Wikipedia:|File:|MediaWiki:|Template:|Help:|Category:|Portal:|Book:|Draft:|Education Program:|TimedText:|Module:|Gadget:|Gadget definition:|Talk:|User talk:|Wikipedia talk:|File talk:|MediaWiki talk:|Template talk:|Help talk:|Category talk:|Portal talk:|Book talk:|Draft talk:|Education Program talk:|TimedText talk:|Module talk:|Gadget talk:|Gadget definition talk:'
        filteredLinks = []
        for link in links:
            if not re.search(negSearch, link):
                filteredLinks.append(link)
        return filteredLinks


    def nlpSimilarity(self, pageName, terminusName, pageLinks):
        #print("     " + str(pageName))
        pageName = pageName.replace("_", " ")
        terminusName = terminusName.replace("_", " ")

        try:
            pageVec = self.wiki2vec.get_entity_vector(pageName).reshape(1, -1)
            endPageVec = self.wiki2vec.get_entity_vector(terminusName).reshape(1, -1)
            #print("PRE COSINE")
            cos = cosine_similarity(pageVec, endPageVec)
            #print("PASSED - " + pageName)
            return cos
        except:
            cos, numLinks = 0, 1
            for i in range(len(pageLinks)):
                if numLinks == 4:
                    break                
                try:
                    linkVec = self.wiki2vec.get_entity_vector(pageLinks[i].replace("_", " ")).reshape(1, -1)
                    endPageVec = self.wiki2vec.get_entity_vector(terminusName).reshape(1, -1)
                    cos = cos + cosine_similarity(linkVec, endPageVec) 
                    numLinks = numLinks + 1
                except:
                    pass
            #traceback.print_exc()
            #print("FAILED TO CALC NLP - " + pageName)
            
            return cos / numLinks


    def genismSimilarity(self, pageName, terminusName):
        try:
            pageName = pageName.replace("_", " ")
            terminusName = terminusName.replace("_", " ")

            curPages = pageName.split(" ")
            endPages = terminusName.split(" ")

            pageVec = self.getVectorsFromWords(curPages)
            terminusVec = self.getVectorsFromWords(endPages)

            cos = cosine_similarity(pageVec, terminusVec)
            print(cos)
            return cos
        except:
            return 0


    def getVectorsFromWords(self, words):
        outputVec = [0]*300
        for word in words:
            #print("!!!!!!!!!!!   " + word)
            try:
                outputVec = outputVec + self.gensim2vec[word]
            except:
                print("Didn't find that term")
        try:        
            outputVec = outputVec / len(words)
        except:
            pass
        return outputVec


    def findJaccardSimilarity(self, pageLinks, terminusLinks, terminusName):
        pLinks = set(pageLinks)
        tLinks = set(terminusLinks)
        terminusLink = "http://www.wikipedia.org/wiki/" + str(terminusName)
        terminusLink = set(terminusLink)

        if len(pLinks.intersection(terminusLink)) != 0:
            return 1
        else:
            return len(pLinks.intersection(tLinks))/len(pLinks.union(tLinks))


#wb = WebScraper()
#print(wb.filterLinks(["Cheese", "Government", "Media:Something", "Template:idk"]))