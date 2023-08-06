import spacy as sp
import src.implicit_word_network as wn

import time
import cProfile


# Path to text file
path = "./example/wiki.txt"

# Entities to search for in corpus
entity_types = ["PERSON", "LOC", "NORP", "ORG", "WORK_OF_ART"]

c = 2  # Cut-off parameter

# Importing data ...
D = wn.readDocuments(path)

# Parsing data ...
nlp = sp.load("en_core_web_sm")
D_parsed = wn.parseDocuments(D, entity_types, nlp=nlp)

# Converting parsing results ...
D_mat = wn.createCorpMat(D_parsed)

# Building graph ...
startTime = time.time()
# cProfile.run("wn.buildGraph(D_mat, c)")
V, Ep = wn.buildGraph(D_mat, c)
executionTime = time.time() - startTime
print("Execution time in seconds: " + str(executionTime))

print(len(V["entities"]))

# Convert to NetworkX object ...
G = wn.convertToNetworkX(V, Ep)

# Plot Graph
wn.plotNetwork(G, mode="interactive")
