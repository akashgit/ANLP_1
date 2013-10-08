'''
Created on Sep 28, 2013

@authors: Greta and Akash
'''
from collections import defaultdict
import re
import math

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
        self.count_of_seen_dict = defaultdict(int)
        self.discount_measure = 0.0

    def pre_processing(self, line):
        line = re.sub(r'[/s ]', '$', line.lower())
        return re.sub(r'[^ a-z $ ]', '', line.lower())
        
    def file2dict(self,filename):
        '''
        Please provide the complete address of the file
        '''
        data_file = open(filename)
        for line in data_file:
#             line = line.split(' ')
            line = self.pre_processing(line)
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
            for bigram in self.bigram_dict:
                self.inverse_dict[self.bigram_dict[bigram]] += 1
            for unigram in self.unigram_dict:
                self.inverse_dict[self.unigram_dict[unigram]] += 1
            
                
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
        singleton = self.inverse_dict[1]
        
        if word not in self.trigram_dict:
            probability_of_unseen = singleton / float(len(self.trigram_dict))
            return probability_of_unseen
        
        c = self.trigram_dict[word]
        Nc = self.inverse_dict[c]
        Nc1 = self.inverse_dict[c+1] # what about the case when C+1 does not exist.
        count_of_seen = (c + 1) * Nc1 / float(Nc)
        probability_of_seen = float(count_of_seen) / float(len(self.trigram_dict))
#         print 'word= ', word, '\t', 'C= ',c,'\t', 'Nc = ',Nc,'\t', 'Nc1 = ', Nc1,'\t', 'Count of Seen = ',count_of_seen
        self.count_of_seen_dict[word] = count_of_seen
        return count_of_seen
    
    def discount(self):
        for word in self.trigram_dict:
            if self.trigram_dict[word] > 20:
                d = self.trigram_dict[word] - self.count_of_seen_dict[word]
#         print d / float(len(self.trigram_dict))
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
        d1 = 0
        d2 = 0
        d3 = 0
        if len(nGram) == 3:
            c = self.trigram_dict[nGram]
        elif len(nGram) == 2:
            c = self.bigram_dict[nGram]
        else:
            c = self.unigram_dict[nGram]
        Y = self.inverse_dict[1]/float((self.inverse_dict[1]+(2*self.inverse_dict[1+1])))
        if self.inverse_dict[c] != 0:
            if c == 1:
                d1 = 1 - (2*Y*self.inverse_dict[c+1]/self.inverse_dict[c])
            if c == 2:
                d2 = 2 - (3*Y*self.inverse_dict[c+1]/self.inverse_dict[c])
            #will never run since there are no nGrams with more than 3 letters.
            if c>=3:
                d3 = 3 - (4*Y*self.inverse_dict[c+1]/self.inverse_dict[c])
            if number == 1:
                return  1 - (2*Y*self.inverse_dict[2]/self.inverse_dict[1])
            elif number == 2:
                return  1 - (2*Y*self.inverse_dict[3]/self.inverse_dict[2])
            elif number == 3:
                return  1 - (2*Y*self.inverse_dict[4]/self.inverse_dict[3])
            else:
                return d1+d2+d3
        else:
            return 0
        
            
    
    def alpha(self,nGram):
        D = self.discount_KN(nGram)
        if len(nGram) == 3:
            ngram_count = self.trigram_dict[nGram]
            return (ngram_count-D)/float(self.bigram_dict[nGram[0:2]])
        elif len(nGram) == 2:
            ngram_count = self.bigram_dict[nGram]
            return (ngram_count-D)/float(self.unigram_dict[nGram[0]])
        else:
            ngram_count = self.unigram_dict[nGram]
            return (ngram_count-D)/float(len(self.unigram_dict))
        
    
    def calc_d(self,nGram):
        counter3 = 0
        counter2 = 0
        n1 = 0
        n2 = 0
        n3 = 0
        sum = 0
        
#         print nGram[2], self.discount_KN(nGram[1:3]), self.discount_KN(nGram[2]), counter3, counter2, sum
        for trigram in self.trigram_dict:
            sum += self.trigram_dict[trigram]
            if trigram[2] == nGram[2] and self.trigram_dict[trigram]==1:
                n1 += 1
            if trigram[2] == nGram[2] and self.trigram_dict[trigram]==2:
                n2 += 1
            if trigram[2] == nGram[2] and self.trigram_dict[trigram]>=3:
                n3 += 1
                
        return (self.discount_KN(nGram,3)*n3 + self.discount_KN(nGram,2)*n2 + self.discount_KN(nGram,1)*n1) / float(sum)
    
    def backoff_KN(self,nGram):
        d = self.calc_d(nGram)
#         print d
        if self.mod_KN(nGram[1:3]) != 0:
#             print 'bigram something',self.mod_KN(nGram[1:3])
            return d * self.mod_KN(nGram[1:3])
        else:
#             print 'unigram something ',d * self.mod_KN(nGram[2])
            return d * self.mod_KN(nGram[2])
    
    def mod_KN(self,nGram):
        if len(nGram)==3:
            if self.trigram_dict[nGram] > 0:
                return self.alpha(nGram)
            else:
                return self.backoff_KN(nGram)
        if len(nGram)==2:
#             nGram = nGram[1:3]
            if self.bigram_dict[nGram] > 0:
                return self.alpha(nGram)
            else:
                return self.backoff_KN(nGram)
        if len(nGram)==1:
#             nGram = nGram[3:4]
            if self.unigram_dict[nGram] > 0:
                return self.alpha(nGram)
            else:
                return self.backoff_KN(nGram)
    
def generateOutput(model, seed_bigram, iteration=0, answer=''):
    iteration += 1
    max_prob = 0.0
    for trigram in model.trigram_dict:
        if trigram[0:2] == seed_bigram:
            knp = model.kneserNey(trigram)
            if knp > max_prob:
                max_prob = knp
                max_prob_trigram = trigram
    answer += max_prob_trigram
#     answer = answer.replace('$',' ')
#     print max_prob_trigram, max_prob_trigram[1:3]
    if iteration < 10:
        answer = generateOutput(model, max_prob_trigram[1:3], iteration, answer)
    return answer

def calcPerplexity(testFile,model):
    n = 0
    p_total = 0.0
    test_model = LanguageModel()
    test_model.file2dict(testFile)
    for letter in test_model.unigram_dict:
        n += test_model.unigram_dict[letter]
    for trigram in test_model.trigram_dict:
#         print 'PP', model.mod_KN(trigram)
        p_total += math.log(abs(model.mod_KN(trigram)))
    entropy = p_total/float(n)
    print 'p_total is: ' ,p_total
    return math.pow(2, entropy)
                   
            
def main():
    model = LanguageModel();
    model.file2dict('../data/training.en')
    for word in model.trigram_dict:
        model.goodTuring(word)
    model.discount()
    
    
    print 'PP is: ', calcPerplexity('../data/test',model)
    
#     for word in model.trigram_dict:
#         model.goodTuring(word)
#         print 'The Kneser-Ney P() for',word,' is : ', model.kneserNey(word)
#     print generateOutput(model,'th')
#         if model.trigram_dict[word] < 10:
#             print word,'\t', model.trigram_dict[word],'\t', model.goodTuring(word)


if __name__ == "__main__":
    main()
        
