#!/usr/bin/env python2
# -*- coding: utf-8 -*- #

from sys import argv
from PIL import Image
#import cv2

from twitterbot import TwitterBot
from picbot import PicBot
from faceflip import face_flip, face_swap, face_mark
import keys



class FaceBot(PicBot, TwitterBot):
	"""
	Whenever you tweet a photo at this bot, it will tweet back at you with an image
	with the faces flipped
	"""
	def bot_init(self):
		""" Initialize and configure the bot """

		############################
		# SETUP  FACE DETECTION    #
		############################
		classifier = "haarcascade_frontalface_default.xml"
		self.faceCascade = cv2.CascadeClassifier(classifier)

		############################
		# REQUIRED: LOGIN DETAILS! #
		############################
		self.config['api_key'] = keys.consumer_key	
		self.config['api_secret'] = keys.consumer_secret
		self.config['access_key'] = keys.access_token
		self.config['access_secret'] = keys.access_token_secret


		######################################
		# SEMI-OPTIONAL: OTHER CONFIG STUFF! #
		######################################

		# how often to tweet, in seconds
		self.config['tweet_interval'] = 1 * 5     # default: 1 minutes

		# use this to define a (min, max) random range of how often to tweet
		# e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
		self.config['tweet_interval_range'] = None

		# only reply to tweets that specifically mention the bot
		self.config['reply_direct_mention_only'] = True

		# only include bot followers (and original tweeter) in @-replies
		self.config['reply_followers_only'] = False

		# fav any tweets that mention this bot?
		self.config['autofav_mentions'] = False

		# fav any tweets containing these keywords?
		self.config['autofav_keywords'] = []

		# follow back all followers?
		self.config['autofollow'] = False



	def on_scheduled_tweet(self):
		""" Make a public tweet to the bot's own timeline. """
		# We might take senteces from somewhere and tweet them on a regular basis ...
		pass # don't do anything here ...


	def on_timeline(self, tweet, prefix):
		""" Actions to take on a timeline tweet. """
		pass # Don't do anything here ...


	def on_mention_without_image(self, tweet, prefix):
		"""
		React to text-only mentions
		"""
		text = "{} Come on, tweet me a photo with some faces in it".format(prefix)
		try:
			self.post_tweet(text[:140], reply_to=tweet)
		except Exception as e:
			print(e)


	def process_image(self, image, prefix=None, fn=face_swap, verb="swapped"):
		"""
		Process the image, swap the faces
		"""

		image, rectangles = fn(image)

		# return new images with comment
		num = len(rectangles)
		if num == 1:
			# comment = "{} here you go. I {} a face for you.".format(prefix, verb)
			comment = "{} Nice pic :) Do you have one with more faces in it?".format(prefix)
		elif num > 1:
			comment = "{} here you go. I {} {} faces for you.".format(prefix, verb, num)
		else:
			comment = "Nice pic. But I couldn't spot any faces :("
		return image, comment 


if __name__ == '__main__':

	bot = FaceBot()
	
	if len(argv) == 1:
		# just run the bot
		print("Running the bot.")
		bot.run()

	elif argv[1] == "test":
		# various tests
		if(len(argv) == 2):
			print "USAGE: facebot.py test [image|mention]"
		else:
			test = argv[2]
			if test == "image":
				print("Testing image flipping")
				img = Image.open("test2.jpg")
				img, comment = bot.process_image(img, "@test", fn=face_flip, verb="flipped" )
				img.show()
				print("COMMENT: {}".format(comment))
			elif test == "mention":
				print("Testing on_mention hook of the bot")
				api = bot.api
				tweet = api.get_status("610561113294512129")
				prefix = bot.get_mention_prefix(tweet)
				bot.on_mention(tweet, prefix)
			else:
				print("Unknown test: {}".format(test))





