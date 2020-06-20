from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


APIkey = "HqeDlIpuh7QPu7hEuf1jhwH2r"
APIsecret = "pmV86PyIkGxK5XVbKyyVpwtRds3vpPXRKYZKfb8r3BVYn0jKx0"
atoken = "1266926371051311106-ROGQG00WNPWIndfTpILM3K3mtHPUDr"
asecret =  "qca3m9VdOUnvQDS0WIwz45zpjyoyTyEBpCbX10bojLOT2"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]
        #sentiment_value, confidence = s.sentiment(tweet)

        print(tweet)

        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(APIkey, APIsecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["TSLA"])