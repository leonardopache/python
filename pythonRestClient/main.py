#!/usr/bin/env python
import requests 
import json
from collections import namedtuple

URL_BASE = 'http://localhost:8080/'

def json2obj(data_json): 
	return json.loads(data_json, object_hook=_json_object_hook)


def _json_object_hook(d):
	return namedtuple('X', d.keys())(*d.values())

class GetTweet:

	def __init__(self):
		get_response = requests.get(url=URL_BASE+'tweet')
		self.tweets = json2obj(get_response.content)

	def print_tweets(d):
		if len(d.tweets) == 0:
			print 'List of tweets empty!!'
		else : 
			for tweet in d.tweets: 
				print 'ID = '+str(tweet.id)+' | Publisher = '+tweet.publisher+' | Tweet = '+tweet.tweet

class GetTweetDiscarded:

	def __init__(self):
		get_response = requests.get(url=URL_BASE+'discard')
		self.tweets = json2obj(get_response.content)

	def print_tweets(d):
		if len(d.tweets) == 0:
			print 'List of tweets discarded empty!!'
		else : 
			for tweet in d.tweets: 
				print 'ID = '+str(tweet.id)+' | Publisher = '+tweet.publisher+' | Tweet = '+tweet.tweet

class PostTweet:
	def __init__(self, publisher, tweet):
		json_data = '{"publisher": \"'+publisher+'\", "tweet": \"'+tweet+'\"}'
		get_response = requests.post(URL_BASE+'tweet', json=json.loads(json_data))
		if get_response.content == '':
			print 'Post Success!!'
		else :
			print str(get_response.content)

class PostDiscardTweet:
	def __init__(self, tweetId):
		json_data = '{"id": '+str(tweetId)+'}'
		get_response = requests.post(URL_BASE+'discard', json=json.loads(json_data))


class Console:

	def menu(d):
		option = 1
		
		while(option != '0'):
			print ' 1 - Print Tweets Not Discaded \n 2 - Print Tweets Discarded \n 3 - Post new Tweet \n 4 - Discard one Tweet \n 0 - Exit '
			option = raw_input()
			
			if(option == '1'):
				GetTweet().print_tweets()
			if(option == '2'):
				GetTweetDiscarded().print_tweets()
			if(option == '3'):
				print 'Input Publisher: '
				publisher = raw_input()
				print 'Input Tweet: '
				tweet = raw_input()
				PostTweet(publisher, tweet)
			if(option == '4'):
				print 'Input ID of tweet to discard: '
				tweetId = raw_input()
				PostDiscardTweet(tweetId)
			
Console().menu()

