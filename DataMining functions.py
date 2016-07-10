
# coding: utf-8

# In[31]:

#imports
import re
import copy
import numpy
import codecs
import collections
import nltk
from stop_words import get_stop_words
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans


# In[32]:

def opening(filename):
    """opens a file for read and returns the list of lines 
    
    Arguments 
    filename -- File to read from 
    """
    with open (filename, 'rb') as f:
        lines = f.readlines()
    return lines


# In[33]:

def opening_fullfile(filename):
    """opens a file for read and returns the whole file
    
    Arguments 
    filename -- File to read from 
    """
    with open (filename, 'rb') as f:
        lines = f.read()
    print type(lines)
    return lines


# In[79]:

def writing(filename, l):
    """opens a file for read and returns the list of lines 
    
    Arguments 
    filename -- File to write to 
    l        -- list to write to the file
    """    
    with open (filename, 'w') as f:        
        for line in l:
            f.write(line.strip())
            f.write("\n")


# In[68]:

def writing_dict(filename, l):
    with open (filename, 'w') as f:        
        for line in l:
            f.write(line.strip())
            f.write("\t")
            f.write(str(l[line]))
            f.write("\n")


# In[111]:

def extract_tweets(l, cleanFile, matching, *args):
    """extract tweet that matches the pattern and returns a string containing the number of rows deleted in each iteration.
    returns a list of lines in the file cleaned.
    
    Arguments:
    l         -- list of tweets
    cleanFile -- Name of the file to write to
    matching  -- True means that you want to remove the tweets matching these patterns, False otherwise
    *args     -- variable length argument that receives the regex patterns you want to match t
        """    
    amend = ""
    starting_len = len(l)  
    it = 1
    for pattern in args:  
        temp_l = []       
        removed_tweets = [pattern + "\n"]
        counter = 0
        pat    = re.compile(pattern)
        for line in l:
            line = line.strip()
            result = pat.findall(line)  
            if (matching and result == []) or ( (not matching ) and (result != []) ):
                temp_l.append(line)
                counter += 1
            else:
                removed_tweets.append(line)   
        writing("iteration " + str(it)+ " removed tweets.txt",removed_tweets)
        l = copy.copy(temp_l)
        amend += "Pattern " +  str(it) + " (" + pattern + " removed: " + str(starting_len - counter) + "lines\n"
        starting_len = counter
        it += 1
    writing(cleanFile, l)
    print amend
    return l


# In[38]:

def distinct_items(l, pattern, outputfile = "distinct_items.txt"): 
    """Gets distinct items from a list given a certain pattern and returns a dictionary of the distinct hashtags in a list
    associated with it's values 
    Arguments:
    l          -- list of lines of the file
    pattern    -- pattern to match for the distinct items
    outputfile -- file to output results to 
    """
    d = {}
    pat = re.compile(pattern)
    for tweet in l:
        grouped_items = pat.findall(tweet)
        for item in grouped_items:
            if item in d.keys():
                d[unicode(item)] += 1
            else:
                d[unicode(item)] = 1
    ordered_d = collections.OrderedDict(sorted(d.items(),  key= lambda x: x[1], 
                                              reverse=True))    
    with open (outputfile, 'w') as f:        
        for item in ordered_d.keys():
            f.write(item + ": " + str(ordered_d[item]) + "\n")    
    return ordered_d


# In[39]:

#TF IDF Calculation
def TFIDF_utf(corpus, outputfile = "TFIDF.txt", includeIDF = True):
    """Takes a file encoded in UTF-8 and calculates the TFIDF, outputs the result to an encoded utf-8 file and returns a zipped
    list where the first element is the feature and the second one is the TFIDF score
    Arguments:
    corpus     -- corpus to calculate TFIDF on
    outputfile -- file to output TFIDF scores to, default value is "TFIDF.txt"
    includeIDF -- default = True, False means that you want to calculate the TF only.
    """
    vectorizer = TfidfVectorizer(min_df=1)
    X = vectorizer.fit_transform(corpus)
    idf = vectorizer.idf_
    feature_tfidf = zip(vectorizer.get_feature_names(), idf)
    tf_dict = collections.OrderedDict(sorted(feature_tfidf, key = lambda x: x[1], reverse= True))
    with codecs.open(outputfile, "w", "utf-8-sig") as temp:
       for k in tf_dict.keys():
           temp.write(k)
           temp.write("\t")
           temp.write(unicode(tf_dict[k]))
           temp.write("\n")
    return feature_tfidf


# In[40]:

def extract_columns(l, extract=False, *args):
    """Removes columns from a list and returns a list of removed columns
    Arguments:
    l        -- a list containing lines from the file
    extract  -- only extract that column, default is False, True means extract only that column number
    *args    -- variable length argument for columns to remove from the file
    """
    counter = 0
    file1 = l
    output = []
    if len(file1[0]) >= max(args):
        for line in file1:
            line = line.strip()
            splitted = line.split("\t")
            new_line = []
            if extract:
                try:
                    new_line.append(splitted[args[0]])
                except:
                    counter+=1 
                    print "Number of lines failed", counter
            else:
                for i in range(len(args)):
                    if i not in args:
                        new_line.append(splitted[i])
            output.append("\t".join(new_line))
    writing("extracted_columns " + " ".join(map( lambda x: str(x), args) ) + ".txt", output)
    return output



# In[41]:

def remove_words(l, cleanFile, *args):
    """removes tweet that matches the pattern and returns a string containing the number of rows deleted in each iteration.
    returns a list of lines with words removed
    
    Arguments:
    l         -- list of tweets
    cleanFile -- Name of the file to write to
    matching  -- True means that you want to remove the tweets matching these patterns, False otherwise
    *args     -- variable length argument that receives the regex patterns you want to match t
        """    
    res = []
    for pattern in args:  
        pat    = re.compile(pattern)
        for line in l:
            line = line.strip("\n")
            result = pat.findall(line)  
            for match in result:
                line = line.replace(match, "")
            res.append(line)
    writing(cleanFile, res)
    return res


# In[42]:

def count_frequency(corpus, ngrams = 1):
    """Takes a corpus and returns a multidimensional array containing counts
    still suitable for counting occurunces in the whole document
    Arguments:
    corpus -- list of lines to count frequency on
    """
    for n in range(1, ngrams + 1):
        print n
        vectorizer = CountVectorizer(min_df=1, ngram_range=(n, n))
        X = vectorizer.fit_transform([corpus])
        counts = zip(vectorizer.get_feature_names(), X.toarray()[0])
        tf_dict = collections.OrderedDict(sorted(counts, key = lambda x: x[1], reverse = True))
        outputfile  = "frequency " + str(n) + " grams.txt" 
        with codecs.open(outputfile, "w", "utf-8-sig") as temp:
           for k in tf_dict.keys():
               temp.write(k)
               temp.write("\t")
               temp.write(unicode(tf_dict[k]))
               temp.write("\n")
    #return X.toarray()    


# In[43]:

def ngrams(input, n, delimeter):
    """takes an input calculate the ngrams on and returns a list of all ngrams    Arguments:
    input     -- input to get ngrams from
    n         -- number of "n"grams
    delimiter -- how the input is delimited (ex. " ", "\t", ","..)
    """
    input  = input.split(delimeter)
    output = []
    if len(input)<n:
        n = len(input)
    for i in range(len(input)-1):
        output.append(input[i:i+n])
    return output


# In[75]:

#Remove stopwords
def remove_stopwords(l, language, outputfile = "stop_words_removed.txt"):
    """Takes a list of lines of a file and returns the list with stopwords removed
    Arguments:
    l -- file list
    language -- language of the input list ex. arabic, english, french, german
    outputfile -- file to output results to, default = "stop_words_removed.txt"
    """
    res = []
    try:
        stop_words = get_stop_words(language)
    except Exception:
        print Exception.message
        return res    
    for line in l:
        for word in line.strip().split(" "):
            if unicode(word, "utf-8") in stop_words:
                line = line.replace(word, "")
        res.append(line)
    writing(outputfile,res)
    return res


# In[82]:

def lexicon_preprocess(lexicon,pos_list,neg_list):
    """takes a list containing a tab delimited lexicon file where the first column is the word and the second column is a range
    of values giving by pos_list,neg_list. returns a dictionary with a key of lexicon word and value is a label in 1 or -1
    Arguments:
    lexicon -- lexicon file
    pos_list-- list containing range of positive values represented in the lexicon
    neg_list-- list containing range of negative values represented in the lexicon
    """
    lexi_dict = {}
    counter = 0
    for line in lexicon:
        line = line.split("\t") 
        try:
            if line[1] in neg_list:
                lexi_dict[line[0]] = -1 
            elif line[1] in pos_list:
                lexi_dict[line[0]] =  1
        except:
            counter +=1 
            print counter 
    return lexi_dict


# In[145]:

def lexicon_polarity(lexi_dict, tweets, outputfile = "pos_neg_tweets.txt", n = 4):
    """takes a file and a lexicon, assigns labels to the file based on this lexicon. 
    lexi_dict  -- labeled lexicon dictionary with the word associated to it's polarity
    tweets     -- list of lines to label according to the lexicon
    outputfile -- file to output the result to, default is "pos_neg_tweets.txt"
    n          -- consider ngrams, 
    
    """
    res    = {}
    for tweet in tweets:
        score = 0
        ngram = ngrams(tweet, n, " ")
        for item in ngram:
            for gram in item:
                if gram in lexi_dict.keys():
                    score += lexi_dict[gram]
        res[tweet] = score
    writing_dict(outputfile, res)
    print "done"
    return res


# In[146]:

def label(file_list, class1_file, class2_file):
    """Takes a file and label it according to two lexicons, neutral
    Arguments:
    file_list   -- list of lines to label
    class1_file -- list of words to label +ve upon
    class2_file -- list of words to label -ve upon 
    """
    file1 = list(set(file_list))
    for i in range(len(class1_file)):
        class1_file[i] = class1_file[i].strip()
    for i in range(len(class2_file)):
        class2_file[i] = class2_file[i].strip()
    class1_list = []
    class2_list = []
    neutral = []
    for line in file1:
        line  = line.strip()
        score = 0
        for word in class1_file:
            pat   = re.compile(word)
            score += len(pat.findall(line))
        for word in class2_file:
            pat = re.compile(word)
            score += -1 * len(pat.findall(line))
        if score   > 0:
            class1_list.append(line + "\t" + str(1))
        elif score < 0:
            class2_list.append(line + "\t" + str(-1))
        else:    
            neutral.append(line + "\t" + str(0))
    writing("class1.txt", class1_list)
    writing("class2.txt", class2_list)
    writing("neutral.txt", neutral)
    print len(file1)
    print len(class1_list)
    print len(class2_list)
    print len(neutral_tweets)


# In[ ]:

####Modeling#####


# In[ ]:

def boolean_model(input):
    """Takes a list of lines to get the boolean model from, returns vectorizer object where you can call
    transform_model(word, vectorizer) on another sentence to transform it into the word vector
    Arguments:
    input -- list of lines
    """
    vectorizer = CountVectorizer(min_df = 1, binary = True)
    corpus = vectorizer(input)
    X = vectorizer.fit_transform(corpus)
    boolean_model = X.toarray()
    return vectorizer


# In[ ]:

def transform_model(l, model):
    """Takes a list representing lines in the file and transforms it into an array of the model and returns a numpy 2d array 
    for the string transformed into the model
    l     -- list containing lines to be transformed
    model -- model to be fitted upon
    """
    return model.transform(l).toarray()


# In[ ]:



