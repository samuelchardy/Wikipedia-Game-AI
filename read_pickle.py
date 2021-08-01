import pickle
import time

def read():
    fullWikiDict = {}
    fullRedirDict = {}

    startTime = time.time()

    for i in range(32):
        i += 1
        print(i)
        fileName = "WikiData/all_pages_{num}.pickle".format(num=i)
        inFile = open(fileName, "rb")
        fileDict = pickle.load(inFile)
        fullWikiDict.update(fileDict)

        fileName = "WikiData/all_redirs_{num}.pickle".format(num=i)
        inFile = open(fileName, "rb")
        fileDict = pickle.load(inFile)
        fullRedirDict.update(fileDict)


    timePassed = time.time() - startTime
    print("Done")

    return fullWikiDict, fullRedirDict