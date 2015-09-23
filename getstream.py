import tweepy,json
from datetime import datetime

# Authentication details. To  obtain these visit dev.twitter.com

consumer_key = 'h3mSe5fRU0wmXuJbcbQ8I5uUM'
consumer_secret = 'IhLlX9GSu1a4oQqDKPPOtRnwRMlT8e8Ndgq1tL14e0rBJx3lf6'
access_token = '125627409-tjCdFyi9VDGi7Doug0Adt2A5uxlyDSxO4Z8YQMUv'
access_token_secret = 'zjv0qipatsyeGnG5kGLcMzlQpfFBcP1ZvpFxQ4URpULBr'

fall = open('all.txt', 'w+')
fallj = open('all.json', 'w+')

totalnum=long(0)

# This is the listener, resposible for receiving data

class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
	global totalnum
        # Twitter returns data in JSON format - we need to decode it first
        tweet = json.loads(data)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
	actual_tweet = tweet['text'].encode('ascii','ignore')
        string =  '@%s:%s' % (tweet['user']['screen_name'],actual_tweet)
	newtab = ':\t'
	newline = '\n\n' 
	ctime = datetime.now().time()
	fall.write(string+newtab+str(ctime)+newline)
	fallj.write(str(tweet))
	totalnum +=1
	print str(totalnum)+" tweet(s) so far."
	return True
    def on_error(self, status):
        print status
	return True
def main():
        l = StdOutListener()
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
	print "Currently running.....\n"
        # There are different kinds of streams: public stream, user stream, multi-user streams
        # In this example follow #programming tag
        # For more details refer to https://dev.twitter.com/docs/streaming-apis
        stream = tweepy.Stream(auth, l)
        stream.filter(track=['#mufc','#MUFC','#cfc','#CFC','#lfc','#LFC'])
if __name__ == '__main__':
    try:
	main()	
    except KeyboardInterrupt:
	global totalnum
	print 'The total number of tweets are:- '+str(totalnum)
        print '\nGoodbye!\n'
	fall.close()
