import praw
import json
#import wikipedia API
#global MAX_COMMENTS_TO_FETCH = 25

def main():
    with open('wikibot_info.json') as cfgFile:
        for line in cfgFile:
            config = json.loads(line.strip())
    with open('already_done') as f:
        for line in f:
            already_done=json.loads(line.strip())
    r=praw.Reddit(user_agent = 'Wiki Bot')
    r.login(config['user'],config['pass'])
    wikibot_names = ['wikibot!', 'wiki-bot!', '!wikibot']
    try:
        for comment in praw.helpers.comment_stream(r,'all'):
            op_text = comment.body.lower()
            calls_wikibot = any(string in op_text for string in wikibot_names)
            if comment.fullname not in already_done['already_done'] and calls_wikibot:
                #format a reply. 
                msg = 'WikiBot here.  This is what I found (ALPHA BUILD):\n\n'
                callIndex = firstQuotes = secondQuotes = False
                wikiError=False
                wikiRequest=[]
                wikiArticle = ''
                language = ''
                print op_text.split(' ')
                for word in op_text.split(' '):
                    if 'wikibot' in word or 'wiki-bot' in word:
                        callIndex = True
                    if '"' in word and callIndex and not firstQuotes:
                        firstQuotes = True
                        wikiRequest.append(str(word).translate(None,'"').encode('utf_8','ignore'))
                        wikiRequest.append(' ')
                    elif callIndex and not firstQuotes:
                        language = str(word)
                    elif '"' in word and callIndex and firstQuotes and not secondQuotes:
                        secondQuotes = True
                        wikiRequest.append(str(word).translate(None,'"').encode('utf_8','ignore'))
                    elif firstQuotes and not secondQuotes:
                        wikiRequest.append(str(word).encode('utf_8','ignore'))
                        wikiRequest.append(' ')
                if not firstQuotes or not secondQuotes:
                    wikiArticle = 'Error: Please put quotation marks (") on both sides of your query. ' +  str(firstQuotes) + ' ' + str(secondQuotes)
                    wikiError = True
                if not wikiError:
                    #use wikipedia wrapper
                    #wikiArticle = wikiWrapper.search(''.join(wikiRequest))
                #temp:
                    wikiArticle += ''.join(wikiRequest)
                msg+=(wikiArticle)
                if language:
                    msg += '\n\n Requested language: ' + language
                msg = msg.replace('&amp;','&')
                msg = msg.replace('&quot;','"')
                msg = msg.replace('&gt;',">")
                msg = msg.replace('&lt;',"<")
                #print msg

                comment.reply(msg)
                already_done['already_done'].append(comment.fullname)
    except KeyboardInterrupt:
        with open('already_done','w+') as f:
            f.write(json.dumps(already_done)+'\n')
        print('Goodbye!')
    
if __name__ == "__main__":
    main()
    