import traceback
import Node as ND
import WebScraper as WB
import WikiGame as WG
import sys

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
    print("python WikiGame.py Data/arg/arg-x-y-z/Data_1/ z 0.5 100 EPCT")
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
            foundTarget, distance, path, numNodes, numSims = WG.MCTS(root, endPage, webScraper, runEpct, expCont)
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