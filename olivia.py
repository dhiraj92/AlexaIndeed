from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import indeedApi as indeed

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
    headlines = "NOPE"
    headline_msg = 'There is nothing implemented yet I have heard a lot of things are coming'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay... bye'
    return statement(bye_text)
	
@ask.intent("SkillIntent", mapping={'s1': 'skill', 'city':'City'}) #,'s3':'skilly','s4':'skillp','s5':'skillq' }) #,'Skill2':'Skill2','Skill3':'Skill3','Skill4':'Skill4','Skill5':'Skill5'})
def skill_intent(s1,city):
    
    #bye_text = 'I read these skills' + s1 + " " + str(city) #+ " " + str(s3) + " " + str(s4) + " " + str(s5)
    res = indeed.skill(['Python','Java'])
    statmentList = [x['jobtitle'] for x in res]
    return statement("......and.....".join(statmentList)) 
    
    
if __name__ == '__main__':
    app.run(debug=True)