'''
Created on Sep 25, 2012

@author: leandro
'''

from scipy import *
import matplotlib.pyplot as plt
import sys


def rankWords(filename):
    
    #Open a file and read its contents
    file = open(filename)    
    data = file.read()
    
    #split the text in words using defualt parameters of
    #function split (we could pass more parameters, regex)
    words = data.split()
    
    #create a dictionary that will contain an entry for
    #each word, and the entry value will correspond to the
    #ocurrence of the given word
    dictionary = {}
    for word in words:        
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
        
    #return a list of words sorted by the key values of
    #the dictionary. Since the key values of the dictionary
    #are the number of ocurrences, this will yield a list
    #of words sorted by frequency of ocurrence
    
    #http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
    sortedwords = sorted(dictionary, key=dictionary.get) 
        
    #for each word in the sorted list, we want to store
    #how many times the word occurs. So we check in the
    #dictionary and store the result in a new list called
    #histogram
    
    histogram = []
    for word in sortedwords:        
        histogram.append(dictionary[word])
    
    plt.xlabel('Rank')
    plt.ylabel('Number of ocurrences')
    plt.plot(histogram)
    plt.plot(histogram, '.')
    plt.show()

def countWords(filename):    
    file = open(filename)    
    data = file.read()
    words = data.split()
    print 'there are ', len(words), ' words in this text file'

if (len(sys.argv) > 1):
    filename = sys.argv[1]    
    countWords(filename)
    rankWords(filename)