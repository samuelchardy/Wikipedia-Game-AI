# WikipediaGameAI

## Introduction
Wikipedia is the worlds largest online encyclopedia, containing 6,277,220 unique articles in its English version.  The nature of the Wikipedia articles is to provide information on a topic, but the explanation of complex topics predicates reference to other articles required to provide definition.  Subsequently, Wikipedia articles provide a pathway from one topic to another closely related topic. This forms the basis of the Wikipedia game, where starting from a random page the players attempt to reach another page using only the incumbent page links. The difficulty in this domain is two-fold, namely the large quantity of articles to search and the difficulty with determining if a new article gets you closer to the target article.

## How Does it Work?
Getting the articles:
* Webscraped using wikipediaapi and beautiful soup.

Exploring paths:
* Monte-Carlo Tree Search, with bespoke modifications to create a dynamic subset variant of UCT.

Analysing similarity between articles:
* Titles are vectorised using word embeddings from Wikipedia2Vec.
* If the title is not known to the Wikipedia2Vec model we use the title of the first three links on that page and average across there vectors.

## Use Instructions
The command line argument take the format: "python WikiGame.py [outDir] [tarDep] [explConst] [trials] [argType]", where these variables mean the following:
* outDir: (STRING) The relative directory for output files to be saved in.
* tarDep: (INT) The number of random links to be followed from the start page to find a target page.
* explConst: (FLOAT in range (0,1)) A constant used to edit the behaviour of the dynamic subset UCT algorithm.
* trials: (INT) Number of games you would like to run.
* argType: (STRING ("UCT" or "EPCT")) Tells the system which algorithm you want to employ.

## Setup (MANUAL)
* pip -r install Requirements.txt
* This system requires a file named "enwiki_20180420_win10_100d.pkl" from https://wikipedia2vec.github.io/wikipedia2vec/pretrained/, this file represents a pretrained word embedding model that is used by the Wikipedia2Vec module.
