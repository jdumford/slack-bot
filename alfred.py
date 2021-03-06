
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import ssl as ssl_lib
import certifi

from tokens import SIGNING_SECRET, SLACK_TOKEN, JIRA_SERVER, JIRA_USER, JIRA_TOKEN
from jira import JIRA
from httpRequests import getUserName
import responses


# Add encryption
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

# Create Flask Server
app = Flask(__name__)

# Set up communication with Slack Events API
slack_events_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)
slack_web_client = WebClient(token=SLACK_TOKEN, ssl=ssl_context)

# Connect with JIRA
options = {'server': JIRA_SERVER}
jira = JIRA(options=options, basic_auth=(JIRA_USER, JIRA_TOKEN))


message_IDs = set()

user_states = {}



def createJiraIssue(userId, message):
    userName = getUserName(userId)
    issue_dict = {
        'project': 'SBI',
        'summary': f'Alfred Bot Recieved a Slack Message from {userName}',
        'description': message,
        'issuetype': {'name': 'Task'},
    }
    new_issue = jira.create_issue(fields=issue_dict)

# def sendHelpDeskEmail(userId, slackMessage):
#     #TO-DO: generate email containing info about the user's problem
#     context = ssl_lib.create_default_context()
#     # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#     with smtplib.SMTP('smtp.gmail.com',587) as server:
#         server.connect("smtp.gmail.com",587)
#         server.ehlo()
#         server.starttls()
#         server.ehlo()
#         server.login("topgunbots@gmail.com", 'Slack12345!!')
#         sender = 'topgunbots@gmail.com'
#         receivers = ['hectorscreativeworld@gmail.com', 'jacobdumford@gmail.com']
#         emailBody = f"""Subject: New Help Desk Message

#         Alfred has recieved a new message on Slack.
#         User ID: {userId}
#         Message: {slackMessage}
#         """
#         print(emailBody)
#         server.sendmail(sender, receivers, emailBody)




# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack_events_adapter.on("message")
def message(payload):

    event = payload["event"]
    if event.get('bot_id') is None:
        messageID = event['client_msg_id']
        if messageID in message_IDs:
            return

        message_IDs.add(messageID)
    
        channel_id = event["channel"]
        user_id = event["user"]
        text = event["text"]
        response_message = {
            "channel": channel_id,
            "username": "Alfred"
        }


        # if user_id not in user_states.keys():
        #     user_states[user_id] = {'hey_alfred': False}


        if 'hey alfred' in text.lower():
            response_message["blocks"] = responses.heyAlfredResponse(user_id)
        elif 'dad joke' in text.lower():
            response_message["blocks"] = responses.dadJoke()
        elif 'support' in text.lower():
            response_message["blocks"] = responses.jiraResponse(user_id, text)
            createJiraIssue(user_id, text)
        

        slack_web_client.chat_postMessage(**response_message)
        
        
if __name__ == "__main__":
    app.run(port=3000)
