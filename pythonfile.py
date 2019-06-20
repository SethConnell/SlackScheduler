# Making Required Imports
from flask import Flask, redirect, request, url_for
app = Flask(__name__)
import requests
import os
import MySQLdb

# Setting slack ids.
clientid = os.getenv('slackclientid')
secretid = os.getenv('slacksecretid')

# Setting database variables.
serverusername = os.getenv("serverusername")
serverpassword = os.getenv("serverpassword")
dbpassword = os.getenv("dbpassword")
dbname = os.getenv("dbname")

globaltoken = ''

# Makes sure table exists. If not, it creates one.
conn = MySQLdb.connect("SethConnell.mysql.pythonanywhere-services.com", serverusername, dbpassword, dbname)
c = conn.cursor()
sql = "CREATE TABLE IF NOT EXISTS `users` (id int(11) NOT NULL auto_increment, username TEXT NOT NULL, password TEXT NOT NULL, slackid TEXT NOT NULL, primary key (id))"
c.execute(sql)


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/auth')
def authorization():
    return """<a href="https://slack.com/oauth/authorize?client_id=594967701703.626802000675&scope=incoming-webhook,chat:write:user"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>"""

# Setting homepage route.
@app.route('/')
def hello_world():
    return render_template('index.html', clientid=clientid)

# Setting authorization page
@app.route('/auth')
def authorization():
    return redirect("https://slack.com/oauth/authorize?client_id=" + clientid + "&scope=incoming-webhook")
    # """<a href="https://slack.com/oauth/authorize?client_id=""" + clientid + """&scope=incoming-webhook"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>"""

# Setting redirect route.
@app.route("/auth/redirect", methods=['GET', 'POST'])
def redirecting():
    if request.method == "POST":
        emailaddress = request.form['email']
        password = request.form["password"]
        retypedpassword = request.form["retypedpassword"]
        if password == retypedpassword and "@" in emailaddress and len(globaltoken) > 0:
            return "Email: " + str(emailaddress) + "<br>Password: " + str(password) + "<br>Usertoken: " + str(globaltoken)
    code = request.args.get('code')
    url = 'https://slack.com/api/oauth.access'
    try:
        payload = {'code': code, 'client_id': str(clientid), 'client_secret': str(secretid), "redirect_uri": "https://www.messageschedule.com/auth/redirect"}
        response = requests.get(url, params=payload)
        data = response.json()
        accesstoken = data["access_token"]
	    
    except HTTPError as e:
        status_code = e.response.status_code
        return status_code

    finally:
        import slack as slack
        f = str(data["access_token"])
        client = slack.WebClient(token=f)
        response = client.chat_postMessage(
            channel='#general',
            text="/shrug")
        assert response["ok"]
        assert response["message"]["text"] == "/shrug"
        global globalclientnid
        globaltoken = data["access_token"]
        return render_template('signup.html')
# Redirect route goes here to notify that the information has been successfully saved.
@app.route("/done", methods=['GET', 'POST'])
def done():
    return "you did it"

# This makes sure that the file is, in fact, the source file for the flask app.
if __name__ == '__main__':
    app.run(port=4390)
