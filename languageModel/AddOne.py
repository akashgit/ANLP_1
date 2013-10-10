import re
from collections import defaultdict
import math

trigrams = defaultdict(int)
bigrams = defaultdict(int)
unigrams = defaultdict(int)

trigrams_test = defaultdict(int)
bigrams_test = defaultdict(int)
unigrams_test = defaultdict(int)


def preprocessing(line):
#     line = re.sub(r'[/s ]', '$', line.lower())
    line = line.lower()
    return re.sub(r'[^a-z]+', '', line.strip())

def generate_model(filename):
    dataFile = open(filename)
    text = ""
    for line in dataFile:
        line = preprocessing(line)
        text += line

    for i in range(0,len(text) - 2):
        if text[i:i+3]=='zau':
            word = text[i:i+3]
        trigrams[text[i:i+3]] += 1
    for i in range(0,len(text) - 1):
        bigrams[text[i:i+2]] += 1
    for i in range(0,len(text)):
        unigrams[text[i]] += 1
            
def generate_test_model(filename):
    dataFile = open(filename)
    text = ""
    for line in dataFile:
        line = preprocessing(line)
        text += line
    for i in range(0,len(text) - 2):
        trigrams_test[text[i:i+3]] += 1
    for i in range(0,len(text) - 1):
        bigrams_test[text[i:i+2]] += 1
    for i in range(0,len(text)):
        unigrams_test[text[i]] += 1
            
def add_one(trigram):
    p =  (trigrams[trigram] + 1) / float( bigrams[trigram[0:-1]] + 26 )
#     if trigram == 'sch':
#     print trigram, p

    return p

def perplexity(test_file, language_model):
    n = 0
    product = 1
    generate_test_model(test_file)
    for unigram in unigrams_test:
        n += unigrams_test[unigram]
    print len(trigrams_test)
    for trigram in trigrams_test:
        for i in range(trigrams_test[trigram]):
            p = add_one(trigram)
            p = (1/p)**(1/float(n))
            product = product * p
    return product


def main():
    language_model = generate_model('../data/training.en')
    print 'perplexity = ', perplexity('../data/test',language_model)

if __name__ == "__main__":
    main()
        
        