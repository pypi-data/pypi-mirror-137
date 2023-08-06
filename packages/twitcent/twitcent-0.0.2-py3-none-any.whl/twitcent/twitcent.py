#!/usr/bin/env python3
from textblob import TextBlob
import tweepy
import pandas as pd
import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import datetime as dt
import fire
from twitcent.user_data.config import main
#nltk.download('vader_lexicon') # Some sentiment analyser


class Tweets:
    
    user_params = main()
    
    def __init__(self, keyword, noOfTweets):
        self.keyword = keyword
        self.noOfTweets = int(noOfTweets)

    @classmethod
    def tweet_api(cls):
        auth = tweepy.OAuthHandler(cls.user_params.get('consumerKey'), cls.user_params.get('consumerSecret'))
        auth.set_access_token(cls.user_params.get('accessToken'), cls.user_params.get('accessTokenSecret'))
        return tweepy.API(auth)


    def get_tweets(self):
        try:
            return tweepy.Cursor(self.tweet_api().search_tweets,  q=self.keyword).items(self.noOfTweets)
        except Exception as e:
            print(e)

    def create_tweets_frame(self):
        tweet_list = []
        created = []
        for tweet in self.get_tweets():
            tweet_list.append(tweet.text)
            created.append(tweet.created_at)

        tweet_list = pd.DataFrame(tweet_list)
        tweet_list['created_at'] = created
        tweet_list.drop_duplicates(inplace = True)
        
        return tweet_list
    
    def preprocess_tweets(self):
        #Cleaning Text (RT, Punctuation etc)
        #Creating new dataframe and new features
        tw_list = pd.DataFrame(self.create_tweets_frame())
        tw_list["text"] = tw_list[0]
        #Removing RT, Punctuation etc
        remove_rt = lambda x: re.sub('RT @\w+: '," ",x)
        rt = lambda x: re.sub("(@[A-Za-z0–9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",x)
        tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
        tw_list["text"] = tw_list.text.str.lower()

        return tw_list

    def sentiments(self):
        #Calculating Negative, Positive, Neutral and Compound values
        tw_list = self.preprocess_tweets()
        tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))

        for index, row in tw_list['text'].iteritems():
            score = SentimentIntensityAnalyzer().polarity_scores(row)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            if neg > pos:
                tw_list.loc[index, 'sentiment'] = "negative"
            elif pos > neg:
                tw_list.loc[index, 'sentiment'] = "positive"
            else:
                tw_list.loc[index, 'sentiment'] = "neutral"
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp

        return tw_list

    def get_results(self, data, feature):
        total=data.loc[:,feature].value_counts(dropna=False)
        percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
        return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])


def sentiments_dict(keyword,noOfTweets):
    try:
        tw_list = Tweets(f'{keyword}', f'{noOfTweets}').sentiments()
        results = Tweets(f'{keyword}', f'{noOfTweets}').get_results(tw_list,"sentiment")

        results_dict = {
            'positive': {
                'total': results.loc['positive']['Total'],
                'percent': results.loc['positive']['Percentage']
            },
            'negative': {
                'total': results.loc['negative']['Total'],
                'percent': results.loc['negative']['Percentage']
            },
            'neutral': {
                'total': results.loc['neutral']['Total'],
                'percent': results.loc['neutral']['Percentage']
            }
        }

        return results_dict
    except Exception as e:
        print(e)

if __name__ == '__main__':
    fire.Fire(sentiments_dict)