import json
import jsonpickle
import clarifai_keyword_call as cla
import clarifai_sentiment_call as csc

def lambda_handler(event, context):
    #TODO:  call newscatcher API

    #assuming 'event' is a json file
    response = open(event, 'r').read()
    curr_dict = jsonpickle.decode(response)
    articles_list = curr_dict['articles']
    for article in articles_list:
        #each article is of type dict
        link = article['link']
        title = article['title']
        pub_date = article['published_date'] # should already be in DATETIME format
        summary = article['summary']
        
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
