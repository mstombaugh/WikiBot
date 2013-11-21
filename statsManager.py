import json

stats = {}

def write():
    with open('stats','w') as f:
                f.write(json.dumps(stats)+'\n')

def delCats():
    sub = raw_input("Enter subreddit: ")
    del stats['categories'][sub]
    write()
    print "Done\n"
    
def changeSubCount():
    sub = raw_input("Enter subreddit: ")
    count = raw_input("Enter count: ")
    stats['subreddits'][sub]['count'] = int(count)
    write()
    print "Done\n"

def changeCallCount():
    count = raw_input("Enter count: ")
    stats['count'] = int(count)
    write()
    print "Done\n"
    
def listSubs():
    for sub in stats['categories']:
        print sub
        
def backup():
    input = raw_input("Input a file name: ")
    
    with open(input,'w') as f:
        f.write(json.dumps(stats)+'\n')
    print "Done\n"

def reset():
    input = raw_input("Are you positive? (y/n): ")
    
    if input == "y":
        global stats 
        stats = {"count": 0, "subreddits": {}, "categories": {}, "queries": []}
        write()
        print "Done\n"
    else:
        None
     
if __name__ == "__main__":
 
    while True:
        with open('stats') as statsFile:
                for line in statsFile:
                    stats = json.loads(line.strip())
       
        options = '---Options---\n1: Delete subreddits categories\n2: Change subreddits count\n3: Change call count\n4: List subreddits with categories\n5: Backup stats file\n6: Reset stats file\n'
        print options
        
        choice = raw_input('Choose option: ')
        
        if choice == '1':
            delCats()
        elif choice == '2':
            changeSubCount()
        elif choice == '3':
            changeCallCount()
        elif choice == '4':
            listSubs()
        elif choice == '5':
            backup()
        elif choice == '6':
            reset()
        else:
            print "Incorrect input"
    
    