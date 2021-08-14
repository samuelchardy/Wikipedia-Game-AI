import random

class Output:
    def __init__(self, outcome, distance, path, numExpandedChildren, numSimulations):
        """
        Creates Output object that stores information for a given output line.

        :param outcome: Was the target page found during the search.
        :param distance: The distance from the start to target page.
        :param path: The sequence of pages from start to target page.
        :param numExpandedChildren: How many articles were explored.
        :param numSimulations: The number of search iterations.
        """
        self.outcome = outcome
        self.distance = distance
        self.path = path
        self.numExpandedChildren = numExpandedChildren
        self.numSimulations = numSimulations



def MCTS(root, terminus, webScraper, euct, exp):
    """
    Runs the MCTS search strategy.

    :param root: The root Node of the search tree.
    :param terminus: The wikipediaapi page that is the search target.
    :param webScraper: A webScraper object that is used for a myriad of functions.
    :param euct: The search strategy utilised.
    :param exp: The used exploration constant.
    :return: Output.outcome, Output.distance, Output.path, Output.numExpandedChildren, Output.numSimulations
    """
    EXPL_CONST = exp
    output = []
    numChildren = -1

    if euct == True:
        numChildren = 1

    terminusLinks = list(terminus.links.keys())
    expandedChildren = {} 

    for i in range(100):
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
                    addedNode = node.addChildByProb()         
                    #addedNode = node.addBestChildByProb()
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
            outcome, children, distance, path = node.expandChildren(terminus.title, expandedChildren, numChildren)
            if outcome == True:
                expandedChildren.update(children)
                output.append(Output(outcome, distance, path, len(expandedChildren), i))
            else:
                expandedChildren.update(children)
                if len(node.children) != 0:
                    childToExpand = random.randrange(0, len(node.children))
                    node = node.children[childToExpand]

        # Simulate
        print("   Simulate")
        node.rollout("RBRP", terminus.title)
        
        # Backprop
        print("   Backprop")
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
