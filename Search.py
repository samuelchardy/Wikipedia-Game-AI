import WebScraper as WB
import sys

class Search:
    def __init__(self):
        """
        Parent class constructor for BFS and DFS, sets the search procedures running
        using the input command line parameters.
        """        
        self.webScraper = WB.WebScraper()

        if len(sys.argv) < 3:
            print("python EPG.py [numOfGames] [targetDepth]")
        else:
            for i in range(int(sys.argv[1])):
                self.run(i, int(sys.argv[2]))




    def saveOutput(self, filenamePrefix, algType, i, startPage, endPage, foundTarget, distance, path, numNodes):
        """
        Saves a single line .csv file with the name as the trial number,
        with all trial data stored accordingly.

        :param filenamePrefix: The directory to save the file within.
        :param algType: The type of search strategy used (BFS/DFS).
        :param i: The trial number.
        :param startPage: The wikipediaapi page for the start article.
        :param endPage: The wikipediaapi page for the target article.
        :param foundTarget: Was the target found (True/False).
        :param distance: Distance from the start to target pages.
        :param path: The sequence of pages from the start to target page.
        :param numNodes: The number of pages explored during the search.
        """
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
