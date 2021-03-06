from glob import glob
import xml.etree.ElementTree as ET
from konlpy.tag import Mecab
from collections import defaultdict, Counter
from math import log
from functools import reduce

# get corpus data
collection = sorted(glob('corpus/*.xml'))
#print(collection)


# parsing xml files
docs = []
for i,doc in enumerate(collection) : 
    tree = ET.parse(doc)
    title = ' '.join(tree.find("title").text.split(' ')[1:])
    content = title + '\n' + tree.find("text").find("p").text
    docs.append(content)

#print(docs)

def docsToDict(docs,SMART) : 
    # change into morphs, make dictionary using Mecab
    # Dictionary format : {"term" : [[docID, tf(term freq)],[docID, tf(term freq)], ...]}
    # doc-freq can be given by len(D["term"])
    tf, idf, norm = SMART

    D = defaultdict(list)
    mecab = Mecab()
    counters = [Counter([y[0] for y in mecab.pos(x) if y[1] in ('VV','VA','VX','VCP','VCN','MM','MAG','MAJ','IC','SL','SH','SN')]+mecab.nouns(x)) for x in docs]
    #counters = [Counter(mecab.morphs(x)) for x in docs]
    #print(counters)
    common = reduce(lambda a,b : a+b,counters)
    #for x in common : 
    #    common[x] /= len(docs)
    
    # tf
    relates = []
    for i,counter in enumerate(counters) : 
        temp=0
        for term in counter : 
            term_freq = counter[term]

            # term freq
            if tf=='n' : 
                pass
            elif tf=='l' : 
                term_freq = 1+log(term_freq)
            elif tf=='a' : 
                term_freq = 0.5 + (0.5*term_freq)/counter.most_common(1)[0][1]
            elif tf=='b' : 
                term_freq = 1 if term_freq>0 else 0
            #elif tf=='L' : 
            #    term_freq = (1+log(term_freq))/(1+log(common[term]))
            else : 
                raise(Exception("Wrong tf! :",tf))
            temp+=term_freq**2
            D[term].append([i,term_freq])
        relates.append(temp**.5)

    # norm
    for term in D : 
        for documents in D[term] : 
            docID,normalized = documents
            coef = relates[docID]
            if norm=='n' : 
                pass
            elif norm=='c' : 
                normalized/=coef
                assert(0<=normalized<=1)
            else : 
                raise(Exception("Wrong norm! :",norm))
            documents[1]=normalized

    # idf and weight
    for term in D : 
        for documents in D[term] : 
            w = documents[1]
            if idf=='n' : 
                pass
            elif idf=='t' : 
                w*=log(len(docs)/len(D[term]))
            elif idf=='p' : 
                w=max(0,log((len(docs)-len(D[term]))/len(D[term])))
            else : 
                raise(Exception("Wrong idf! :",idf))
            documents[1] = w
    return D

documents = docsToDict(docs,'ltc')
query = input("????????? ??????????????? : ")
print("?????? :",query)
query = docsToDict([query],'lnc')

score = defaultdict(float)
for query_term in query : 
    query_weight = query[query_term][0][1]
    for doc_info in documents[query_term] : 
        docID, doc_weight = doc_info
        score[docID] += query_weight*doc_weight


print('======================')
for i,num in enumerate(sorted(score,key=lambda x: score[x],reverse=True)) : 
    if i==5 : break
    print(num+1,docs[num])
    print("score :",score[num])








    
    
    
