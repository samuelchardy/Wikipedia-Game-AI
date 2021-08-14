import Node as ND
import WebScraper as WB
import urllib.parse
import time
import os


def getPage():
    validPage = False
    page, vec = None, None

    while validPage is not True:
        try:
            page = webScraper.getRandomPage()
            vec = webScraper.wiki2vec.get_entity_vector(page.title).reshape(1, -1)
            validPage = True
        except:
            validPage = False
    return page


startTime = time.time()
webScraper = WB.WebScraper()
lines = []

for i in range(100):
    filename = str(i) + ".csv"

    if os.path.exists(filename) is not True:
        firstPage = getPage()
        secondPage = getPage()

        cosDist = webScraper.nlpSimilarity(firstPage.title, secondPage.title, [])
        eucDist = webScraper.nlpSimilarity(firstPage.title, secondPage.title, [], False)

        # print("Cos dist: " + str(cosDist[0][0]))
        # print("Euc dist: " + str(eucDist[0][0]))

        numLinks = len(webScraper.filterLinks(list(firstPage.links.keys())))
        line = firstPage.title + "," + secondPage.title + "," + str(cosDist[0][0]) + "," + str(eucDist[0][0]) + "," + str(numLinks)

        file = open(filename, "w")
        file.write(line)
        file.close()

exeTime = time.time() - startTime
print("Done")
print("Time: " + str(round(exeTime/60, 1)) + " mins")


