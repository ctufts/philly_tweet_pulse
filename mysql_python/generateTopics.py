from gensim import corpora, models
import pyLDAvis.gensim
import mysql.connector
import configSettings as cs
import collections
import pickle
import os.path

corpusObject = open('data/corpus','rb')  
dictionaryObject = open('data/dictionary','rb')  
# load the object from the file into var b
corpus = pickle.load(corpusObject) 
dictionary = pickle.load(dictionaryObject)

corpusObject.close()
dictionaryObject.close()

# #LDA using 4 cores
# dictionary = corpora.Dictionary(filtered_tweets)
# corpus = [dictionary.doc2bow(text) for text in filtered_tweets]

ldamodel = models.ldamulticore.LdaMulticore(corpus, num_topics=20, 
                                                   id2word = dictionary, passes=50)

# # generate vis
data_vis = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
# save into html
# pyLDAvis.prepared_data_to_html(data_vis)

# print(dname + "/topic.html")
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("absolute path = ", parent_directory)

# write html to file
pyLDAvis.save_json(data_vis, parent_directory + "/app/static/lda.json")
# pyLDAvis.save_json(data_vis, 'lda.json')

# shot html data



