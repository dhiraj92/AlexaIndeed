from indeed import IndeedClient

client = IndeedClient(8836246992678581)


def skill(l):
    #print l
    #print " AND ".join(l)
    params = {
        'q' : " AND ".join(l),
        'l' : "phoenix",
        'userip' : "1.2.3.4",
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'limit' : "50"
    }
    
    search_response = client.search(**params)
    return search_response['results']
    
#print skill(["Python","Java"])