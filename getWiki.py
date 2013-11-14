#import wikipedia
import requests
import wikipedia

class Wiki(object):

    def __init__(self):
        self.lang = "en"
        self.site = False
       
    def searchwiki(self, input, lang, site):
        response = ''
        term = input.encode('ascii', 'ignore')
        self.lang = lang
        categories = []
        self.site = site
        
        wikipedia.set_lang(lang)

        try:
            wikipedia.page(term)
        except requests.exceptions.ConnectionError:
            wikipedia.set_lang("en")
            lang = "en"
        except:
            pass

        try:
            results = wikipedia.page(term)
            summary = (results.summary[:9000] + '...') if len(results.summary) > 9000 else results.summary
            if site:
                response = response + "Here is what WikiBot found on" + " \"" + term + "\": <br><b>" + results.title +"</b><br>" + summary + "<br>" + "Link to article: <a href=\"" + results.url + "\">" + results.title + "</a><br>"
            else:
                response = response + "Here is what WikiBot found on" + " \"" + term + "\":\n\n**" + results.title +"**  \n> " + summary + "\n\n" + "Link to article" + " [" + results.title + "](" + self.formaturl(results.url) + ")\n\n"
            
            response = self.recommender(results, response)
            
            response = self.wikifooter(response)
            
            if not site:
                categories = results.categories
            
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
                    x = wikipedia.page(option.encode('ascii', 'ignore'))
                except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                    if site:
                        response = response + "<li>" + option + ": Sorry couldn't fetch the link." + "</li>"
                    else:
                        response = response + "* " + option + ": Sorry couldn't fetch the link." + "  \n"
                else:
                    if site:
                        response = response + "<li><a href=\"" + x.url + "\">" + x.title + "</a>: " + wikipedia.summary(option.encode('ascii', 'ignore'), sentences=1) + "<li>"
                    else:
                        response = response + "* [" + x.title + "](" + self.formaturl(x.url) + "): " + wikipedia.summary(option.encode('ascii', 'ignore'), sentences=1) + "  \n"
             
            if site:
                response = response + "</ul>"
                
            response = self.wikifooter(response)  
            
        except wikipedia.exceptions.PageError as e:
            response = response + "Sorry, WikiBot can not find a page on" + " \"" + term + "\"."
            response = self.wikifooter(response)
         
        return response, categories
        
    def recommender(self, page, response):
        recs = wikipedia.search(page.title,results=4)
        if len(recs) > 1:
            if self.site:
                response = response + "Here are other related articles:<br><ul>"
            else:
                response = response + "Here are other related articles:" + "  \n"
            for rec in recs:
                if rec != page.title:
                    x = wikipedia.page(rec)
                    if self.site:
                        response = response + "<li><a href\"" + x.url + "\">" + x.title + "</a></li>"
                    else:
                        response = response + "[" + x.title + "](" + self.formaturl(x.url) + ")  \n"
            if self.site:
                response = response + "</ul>"
            
        return response
    
    def formaturl(self, url):
        url = url.replace("(","\(")
        url = url.replace(")","\)")
        return url
    
    def wikifooter(self, input):
        if self.site:
            return input.encode('ascii', 'ignore')
        else:
            input = input + "\n\nFor more information on WikiBot, visit [wiki-bot.net](http://www.wiki-bot.net/)."
        return input.encode('ascii', 'ignore')
        
if __name__ == "__main__":
    search = Wiki()
    output =  search.searchwiki("Texas A&M", "en", True)
    print output[0]
    print output[1]
                