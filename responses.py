import requests
from bs4 import BeautifulSoup
import random

keyWordLinks = {
    'zoom': 'https://zoom.us/',
    'slack': 'https://slack.com/'
}

# For when the user has never initiated contact with Alfred before
def heyAlfredPrompt(userId):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hello  <@{userId}>, I am taken a nap please type 'Hey Alfred' and if you want to wake me up .",
            },
        }
    ]
    return blocks

# Responding whenever someone says "Hey Alfred"
def heyAlfredResponse(userId):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hello <@{userId}>, I am a bot designed to help solve your problems.",
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Would you please describe your problem, so I can send an email to our Help Desk?",
            },
        }
    ]
    return blocks

# Informs the user that a Jira ticket has been created
def jiraResponse(userId, text):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Thank you <@{userId}>. I genarated helpdesk ticket for and you should receive a respond in a few moments.",
            }
        }
    ]

    for k in keyWordLinks.keys():
        if k in text.lower():
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"I see that you need help with {k}. Check out this link. It might help: {keyWordLinks[k]}",
                }
            }
            blocks.append(block)

    return blocks

def dadJoke():
    # Create the "blocks" object to be sent to slack
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "So you want to hear a dad joke? Try this one: ",
            }
        }
    ]

    
    

    # Visit the url of the dad jokes
    URL = 'https://www.countryliving.com/life/a27452412/best-dad-jokes/'
    page = requests.get(URL)

    # "scrape" the website to obtain a list of dad jokes
    soup = BeautifulSoup(page.content, 'html.parser')
    articleBody = soup.find('div', attrs={'class': 'article-body-content'})
    jokes = articleBody.findAll('li')

    # randomly select 1 joke
    rand_index = random.randint(0, len(jokes)-1)
    joke = jokes[rand_index].text

    # put joke in a "block" object and append that block to the list
    block = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": joke,
            }
        }
    blocks.append(block)

    # return object
    return blocks