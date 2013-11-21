from wikibot import WikiBot

"""
This program's purpose is to issue a query to the system to change the stats file
"""

bot = WikiBot()
bot.setUp()

while True:
    
    try:
        sub = raw_input(">>Subreddit: ")
    except KeyboardInterrupt:
            break
        
    while True:   
        try:
            query = raw_input(">>Query: ")
        except KeyboardInterrupt:
            break

        try:
            bot.parseComments(op_text = 'wikibot! "' + query + '"', subreddit = sub)
            print ">>Added ", query, sub
        except Exception as e:
            print e