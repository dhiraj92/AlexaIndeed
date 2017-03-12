from indeed import IndeedClient
import pandas as pd


class indeed:   
    
    #jobDataFrame 
    
    def __init__(self):
        self.jobDataFrame= pd.DataFrame();
        self.client = IndeedClient(8836246992678581);
        
    def skill(self,l,city,jobtype):
        #print l
        #print " AND ".join(l)
        params = {
            'q' : " AND ".join(l),
            'l' : "".join([city]),
            'jt' : "".join([jobtype]),
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

    def skillOR(self,l,city,jobtype):
        #print l
        #print " AND ".join(l)
        params = {
            'q' : " OR ".join(l),
            'l' : "".join([city]),
            'jt' : "".join([jobtype]),
            'userip' : "1.2.3.4",
            'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
            'limit' : "50"
        }
        
        search_response = self.client.search(**params)
        return search_response['results']

    
    def similarJobs(self,job):
        sampledf = pd.read_csv("sample.csv",encoding='UTF-8')        
        jobNo = "e5c7b9cbf1a50268"
        self.dataJob = sampledf.loc[sampledf['jobkey'] == jobNo]
        df= sampledf[sampledf["jobkey"] != jobNo]
        
        df.ix[df.city == self.dataJob.city.iloc[0], ['city','country','formattedLocation','formattedLocationFull','state']] = 1
        df.ix[df.city != 1, ['city','country','formattedLocation','formattedLocationFull','state']] = 0
        df.ix[df.company == self.dataJob.city.iloc[0], ['company','country','formattedLocation','formattedLocationFull','state']] = 1
        df.ix[df.city != 1, ['city','country','formattedLocation','formattedLocationFull','state']] = 0

#        df['city'] = ['red' if x == 'Z' else 'green' for x in df['Set']]
        del df['stations']
        del df['Unnamed: 0']
        import pdb; pdb.set_trace()
        
        return sampledf
        


#df =  indeed.similarJobs("xyz")
