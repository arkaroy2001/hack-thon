import json
import requests
import clarifai_keyword_call as ckc
import clarifai_sentiment_call as csc
import rds_connector as rdsc

# set api key (currently: Arka's Pro Plan Trial)
newscatcher_dict = {
    "headers" : {"x-api-key": "hbbY3NYx4ObIX_D5piArtou9irDsbhRkrHj7qGRXi1w"},
    "querystring" : {"when":"24h", "lang":"en", "ranked_only":"True", "page_size":100},
    "url" : "https://api.newscatcherapi.com/v2/latest_headlines"
}

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:()')

def lambda_handler(event, context):
    query_results = ""
    for i in range(1):
        sql_stmt = "INSERT INTO Articles (link, title, pub_date, sentiment, category, summary) VALUES "
        newscatcher_response = requests.request("GET", newscatcher_dict["url"], 
            headers=newscatcher_dict["headers"], 
            params=newscatcher_dict["querystring"])

        curr_dict = newscatcher_response.json()
        articles_list = curr_dict['articles']
        summary_arr = []
        title_arr = []

        for article in articles_list:
            # our particular sentiment analysis model can only take a maximum of 512 words
            summary = ''.join(filter(whitelist.__contains__, article['summary']))[:512]
            summary_arr.append(summary)
            title_arr.append(article['title'])

        # processing sentiment analysis (clarifai)
        curr_sentiment_giver = csc.Sentiment_giver(summary_arr)
        sentiment_values = curr_sentiment_giver.get_sentiments()

        # processing keyword analysis (clarifai)
        curr_keyword_giver = ckc.Keyword_giver(title_arr)
        categories = curr_keyword_giver.get_keywords()

        # if any of the following output lists are empty, then there was an error in processing and we
        # should ignore the current batch of articles
        if len(sentiment_values) == 0 or len(categories) == 0:
            print(str(len(sentiment_values)))
            print(sentiment_values)
            print("\n")
            print(str(len(categories)))
            print(categories)
            continue

        article_id = 0
        for article in articles_list:
            #each article is of type dict
            link = article['link']
            title = article['title'].replace('"','')
            pub_date = article['published_date'] # should already be in DATETIME format
            summary = summary_arr[article_id]
            category = article['topic']
            
            # "news" is too trivial of a category
            if (category == None) or (category == "news"):
                if len(categories[article_id]) == 0:
                    article_id += 1
                    continue
                category = categories[article_id]

            sentiment = sentiment_values[article_id]

            # now adding to our sql statement
            sql_stmt += "\t('" + link + "', '" + title + "', '" + pub_date + "', " + str(sentiment) + ", '" + category + "', '" + summary + "'),\n"
            article_id += 1



        # now we've added all article tuples into sql_stmt
        sql_stmt = sql_stmt[:-2] # getting rid of last comma and new-line character
        sql_stmt += ";" # adding the semicolon for the SQL statement

        # now we must run sql_stmt on RDS
        rds_cnctr = rdsc.RDS_connector(sql_stmt) #this will print something to console if an error occurs
        query_results += "RESULTS OF API CALL #" + str(i+1) + " ...\n" + rds_cnctr.add_tuples() + "\n\n"

    return {
        'statusCode': 200,
        'body': json.dumps(query_results)
    }