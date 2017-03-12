from indeed import IndeedClient
import pandas as pd
import textSim

class indeed:   
    
    #jobDataFrame 
    
    def __init__(self):
        self.jobDataFrame= pd.DataFrame();
        self.client = IndeedClient(8836246992678581);
        
    def skill(self,l):
        #print l
        #print " AND ".join(l)
        params = {
            'q' : " AND ".join(l),
            'l' : "phoenix",
            'userip' : "1.2.3.4",
            'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'limit' : "25",
            'start' : 0,
            'highlight' : 1
          
        }
        i = 25
        search_response = self.client.search(**params)
        results = []
        while(i<100 and i<search_response['totalResults']):        
            results += search_response['results']
            params['start'] += 25
            search_response = self.client.search(**params)
            results += search_response['results']
            i+=25
            print (params['start'])
        self.jobDataFrame = pd.DataFrame(results).drop_duplicates('jobkey')
        self.jobDataFrame.to_csv("sample.csv",encoding='UTF-8')
        return results    

    def skillOR(self,l):
        #print l
        #print " AND ".join(l)
        params = {
            'q' : " OR ".join(l),
            'l' : "phoenix",
            'userip' : "1.2.3.4",
            'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'limit' : "50"
        }
        
        search_response = self.client.search(**params)
        return search_response['results']

    
    def similarJobs(self,job):
        sampledfo = pd.read_csv("sample.csv",encoding='UTF-8')
        sampledf = sampledfo.copy()
        del sampledf['stations']
        del sampledf['Unnamed: 0']
        del sampledf['source']
        del sampledf['onmousedown']
        del sampledf['formattedLocation']
        del sampledf['formattedLocationFull']
        del sampledf['url']
        del sampledf['date']
        del sampledf['formattedRelativeTime']
        sampledf['indeedApply'] = [0 if x == 'false' else 1 for x in sampledf['indeedApply']]
        sampledf['expired'] = [0 if x == 'false' else 1 for x in sampledf['expired']]
        sampledf['sponsored'] = [0 if x == 'false' else 1 for x in sampledf['sponsored']]
        jobNo = "e5c7b9cbf1a50268"
        self.dataJob = sampledf.loc[sampledf['jobkey'] == jobNo]
        df= sampledf[sampledf["jobkey"] != jobNo]
#        df[''] = ['red' if x == 'Z' else 'green' for x in df['Set']]
        df.ix[df.city == self.dataJob.city.iloc[0], ['city','country','state']] = 1
        df.ix[df.city != 1, ['city','country','state']] = 0
        df.ix[df.company == self.dataJob.company.iloc[0], ['company']] = 1
        df.ix[df.company != 1, ['company']] = 0
    

#        df[''] = df.apply(my_test2, axis=1)

        df['snippet'] = [textSim.cosine_sim(x,self.dataJob.snippet.iloc[0]) for x in df['snippet']]
        df['jobtitle'] = [textSim.cosine_sim(x,self.dataJob.jobtitle.iloc[0]) for x in df['jobtitle']]
        
        df['variance'] = df['city'] + df['company'] + df['country'] + df['expired'] + df['indeedApply']+ 10*df['snippet']+5*df['jobtitle']
        
        result = df.sort(['variance'], ascending=False)
        #import pdb; pdb.set_trace()
        return result['jobkey'][:10].tolist()
        
indeed = indeed() 
#res = indeed.skill(["Python"])
sampledfo = pd.read_csv("sample.csv",encoding='UTF-8')
simList =  indeed.similarJobs("xyz")
simDict = []
for x in simList:
    s = sampledfo.loc[sampledfo['jobkey'] == x]
    simDict.append(s.to_dict())
#d = sampledfo.loc[sampledfo['jobkey'] == "e5c7b9cbf1a50268"]