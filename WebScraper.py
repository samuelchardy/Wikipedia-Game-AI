import random
import Page as P
from wikipedia2vec import Wikipedia2Vec
import copy
import random
from sklearn.metrics.pairwise import cosine_similarity


class WebScraper:
    def __init__(self, wiki, redirs):
        self.wiki = wiki
        self.wikiKeys = list(self.wiki.keys())
        self.wikiLen = len(self.wiki)
        self.redirs = redirs
        self.wiki2vec = Wikipedia2Vec.load("enwiki_20180420_win10_100d.pkl")


    def getPage(self, title):
        try:
            output = self.wiki[title]
            #print("Wiki")
            return output
        except:
            try:
                output = self.redirs[title]
                output = self.wiki[output[0]]
                #print("redirs")
                return output
            except:
                print("Not Found:  " + title)
                return []


    def getRandomPage(self):
        randomNum = random.randrange(0, self.wikiLen)
        key = self.wikiKeys[randomNum]
        links = self.wiki[key]
        page = P.Page(key, links)
        return page


    def getStartEndPair(self, depth):
        startPage = self.getRandomPage()
        tempPage = copy.deepcopy(startPage)
        #name = ""

        for i in range(depth):
            try:
                links = tempPage.links
                link = links[random.randrange(0, len(links))]
                #name = link.replace(" ", "_")
                tempPage = P.Page(link, self.wiki[link])
            except:
                #print(tempPage.title)
                #traceback.print_exc()
                i = i - 1
        #name = name.replace("_", " ")

        return startPage, tempPage


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