import random
from math import sqrt
from math import log
import traceback
import WebScraper as WB


class Node:
    def __init__(self, parent, articlePage, depth, webScraper):
        """
        Creates a Node and initialises the relevant attributes for proper operation.

        :param parent: The Node object that created this Node.
        :param articlePage: A wikipediaapi page for this Node's wikipedia article.
        :param depth: The depth of this node in the Monte-Carlo tree.
        :param webScraper: An object of the WebScraper class which provides much functionality.
        """
        self.parent = parent
        self.depth = depth
        self.page = articlePage
        self.subTreeVal = 0.0
        self.numOfVisits = 0
        self.uct = 0.0
        self.children = []
        self.reserveChildren = {}
        self.reserveDist = {}
        self.webScraper = webScraper
        self.childrenLinks = self.webScraper.filterLinks(list(self.page.links.keys()))


    def calcUCT(self):
        """
        Calculates/updates the upper confidence bound for trees value for this Node,
        storeing it as an instance variable.
        """
        if self.numOfVisits == 0:
            self.uct = 100000.0
        else:
            numParVisits = self.parent.numOfVisits
            explore = 2*(0.9)*(sqrt((2*log(numParVisits))/self.numOfVisits))
            self.uct = (self.subTreeVal/self.numOfVisits) + explore


    def addBestChildByProb(self):
        """
        Probabilistically selects the highest reward child Node from this Node for expansion.

        :return: A dict of the title of the best page and the current tree depth.
        """
        EXPL_CONST = 0.3
        key = list(self.reserveChildren.keys())

        if len(key) == 0:
            return False
        else:
            key = key[0]

        actionIndex = random.randrange(0, 100)
        newActionProb = self.reserveChildren[key] * EXPL_CONST * 100

        if actionIndex < newActionProb:
            newPage = self.webScraper.wiki.page(key)
            nodeToAdd = Node(self, newPage, self.depth+1, self.webScraper)

            self.children.append(nodeToAdd)
            del self.reserveChildren[key]
            return {self.children[-1].page.title: self.depth+1}
        else:
            return False


    def addChildByProb(self):
        """
        Selects a child Node of this Node to expand where selection
        probability is proportional to child Node reward.

        :return: A dict of the title of the page to expand and the current tree depth.
        """
        if self.reserveDist == None:
            return False

        keys = list(self.reserveDist.keys())
        actionIndex = random.randrange(0, 100)

        if sum(self.reserveDist.values()) == 0:
            return False

        for key in keys:
            if self.reserveDist[key]*100 > actionIndex:
                if self.notAlreadyBeenTaken(key):
                    newPage = self.webScraper.wiki.page(key)
                    nodeToAdd = Node(self, newPage, self.depth+1, self.webScraper)

                    self.children.append(nodeToAdd)
                    #del self.reserveChildren[key]
                    #del self.reserveDist[key]

                    #self.reserveDist = self.makeReservesDist(self.reserveChildren)
                    return {self.children[-1].page.title: self.depth+1}
                else:
                    print("OH NO")
                    return False


    def notAlreadyBeenTaken(self, key):
        """
        Checks is a page has been explored previously, and returns the result.

        :param key: The title of the page to check.
        :return: Boolean value, for if a child Node has already been explored.
        """
        for child in self.children:
            if child.page.title == key:
                return False
        return True


    def makeReservesDist(self, reserveChildren):
        """
        Creates a dict for storing unselected child Nodes,
        and updates their selection probability. 

        :param reserveChildren: child Nodes that are not currently considered by UCT.
        :return: An updated dict of titles and selections probabilities based.
        """
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


    def rollout(self, policy, terminusName):
        """
        Performs the rollout function of MCTS by assessing future rewards.

        :param policy: The action selection strategy.
        :param terminusName: The title of the target wikipedia page.
        """
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
                    nlpScore[child] = self.webScraper.nlpSimilarity(child, terminusName, [])

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
                page = self.webScraper.wiki.page(action)
                links = self.webScraper.filterLinks(list(page.links.keys()))
                self.subTreeVal = self.subTreeVal + self.webScraper.nlpSimilarity(page.title, terminusName, links)
                #self.subTreeVal = self.subTreeVal + webScraper.genismSimilarity(page.title, terminusName)
            except:
                raise
                print("       404 - HTTP FAILED CONNECTION - " + action)
                i = i-1

        self.subTreeVal = self.subTreeVal / 10   
        self.numOfVisits = self.numOfVisits + 1


    def expandChildren(self, terminusName, expanded, numChildren):
        """
        Expands a Node by initialises the child Nodes that correspond to page links.

        :param terminusName: The title of the target wikipedia page.
        :param expanded: A list of the currently expanded pages.
        :param numChildren: The number of children to expand from each Node.
        :return: Is target found, updated list of expanded Nodes, depth of target if found, path to target if found.
        """
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
            nlpScore[child] = self.webScraper.nlpSimilarity(child, terminusName, [])
            
        sortedList = sorted(nlpScore.items(), key=lambda x:(-x[1],x[0]))
        banditArms = dict(sortedList)
        expandedArticles = list(expanded.keys())

        for key in banditArms.keys():
            if key not in expandedArticles:
                if len(self.children) < numChildren:
                    newPage = self.webScraper.wiki.page(key)
                    nodeToAdd = Node(self, newPage, self.depth+1, self.webScraper)
                    self.children.append(nodeToAdd)
                    expandedChildren.update({key: self.depth+1})
                else:
                    self.reserveChildren.update({key: banditArms[key]})
            links.remove(key)
        self.reserveDist = self.makeReservesDist(self.reserveChildren)
        return False, expandedChildren, None, None


    def backpropUpdates(self, rolloutVal):
        """
        Performs the backpropagations functionality of MCTS, including
        updating the Node value and visit quantities.

        :param rolloutVal: The value of the rollout of this node.
        """
        self.subTreeVal = self.subTreeVal + rolloutVal
        self.numOfVisits = self.numOfVisits + 1