from Mysql import Mysql
from Extract_data import Extract
from Api_twitter import StreamTwitter
from pprint import pprint
import os

if __name__ == "__main__":
    extract = Extract()
    if "ACCESS_TOKEN_TWT" not in os.environ :
        extract.usage_accessToken()
    stream = StreamTwitter()
    stream.reset_rules()
    stream.set_rules('keywords')
    stream.set_rules('user')
    stream.set_rules('hashtags')
    stream.get_rules(1)
    ''' UNCOMMENT THE FOLLOWING LINES TO CONNECT TO STREAM  / AFTER SETTING RULES'''

    while (True):
        stream.connect_stream()
        sleep(10)
    # stream.set_rules('keywords')
     
