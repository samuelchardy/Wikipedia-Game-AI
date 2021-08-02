import Search as search
import Node as ND
import traceback

class BFS(search.Search):
    def run(self, gameNum, depth):
        worked = False
        self.filenamePrefix = "Data/BFS/"
        
        while worked == False:  
            found, expandedChildren, foundDepth = False, {}, ""
            pageQueue = []
            startPage, endPage = self.webScraper.getStartEndPair(depth)

            try:
                cosDist = self.webScraper.nlpSimilarity(startPage.title, endPage.title, [])
                if cosDist > 0:
                    root = ND.Node(None, startPage, 0)

                    for i in range(300):
                        print(root.page.title)
                        found, children, foundDepth, path = root.expandChildren(endPage.title, expandedChildren, self.webScraper, -1)
                        expandedChildren.update(children)

                        if found is True:
                            break

                        for child in root.children:
                            pageQueue.append(child)

                        root = pageQueue.pop(0)

                    self.saveOutput("Data/BFS/", "BFS", gameNum, startPage, endPage, found, foundDepth, path, len(expandedChildren))
                    worked = True

            except:
                traceback.print_exc()
                print("Start fail - getting new start node")


BFS()