class TextAnalyzer(object):
    inputString = ""
    def __init__ (self, inputString):
          # remove punctuation
        self.inputString = inputString.replace('.','').replace('!','').replace('?','').replace(',','').lower()
  
        
    def freqAll(self):        
        # split text into words
        fmt_list = self.inputString.split(' ')
        words_dict = {}
        
        # Create dictionary
        for word in set(fmt_list):
            if word in words_dict.keys():
                words_dict[word] +=1
            else:
                words_dict[word] = 1
            #words_dict[word] = words_dict.count(word)  //we could have only this instructions below the for loop
        return words_dict


    
    def freqOf(self,word):
        fmt_list = self.inputString.split(' ')
        return fmt_list.count(word)
    ## melhor seria usar a funçao freqAll que devolve o dicionario e dai ver se o
    ## word no paramentro existe e dai, returnar o seu valor,se nao devolve 0