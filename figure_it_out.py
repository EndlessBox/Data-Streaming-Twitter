from Mysql import Mysql
from Extract_data import Extract
from Api_twitter import StreamTwitter
from pprint import pprint
import os
import json
import sys
import time

def connect_stream(keywords, log):
    extract = Extract()
    if "ACCESS_TOKEN_TWT" not in os.environ :
        extract.usage_accessToken()
    stream = StreamTwitter(1)
    stream.reset_rules()
    stream.set_rules(keywords)
    if (stream.log) :
        stream.get_rules(1)
    i = 0
    while (True) :
        stream.connect_stream()
        time.sleep((2 ** i) + 60)
        i += 1


if __name__ == "__main__":

    # hey = open("test.json", "r")
    # clean = (hey.read()).replace("}{", "},{")
    # pprint(json.loads(clean))


    # db = Mysql("localhost", "root", "hello", "Tweets", 3306)
    # db.create_db()

    """
        Un-comment to connect stream.
        1 : the programe will make a test.json to store and print logs
        0 : no logs
    """
    connect_stream(list(['hashtags', 'keywords', 'user']), 1)

    """
        author_id
        time_of_creation
        language
        possibly_sensitive
        stats/like_count
        stats/retweet_count
        stats/reply_count
        stats/quote_count
        text
        ~~ : matching rules
    """