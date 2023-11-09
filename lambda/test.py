import json
import requests
import clarifai_keyword_call as ckc
import clarifai_sentiment_call as csc
import rds_connector as rdsc

# set api key (currently: Soham's)
newscatcher_dict = {
    "headers" : {"x-api-key": "ShxLGMc-1lxB9uRimqA5NSHaihERfB0414nR_b71rq8"},
    "querystring" : {"when":"24h", "lang":"en", "ranked_only":"True", "page_size":100},
    "url" : "https://api.newscatcherapi.com/v2/latest_headlines"
}

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:()')

query_results = ""
for i in range(1):
    sql_stmt = "INSERT INTO Articles (link, title, pub_date, sentiment, category, summary) VALUES\n"
    newscatcher_response = requests.request("GET", newscatcher_dict["url"], 
        headers=newscatcher_dict["headers"], 
        params=newscatcher_dict["querystring"])

    curr_dict = newscatcher_response.json()
    articles_list = curr_dict['articles']
    count = 1
    for article in articles_list:
        #each article is of type dict
        link = article['link']
        title = ''.join(filter(whitelist.__contains__, article['title']))[:2430]
        pub_date = article['published_date'] # should already be in DATETIME format
        summary = ''.join(filter(whitelist.__contains__, article['summary']))[:2430]
        category = article['topic']
        
        if (category == None) or (category == "news"):
            #now we process excerpt for categories using clarafai model
            curr_keyword_giver = ckc.Keyword_giver(title)
            # keywords will be in a list
            category = curr_keyword_giver.get_keywords()
            if len(category) == 0:
                print(str(count) + " failed at CATEGORY")
                count += 1
                continue # don't want to add this article to our DB if category field is empty (i.e. an error occured)

        # processing sentiment analysis
        curr_sentiment_giver = csc.Sentiment_giver(summary)
        sentiment_value = curr_sentiment_giver.get_sentiments() # [positive, neutral, negative]
        if len(sentiment_value) == 0:
            print(str(count) + " failed at SENTIMENT")
            count += 1
            continue
        sentiment = sentiment_value[0] - sentiment_value[2] #positive value minus negative value

        #making sure title doesn't have any double quotes to mess up our sql statement
        title.replace('"','')

        sql_stmt += "\t('" + link + "', '" + title + "', '" + pub_date + "', " + str(sentiment) + ", '" + category + "', '" + summary + "'),\n"
        print(str(count) + " success!!!")
        count += 1

    # now we've added all article tuples into sql_stmt
    sql_stmt = sql_stmt[:-2]
    sql_stmt += ";"

    # now we must run sql_stmt on RDS
    rds_cnctr = rdsc.RDS_connector(sql_stmt) #this will print something to console if an error occurs
    query_results += "RESULTS OF API CALL #" + str(i+1) + " ...\n" + rds_cnctr.add_tuples() + "\n\n"
    print(query_results)