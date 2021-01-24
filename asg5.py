# CS 4372 Assignment 4
# Dat Tran - dmt170030 and Austin Luong - atl170030

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import preprocessor as p
import nltk
import os
import json
from urllib3.exceptions import ProtocolError

nltk.download('punkt')
java_path = "C:/Program Files/Java/jdk1.8.0_241/bin/java.exe"
os.environ['JAVAHOME'] = java_path

access_token = "" # Fill access token here
access_token_secret = "" # Fill access token secret here
consumer_key = "" # Fill api key here
consumer_secret = "" # Fill api key secret here

st = StanfordNERTagger('D:/stanford-ner-4.2.0/stanford-ner-2020-11-17/classifiers/english.muc.7class.distsim.crf.ser.gz',
					   'D:/stanford-ner-4.2.0/stanford-ner-2020-11-17/stanford-ner.jar',
					   encoding='utf-8')

a = 0
b = 0
c = 0
d = 0
e = 0
f = 0
g = 0

class StdOutListener(StreamListener):
	def on_data(self,data):
		global a
		global b
		global c
		global d
		global e
		global f
		global g
		all_data = json.loads(data)
		tweet = all_data["text"]
		tweet = p.clean(tweet)
		tokenized_text = word_tokenize(tweet)
		classified_text = st.tag(tokenized_text)
		for i in range(len(classified_text)):
			if classified_text[i][1] == "LOCATION":
				a = a + 1
			elif classified_text[i][1] == "ORGANIZATION":
				b = b + 1
			elif classified_text[i][1] == "DATE":
				c = c + 1
			elif classified_text[i][1] == "MONEY":
				d = d + 1
			elif classified_text[i][1] == "PERSON":
				e = e + 1
			elif classified_text[i][1] == "PERCENT":
				f = f + 1
			elif classified_text[i][1] == "TIME":
				g = g + 1
		print("Location Count is: " + str(a))
		print("Organization Count is: " + str(b))
		print("Date Count is: " + str(c))
		print("Money Count is: " + str(d))
		print("Person Count is: " + str(e))
		print("Percent Count is: " + str(f))
		print("Time Count is: " + str(g), '\n')
		return a,b,c,d,e,f,g

	def on_error(self, status):
		print(status)

l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

while True:
    try:
        stream.filter(track=['aws', 'sagemaker', 'georgia'])

    except (ProtocolError, AttributeError):
        continue
