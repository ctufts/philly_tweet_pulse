import collections
import happierfuntokenizing


tok = happierfuntokenizing.Tokenizer()
tweet = '@AmazingPhil HAPPY NEW YEAR PHILLY! Hope you have a great one, you deserve it! ??'
sentence =  list(tok.tokenize(tweet.lower()))
tweet_length = len(sentence)
words = collections.Counter(sentence)
for key, value in words.items():
	data = [key,value, tweet_length]
	print(data)