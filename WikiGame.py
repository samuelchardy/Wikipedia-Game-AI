import random
import traceback
import copy
import Node as ND
import WebScraper as WB

def MCTS(root, terminus, webScraper, euct):
    EXPL_CONST = 0.66

    terminusLinks = list(terminus.links.keys())
    expandedChildren = {} 

    for i in range(300):
        print("\nITERATION " + str(i))

        # UCT
        node = root
        while len(node.children) != 0:
            print("   UCT")
            bestUCT = -1.0
            bestIndex = -1
            i = 0
            addedNode = False
            
            if euct is True:
                actionIndex = random.randrange(0, 100)
                if actionIndex < EXPL_CONST*100:
                    #addedNode = node.addChildByProb(webScraper)            
                    addedNode = node.addBestChildByProb(webScraper)
                if addedNode is not False:
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
            outcome, children, distance, path = node.expandChildren(terminus.title, expandedChildren, webScraper)
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

lines = []
i = 0

while i < 100:
    startPage, endPage = webScraper.getStartEndPair(3)

    try:
        cosDist = webScraper.nlpSimilarity(startPage.title, endPage.title, [])
        #print(cosDist)
        print(startPage.title + "  ---  " + endPage.title)
        
        if cosDist > 0:
            root = ND.Node(None, startPage, 0)

            foundTarget, distance, path, numNodes, numSims = MCTS(root, endPage, webScraper, True)

            simMethod = "W2V"
            knowMethod = "JT"
            expConstant = 0.05

            line = startPage.title + "," + endPage.title + "," + str(foundTarget) + "," + str(distance) + "," + path + "," + str(numNodes) + "," + str(numSims) + "," + simMethod + "," + knowMethod + "," + str(expConstant) + "\n"
            filename = "Data/" + str(i) + ".csv"
            file = open(filename, "w")
            file.write(line)
            file.close()

            i = i + 1
    except:
        traceback.print_exc()
        print("Start fail - getting new start node")
