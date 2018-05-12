#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
This Command line App collect and store last tweets from:TunnelToulon's twitter account

TODO: Import config from some JSON file
    So users won't need to get their noise in here in order to customize things
    https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
    https://docs.python.org/3.6/library/configparser.html?highlight=config%20file#module-configparser
TODO: Test for bugs, stability and max values with garbage inputs
'''

if __name__ == '__main__':

    import logging
    #import logging.config # will be used to import config from json file
    import json
    import tweepy # Twitter mining/streaming lib
    import argparse # Command line the easy way

    # Files management
    from time import strftime
    from os import path as os_path
    from pathlib import Path as pathlib_Path

    # This python script directory -> where to look for config files etc
    #PROJECT_DIR = os_path.dirname(os_path.abspath(__file__))
    PROJECT_DIR = os_path.dirname(os_path.realpath(__file__))

    #------------------------------------------------
    # APP CONFIG
    # TODO: import those from json file
    #------------------------------------------------
    # Name of the folder used to store every file : logs and gathered tweets
    # NOTE This folder will be created inside the current active directory
    sub_path = pathlib_Path("output/")
    # JSON file containing CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    #   Create an App to get them : https://apps.twitter.com/
    # Path is relative to this python script directory
    # If no path and just a name, must be in the same directory as this script
    twitter_oauth_path = 'oauth.json'
    # Prefix used for files name generation
    output_files_prefix = 'Collect'
    # Log Level Config - For now it is done with Command-Line (see later)


    # Tweek to look for the oauth file in the same directory as this python file
    # TODO There must be a better way !
    twitter_oauth_path = os_path.join(PROJECT_DIR, twitter_oauth_path)
    # If subpath doesn't exist, mkdir
    # This folder will be used to store every files generated (log, txt, json)
    sub_path.mkdir(parents=True, exist_ok=True)

    #---------------------------------------------------
    # ARGPARSE
    #---------------------------------------------------
    parser = argparse.ArgumentParser(description="Collect and store to disk the last $limit tweets from: $target's twitter account")
    parser.add_argument("target",
        help="target account to grab tweets from")

    parser.add_argument("-l", "--limit",
        help="maximum number of tweets the app will try to grab from the target twitter account. Default is 1", type=int, default=1)

    parser.add_argument("--loglvl",
        type=int,
        default=1,
        choices=[0,1,2,3,4,5],
        help="set the log level with an interger : {0: 'NONE', 1: 'DEBUG', 2: 'INFO', 3: 'WARN', 4: 'ERROR', 5: 'CRITICAL'}. Default is DEBUG"
    )

    parser.add_argument("-t", "--txt",
        action="store_true",
        help="Generate a TXT file with tweet's text content. JSON one will still be generated"
    )

    args = parser.parse_args()

    #---------------------------------------------------
    # LOG LEVEL
    #---------------------------------------------------
    # Get the numeric values of logging levels
    #https://docs.python.org/3.6/library/logging.html#logging-levels
    # Levels are constants
    # NOTSET = 0, DEBUG = 10, INFO = 20, WARNING = 30, ERROR = 40, CRITICAL = 50   
    log_lvl = [ 0, 10, 20, 30, 40, 50 ]
    log_lvl = log_lvl[args.loglvl]
    # Log_lvl 0 from command-line mean "NONE", and not "NOTSET"
    # In case of "NONE", we raise a flag that will allow to skip all log events
    if (log_lvl == 0):
        noLogs = True
    else:
        noLogs = False


    #---------------------------------------------------
    # Output_Files Name Generation
    #---------------------------------------------------
    # Protection against lonnnnnggg file names
    if (len(output_files_prefix) > 32):
        output_files_prefix = output_files_prefix[:33]
    # Generate file name from prefix, target(twitter account) and current time
    # so that each run is stored in a new file
    output_files_stem = output_files_prefix + '_' + args.target
    output_files_stem += '_' + strftime("%Y_%m_%d-%H_%M_%S")
    output_files_base = os_path.join(sub_path , output_files_stem)

    #---------------------------------------------------
    # LOGGER
    #---------------------------------------------------
    if (not noLogs):

        logger = logging.getLogger(__name__)
        logger_log_lvl = file_handler_log_lvl = console_handler_log_lvl = log_lvl
        logger.setLevel(log_lvl)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(output_files_base+'.log')
        file_handler.setLevel(log_lvl)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_lvl)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        #logger.debug('debug message test')
        #logger.info('info message test')
        #logger.warn('warn message test')
        #logger.error('error message test')
        #logger.critical('critical message test')

    def log (lvl, msg):
        if (not noLogs):
            getattr(logger, lvl)(msg)
        else:
            pass

    #---------------------------------------------------
    # Twitter Authentification with Tweepy
    #---------------------------------------------------
    # Import Twitter credentials from json file


    with open(twitter_oauth_path,'r', encoding='utf-8') as json_data:
        try:
            oauth_d = json.load(json_data)
            #log('info','{}'.format(oauth_d))
        except:
            log('critical','Error decoding json file with twitter credentials')
            exit(1)
    log('info', 'Twitter Credentials successfully imported from \"{}\"'.format(os_path.basename(twitter_oauth_path)))

    auth = tweepy.OAuthHandler(oauth_d["CONSUMER_KEY"], oauth_d["CONSUMER_SECRET"])
    auth.set_access_token(oauth_d["ACCESS_TOKEN"], oauth_d["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(
        auth_handler = auth,
        retry_count=2,
        retry_delay=10,
        wait_on_rate_limit = True,
        wait_on_rate_limit_notify = True
        )

    if (not api):
        log('critical', 'Couldn\'t connect to the Twitter API')
        exit(1)

    '''
    # update status
    try:
        api.update_status('Status update from python!')
    except tweepy.TweepError as e:
        logger.warn("Got error \'"+e.reason+"\' after trying to update twitter status.")

    # Will download twitter account home timeline tweets and print each one of their texts to the console
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)

    # Returns the most recent statuses posted from the user specified
    # public_tweets = api.user_timeline(id = 'TunnelToulon', count = 2, page = 1)
    '''
    #---------------------------------------------------
    # Tweepy: Collect Tweets
    #---------------------------------------------------
    log('info','Collect from:{} with limit:{}'.format(args.target, args.limit))
    log('info','START')
    collected_tweets = tweepy.Cursor(   
        api.user_timeline,
        id = args.target,
        #count = 2,
        #page = 1,
        tweet_mode='extended'
    ).items(args.limit)


    # TODO create new file when current one is bigger/older than..
    for tweet in collected_tweets:

        # Those line can quickly flood the console
        #print( json.dumps('id: '+ tweet._json["id_str"]+' : created_at: '+tweet._json["created_at"], ensure_ascii=False) )
        #print( '','','','','', json.dumps('full_text: '+tweet._json["full_text"], ensure_ascii=False) )

        # Generate JSON file and append it with tweet's JSON content
        with open(output_files_base+'.json', 'a', encoding='utf8') as json_tweets:
            #TODO try:
            #except:
            json_tweets.write(json.dumps(tweet._json, ensure_ascii=False) )
            json_tweets.write('\n')
        
        if (args.txt): # If specified from command-line, generate txt file with tweets content
            with open(output_files_base+'.txt', 'a', encoding='utf8') as text_tweets:
                #TODO try:
                #except:
                text_tweets.write(tweet.full_text)
                text_tweets.write('\n\n')
    log('info','DONE')

    #check how many queries we have left
    log('info', api.rate_limit_status()['resources']['search'])

