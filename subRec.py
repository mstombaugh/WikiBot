import json
from getWiki import Wiki

def subRec(articleCats):
    #get stats file for categories
    with open('stats') as statsFile:
            for line in statsFile:
                stats = json.loads(line.strip())
                
    #create dicitonary containing only categories in common with articleCats
    categories = {}
    for sub in stats['categories']:
        for cat in stats['categories'][sub]:
            if cat in articleCats:
                try:
                    categories[sub][cat] = stats['categories'][sub][cat]
                except KeyError:
                    categories[sub] = {} 
                    categories[sub][cat] = stats['categories'][sub][cat]
                    
    print categories
    
if __name__ == "__main__":
    wiki = Wiki()
    results, cats = wiki.searchwiki("Johnny Manziel","en",False)
    subRec(cats)