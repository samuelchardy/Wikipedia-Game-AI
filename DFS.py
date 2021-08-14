import Search as search
import Node as ND
import traceback

class DFS(search.Search):
    def run(self, gameNum, depth):
        """
        Runs the full depth-first search.

        :param gameNum: Trial number of the current game.
        :param depth: The depth to choose a target page from the start page.
        """
        worked = False
        self.filenamePrefix = "Data/DFS/"

        while worked == False:
            found, expandedChildren, foundDepth = False, {}, ""
            startPage, endPage = self.webScraper.getStartEndPair(depth)

            print(startPage.title + "   " + endPage.title)
            try:
                cosDist = self.webScraper.nlpSimilarity(startPage.title, endPage.title, [])

                if cosDist > 0:
                    root = ND.Node(None, startPage, 0)

                    for i in range(100):
                        print(root.page.title)
                        found, children, foundDepth, path = root.expandChildren(endPage.title, expandedChildren, self.webScraper, -1)
                        expandedChildren.update(children)

                        if found is True:
                            break

                        root = root.children[0]
                    fileName = "Data/DFS/DFS-" + str(depth) + "/"
                    self.saveOutput(fileName, "DFS", gameNum, startPage, endPage, found, foundDepth, path, len(expandedChildren))
                    worked = True

            except:
                traceback.print_exc()
                print("Start fail - getting new start node")


DFS()