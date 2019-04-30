collect_tweets_cli
======

This Command line Python App try to collect a given number of tweets from a given twitter account and put them into some json file.

Prerequisites
------------
- [Tweepy](https://github.com/tweepy/tweepy)

The easiest way to install the latest version
is by using pip/easy_install to pull it from PyPI:

    pip install tweepy

[Tweepy Documentation](http://tweepy.readthedocs.io/en/v3.6.0/)

Installation
------------

	$ git clone https://github.com/LaChouetteInformatique/CollectTweets_PythonCLI
	$ cd CollectTweets_PythonCLI
	
Configuration
-------------

1. Make some oauth.json file from model, ex :

		$ cp oauth_empty.json oauth.json

2. Enter you twitter app credentials into it one way or another, ex :

	- go to [Your Twitter App](https://apps.twitter.com/)
	- make one if you don't already have
	- go to Keys and Access Tokens screen
	- copy/get the Consumer Key, Consumer Secret, Access Token, Access Token Secret
	- paste into oauth.json

Run
---

	$ python collect_tweets_app.py -h

## Acknowledgments

* Thanks to the teacher who pushed me to make this as a tweetter discovery exercice
* Hat tip to anyone who's code was used
