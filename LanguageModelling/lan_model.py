# Goal:
# Apply different language models like unigram, bigram, trigram on the given twitter corpus and codemixed corpus.
# Find CMI and Perplexity for each of the above models.
# Compare perplexity and analyse the best among them.

# Steps:
# Preprocess the data (Apply tokenization and stemming).
# Store all the words(V) in a dictionary with unique id's and their frequencies in a list.
# Create a V*V matrix with all bigram totalLiness.
# Apply add-one smoothing on the matrix.
# For every sentence in the corpus, find probabilities P( word(n)|word(n-1) ) of each word in the sequence and thereby find the perplexity of each sentence.
# Take the average of all the perplexities.
# Analyse the perplexities of different models.

# Variables:
# wordDict: Dictionary which stores all the words.
# index: To give unique id's to every word in the dictionary.
# V: Vocabulary size.

# Code
import numpy as np
import nltk
import os
import sys
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize
from bs4 import BeautifulSoup
import json
import re
porter = PorterStemmer()

# Put words in dictionary
index=0		# Index of word in dictionary
totalLines=0		# Total number of lines
tokens=0	# Total number of words in the corpus
V=0
V_tri=0
matrix=np.zeros((1,1))
wordDict = {}
bigram_perplex=[]
trigram_dict={}
secondDict={}

def get_count():
	global index
	return index

def createMatrix(row,col):
	global matrix
	matrix = np.zeros((row,col))

def putInDict(filename):
	global totalLines, tokens, index
	with open(filename) as file:
		for line in file:
			totalLines+=1
			# line = "My name is Abhishek and the name of the boy who was standing there is not Abhishek"
			listOfWords = wordpunct_tokenize(line)
			tokens = tokens + len(listOfWords)
			for word in listOfWords:
				word = porter.stem(word)
				if word in wordDict:
					wordDict[word][1]+=1
				else:
					wordDict[word] = [index, 1]
					index+=1
	print wordDict

def unigramPerplexity():
	global filename, totalLines, tokens, index
	with open(filename) as file:
		perplexities=[]
		for line in file:
			listOfWords = wordpunct_tokenize(line)
			l = len(listOfWords)
			prob=[]
			for i in range(l):
				word=listOfWords[i]
				prob.append(wordDict[word][1]/float(tokens))
			per=1
			for p in prob:
        			per = per*p
        		per=1/float(per)
        		perplexities.append(pow(per, 1/float(l)))
	PP=0
	for i in perplexities:
		PP=PP+i
	PP=PP/float(len(perplexities))
	return PP

def createBigram():
	global filename, totalLines, tokens, index
	with open(filename) as file:
		for line in file:
			listOfWords = wordpunct_tokenize(line)
			l = len(listOfWords)
			if l!=0:
				word = listOfWords[0]
				matrix[V][wordDict[word][0]]+=1	
			for i in range(l-1):
				word = listOfWords[i]
				next_word = listOfWords[i+1]
				matrix[wordDict[word][0]][wordDict[next_word][0]]+=1
	print wordDict
	print matrix
	
def bigramPerplexity():
	global filename, totalLines, tokens, index
	with open(filename) as file:
		perplexities=[]
		for line in file:
			listOfWords = wordpunct_tokenize(line)
			l = len(listOfWords)
			prob=[]
			if l!=0:
				wo