import random

class Output:
    def __init__(self, outcome, distance, path, numExpandedChildren, numSimulations):
        self.outcome = outcome
        self.distance = distance
        self.path = path
        self.numExpandedChildren = numExpandedChildren
        self.numSimulations = numSimulations



def MCTS(root, terminus, webScraper, euct, exp):
    EXPL_CONST = exp
    output = []
    numChildren = 10

    if euct == True:
        numChildren = 1

    expandedChildren = {} 

    for i in range(300):
        #print("\nITERATION " + str(i))

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
        #print("     " + node.page.title)

        # Expand
        if node.numOfVisits != 0 and len(node.childrenLinks) != 0:
            #print("   Expand")
            outcome, children, distance, path = node.expandChildren(terminus.title, expandedChildren, webScraper, numChildren)
            if outcome == True:
                expandedChildren.update(children)
                output.append(Output(outcome, distance, path, len(expandedChildren), i))
            else:
                expandedChildren.update(children)
                if len(node.children) != 0:
                    childToExpand = random.randrange(0, len(node.children))
                    node = node.children[childToExpand]

        # Simulate
        #print("   Simulate")
        node.rollout("RBRP", terminus.title, webScraper)
        
        # Backprop
        #print("   Backprop")
        rolloutVal = node.subTreeVal

        while node.parent != None:
            node = node.parent
            node.backpropUpdates(rolloutVal)

    if len(output) == 0:
        return False, "", "", len(expandedChildren), 300
    else:
        minimum = 10000000
        finalOutput = None
        for out in output:
            if out.distance < minimum:
                minimum = out.distance
                finalOutput = out
        return finalOutput.outcome, finalOutput.distance, finalOutput.path, finalOutput.numExpandedChildren, finalOutput.numSimulations
