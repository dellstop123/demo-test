from flask import Flask, redirect, url_for, session, render_template, request
from flask_oauth import OAuth
from flaskext.mysql import MySQL
import pymysql
# from urllib2 import Request, urlopen, URLError
# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = '685526582936-obe4bpvijn4s3p0luns5b42g5a7kj77l.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'bSbA0FzotoIMDHDBzrDz2heg'
# one of the Redirect URIs from Google APIs console
REDIRECT_URI = '/oauth2callback'

SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY
oauth = OAuth()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'resume'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)


google = oauth.remote_app('google', base_url='https://www.google.com/accounts/',
authorize_url='https://accounts.google.com/o/oauth2/auth', request_token_url=None,
request_token_params={
    'scope': 'https://www.googleapis.com/auth/userinfo.email', 'response_type': 'code'},
access_token_url='https://accounts.google.com/o/oauth2/token',
access_token_method='POST', access_token_params={'grant_type': 'authorization_code'},
consumer_key=GOOGLE_CLIENT_ID, consumer_secret=GOOGLE_CLIENT_SECRET)


@app.route('/')
def index():
 return render_template('google_login.html')
 access_token = session.get('access_token')
 if access_token is None:
   return redirect(url_for('login'))
 access_token = access_token[0]
 
 import urllib.request 

 headers = {'Authorization': 'OAuth '+access_token}
 req = urllib.request.Request('https://www.googleapis.com/oauth2/v1/userinfo',None, headers)
 try:
  res = urllib.request.urlopen(req)
  # return render_template('google_login.html')
 except urllib.error.URLError as e:
  if e == 401:
# Unauthorized - bad token
    session.pop('access_token', None)
    # return redirect(url_for('login'))
  return res.read()

 return res.read()

@app.route('/login')
def login():
 callback = url_for('authorized', _external=True)
 return google.authorize(callback=callback)


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
 access_token = resp['access_token']
 session['access_token'] = access_token, ''
 return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
 return session.get('access_token')

@app.route('/google_login',methods = ['POST'])
def google_login():
 text1 = request.form.get('text1')
 text2 = request.form.get('text2')
 text3 = request.form.get('text3')
 text4 = request.form.get('text4')
 text5 = request.form.get('text5')
 conn = mysql.connect()
 cursor = conn.cursor()
 cursor.execute("Insert into social_login(username,email,phone_number,Authorization,social_platform_id,created_at) values(%s,%s,%s,%s,%s,%s)",(text1,text2,text3,text4,text5,''))     
 conn.commit()
 cursor.close()
 return "Inserted Successfully"
    

def main():
 app.run(debug=True, port= 5000)

if __name__ == '__main__':
 main()
