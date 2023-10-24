# This is just scratch paper

import clarifai_sentiment_call as csc

summary = "Look inside this stunning Bearsden villa worth over half a million pounds."
sentiment = csc.Sentiment_giver(summary)
lis = sentiment.get_sentiments()
print(lis)