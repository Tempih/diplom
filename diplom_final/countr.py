#!/usr/bin/env python
import sys
import os
import random
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
k = []
def gen_arr(k):
    z = random.randint(0, len(word_set)
    if z in k:
        po(k)
    else:
        k.append(z)
lists = []
for line in sys.stdin:
    lists.extend(eval(line))
word_set = set()
for i in lists:
    for word in i:
        i[i.index(word)] = i[i.index(word)].lower()
        if '@' in word:
            i.remove(word)
        if '--' in word:
            i.remove(word)
        if ':' in word:
            i[i.index(word)] = i[i.index(word)].replace(':','')
        if '(' in word:
            i[i.index(word)] = i[i.index(word)].replace('(','')
        if ')' in word:
            i[i.index(word)] = i[i.index(word)].replace(')','')
        if '~' in word:
            i[i.index(word)] = i[i.index(word)].replace('~','')
        if ' ' in word:
            i[i.index(word)] = i[i.index(word)].replace(' ','')
        if '#' in word:
            i[i.index(word)] = i[i.index(word)].replace('#','')
        if '[' in word:
            i[i.index(word)] = i[i.index(word)].replace('[','')
        if ']' in word:
            i[i.index(word)] = i[i.index(word)].replace(']','')
        if '?' in word:
            i[i.index(word)] = i[i.index(word)].replace('?','')
        if '.' == word[-1]:
            i[i.index(word)] = i[i.index(word)].replace('.','')
        if ',' in word:
            i[i.index(word)] = i[i.index(word)].replace(',','')
        if '!' in word:
            i[i.index(word)] = i[i.index(word)].replace('!','')
        i[i.index(word)] = lemmatizer.lemmatize(i[i.index(word)])
    word_set = word_set.union(set(i))
check = [
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves"]
for stop_word in check:
    if stop_word in word_set:
        word_set.remove(stop_word)
random.seed(42)
if len(word_set) > 3000:
    for i in range(3000):
        po(k)
    main_word = []
    word_set = list(word_set)
    for i in k:
        main_word.append(word_set[i])
print(main_word)
