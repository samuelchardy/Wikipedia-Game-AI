import wikipediaapi
from wikipedia2vec import Wikipedia2Vec
from bs4 import BeautifulSoup
import urllib 
import copy
import random
from sklearn.metrics.pairwise import cosine_similarity
import re
import traceback


class WebScraper:
    def __init__(self):
        """
        Initialises the wikipediaapi module and loads Wikipedia2Vec pretrained vectors.
        """
        self.wiki = wikipediaapi.Wikipedia('en')
        self.wiki2vec = Wikipedia2Vec.load("enwiki_20180420_win10_100d.pkl")


    def getRandomPage(self):
        """
        Gets a random wikipedia page and transforms it into a wikipediaapi page.

        :return: A wikipediaapi page for a random wikipedia page.
        """
        page = urllib.request.urlopen("https://en.wikipedia.org/wiki/Special:Random").read().decode("utf-8")
        name = BeautifulSoup(page, features="html.parser").select("#firstHeading")[0].text
        name = name.replace(" ", "_")
        page = self.wiki.page(name)
        return page


    def getStartEndPair(self, depth):
        """
        Navigates a path from a random start page via
        [depth] number of links to find an end page.
        
        :param depth: The number of links to follow from the start page.
        :return: Two wikipediaapi pages, the start and end pages respectively.
        """
        startPage = self.getRandomPage()
        tempPage = copy.deepcopy(startPage)
        name = ""

        for i in range(depth):
            try:
                link = None
                links = self.filterLinks(list(tempPage.links.keys()))
                if len(links) > 0:
                    link = links[random.randrange(0, len(links))]
                else:
                    raise Exception()
                name = link.replace(" ", "_")
                tempPage = self.wiki.page(name)
            except:
                i = i - 1
        name = name.replace("_", " ")
        return startPage, tempPage


    def filterLinks(self, links):
        """
        Filters the links using regex and returns the valid links.

        :param links: A list of strings, each is a link title from a wikipedia page.
        :return: A list comprised of those links passed in that are usable/valid.
        """
        negSearch = 'Media:|Special:|User:|Wikipedia:|File:|MediaWiki:|Template:|Help:|Category:|Portal:|Book:|Draft:|Education Program:|TimedText:|Module:|Gadget:|Gadget definition:|Talk:|User talk:|Wikipedia talk:|File talk:|MediaWiki talk:|Template talk:|Help talk:|Category talk:|Portal talk:|Book talk:|Draft talk:|Education Program talk:|TimedText talk:|Module talk:|Gadget talk:|Gadget definition talk:'
        filteredLinks = []
        for link in links:
            if not re.search(negSearch, link):
                filteredLinks.append(link)
        return filteredLinks


    def nlpSimilarity(self, pageName, terminusName, pageLinks):
        """
        Returns a similarity score in the range (0,1) for
        two page titles from wikipedia.

        :param pageName: The title of the current wikipedia page.
        :param terminusName: The title of the target wikipedia page.
        :param pageLinks: The links present on the current wikipedia page.
        """
        pageName = pageName.replace("_", " ")
        terminusName = terminusName.replace("_", " ")

        try:
            pageVec = self.wiki2vec.get_entity_vector(pageName).reshape(1, -1)
            endPageVec = self.wiki2vec.get_entity_vector(terminusName).reshape(1, -1)
            cos = cosine_similarity(pageVec, endPageVec)
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
            return cos / numLinks