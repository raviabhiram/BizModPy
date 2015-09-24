from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import matplotlib.pyplot as plt
import re
import string
import pylab
# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = "Kl1uMbHmRcRXRFf5UGcF4Pvhb"
consumer_secret = "e2InX8odyXcrDLwXeQhpHWmrj8Iq9LH48yn5L6UbDzDER6DpSN"
access_token = "746495640-s786UjERJxpMnw8rUfFPRp0WdN0yxuG4B9qrN9UV"
access_token_secret = "ld7kzIQsU2QRJeoRZREi0YLkUnmQNOqGraTfPus6f3EsW"

#listener thatprints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    #l = StdOutListener()
    #auth = OAuthHandler(consumer_key, consumer_secret)
    #auth.set_access_token(access_token, access_token_secret)
    #stream = Stream(auth, l)

    #This line filters Twitter Streams to capture data by the keywords
    #stream.filter(track=['NapoliJuve','FCBAtleti'])

    #store tweets in txt file
    tweets_data_path = 'tweetdata2.1.txt'
    #tweets_data_path_epl = 'tweetdata_epl.txt'
    tweets = pd.DataFrame()

    def word_in_text(word, text):
        word = word.lower()
        text = text.lower()
        match = re.search(word,text)
        if match:
            return True
        return False
    
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")

    
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
            
        except:
            continue

    #print tweets_data
    print len(tweets_data)

    
    #print len(tweets_data_epl)

    

    tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
    tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
    tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, tweets_data)

    tweets_by_lang = tweets['lang'].value_counts()
    #print(tweets_by_lang)

    #graph to indicate the top 5 languages in which tweets were written
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Languages', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
    tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')
    #pylab.show()

    tweets_by_country = tweets['country'].value_counts()

    #graph to indicate the top 5 countries from which tweets were sent 
    fig, ax = plt.subplots()
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=10)
    ax.set_xlabel('Countries', fontsize=15)
    ax.set_ylabel('Number of tweets' , fontsize=15)
    ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
    tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')
    pylab.show()
    
    tweets['NapoliJuve'] = tweets['text'].apply(lambda tweet: word_in_text('NapoliJuve', tweet))
    tweets['FCBAtleti'] = tweets['text'].apply(lambda tweet: word_in_text('FCBAtleti', tweet))
    tweets['MUNSOU'] = tweets['text'].apply(lambda tweet: word_in_text('MUNSOU', tweet))

    print "Number of Napoli vs Juve tweets: " + str(tweets['NapoliJuve'].value_counts()[True])
    print "Number of Barcelona vs Atleti tweets: " + str(tweets['FCBAtleti'].value_counts()[True])
    print "Number of Manchester United vs Saints tweets: " + str(tweets['MUNSOU'].value_counts()[True])

    leagues=['NapoliJuve','FCBAtleti','MUNSOU']
    
    tweets_by_league=[tweets['NapoliJuve'].value_counts()[True],tweets['FCBAtleti'].value_counts()[True],tweets['MUNSOU'].value_counts()[True]]
    x_pos = list(range(len(leagues)))
    
    width = 0.8
    fig, ax = plt.subplots()
    plt.bar(x_pos, tweets_by_league, 0.8, alpha=1, color='g')

    # Setting axis labels and ticks
    ax.set_ylabel('Number of tweets', fontsize=15)
    ax.set_title('Ranking: NapoliJuve vs. FCBAtleti vs. MUNSOU', fontsize=10, fontweight='bold')
    ax.set_xticks([p + 0.4 * width for p in x_pos])
    ax.set_xticklabels(leagues)
    plt.grid()
    pylab.show()

    

