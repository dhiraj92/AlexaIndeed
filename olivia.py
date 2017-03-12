from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import indeedApi as indeed

import logging
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, "/")


@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hello welcome to olivia app. I perform job searches based on your skills, and also the good old keyword search. So then, go ahead , ask me!'
    return question(welcome_message).reprompt("I didnt get you. Give me a skill or keyword.")
    
#==============================================================================================================
@ask.intent("YesIntent")
def share_headlines():
    result = "GoodBye"
    return statement(result)

#==============================================================================================================
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Cool. All the best for your job search!... byebye'
    return statement(bye_text)


@ask.intent("QueryIntent", mapping={'s1': 'Query'}) 
def skill_intent(s1):    
    session.attributes['skills'] = [s1]
    session.attributes['operation']="key"
    return question("Great keyword search then! Which city should the jobs be in?").reprompt("I didn't get you. Which city should the jobs be in?")
 
                    
        
@ask.intent("SkillIntent", mapping={'s1': 'skill', 's2':'skillx','s3':'skilly'}) 
def skill_intent(s1,s2,s3):
    skillList = []

    for skill in s1,s2,s3:

       if skill is not None:
          skillList.append(skill)
    session.attributes['skills'] = skillList
    session.attributes['operation'] = 'and'
    return question("Great! Which city should the jobs be in?").reprompt("I didn't get you. Which city should the jobs be in?")
 
            
#==============================================================================================================

@ask.intent("CityIntent", mapping={'city':'City'})
def getCity(city):

    
    session.attributes['city'] = city
    ques = "Looking for Jobs in "+city
    return question(ques + ". I can filter results to Full time or Intern positions. What would you prefer?").reprompt("Didn't get you. Would you like Intern positions or Full time?")


#==============================================================================================================        

@ask.intent("CategoryIntent",mapping={'jobtype':'Jobtype'})   
def getCategory(jobtype):
    #session.attributes['jobtype']=jobtype
    ind = indeed.indeed()
    session.attributes['jobtype'] = jobtype
    if session.attributes['operation'] == "and":
        res = ind.skill(session.attributes['skills'],session.attributes['city'],jobtype)
    elif session.attributes['operation'] == "or":
        res = ind.skillOR(session.attributes['skills'],session.attributes['city'],jobtype)
    else:
        res = ind.skill(session.attributes['skills'],session.attributes['city'],jobtype)
    session.attributes['jobList'] = res[:5]
    statmentList = [(x['jobtitle'],x['company'],x['url']) for x in res]
    urlList = ""
    count =1
    result = jobtype + " Jobs for"
    result = result + " and ".join(session.attributes['skills']) + " in " + session.attributes['city'] + " are " 
    for job in statmentList:
        if count < 6:
            result = result + " Job "  + str(count)+ ": " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
            urlList = urlList + str(count)+ " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
            count+=1
    return question(result + " I've sent this data in a card to your Alexa app. Do you want smiliar jobs to any of these jobs? Give me the job number.") \
            .standard_card(title= jobtype + 'Jobs for ' + " , ".join(session.attributes['skills']),
                       text=urlList)

    
    


#==============================================================================================================          
@ask.intent("SkillIntentOR", mapping={'s1': 'skill', 's2':'skillx','s3':'skilly'}) 
def skill_intentOR(s1,s2,s3):

    skillList = []

    for skill in s1,s2,s3:
       if skill is not None:
          skillList.append(skill)
    session.attributes['skills'] = skillList
    session.attributes['operation'] = 'or'
    return question("Great! Which city should the jobs be in?").reprompt("I didn't get you. Which city should the jobs be in?")
    
@ask.intent("findSimilar", mapping={'code':'code'}) 
def findSimilar(code):  
    ind = indeed.indeed()
    code = int(code)
    jobCode = session.attributes['jobList'][code-1]['jobkey']
    simJobs = ind.similarJobs(jobCode)
    
    statmentList = [(x['jobtitle'],x['company'],x['url']) for x in simJobs]
    urlList = ""
    count =1
    result = "Jobs similar to "
    result = result + (session.attributes['jobList'][code-1]['jobtitle'])+ " are " 
    for job in statmentList:
        if count < 6:
            result = result + " Job "  + str(count)+ ",  " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
            urlList = urlList + str(count)+ " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
            count+=1
    return statement(result + "  I've sent this data in a card to your Alexa app. All the best for your job search!") \
            .standard_card(title= session.attributes['jobtype'] + 'Jobs similar to Job ' + session.attributes['jobList'][code-1]['jobtitle'],text=urlList)
#==============================================================================================================
if __name__ == '__main__':
    app.run(debug=True)