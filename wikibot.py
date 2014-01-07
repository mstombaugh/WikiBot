import praw
import json
from getWiki import Wiki
from unidecode import unidecode

class WikiBot:
    def setUp(self):
        self.stats = {}
        self.already_done = {}
        self.config = {}
        with open('wikibot_info.json') as cfgFile:
            for line in cfgFile:
                self.config = json.loads(line.strip())
                
        with open('already_done') as f:
            for line in f:
                self.already_done=json.loads(line.strip())
                
        with open('stats') as statistics:
            for line in statistics:
                try:
                    self.stats = json.loads(line.strip())
                    
                except Exception as e:
                    self.stats = json.loads('{"count": 1, "subreddits": {}, "categories": {}, "queries": []}'.strip())
                    print e
        self.r=praw.Reddit(user_agent = 'Wiki Bot')
        self.r.login(self.config['user'],self.config['pass'])
        self.wikibot_names = ['wikibot!', 'wiki-bot!', '!wikibot']
        self.wiki = Wiki()

    def run(self):
        try:
            for comment in praw.helpers.comment_stream(self.r,'all', limit = None):
                op_text = unidecode(comment.body.lower())
                self.parseComments(op_text, subreddit=comment.subreddit.display_name , onReddit = True, comment = comment)
        except KeyboardInterrupt:
            with open('already_done','w+') as f:
                f.write(json.dumps(self.already_done)+'\n')
            with open('stats','w+') as statistics:
                statistics.write(json.dumps(self.stats)+'\n')
            print('Goodbye!')
        except Exception as e:
            with open('already_done','w+') as f:
                f.write(json.dumps(self.already_done)+'\n')
            with open('stats','w+') as statistics:
                statistics.write(json.dumps(self.stats)+'\n')
            print 'error2 ' + str(e)
            self.run()
        
    def convertLanguageCode(self,language):
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
                
    def parseComments(self,op_text='', subreddit='WikiBot', onReddit = False, comment = None):
            global msg
            if onReddit:
                fullname = comment.fullname
            else:
                fullname = ''
            calls_wikibot = any(string in op_text for string in self.wikibot_names)
            if fullname not in self.already_done['already_done'] and calls_wikibot or not onReddit:
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
                        wikiRequest.append(unidecode(str(word).translate(None,'"')))
                        wikiRequest.append(' ')
                    elif codeWordFound and not firstQuotes and '"' not in word:
                        language = str(word)
                    elif '"' in word and codeWordFound and firstQuotes and not secondQuotes:
                        secondQuotes = True
                        wikiRequest.append(unidecode(str(word).translate(None,'"')))
                    elif firstQuotes and not secondQuotes:
                        wikiRequest.append(unidecode(str(word)))
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
                    wikiArticle, categories = self.wiki.searchwiki(msg,self.convertLanguageCode(language),False)
               
                #print comment.subreddit.display_name
                #make sure people can't ask wikibot about itself, otherwise we could cause an infinite loop of wikibot calls
                if(onReddit and not any(string in msg for string in self.wikibot_names)):
                    comment.reply(wikiArticle)
                    self.already_done['already_done'].append(fullname)
                #if not 'wikibot' in subreddit.lower():
                    #stats section Jan 07, 2014: removed stats section because it was causing errors and people were searching for unrelated queries on Reddit.
                    '''if not self.stats['categories']:
                        self.stats['categories'] = {}
                    if not self.stats['subreddits']:
                        self.stats['subreddits'] = {}
                    if not self.stats['queries']:
                        self.stats['queries'] = []
                    if not self.stats['count']:
                        self.stats['count'] = 0
                    
                    #print 'loaded base dict'
                    #make sure category is in the list
                    if subreddit not in self.stats['categories']:
                        self.stats['categories'][subreddit] = {}
                    if subreddit not in self.stats['subreddits']:
                        self.stats['subreddits'][subreddit] = {}
                    #print stats
                    #add categories to subreddit
                    for cat in categories:
                        try:
                            if cat not in self.stats['categories'][subreddit]:
                                self.stats['categories'][subreddit][cat] = 1
                            else:
                                 self.stats['categories'][subreddit][cat] += 1
                        except:
                            self.stats['categories'][subreddit][cat] = 1
                            print 'exception'
                    #total count
                    try:
                        self.stats['count'] += 1
                    except:
                        self.stats['count'] = 1
                    #individual subreddit count    
                    try:
                        self.stats['subreddits'][subreddit]['count'] += 1
                    except:
                        if not self.stats['subreddits'][subreddit]:
                            self.stats['subreddits'][subreddit] = {}
                        self.stats['subreddits'][subreddit]['count'] = 1
                    #last 10 queries
                    try:
                        self.stats['queries'].insert(0,msg)
                        if len(self.stats['queries']) > 10:
                            self.stats['queries'].pop()
                    except Exception as e:
                        if not self.stats['queries']:
                            self.stats['queries'] = []
                        self.stats['queries']= [msg]
                        print 'creating queries list' + str(e)
                    with open('stats','w+') as statistics:
                        statistics.write(json.dumps(self.stats)+'\n')
                    '''
if __name__ == "__main__":
   bot = WikiBot()
   bot.setUp()
   bot.run()
    