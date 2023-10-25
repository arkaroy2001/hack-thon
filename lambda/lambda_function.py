import json
import jsonpickle
import requests
import clarifai_keyword_call as cla
import clarifai_sentiment_call as csc

# set api key (currently: Soham's)
newscatcher_dict = {
    headers = {"x-api-key": "ShxLGMc-1lxB9uRimqA5NSHaihERfB0414nR_b71rq8"},
    querystring = {"when":"24h","lang":"en","ranked_only":"True", "page_size":100},
    url = "https://api.newscatcherapi.com/v2/latest_headlines"
}

def lambda_handler(event, context):
    #TODO:  fix newscatcher GET call
    newscatcher_response = requests.request("GET", newscatcher_dict[url], 
        headers=newscatcher_dict[headers], 
        params=newscatcher_dict[querystring])

    curr_dict = jsonpickle.decode(newscatcher_response)
    articles_list = curr_dict['articles']
    for article in articles_list:
        #each article is of type dict
        link = article['link']
        title = article['title']
        pub_date = article['published_date'] # should already be in DATETIME format
        summary = ''.join(filter(whitelist.__contains__, article['summary']))[:2430]
        category = article['topic']
        
        if (category == None) or (category == "news"):
            tried_keyword_api = True
            #now we process excerpt for categories using clarafai model
            curr_keyword_giver = ckc.Keyword_giver(title)
            # keywords will be in a list
            category = curr_keyword_giver.get_keywords()
            if len(category) == 0:
                continue # don't want to add this article to our DB if category field is empty (i.e. an error occured)

        # processing sentiment analysis
        curr_sentiment_giver = csc.Sentiment_giver(summary)
        sentiment_value = curr_sentiment_giver.get_sentiments() # [positive, neutral, negative]
        if len(sentiment_value) == 0:
            continue

        # putting necessary fields into dictionary
        # putting necessary fields into dictionary
        dictionary = {
            "link": link,
            "title": title,
            "pub_date": pub_date,
            "sentiments": sentiment_value,
            "category": category,
            "summary": summary
        }

        # converting dictionary to json to eventually be pushed onto s3
        outfile = open("sample-db/article"+str(counter)+".json","w+")
        json.dump(dictionary, outfile)
        outfile.close()
        # delete file locally once finished uploading to S3
        #TODO: send current-article.json to s3



    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
