import wikipedia
import requests

class Wiki(object):

    def searchwiki(self, input, lang):
        response = ""
        term = input.encode('ascii', 'ignore')
        
        wikipedia.set_lang(lang)
        try:
            wikipedia.search(term)
        except requests.exceptions.ConnectionError:
            wikipedia.set_lang("en")
        
        try:
            results = wikipedia.page(term)
        except wikipedia.exceptions.DisambiguationError as e:
            if len(e.options) >= 6:
                response = response + "Your query " + term + " to WikiBot returned a disambiguation page. Here are the top 5 pages:  \n"
            else:
                response = response + "Your query " + term + " to WikiBot returned a disambiguation page. Here are the pages:  \n"
            count = 0
            
            for option in e.options:
                count += 1
                if count >= 6:
                    break  
                try:
                    x = wikipedia.page(option.encode('ascii', 'ignore'))
                except wikipedia.exceptions.PageError as t:
                    response = response + option + ": Sorry couldn't fetch the link.  \n"
                except wikipedia.exceptions.DisambiguationError as t:
                    response = response + option + ": Sorry couldn't fetch the link.  \n"
                else:
                    response = response + "[" + x.title + "](" + self.formaturl(x.url) + "): " + wikipedia.summary(option.encode('ascii', 'ignore'), sentences=1) + "  \n"
                    
            response = self.wikifooter(response)
            return response    
        except wikipedia.exceptions.PageError as e:
            response = response + "Sorry, WikiBot can not find a page on \"" + term + "\"."
            response = self.wikifooter(response)
            return response
        
        summary = (results.summary[:9000] + '..') if len(results.summary) > 9000 else results.summary
        response = response + "Here is what WikiBot found on \"" + term + "\":\n\n" + results.title +"  \n" + summary + "\n\n" + "Link to article [" + results.title + "](" + self.formaturl(results.url) + ")\n\n"
        
        response = self.recommender(results, response, term)
        
        response = self.wikifooter(response)
        
        return response
    
    def recommender(self, page, response, term):
        recs = wikipedia.search(term,results=4)
        if len(recs) > 1:
            response = response + "Here are other related articles:  \n"
            for rec in recs:
                if rec != page.title:
                    x = wikipedia.page(rec)
                    response = response + "[" + x.title + "](" + self.formaturl(x.url) + ")  \n"

        return response
    
    def formaturl(self, url):
        url = url.replace("(","\(")
        url = url.replace(")","\)")
        return url
    
    def wikifooter(self, input):
        input = input + "\n\nFor more information on WikiBot, visit [wiki-bot.net](http://www.wiki-bot.net/)."
        return input.encode('ascii', 'ignore')
        
if __name__ == "__main__":
    search = Wiki()
    print search.searchwiki("Texas A&M", "en")
                