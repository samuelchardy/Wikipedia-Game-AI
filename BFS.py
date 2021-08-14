import Search as search
import Node as ND
import traceback

class BFS(search.Search):
    def run(self, gameNum, depth):
        """
        Runs the full breadth-first search.

        :param gameNum: Trial number of the current game.
        :param depth: The depth to choose a target page from the start page.
        """
        worked = False
        self.filenamePrefix = "Data/BFS/"
        
        while worked == False:  
            found, expandedChildren, foundDepth, path = False, {}, "", ""
            pageQueue = []
            startPage, endPage = self.webScraper.getStartEndPair(depth)

            try:
                cosDist = self.webScraper.nlpSimilarity(startPage.title, endPage.title, [])
                if cosDist > 0:
                    root = ND.Node(None, startPage, 0, self.webScraper)

                    for i in range(100):
                        print(root.page.title)
                        found, children, foundDepth, path = root.expandChildren(endPage.title, expandedChildren, -1)
                        print(len(children))
                        expandedChildren.update(children)

                        if found is True:
                            break

                        for child in root.children:
                            pageQueue.append(child)

                        root = pageQueue.pop(0)

                    fileName = "Data/BFS/BFS-" + str(depth) + "/"
                    self.saveOutput(fileName, "BFS", gameNum, startPage, endPage, found, foundDepth, path, len(expandedChildren))
                    worked = True

            except:
                traceback.print_exc()
                print("Start fail - getting new start node")


BFS()