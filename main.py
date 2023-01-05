from flask import Flask
import logging
import requests
import charset_normalizer as chardet
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import urllib
import http.cookiejar as cookielib
import urllib.request as urllib2
import urllib.parse
from HelloAnalytics import get_report,initialize_analyticsreporting,print_response
logging.basicConfig(filename='logs.log',level=logging.DEBUG)
app = Flask(__name__)

@app.route('/', methods=["GET"])

def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async 
    src="https://www.googletagmanager.com/gtag/js?id=UA-253043112-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-253043112-1');
    </script>
     """
    return prefix_google + "Hello World Welcome to website"
# Lab 2 y=test logger on python
@app.route('/logger', methods=["GET"])
def print_logs():
    app.logger.info('Info level log')
    with open('logs.log','r') as f:
        content_log=f.read()
    print(content_log)
    return content_log


#Google analytics
@app.route('/cookies', methods=["GET","POST"])
def cookies():
    req=requests.get("https://www.google.com/")
    return req.cookies.get_dict()
@app.route('/ganalytics', methods=["GET","POST"])
def ganalytics():
    req=requests.get("https://analytics.google.com/analytics/web/?hl=fr#/a253043112w348019541p282345821/admin/ga4-setup-assistant")
    return req.text

#@app.route('/loggin_google')
#def test_login():
#    username = 'bigchrismich@gmail.com' # Gmail Address
#    password = 'Bigong01759@' # Gmail Password
#    cookie_jar = cookielib.CookieJar() 
#    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar)) 
#    login_dict = urllib.parse.urlencode({'username' : username, 'password' :password}) 
#    opener.open('https://accounts.google.com/ServiceLogin', login_dict) 
#    response = opener.open('https://plus.google.com/explore')
#    return response.read()

@app.route('/users')
def fetch_users():
    SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    KEY_FILE_LOCATION = 'tp2-digital-traces-bcb0d46a6e65.json'
    VIEW_ID = '282345821'
    analytics = initialize_analyticsreporting()
    resp= get_report(analytics)
    print_response(resp)
    a=resp['reports'][0]['data']
    a.keys()
    x=a.values()
    print(type(x))
    k=[]
    for i in x:
      k.append(i)
      #print(";",i)
    b=k[3]
    print(type(b))
    for i in b:
      print(";",i)
    c=b[0]
    print(c['values'][0])
    #k=[]
    for e in a:
      k.append(e)
    print(k[1])
    p=k[1][0]
    print(p['values'][1])
    return "the number of visitors fetched is  "+p['values'][1]


#Request with oauth