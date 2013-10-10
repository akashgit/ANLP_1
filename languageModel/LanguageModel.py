'''
Created on Sep 28, 2013

@authors: Greta and Akash
'''
from collections import defaultdict
import re
import math
import random
import string
import pickle

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
        self.inverse_dict3 = defaultdict(int)
        self.inverse_dict2 = defaultdict(int)
        self.inverse_dict1 = defaultdict(int)
        self.simple_prob_index = defaultdict(int)
        self.count_of_seen_dict = defaultdict(int)
        self.discount_measure = 0.0

    def pre_processing(self, line):
        line = line.lower()
        line = re.sub(r'[\s]', '$', line)
        line = re.sub(r'[\n]', '#', line)
        line = re.sub(r'[\.]', '%', line)
        return re.sub(r'[^a-z,$#%]+', '', line)
        
    def file2dict(self,filename):
        '''
        Please provide the complete address of the file
        '''
        data_file = open(filename)
        for line in data_file:
            line = self.pre_processing(line)
            for i in range(len(line)):
                if len(line[i:i+3])==3:
                    trigram = line[i:i+3] 
                    self.trigram_dict[trigram] += 1
                if len(line[i:i+2])==2:
                    bigram = line[i:i+2]
                    self.bigram_dict[bigram] += 1
                unigram = line[i]
                self.unigram_dict[unigram] += 1
                
        for trigram in self.trigram_dict:
            self.inverse_dict3[self.trigram_dict[trigram]] += 1 
        for bigram in self.bigram_dict:
            self.inverse_dict2[self.bigram_dict[bigram]] += 1
        for unigram in self.unigram_dict:
            self.inverse_dict1[self.unigram_dict[unigram]] += 1
            
            
                
    def calculateProbability(self,trigram,bigram,d=0):
        if d == 0:
            if self.trigram_dict[trigram] != 0:
                return self.trigram_dict[trigram]/float(self.bigram_dict[bigram])
            else:
                return 0
        else:
            if self.trigram_dict[trigram] != 0:
                return (self.trigram_dict[trigram] - self.discount_measure) /float(self.bigram_dict[bigram])
            else:
                return 0
                
            
    def goodTuring(self, word):
        '''
        Set of all the words that appear once
        '''
        singleton = self.inverse_dict3[1]
        '''
        For unseen trigrams
        '''
        if word not in self.trigram_dict:
            probability_of_unseen = singleton / float(len(self.trigram_dict))
            return probability_of_unseen
        else:
            c = self.trigram_dict[word]
            if self.inverse_dict3[c+1]!=0:
                Nc = self.inverse_dict3[c]
                Nc1 = self.inverse_dict3[c+1] # what about the case when C+1 does not exist.
                count_of_seen = (c + 1) * Nc1 / float(Nc)
            else:    
                count_of_seen = c
            
            probability_of_seen = count_of_seen / float(self.bigram_dict[word[0:2]])
            return probability_of_seen
    
    def discount(self):
        for word in self.trigram_dict:
            if self.trigram_dict[word] > 20:
                d = self.trigram_dict[word] - self.count_of_seen_dict[word]
        self.discount_measure =  d / float(len(self.trigram_dict))
        return self.discount_measure
        
    def beta(self, trigram):
        follow_count = 0
        for word in self.trigram_dict:
            if word[0:2] == trigram[0:2]:
                follow_count += 1
        d = self.discount()
        return d / self.bigram_dict[trigram[0:2]] * follow_count
        
    def continuation_probability(self,word):
        number_of_bigram = 0
        for bigram in self.bigram_dict:
            if bigram == word[0:2]:
                number_of_bigram += 1
        return number_of_bigram/float(len(self.bigram_dict))
        
        
    def kneserNey(self,word):
        return max(self.calculateProbability(word, word[0:2],1),0) + self.beta(word)*self.continuation_probability(word)
    
    def discount_KN(self,nGram,number=0):
        c = self.trigram_dict[nGram] + self.bigram_dict[nGram] + self.unigram_dict[nGram] 
        d1 = 0
        d2 = 0
        d3 = 0
        Y = self.inverse_dict3[1]/float((self.inverse_dict3[1]+(2*self.inverse_dict3[1+1])))
        if c == 1:
            d1 = 1 - (2*Y*self.inverse_dict3[c+1]/self.inverse_dict3[c])
        if c == 2:
            d2 = 2 - (3*Y*self.inverse_dict3[c+1]/self.inverse_dict3[c])
        if c>=3:
            d3 = 3 - (4*Y*self.inverse_dict3[4]/self.inverse_dict3[3])
            
        if number == 1:
            return  1 - (2*Y*self.inverse_dict3[2]/self.inverse_dict3[1])
        elif number == 2:
            return  1 - (2*Y*self.inverse_dict3[3]/self.inverse_dict3[2])
        elif number == 3:
            return  1 - (2*Y*self.inverse_dict3[4]/self.inverse_dict3[3])
        else:
            return d1+d2+d3
#         if len(nGram) == 3:
#             
#             if c == 1:
#                 d1 = 1 - (2*Y*self.inverse_dict3[c+1]/self.inverse_dict3[c])
#             if c == 2:
#                 d2 = 2 - (3*Y*self.inverse_dict3[c+1]/self.inverse_dict3[c])
#             if c>=3:
#                 d3 = 3 - (4*Y*self.inverse_dict3[4]/self.inverse_dict3[3])
#                 
#             if number == 1:
#                 return  1 - (2*Y*self.inverse_dict3[2]/self.inverse_dict3[1])
#             elif number == 2:
#                 return  1 - (2*Y*self.inverse_dict3[3]/self.inverse_dict3[2])
#             elif number == 3:
#                 return  1 - (2*Y*self.inverse_dict3[4]/self.inverse_dict3[3])
#             else:
#                 return d1+d2+d3
#             
#         elif len(nGram) == 2:
#             if c == 1:
#                 d1 = 1 - (2*Y*self.inverse_dict2[c+1]/self.inverse_dict2[c])
#             if c == 2:
#                 d2 = 2 - (3*Y*self.inverse_dict2[c+1]/self.inverse_dict2[c])
#             if c>=3:
#                 d3 = 3 - (4*Y*self.inverse_dict2[4]/self.inverse_dict2[3])
#                 
#             if number == 1:
#                 return  1 - (2*Y*self.inverse_dict2[2]/self.inverse_dict2[1])
#             elif number == 2:
#                 return  1 - (2*Y*self.inverse_dict2[3]/self.inverse_dict2[2])
#             elif number == 3:
#                 return  1 - (2*Y*self.inverse_dict2[4]/self.inverse_dict2[3])
#             else:
#                 return d1+d2+d3
#         
#         else:
#             if c == 1:
#                 d1 = 1 - (2*Y*self.inverse_dict1[c+1]/self.inverse_dict1[c])
#             if c == 2:
#                 d2 = 2 - (3*Y*self.inverse_dict1[c+1]/self.inverse_dict1[c])
#             if c>=3:
#                 d3 = 3 - (4*Y*self.inverse_dict1[4]/self.inverse_dict1[3])
#             
#             
#             if number == 1:
# #                 print 1 - (2*Y*self.inverse_dict1[2]/self.inverse_dict1[1])
#                 return  1 - (2*Y*self.inverse_dict1[2]/self.inverse_dict1[1])
#             elif number == 2:
# #                 print 1 - (2*Y*self.inverse_dict1[3]/self.inverse_dict1[2])
#                 return  1 - (2*Y*self.inverse_dict1[3]/self.inverse_dict1[2])
#             elif number == 3:
# #                 print 1 - (2*Y*self.inverse_dict1[5]/self.inverse_dict1[4])
#                 return  1 - (2*Y*self.inverse_dict1[4]/self.inverse_dict1[3])
#             else:
#                 return d1+d2+d3
        
            
    
    def alpha_high(self,trigram):
        D = self.discount_KN(trigram)
        trigram_count = self.trigram_dict[trigram]
        return (trigram_count-D)/float(self.bigram_dict[trigram[0:2]])
        
    
    def alpha_low_bigram(self,bigram):
        D = self.discount_KN(bigram)
        bigram_history_count = 0
        for trigram in self.trigram_dict:
            if trigram[1:3] == bigram:
                bigram_history_count += 1
        unigram_history_count = 0
        for ngram in self.bigram_dict:
            if len(ngram)>1:
                if ngram[1] == bigram[0]:
                    unigram_history_count += 1
        continuation_probability = (bigram_history_count - D)/float(unigram_history_count)
        return continuation_probability
    
    def alpha_low_unigram(self,unigram):
        D = self.discount_KN(unigram)
        unigram_history_count = 0
        for ngram in self.bigram_dict:
            if len(ngram)>1:
                if ngram[1] == unigram:
                    unigram_history_count += 1
        continuation_probability = (unigram_history_count - D)/float(len(self.unigram_dict))
        return continuation_probability
           
    
    def calc_d_bigram(self,bigram):
        
        n1 = 0
        n2 = 0
        n3 = 0
        sum = 0
        for trigram in self.trigram_dict:
            if trigram[0:2] == bigram:
                sum += 1
            if sum == 0:
                return 0
            if trigram[0:2] == bigram and self.trigram_dict[trigram]==1:
                n1 += 1
            if trigram[0:2] == bigram and self.trigram_dict[trigram]==2:
                n2 += 1
            if trigram[0:2] == bigram and self.trigram_dict[trigram]>=3:
                n3 += 1
                
        return (self.discount_KN(bigram,3)*n3 + self.discount_KN(bigram,2)*n2 + self.discount_KN(bigram,1)*n1) / float(sum)
    
    def calc_d_unigram(self,unigram):
        
        n1 = 0
        n2 = 0
        n3 = 0
        sum = 0
        for bigram in self.bigram_dict:
            if bigram[0] == unigram:
                sum += 1
            if bigram[0] == unigram and self.bigram_dict[bigram]==1:
                n1 += 1
            if bigram[0] == unigram and self.bigram_dict[bigram]==2:
                n2 += 1
            if bigram[0] == unigram and self.bigram_dict[bigram]>=3:
                n3 += 1
        d = (self.discount_KN(unigram,3)*n3 + self.discount_KN(unigram,2)*n2 + self.discount_KN(unigram,1)*n1) / float(sum)        
        return d
    
    def backoff_KN_unigram(self,nGram):
        d = self.calc_d_unigram(nGram)
        return d * self.alpha_low_unigram(nGram[-1])
    
    
    def mod_KN_bigram(self,bigram):
        if self.bigram_dict[bigram] > 0:
            return self.alpha_low_bigram(bigram)
        else:
            return self.backoff_KN_unigram(bigram[1])
    
    def backoff_KN_bigram(self,nGram):
        d = self.calc_d_bigram(nGram)
        if self.mod_KN_bigram(nGram) != 0 and d != 0:
            return d * self.mod_KN_bigram(nGram)
        else:
            return self.backoff_KN_unigram(nGram[1])
    
    def mod_KN(self,trigram):
        if self.trigram_dict[trigram] > 0:
            return self.alpha_high(trigram)
        else:
            return self.backoff_KN_bigram(trigram[1:3])

    
    def add_one(self,trigram):
        p = (self.trigram_dict[trigram] + 1) / float( self.bigram_dict[trigram[0:2]] + 30)
        return p
    
def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

    
def generateOutput(model, seed_bigram):
    weight_list = list()
    term_list = list()
    
#     print 'the seed_bigram is ',seed_bigram
    for trigram in model.trigram_dict:
        if seed_bigram == '. ':
                print 'fuck off', trigram
        if trigram[0:2] == seed_bigram:
            knp = model.goodTuring(trigram)
            weight_list.append(knp)
            term_list.append(trigram[2])
#     print 'the seed_bigram is',len(seed_bigram),seed_bigram       
    index = weighted_choice(weight_list)
    return term_list[index]

def randomOutput(model, seed_bigram):
    answer = seed_bigram
    for i in range(500):
        answer += generateOutput(model, seed_bigram)
        seed_bigram = answer[-2:]
    answer = answer.replace('$',' ')
    answer = answer.replace('#','\n')
    answer = answer.replace('%','.')
    return answer.replace('$',' ')

def calcPerplexity(testFile,model):
    n = 0
    test_model = LanguageModel()
    test_model.file2dict(testFile)
    for letter in test_model.unigram_dict:
        n += test_model.unigram_dict[letter]
    answer = 1.0
    for trigram in test_model.trigram_dict:
        for i in range(test_model.trigram_dict[trigram]):
            p = 1/float(model.add_one(trigram))
            answer = answer * math.pow(abs(p), (1/float(n)) )

    return answer

def write_model(model):
    language_model = open('language_model.txt','a')
    model_dict = defaultdict(int)
    character_set = string.ascii_lowercase+'$'+'#'+'%'
    for i in character_set:
        for j in character_set:
            for k in character_set:
                word = i+j+k
                probability = model.goodTuring(word)
                model_dict[word] = probability
    pickle.dump(model_dict, language_model)
                   
            
def main():
    model = LanguageModel();
    model.file2dict('../data/training.en')
    print randomOutput(model,'ta')
    print calcPerplexity('../data/test',model)
#     write_model(model)



if __name__ == "__main__":
    main()
        
