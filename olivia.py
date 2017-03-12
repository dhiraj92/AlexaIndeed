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
    welcome_message = 'Hello welcome to olivia application what can I do for you?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    #headlines = get_headlines()
    #headlines = "NOPE"
    #headline_msg = 'There is nothing implemented yet I have heard a lot of things are coming'.format(headlines)
    sessionAttr = session.attributes['resultset']
    print(sessionAttr)
    #result = [x['jobtitle'] for x in sessionAttr]
    return statement(result)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)
	
@ask.intent("SkillIntent", mapping={'s1': 'skill', 's2':'skillx','s3':'skilly','city':'City'}) 
def skill_intent(s1,s2,s3,city):
    skillList = []
    for skill in s1,s2,s3:
        if skill is not None:
            skillList.append(skill)
    res = indeed.skill(skillList)
    count = 1;
    session.attributes['resultset'] = res
    statmentList = [(x['jobtitle'],x['company'],x['url']) for x in res]
    
    if city is None:
         result = "I found these jobs for " + " and ".join(skillList) + " "
    else:
        result = "I found these jobs for " + " and ".join(skillList) + " in " + city + ". "
    urlList = ""
    for job in statmentList:
        result = result +  str(count)+ " " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
        
        if count < 10: 
            urlList = urlList + str(count)+ " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
        count+=1
    return question(result + ". Do you want me to filter data?") \
            .standard_card(title='Jobs for ' + " and ".join(skillList),
                       text=urlList)
    
@ask.intent("SkillIntentOR", mapping={'s1': 'skill', 's2':'skillx','s3':'skilly','city':'City'}) 
def skill_intentOR(s1,s2,s3,city):
    skillList = []
    for skill in s1,s2,s3:
        if skill is not None:
            skillList.append(skill)
    count = 1;
    res = indeed.skillOR(skillList)
    statmentList = [(x['jobtitle'],x['company']) for x in res]
    if city is None:
         result = "I found these jobs for " + "or ".join(skillList) + " "
    else:
        result = "I found these jobs for " + "or ".join(skillList) + " in " + city + ". "
    
    for job in statmentList:
        
        result = result +  str(count)+ " " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
        count+=1
    return question(result + ". Do you want me to filter data?") 
    
    
if __name__ == '__main__':
    app.run(debug=True)