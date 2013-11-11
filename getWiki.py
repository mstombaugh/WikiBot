import wikipedia

class Wiki(object):

    def searchwiki(self, input):
        response = ""
        term = input.encode('ascii', 'ignore')
        
        try:
            results = wikipedia.page(term)
        except wikipedia.exceptions.DisambiguationError as e:
            if len(e.options) >= 6:
                response = response + "Your query to WikiBot returned a disambiguation page. Here are the top 5 pages:  \n"
            else:
                response = response + "Your query to WikiBot returned a disambiguation page. Here are the pages:  \n"
            count = 0
            
            for option in e.options:
                count += 1
                if count >= 6:
                    break
                try:
                    x = wikipedia.page(option.encode('ascii', 'ignore'))
                except wikipedia.exceptions.PageError as t:
                    response = response + x.title +"  \n"
                except wikipedia.exceptions.DisambiguationError as t:
                    response = response + x.title +"  \n"
                else:
                    response = response + "[" + x.title + "](" + str(x.url) + "): " + wikipedia.summary(option.encode('ascii', 'ignore'), sentences=1) + "  \n"
                    
            response = self.wikifooter(response)
            return response    
        except wikipedia.exceptions.PageError as e:
            response = response + "Sorry, WikiBot can not find a page on \"" + term + "\"."
            response = self.wikifooter(response)
            return response
        
        summary = (results.summary[:9000] + '..') if len(results.summary) > 9000 else results.summary
        response = response + "Here is what WikiBot found on \"" + term + "\":\n\n" + results.title +"  \n" + summary + "\n\n" + "Link to article [" + results.title + "](" + str(results.url) + ")"
        
        response = self.wikifooter(response)
        return response
    
    
    def wikifooter(self, input):
        input = input + "\n\nFor more information on WikiBot, visit [wiki-bot.net](http://www.wiki-bot.net/)."
        return input.encode('ascii', 'ignore')
        
if __name__ == "__main__":
    search = Wiki()
    print search.searchwiki("Barack Obama")
                