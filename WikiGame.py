import random
import traceback
import copy
import Node as ND
import WebScraper as WB
import sys

def MCTS(root, terminus, webScraper, euct, exp):
    EXPL_CONST = exp
    numChildren = 10

    if euct == True:
        numChildren = 1

    terminusLinks = list(terminus.links.keys())
    expandedChildren = {} 

    for i in range(300):
        print("\nITERATION " + str(i))

        # UCT
        node = root
        while len(node.children) != 0:
            print("   UCT   " + node.page.title + "   " + str(len(node.children)))
            bestUCT = -1.0
            bestIndex = -1
            i = 0
            addedNode = False
            
            if euct is True:
                actionIndex = random.randrange(0, 100)
                if actionIndex < EXPL_CONST*100:
                    addedNode = node.addChildByProb(webScraper)         
                    #addedNode = node.addBestChildByProb(webScraper)
                if addedNode != False:
                    expandedChildren.update(addedNode) 


            for child in node.children:
                child.calcUCT()

                if child.uct > bestUCT:
                    bestUCT = child.uct
                    bestIndex = i
                i = i + 1
            node = node.children[bestIndex]              
        print("     " + node.page.title)

        # Expand
        if node.numOfVisits != 0 and len(node.childrenLinks) != 0:
            print("   Expand")
            outcome, children, distance, path = node.expandChildren(terminus.title, expandedChildren, webScraper, numChildren)
            if outcome == True:
                expandedChildren.update(children)
                return outcome, distance, path, len(expandedChildren), i 
            else:
                expandedChildren.update(children)
                if len(node.children) != 0:
                    childToExpand = random.randrange(0, len(node.children))
                    node = node.children[childToExpand]

        # Simulate
        print("   Simulate")
        node.rollout(terminusLinks, terminus.title, webScraper)
        
        # Backprop
        print("   Backprop")
        rolloutVal = node.subTreeVal

        while node.parent != None:
            node = node.parent
            node.backpropUpdates(rolloutVal)

    return False, "", "", len(expandedChildren), 300




webScraper = WB.WebScraper()
argsPassed = True
runEpct = False
i = 0

filenamePrefix = sys.argv[1]
depthOfTarget = int(sys.argv[2])
expCont = float(sys.argv[3])
numOfTrials = int(sys.argv[4])
argType = sys.argv[5]

if len(sys.argv) < 6:
    print("python WikipediaGame.py Data/arg/arg-x-y-z/Data_1/ z 0.5 100 EPCT")
    argsPassed = False

if argType != "UCT":
    runEpct = True


while i < numOfTrials and argsPassed:
    startPage, endPage = webScraper.getStartEndPair(depthOfTarget)

    try:
        cosDist = webScraper.nlpSimilarity(startPage.title, endPage.title, [])
        #print(cosDist)
        print(startPage.title + "  ---  " + endPage.title)
        
        if cosDist > 0:
            root = ND.Node(None, startPage, 0)
            foundTarget, distance, path, numNodes, numSims = MCTS(root, endPage, webScraper, runEpct, expCont)
            simMethod = "W2V"

            try:
                line = startPage.title + "," + endPage.title + "," + str(foundTarget) + "," + str(distance) + "," + path + "," + str(numNodes) + "," + str(numSims) + "," + simMethod + "," + argType + "," + str(expCont) + "\n"
                filename = filenamePrefix + str(i) + ".csv"
                file = open(filename, "w")
                file.write(line)
                file.close()
            except:
                line = "_,_," + str(foundTarget) + "," + str(distance) + ",_," + str(numNodes) + "," + str(numSims) + "," + simMethod + "," + argType + "," + str(expCont) + "\n"
                filename = filenamePrefix + str(i) + ".csv"
                file = open(filename, "w")
                file.write(line)
                file.close()

            i = i + 1
    except:
        traceback.print_exc()
        print("Start fail - getting new start node")
