from gensim import corpora, models
import pyLDAvis.gensim
import mysql.connector
import configSettings as cs
import collections
import pickle
import os.path

parent_directory = os.path.abspath(os.path.dirname(__file__))
corpusObject = open(parent_directory + '/data/corpus','rb')  
dictionaryObject = open(parent_directory + '/data/dictionary','rb')  
# load the object from the file into var b
corpus = pickle.load(corpusObject) 
dictionary = pickle.load(dictionaryObject)

corpusObject.close()
dictionaryObject.close()

# #LDA using 4 cores
# dictionary = corpora.Dictionary(filtered_tweets)
# corpus = [dictionary.doc2bow(text) for text in filtered_tweets]

ldamodel = models.ldamulticore.LdaMulticore(corpus, num_topics=8, 
                                                   id2word = dictionary, passes=50)

# # generate vis
data_vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
# save into html
# pyLDAvis.prepared_data_to_html(data_vis)

# print(dname + "/topic.html")
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# write html to file
pyLDAvis.save_json(data_vis, parent_directory + "/FlaskApp/static/data/lda.json")
# pyLDAvis.save_json(data_vis, 'lda.json')

# shot html data



