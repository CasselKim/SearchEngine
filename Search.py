from glob import glob
import xml.etree.ElementTree as ET
from kiwipiepy import Kiwi
kiwi = Kiwi()


# get corpus data
files = glob('corpus\*.xml')
docs = []
for f in files : 
    tree = ET.parse(f)
    content = tree.find("title").text + '\n' + tree.find("text").find("p").text
    docs.append(content)
    
print(docs)


    
    
    
