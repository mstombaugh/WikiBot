import json
import math

def subRec(articleCats):
    #get stats file for categories
    with open('stats') as statsFile:
            for line in statsFile:
                stats = json.loads(line.strip())
              
    #create dicitonary containing only categories in common with articleCats
    ignore = ['WikiBot']
    categories = {}
    for sub in stats['categories']:
        if sub not in ignore:
            for cat in stats['categories'][sub]:
                if cat in articleCats:
                    try:
                        categories[sub][cat] = stats['categories'][sub][cat]
                    except KeyError:
                        categories[sub] = {} 
                        categories[sub][cat] = stats['categories'][sub][cat]
    
    #calculate similarity with cosin
    similarity = {}
       
    for sub in categories:
        sum = 0
        for cat in categories[sub]:
            sum += categories[sub][cat]
        
        magSum = 0
        for cat in categories[sub]:
            magSum += math.pow(categories[sub][cat],2)
        magSum = math.sqrt(magSum)
        
        similarity[sub] = sum / (len(articleCats) * magSum)
    
    #get top three similarites
    return sorted(similarity.items(), key=lambda x: x[1], reverse = True)[:3]
       