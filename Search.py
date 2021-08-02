import WebScraper as WB
import sys

class Search:
    def __init__(self):
        self.webScraper = WB.WebScraper()

        if len(sys.argv) < 3:
            print("python EPG.py [numOfGames] [targetDepth]")
        else:
            for i in range(int(sys.argv[1])):
                self.run(i, int(sys.argv[2]))




    def saveOutput(self, filenamePrefix, algType, i, startPage, endPage, foundTarget, distance, path, numNodes):
        try:
            line = startPage.title + "," + endPage.title + "," + str(foundTarget) + "," + str(distance) + "," + path + "," + str(numNodes) + ",100,None," + algType + ",0\n"
            filename = self.filenamePrefix + str(i) + ".csv"
            file = open(filename, "w")
            file.write(line)
            file.close()
        except:
            line = "_,_," + str(foundTarget) + "," + str(distance) + ",_," + str(numNodes) + ",300,None," + algType + ",0\n"
            filename = self.filenamePrefix + str(i) + ".csv"
            file = open(filename, "w")
            file.write(line)
            file.close()
