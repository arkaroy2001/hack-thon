import json
import jsonpickle
import clarifai_keyword_call as cla

def lambda_handler(event, context):
    #assuming 'event' is a json file
    response = open(event, 'r').read()
    curr_dict = jsonpickle.decode(response)
    articles_list = curr_dict['articles']
    for article in articles_list:
        #each article is of type dict
        link = article['link']
        excerpt = article['excerpt']
        title = article['title']
        pub_date = article['published_date']
        summary = article['summary']

        #now we process excerpt for keywords using clarafai model
        curr_keyword_giver = cla.Keyword_giver(title)
        # keywords will be in a list
        keywords_list = curr_keyword_giver.get_keywords()

        sentiment_value = 0
        #TODO: everything else



    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
