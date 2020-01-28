from Extract_data import Extract
from Mysql import Mysql
import requests
import json
import os
import sys
import time
from pprint import pprint

class StreamTwitter:

    def __init__(self, log):
        self.extract = Extract()
        self.sql = Mysql("localhost", "root", "hello", "tweets", 3306)
        # self.colors = Colors()
        self.stream_url = self.extract.api['TwitterStream']
        self.stream_rules_url = self.extract.api['TwitterStreamRules']
        self.rules = self.extract.api['TwitterStreamRulesSettings']
        self.auth = lambda x: {"Authorization" : "Bearer {}".format(x), "Content-type": "application/json"}
        self.conn = 0
        self.log = lambda log: (log == 1)

    def connect_stream(self):

        try :
            access_token = os.environ.get('ACCESS_TOKEN_TWT')
            if (self.conn == 0):
                response = requests.get(self.stream_url, headers=self.auth(access_token), stream=True, params={"format": "detailed"})
                self.conn = 1
            for line in response.iter_lines() :
                if (line):
                    json_dict = json.loads(line)
                    if (self.log) :
                        pprint(json_dict)
                    self.load_twt_to_db(json_dict)
                    
        except Exception as err :
            print(err)
            response.close()
            sys.exit()
        else :
            print("success !")
            response.close()

    def load_twt_to_db(self, tweet_dict) :
        try :
            author_id = tweet_dict['data']['author_id']
            created_at = tweet_dict['data']['created_at']
            lang = tweet_dict['data']['lang']
            possibly_sensitive = (tweet_dict['data']['possibly_sensitive'] == 'True')
            like_count = tweet_dict['data']['stats']['like_count']
            retweet_count = tweet_dict['data']['stats']['retweet_count']
            reply_count = tweet_dict['data']['stats']['reply_count']
            quote_count = tweet_dict['data']['stats']['quote_count']
            twt_body = tweet_dict['data']['text']
            self.sql.db_add(author_id, created_at, lang, possibly_sensitive, like_count, retweet_count, reply_count, quote_count, twt_body)
        except Exception as err :
            print (err)
            sys.exit()


    def  set_rules(self, rules):
        payload = []
        try :

            access_token = os.environ.get('ACCESS_TOKEN_TWT')
            ''' 
                Evaluat Rule given if it's in our Rules list ! 
                Examined file : 'data_sources.json'  

                Check if the given rule has some content*
                * (content) : the keyword, hashtags, user's that we will match againts twitter and filter tweets upon !          
            '''
            for rule in rules :
                if rule not in self.rules :
                    raise ModuleNotFoundError('Rule type is uncorrect')
                elif self.rules[rule] == None :
                    raise KeyError ('Error : empty rules')

            '''
                After checking the rules given, we transform them to the correct format* for the api call.
                * (format) : json format example : [{"value" : "cat has:media*"}, {"value" : "dog"}]
                * (has:media) : optional parametrs check twitter operators !
            '''
            for rule in rules :
                for key in self.rules[rule] :
                    if key :
                        payload.append({'value' : key})
            '''
                manage all errors raised above.
            '''
            rules = dict({"add" : payload})
            response = requests.post(self.stream_rules_url, headers=self.auth(access_token), json=rules)
            if response.status_code is not 201:
                raise AssertionError (response.text)
        except AssertionError as set_rule_error :
            print (f"Rules were not setted")
            print (f"Error : %s" % set_rule_error)
            
        except KeyError as err:
            print (err)
            sys.exit()

        except ValueError as v_err :
            print (f"Error  : %s." % v_err)
            print (f"Update : '%s' file." % self.extract.data_source_file_name)
            print (f"Section : %s." % self.stream_rules_url)
            sys.exit()

        except ModuleNotFoundError as err :
            print (f"Error : %s" % err)
            print ("Try on of the followings keywords")
            for rules in self.rules :
                print ("* " + rules + " *")
            print ("\nOR\n")
            print (f"Add your own rules in %s using the same format as in the file" % self.extract.data_source_file_name)
            sys.exit()

        finally :
            if (self.log) :
                for rule in rules :
                    print (rule, end='\n')
                print('')
                print("rules were added succefully")



    def get_rules(self, log=0):
        try :
            access_token = os.environ.get('ACCESS_TOKEN_TWT')
            response = requests.get(self.stream_rules_url, headers=self.auth(access_token))
            if (response.status_code is not 200) :
                raise Exception(response.text)
            if (log == 1) :
                pprint(response.json())
        except Exception as err :
            print(err)
            sys.exit()
        finally :
            if (log == 1) :
                pprint(response.json())
            return (response.json())
    
    def reset_rules(self):
        rules = self.get_rules(0)
        rules_ids = list()
        if ('data' not in rules):
            print('Empty set of rules.')
            return
        for rule in rules['data']:
            rules_ids.append(rule['id'])
        rules = dict({'delete': {"ids" : rules_ids}})
        try :
            acces_token = os.environ['ACCESS_TOKEN_TWT']
            response = requests.post(self.stream_rules_url, headers=self.auth(acces_token), json=rules)
            print(response.text)
        except Exception as err :
            print(err)
            sys.exit()
        finally :
            return (response.json())
        
        
