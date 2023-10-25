# This is just scratch paper

import clarifai_sentiment_call as csc
import clarifai_keyword_call as ckc

summary = ["Look inside this stunning Bearsden villa worth over half a million pounds.",
            "Virtual Vet Telemedicine Market An Professional Research Report 2023-2030",
            "TT U19s win three-day opener against Jamaica"]
for s in summary:
    sentiment = ckc.Keyword_giver(s)
    lis = sentiment.get_keywords()
    print(lis)