#import wikipedia
import requests
import wikipedia
from translate import Translator

class Wiki(object):

    def __init__(self):
        self.transOn = False
        self.lang = "en"
        if self.transOn:
            self.translator = Translator('94e6a5a0-a63f-41d3-b894-91404be2bdad', 'sontKet36l8KSU5WP7YOYEUUbzHVoEnpo+r7G5ZDFNU')
        
    def searchwiki(self, input, lang):
        response = ''
        term = input.encode('ascii', 'ignore')
        self.lang = lang
        categories = []
        
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
            response = response + self.trans("Here is what WikiBot found on") + " \"" + term + "\":\n\n**" + results.title +"**  \n> " + summary + "\n\n" + self.trans("Link to article") + " [" + results.title + "](" + self.formaturl(results.url) + ")\n\n"
            
            response = self.recommender(results, response, term)
            
            response = self.wikifooter(response)
            
            categories = results.categories
            
        except wikipedia.exceptions.DisambiguationError as e:
            response=''
            if len(e.options) >= 6:
                response = response + self.trans("Your query") + " \"" + term + "\" " + self.trans("to WikiBot returned a disambiguation page. Here are the top 5 pages:") + "  \n\n"
            else:
                response = response + self.trans("Your query") + " \"" + term + "\" " + self.trans("to WikiBot returned a disambiguation page. Here are the pages:") + "  \n\n"
            count = 0
            
            for option in e.options:
                count += 1
                if count >= 6:
                    break  
                try:
                    x = wikipedia.page(option.encode('ascii', 'ignore'))
                except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
                    response = response + "* " + option + ": " + self.trans("Sorry couldn't fetch the link.") + "  \n"
                else:
                    response = response + "* [" + x.title + "](" + self.formaturl(x.url) + "): " + wikipedia.summary(option.encode('ascii', 'ignore'), sentences=1) + "  \n"
                    
            response = self.wikifooter(response)  
            
        except wikipedia.exceptions.PageError as e:
            response = response + self.trans("Sorry, WikiBot can not find a page on") + " \"" + term + "\"."
            response = self.wikifooter(response)
         
        if len(categories) == 0:
            return (response, None)
        else:
            return response, categories
        
    def recommender(self, page, response, term):
        recs = wikipedia.search(term,results=4)
        if len(recs) > 1:
            response = response + self.trans("Here are other related articles:") + "  \n"
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
        input = input + "\n\n" + self.trans("For more information on WikiBot, visit") + " [wiki-bot.net](http://www.wiki-bot.net/)."
        return input.encode('ascii', 'ignore')
        
    def trans(self,string):
        if self.transOn:
            try:
                return self.translator.translate(string,self.lang)
            except Exception as e:
                print e
                return string
        else:
            return string
        
if __name__ == "__main__":
    search = Wiki()
    output =  search.searchwiki("Bowen Loftin", "en")
    print output[0]
    print output[1]
                