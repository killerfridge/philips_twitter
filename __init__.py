from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
import datetime as dt


ckey = '174okOoY7G6cTh8DsDPgFsUCF'
csecret = 'iRXkhd2welmWDMOTb8FLhMTypX7HDBmdpi2KFmceoDI2uhnh3L'
atoken = '95300715-4QI5aoymwxfGUOgsoDFgwaXEsfG4pXhSsN0rj0wA7'
asecret = '7o6EAohXUQkVV4MCMTsOlXCHU862TgNdsHUhEhFMJPrRA'

con = sqlite3.connect('sentiments.sqlite')

con.execute('create table if not exists tweets (created datetime, tweet char, user char);')


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data['text']
        time = dt.datetime.now()
        user = all_data['user']['screen_name']
        con.execute('insert into tweets (created, tweet, user) values (?, ?, ?)', (time, tweet, user))
        print(tweet)
        con.commit()

    def on_error(self, status):
        print(status)


auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track=['philips'])
