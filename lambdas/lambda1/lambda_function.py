import clarifai_keyword_call as ckc
import clarifai_sentiment_call as csc
import rds_connector as rdsc
import json
from newscatcherapi import NewsCatcherApiClient

# set api key (currently: Arka's Pro Plan Trial)
newscatcherapi = NewsCatcherApiClient(x_api_key='hbbY3NYx4ObIX_D5piArtou9irDsbhRkrHj7qGRXi1w')

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ.,;:-')

def lambda_handler(event, context):
    query_results = ""
    for i in range(25):
        sql_stmt = "INSERT INTO Articles (link, title, pub_date, sentiment, category, summary) VALUES "
        
        curr_dict = newscatcherapi.get_latest_headlines(lang='en',when='24h',page_size=100,ranked_only=True,page=i+1)

        articles_list = curr_dict['articles']
        summary_arr = []
        title_arr = []

        curr_ind = 0
        for article in articles_list:
            if article['summary'] is None or len(article['summary']) == 0:
                continue
            
            # our particular sentiment analysis model can only take a maximum of 512 words
            summary = ''.join(filter(whitelist.__contains__, article["title"]))
            x = summary.split()
            num_words = len(x)
            if num_words > 400:
                x = x[:400]
                num_words = 400
            if num_words < 2:
                continue
            
            summary = ' '.join(x)
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
            print("API call#", i+1, " failed!")
            print(sentiment_values)
            print(categories)
            continue

        article_id = 0
        for article in articles_list:
            if article['summary'] is None or len(article['summary']) == 0:
                continue
            
            # our particular sentiment analysis model can only take a maximum of 512 words
            summary = ''.join(filter(whitelist.__contains__, article["title"]))
            x = summary.split()
            num_words = len(x)
            if num_words > 400:
                x = x[:400]
                num_words = 400
            if num_words < 2:
                continue
            
            #each article is of type dict
            link = article['link']
            title = article['title'].replace("'","") # sql statements use single quotes to wrap around strings (don't want to mess with that)
            pub_date = article['published_date'] # should already be in DATETIME format
            summary = article['summary'].replace("'","")
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
        query_results += "RESULTS OF API CALL #" + str(i+1) + ": " + rds_cnctr.add_tuples() + "..."

    return {
        'statusCode': 200,
        'body': json.dumps(query_results)
    }