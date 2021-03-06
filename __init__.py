from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3
import datetime as dt
import sys

def main(search_term=None):
    if not search_term:
        search_term = 'cars'
    ckey = '174okOoY7G6cTh8DsDPgFsUCF'
    csecret = 'iRXkhd2welmWDMOTb8FLhMTypX7HDBmdpi2KFmceoDI2uhnh3L'
    atoken = '95300715-4QI5aoymwxfGUOgsoDFgwaXEsfG4pXhSsN0rj0wA7'
    asecret = '7o6EAohXUQkVV4MCMTsOlXCHU862TgNdsHUhEhFMJPrRA'

    con = sqlite3.connect('sentiments.sqlite')

    con.execute('create table if not exists tweets (created datetime, tweet char, user char, lang char, search char);')
    COUNTER = 0

    class Listener(StreamListener):

        def __init__(self, api=None):
            super().__init__(api)
            self.COUNTER = 0

        def on_data(self, data):
            all_data = json.loads(data)
            # print(all_data.keys())
            tweet = all_data['text']
            time = dt.datetime.now()
            user = all_data['user']['screen_name']
            lang = all_data['lang']
            con.execute('insert into tweets (created, tweet, user, lang, search) values (?, ?, ?, ?, ?)',
                        (time, tweet, user, lang, search_term))
            print(f'{user} said:\n{tweet}')
            con.commit()
            self.COUNTER += 1
            # print(self.COUNTER)

        def on_error(self, status):
            print(status)

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitter_stream = Stream(auth, Listener())

    twitter_stream.filter(track=[search_term])


if __name__=='__main__':
    if sys.argv[1]:
        main(sys.argv[1])
    else:
        main()