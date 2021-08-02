import random
from math import sqrt
from math import log
import traceback
import WebScraper as WB


class Node:
    def __init__(self, parent, articlePage, depth):
        self.parent = parent
        self.depth = depth
        self.page = articlePage
        self.subTreeVal = 0.0
        self.numOfVisits = 0
        self.uct = 0.0
        self.children = []
        self.reserveChildren = {}
        self.reserveDist = {}
        self.childrenLinks = WB.WebScraper().filterLinks(list(self.page.links.keys()))


    def calcUCT(self):
        if self.numOfVisits == 0:
            self.uct = 100000.0
        else:
            numParVisits = self.parent.numOfVisits
            explore = 2*(0.9)*(sqrt((2*log(numParVisits))/self.numOfVisits))
            self.uct = (self.subTreeVal/self.numOfVisits) + explore


    def addBestChildByProb(self, webScraper):
        EXPL_CONST = 0.3
        key = list(self.reserveChildren.keys())

        if len(key) == 0:
            return False
        else:
            key = key[0]

        actionIndex = random.randrange(0, 100)
        newActionProb = self.reserveChildren[key] * EXPL_CONST * 100

        if actionIndex < newActionProb:
            newPage = webScraper.wiki.page(key)
            nodeToAdd = Node(self, newPage, self.depth+1)

            self.children.append(nodeToAdd)
            del self.reserveChildren[key]
            return {self.children[-1].page.title: self.depth+1}
        else:
            return False



    def addChildByProb(self, webScraper):
        if self.reserveDist == None:
            return False

        keys = list(self.reserveDist.keys())
        actionIndex = random.randrange(0, 100)

        if sum(self.reserveDist.values()) == 0:
            return False

        for key in keys:
            if self.reserveDist[key]*100 > actionIndex:
                if self.notAlreadyBeenTaken(key):
                    newPage = webScraper.wiki.page(key)
                    nodeToAdd = Node(self, newPage, self.depth+1)

                    self.children.append(nodeToAdd)
                    #del self.reserveChildren[key]
                    #del self.reserveDist[key]

                    #self.reserveDist = self.makeReservesDist(self.reserveChildren)
                    return {self.children[-1].page.title: self.depth+1}
                else:
                    print("OH NO")
                    return False


    def notAlreadyBeenTaken(self, key):
        for child in self.children:
            if child.page.title == key:
                return False
        return True


    def makeReservesDist(self, reserveChildren):
        #self.reserveDist.clear()
        reserveDist = {}

        if len(reserveChildren) > 0:
            resSum = sum(reserveChildren.values())
            
            if resSum != 0:
                keys = list(reserveChildren.keys())
                for i in range(len(keys)):
                    reserveDist[keys[i]] = reserveChildren[keys[i]]/resSum
                    if i != 0:
                        reserveDist[keys[i]] = reserveDist[keys[i]] + reserveDist[keys[i-1]]
            return reserveDist



    def rollout(self, policy, terminusName, webScraper):
        page = self.page
        links = self.childrenLinks
        self.subTreeVal = 0


        for i in range(10):
            actionIndex = None
            action = None

            if len(links) == 0:
                break
            
            if policy == "RBRP":
                nlpScore = {}

                for child in links:
                    nlpScore[child] = webScraper.nlpSimilarity(child, terminusName, [])

                sortedList = sorted(nlpScore.items(), key=lambda x:(-x[1],x[0]))
                sortedList = dict(sortedList)
                sortedDict = self.makeReservesDist(sortedList)
                randAction = random.randrange(0, 100)

                for key in sortedDict:
                    if sortedDict[key]*100 > randAction:
                        actionIndex = links.index(key)
                        break 
                
            if action == None:
                actionIndex = random.randrange(0, len(links))

            try:
                action = links[actionIndex]
                action = action.replace(" ", "_")
                #print(action)
                page = webScraper.wiki.page(action)
                links = webScraper.filterLinks(list(page.links.keys()))
                self.subTreeVal = self.subTreeVal + webScraper.nlpSimilarity(page.title, terminusName, links)
                #self.subTreeVal = self.subTreeVal + webScraper.genismSimilarity(page.title, terminusName)
            except:
                traceback.print_exc()
                print("       404 - HTTP FAILED CONNECTION - " + action)
                i = i-1

        self.subTreeVal = self.subTreeVal / 10   
        self.numOfVisits = self.numOfVisits + 1


    def expandChildren(self, terminusName, expanded, webScraper, numChildren):
        links = self.childrenLinks
        expandedChildren = {}

        if numChildren < 0:
            numChildren = len(links)

        # Check if any of the links appear in target page links
        terminusTitle = str(terminusName).replace("_", " ")
        for child in links:
            if child == terminusTitle:
                print("       FOUND " + str(terminusName))
                print("           " + str(child))
                path = str(terminusName)
                node = self
                while True:
                    print("           " + str(node.page.title))
                    path = path + "###" + str(node.page.title) 
                    if node.parent == None:
                        break
                    node = node.parent
                return True, expandedChildren, self.depth+1, path 

        nlpScore = {}

        for child in links:
            nlpScore[child] = webScraper.nlpSimilarity(child, terminusName, [])
            
        sortedList = sorted(nlpScore.items(), key=lambda x:(-x[1],x[0]))
        banditArms = dict(sortedList)
        expandedArticles = list(expanded.keys())

        for key in banditArms.keys():
            if key not in expandedArticles:
                if len(self.children) < numChildren:
                    newPage = webScraper.wiki.page(key)
                    nodeToAdd = Node(self, newPage, self.depth+1)
                    self.children.append(nodeToAdd)
                    expandedChildren.update({key: self.depth+1})
                else:
                    self.reserveChildren.update({key: banditArms[key]})
            links.remove(key)
        self.reserveDist = self.makeReservesDist(self.reserveChildren)
        return False, expandedChildren, None, None


    def backpropUpdates(self, rolloutVal):
        self.subTreeVal = self.subTreeVal + rolloutVal
        self.numOfVisits = self.numOfVisits + 1