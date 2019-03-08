from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
import datetime as dt

SEARCH_TERM = 'lumea'
ckey = '174okOoY7G6cTh8DsDPgFsUCF'
csecret = 'iRXkhd2welmWDMOTb8FLhMTypX7HDBmdpi2KFmceoDI2uhnh3L'
atoken = '95300715-4QI5aoymwxfGUOgsoDFgwaXEsfG4pXhSsN0rj0wA7'
asecret = '7o6EAohXUQkVV4MCMTsOlXCHU862TgNdsHUhEhFMJPrRA'

con = sqlite3.connect('sentiments.sqlite')

con.execute('drop table if exists tweets;')
con.execute('create table if not exists tweets (created datetime, tweet char, user char, lang char, search char);')


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        # print(all_data.keys())
        tweet = all_data['text']
        time = dt.datetime.now()
        user = all_data['user']['screen_name']
        lang = all_data['lang']
        con.execute('insert into tweets (created, tweet, user, lang, search) values (?, ?, ?, ?, ?)',
                    (time, tweet, user, lang, SEARCH_TERM))
        print(tweet)
        con.commit()

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track=['philips'])
