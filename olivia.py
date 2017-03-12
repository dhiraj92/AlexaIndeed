from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import indeedApi as indeed
<<<<<<< HEAD
import logging
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
=======
from random import randint
import logging
log = logging.getLogger()
>>>>>>> cb3760b17148aed3d7ee94c12163ae730afb6afd
app = Flask(__name__)
ask = Ask(app, "/")


@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hello welcome to olivia app. What skills are you looking for?'
    return question(welcome_message)
    
#==============================================================================================================
@ask.intent("YesIntent")
def share_headlines():
    #headlines = get_headlines()
    #headlines = "NOPE"
    #headline_msg = 'There is nothing implemented yet I have heard a lot of things are coming'.format(headlines)
<<<<<<< HEAD
    sessionAttr = session.attributes['resultset']
    print(sessionAttr)
    #result = [x['jobtitle'] for x in sessionAttr]
=======
    result= ""
    result = [x['jobtitle'] for x in session.attributes['resultset']]
>>>>>>> cb3760b17148aed3d7ee94c12163ae730afb6afd
    return statement(result)

#==============================================================================================================
@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)
def _json_date_handler(obj):
        return obj
@ask.intent("SkillIntent", mapping={'s1': 'skill', 's2':'skillx','s3':'skilly'}) 
def skill_intent(s1,s2,s3):
#    skillList = []
#    ind = indeed.indeed()
#    for skill in s1,s2,s3:
#        if skill is not None:
#            skillList.append(skill)
#    res = ind.skill(skillList)
#    count = 1;
#   
#    session.attributes['resultset'] = res
#    #session.attributes_encoder = _json_date_handler
#    statmentList = [(x['jobtitle'],x['company'],x['url']) for x in res]
#    
#    if city is None:
#         result = "I found these jobs for " + " and ".join(skillList) + " "
#    else:
#        result = "I found these jobs for " + " and ".join(skillList) + " in " + city + ". "
#    urlList = ""
#    for job in statmentList:
#        if count < 6:
#            result = result +  str(count)+ " " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
#            urlList = urlList + str(count)+ " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
#            count+=1
#    return question(result + ". Do you want me to filter data?") \
#            .standard_card(title='Jobs for ' + " and ".join(skillList),
#                       text=urlList)
    skillList = []

    for skill in s1,s2,s3:
<<<<<<< HEAD
        if skill is not None:
            skillList.append(skill)
    res = indeed.skill(skillList)
    count = 1;
    session.attributes['resultset'] = res
    statmentList = [(x['jobtitle'],x['company'],x['url']) for x in res]
=======
       if skill is not None:
          skillList.append(skill)
    session.attributes['skills'] = skillList
    session.attributes['operation'] = 'and'
    return question("Great! Which city should the jobs be in?")
 
            
#==============================================================================================================

@ask.intent("CityIntent", mapping={'city':'City'})
def getCity(city):
>>>>>>> cb3760b17148aed3d7ee94c12163ae730afb6afd
    
    session.attributes['city'] = city
    ques = "Looking for Jobs in "+city
    return question(ques + ". I can filter results to Full time or Intern positions. What would you prefer?")


#==============================================================================================================        

@ask.intent("CategoryIntent",mapping={'jobtype':'Jobtype'})   
def getCategory(jobtype):
    #session.attributes['jobtype']=jobtype
    ind = indeed.indeed()
    if session.attributes['operation'] == "and":
        res = ind.skill(session.attributes['skills'],session.attributes['city'],jobtype)
    elif session.attributes['operation'] == "or":
        res = ind.skillOR(session.attributes['skills'],session.attributes['city'],jobtype)
    statmentList = [(x['jobtitle'],x['company'],x['url']) for x in res]
    urlList = ""
    count =1
    result = ""
    for job in statmentList:
        if count < 6:
            result = result +  str(count)+ " " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
            urlList = urlList + str(count)+ " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
            count+=1
    return question(result) \
            .standard_card(title='Jobs for ' + " or ".join(session.attributes['skills']),
                       text=urlList)

    
    


#==============================================================================================================          
@ask.intent("SkillIntentOR", mapping={'s1': 'skill', 's2':'skillx','s3':'skilly'}) 
def skill_intentOR(s1,s2,s3):
#    skillList = []
#    ind = indeed.indeed()
#    for skill in s1,s2,s3:
#        if skill is not None:
#            skillList.append(skill)
#    count = 1;
#    res = ind.skillOR(skillList)
#    session.attributes['resultset'] = res
#    statmentList = [(x['jobtitle'],x['company']) for x in res]
#    if city is None:
#         result = "I found these jobs for " + "or ".join(skillList) + " "
#    else:
#        result = "I found these jobs for " + "or ".join(skillList) + " in " + city + ". "
#    urlList = ""
#    for job in statmentList:
#        if count < 6:
#            result = result +  str(count)+ " " +job[0].replace("&","and")  + ", at " + job[1].replace("&","and")  + ", "
#            urlList = urlList + str(count)+ " " + job[0] + ", " + job[1] + " \n URL: " + job[2] + " \n "
#            count+=1
#    return question(result + ". Do you want me to filter data?") \
#            .standard_card(title='Jobs for ' + " or ".join(skillList),
#                       text=urlList)
    skillList = []

    for skill in s1,s2,s3:
       if skill is not None:
          skillList.append(skill)
    session.attributes['skills'] = skillList
    session.attributes['operation'] = 'or'
    return question("Great! Which city should the jobs be in?")
    

#==============================================================================================================
if __name__ == '__main__':
    app.run(debug=True)