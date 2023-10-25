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
        summary = article['summary']
        
        # uncomment the part below if we want to use the clarifai model for keywords
        """
        #now we process excerpt for keywords using clarafai model
        curr_keyword_giver = cla.Keyword_giver(title)
        # keywords will be in a list
        keywords_list = curr_keyword_giver.get_keywords()
        if keywords_list:
            continue # don't want to add this article to our DB if list is empty (i.e. an error occured)
        """

        # processing sentiment analysis
        curr_sentiment_giver = csc.Sentiment_giver(summary)
        sentiment_value = curr_sentiment_giver.get_sentiments() # [positive, neutral, negative]

        # putting necessary fields into dictionary
        dictionary = {
            "link" = link,
            "title" = title,
            "pub_date" = pub_date,
            "sentiments" = sentiment_value
            "summary" = summary
        }

        # converting dictionary to json to eventually be pushed onto s3
        with open("current-article.json", "w") as outfile: 
            json.dump(dictionary, outfile)
        #TODO: send current-article.json to s3



    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
