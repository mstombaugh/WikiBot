import praw
import json
from getWiki import Wiki

def main():
    stats = {}
    with open('wikibot_info.json') as cfgFile:
        for line in cfgFile:
            config = json.loads(line.strip())
    with open('already_done') as f:
        for line in f:
            already_done=json.loads(line.strip())
    with open('stats') as statistics:
        for line in statistics:
            stats = json.loads(line.strip())
    r=praw.Reddit(user_agent = 'Wiki Bot')
    r.login(config['user'],config['pass'])
    wikibot_names = ['wikibot!', 'wiki-bot!', '!wikibot']
    wiki = Wiki()
    try:
        for comment in praw.helpers.comment_stream(r,'all'):
            op_text = comment.body.lower()
            calls_wikibot = any(string in op_text for string in wikibot_names)
            if comment.fullname not in already_done['already_done'] and calls_wikibot:
                #format a reply. 
                #msg = 'WikiBot here.  This is what I found (ALPHA BUILD):\n\n'
                codeWordFound = firstQuotes = secondQuotes = False
                wikiError=False
                wikiRequest=[]
                wikiArticle = ''
                language = 'english'
                print op_text.split(' ')
                for word in op_text.split(' '):
                    if 'wikibot' in word or 'wiki-bot' in word and not codeWordFound:
                        codeWordFound = True
                    elif '"' in word and codeWordFound and not firstQuotes:
                        firstQuotes = True
                        wikiRequest.append(str(word).translate(None,'"').encode('utf_8','ignore'))
                        wikiRequest.append(' ')
                    elif codeWordFound and not firstQuotes and '"' not in word:
                        language = str(word)
                    elif '"' in word and codeWordFound and firstQuotes and not secondQuotes:
                        secondQuotes = True
                        wikiRequest.append(str(word).translate(None,'"').encode('utf_8','ignore'))
                    elif firstQuotes and not secondQuotes:
                        wikiRequest.append(str(word).encode('utf_8','ignore'))
                        wikiRequest.append(' ')
                    if '"' in word and word.count('"')>1:
                        secondQuotes = True
                if not firstQuotes or not secondQuotes:
                    wikiArticle = 'Error: Please put quotation marks (") on both sides of your query. '
                    wikiError = True
                if not wikiError: 
                    msg =''.join(wikiRequest)
                    msg = msg.replace('&amp;','&')
                    msg = msg.replace('&quot;','"')
                    msg = msg.replace('&gt;',">")
                    msg = msg.replace('&lt;',"<")
                    msg = msg.strip()
                    print msg + ' ' + language
                    wikiArticle = wiki.searchwiki(msg,convertLanguageCode(language))
                #msg=(wikiArticle)
                #if language:
                #    msg += '\n\n Requested language: ' + language
               
                print comment.subreddit.display_name
                try:
                    if msg.strip() not in stats[comment.subreddit.display_name]:
                        stats[comment.subreddit.display_name].append(msg.strip())
                except Exception as e:
                    stats[comment.subreddit.display_name] = [msg.strip()]
                    print e

                comment.reply(wikiArticle)
                already_done['already_done'].append(comment.fullname)
    except KeyboardInterrupt:
        with open('already_done','w+') as f:
            f.write(json.dumps(already_done)+'\n')
        with open('stats','w+') as statistics:
            statistics.write(json.dumps(stats)+'\n')
        print('Goodbye!')
    except Exception as e:
        with open('already_done','w+') as f:
            f.write(json.dumps(already_done)+'\n')
        with open('stats','w+') as statistics:
            statistics.write(json.dumps(stats)+'\n')
        print e
        main()
    
def convertLanguageCode(language):
        try:
            return{
                'english'   : 'en',
                'dutch'     : 'nl',
                'german'    : 'de',
                'sweedish'  : 'sv',
                'french'    : 'fr',
                'italian'   : 'it',
                'russian'   : 'ru',
                'spanish'   : 'es',
                'polish'    : 'pl',
                'waray-waray' : 'war',
                'cebuano'   : 'ceb',
                'cietnamese': 'vi',
                'japanese'  : 'ja',
                'portuguese': 'pt',
                'chinese'   : 'zh',
                'ukranian'  : 'uk',
                'catalan'   : 'ca',
                'norwegian' : 'no',
                'finnish'   : 'fi',
                'persian'   : 'fa',
                'indonesian': 'id',
                'czech'     : 'cs',
                'korean'    : 'ko',
                'hungarian' : 'hu',
                'arabic'    : 'ar',
                'malay'     : 'ms',
                'romanian'  : 'ro',
                'serbian'   : 'sr',
                'minangkabau':'min',
                'turkish'   : 'tr',
                'kazakh'    : 'kk',
                'slovak'    : 'sk',
                'esperanto' : 'eo',
                'danish'    : 'da',
                'basque'    : 'eu',
                'lithuanian': 'lt',
                'bulgarian' : 'bg',
                'hebrew'    : 'he',
                'croatian'  : 'hr',
                'slovenian' : 'sl',
                'uzbek'     : 'uz',
                'volapuk'   : 'vo',
                'estonian'  : 'et',
                'hindi'     : 'hi',
                'galician'  : 'gl',
                'nynorsk'   : 'nn',
                'simple'    : 'simple'
            }[language.lower()]
        except:
            return language
            
            

if __name__ == "__main__":
    main()
    