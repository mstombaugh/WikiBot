import requests
import wikipedia
import subRec as subRec
from unidecode import unidecode

class Wiki(object):

    def __init__(self):
        self.lang = "en"
        self.site = False
       
    def searchwiki(self, input, lang, site):
        response = ''
        term = unidecode(input)
        self.lang = lang
        categories = []
        self.site = site
        
        wikipedia.set_lang(lang)

        try:
            wikipedia.page(term)
        except requests.exceptions.ConnectionError:
            wikipedia.set_lang("en")
            lang = "en"
        except Exception as e:
            pass

        try:
            results = wikipedia.page(term, extraLevel = True)
            title = results.title
            summary = (results.summary[:9000] + '...') if len(results.summary) > 9000 else results.summary
            if site:
                response = response + "<p>Here is what WikiBot found on" + " \"" + term + "\":</p><p><b>" + title +"</b></p><p style=\"text-indent:50px;\">" + summary + "</p>" + "<p>Link to article: <a href=\"" + results.url + "\">" + title + "</a></p>"
            else:
                response = response + "Here is what WikiBot found on" + " \"" + term + "\":\n\n**" + results.title +"**  \n> " + summary + "\n\n" + "Link to article" + " [" + results.title + "](" + self.formaturl(results.url) + ")\n\n"
            
            response = self.recommender(title, response)
            
            categories = results.categories
            
            response = self.subRecommender(response, categories)
            
            response = self.wikifooter(response)
            

        except wikipedia.exceptions.DisambiguationError as e:
            response=''
            if len(e.options) >= 6:
                if site:
                    response = response + "Your query" + " \"" + term + "\" " + "to WikiBot returned a disambiguation page. Here are the top 5 pages:" + "<br><ul>"
                else:
                    response = response + "Your query" + " \"" + term + "\" " + "to WikiBot returned a disambiguation page. Here are the top 5 pages:" + "  \n\n"
            else:
                if site:
                    response = response + "Your query" + " \"" + term + "\" " + "to WikiBot returned a disambiguation page. Here are the pages:" + "<br><ul>"
                else:
                    response = response + "Your query" + " \"" + term + "\" " + "to WikiBot returned a disambiguation page. Here are the pages:" + "  \n\n"
            count = 0
            
            for option in e.options:
                count += 1
                if count >= 6:
                    break  
                try:
                    x = wikipedia.page(unidecode(option))
                except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                    if site:
                        response = response + "<li>" + option + ": Sorry couldn't fetch the link." + "</li>"
                    else:
                        response = response + "* " + option + ": Sorry couldn't fetch the link." + "  \n"
                else:
                    if site:
                        response = response + "<li><a href=\"" + x.url + "\">" + x.title + "</a>: " + wikipedia.summary(unidecode(option), sentences=1) + "</li>"
                    else:
                        response = response + "* [" + x.title + "](" + self.formaturl(x.url) + "): " + wikipedia.summary(unidecode(option), sentences=1) + "  \n"
             
            if site:
                response = response + "</ul>"
                
            response = self.wikifooter(response)  
            
        except wikipedia.exceptions.PageError as e:
            response = response + "Sorry, WikiBot can not find a page on" + " \"" + term + "\"."
            response = self.wikifooter(response)
         
        return response, categories
        
    def recommender(self, title, response):
        recs = wikipedia.search(title,results=4)
        if len(recs) > 1:
            if self.site:
                response = response + "<p>Here are other related articles:</p><ul>"
            else:
                response = response + "Here are other related articles:" + "  \n"
            for rec in recs:
                if rec != title:
                    try:
                        x = wikipedia.page(rec)
                        if self.site:
                            response = response + "<li><a href=\"" + x.url + "\">" + x.title + "</a></li>"
                        else:
                            response = response + "[" + x.title + "](" + self.formaturl(x.url) + ")  \n"
                    except:
                        pass
            if self.site:
                response = response + "</ul>"
            
        return response
        
    def subRecommender(self, response, categories):
        subs = subRec.subRec(categories)
        
        if len(subs) > 0:
            if self.site:
                response = response + "<p>Based on what kinds of articles subreddits search for with WikiBot, here are related subreddits:</p></ul>"
                for sub in subs:
                    response = response + '<li><a href="http://www.reddit.com/r/' + sub[0] + '">/r/' + sub[0] + "</a> based on similar categories like \"" + sub[1][0][0].replace("_"," ") + "\"</li>"
                response = response + "</ul>"
            else:
                response = response + "\n\nBased on what kinds of articles subreddits search for with WikiBot, here are related subreddits:  \n"
                for sub in subs:
                    response = response + "/r/" + sub[0] + " based on similar categories like \"" + sub[1][0][0].replace("_"," ") + "\"  \n"
                    
        return response
    
    def formaturl(self, url):
        url = url.replace("(","\(")
        url = url.replace(")","\)")
        return url
    
    def wikifooter(self, input):
        if self.site:
            return unidecode(input)
        else:
            input = input + "\n\nFor more information on WikiBot, visit [wiki-bot.net](http://www.wiki-bot.net/)."
        return unidecode(input)
        
if __name__ == "__main__":
    search = Wiki()
    output =  search.searchwiki("oxyhydrogen", "en", False)
    print output[0]
              
