from glob import glob
import xml.etree.ElementTree as ET
from konlpy.tag import Mecab
from collections import defaultdict, Counter

# get corpus data
collection = sorted(glob('corpus/*.xml'))
print(collection)

# parsing xml files
docs = []
for doc in collection : 
    tree = ET.parse(doc)
    content = tree.find("title").text + '\n' + tree.find("text").find("p").text
    docs.append(content)
print(docs)

# change into morphs, make dictionary using Mecab
D = defaultdict(list)
mecab = Mecab()
for i,x in enumerate(docs) : 
    terms = mecab.morphs(x)
    counter = Counter(terms)
    for term in counter : 
        D[term].append([i,counter[term]])
print(D)   






    
    
    
