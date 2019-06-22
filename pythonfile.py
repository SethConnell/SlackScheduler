# Making Required Imports
from flask import Flask, redirect, request, url_for, session
app = Flask(__name__)
app.config["SECRET_KEY"] = "lkmaslkdsldsamdlsdmasldsmkdd"
import requests
import os
from dbfunctions import *

# Setting slack ids.
clientid = os.getenv('slackclientid')
secretid = os.getenv('slacksecretid')

globaltoken = ''

verifySetup()

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
    global globaltoken
    if request.method == "POST":
        emailaddress = request.form['email']
        password = request.form["password"]
        retypedpassword = request.form["retypedpassword"]
        if password == retypedpassword and "@" in emailaddress and len(globaltoken) > 0:
            session["user"] = emailaddress
            createUser(emailaddress, password, globaltoken)
            return "Everything created successfully!"
        else:
            return "Need to fix globaltoken setting."
    else:
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
            globaltoken = data["access_token"]
            return render_template('signup.html')
        
# Redirect route goes here to notify that the information has been successfully saved.
@app.route("/done", methods=['GET', 'POST'])
def done():
    return "you did it"

#Logs out user.
@app.route("/logout")
def logout():
    session.clear()
    return "You're all logged out."

# This makes sure that the file is, in fact, the source file for the flask app.
if __name__ == '__main__':
    app.run(port=4390)
