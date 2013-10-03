'''
Created on Sep 28, 2013

@author: Akash Srivastava S1362249
'''
from collections import defaultdict

class LanguageModel():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.trigram_dict = defaultdict(int)
        self.bigram_dict = defaultdict(int)
        self.unigram_dict = defaultdict(int)
        self.inverse_dict = defaultdict(int)
        self.simple_prob_index = defaultdict(int)
        

    def pre_processing(self, line):
        line =  re.sub(r'[a-z\s\,.]', '', line.lower())
        
    def file2dict(self,filename):
        '''
        Please provide the complete address of the file
        '''
        data_file = open(filename)
        for line in data_file:
            line = line.split(' ')
            for i in range(len(line)):
                if i < len(line)-3:
                    trigram = line[i:i+3]
            trigram = str(trigram).strip('[]') 
                    self.trigram_dict[trigram] += 1
                if i < len(line)-2:
                    bigram = line[i:i+2]
            bigram = str(bigram).strip('[]')
                    self.bigram_dict[bigram] += 1
                unigram = line[i]
        unigram = str(unigram).strip('[]')
                self.unigram_dict[unigram] += 1
                
    for trigram in self.trigram_dict:
            self.inverse_dict[self.trigram_dict[trigram]] += 1 
            
                
    def calculateProbability(self,trigram,bigram):
        if self.trigram_dict[trigram] != 0:
            return self.trigram_dict[trigram]/float(self.bigram_dict[bigram])
        else:
            return 0
            
    def goodTuring(self, word):
        singleton = self.inverse_dict[1]
        
        if word not in self.trigram_dict:
            probability_of_unseen = singleton / float(len(self.trigram_dict))
            return probability_of_unseen
        
        c = self.trigram_dict[word]
        Nc = self.inverse_dict[c]
        Nc1 = self.inverse_dict[c+1]
        count_of_seen = (c + 1) * Nc1 / float(Nc)
        probability_of_seen = float(count_of_seen) / float(len(self.trigram_dict))
        return probability_of_seen
        
    def kneserNey(self,word):
        for bigram in self.bigram_dict:
            second_term = bigram.split(' ')[1]
            if second_term == word:
                
            

def main():
  model = LanguageModel();
  model.file2dict('training.en')
  for word in model.trigram_dict:
      print word,'\t', model.trigram_dict[word],'\t', model.goodTuring(word)


if __name__ == "__main__":
  main()
        
