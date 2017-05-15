import os
import time
import random

from responses import lunch_responses, lunch_keywords
from slackclient import SlackClient

# constants
BOT_ID = os.environ.get('bot_id')
TOKEN = os.environ.get('token')
AT_BOT = "<@{}>".format(BOT_ID)
EXAMPLE_COMMAND = "do"
BOT_NAME = 'slackmate'
COMMANDS = ['do', 'what', 'calculate']
KEYWORDS = lunch_keywords
KEYWORD_TRIGGER_PERCENT = 100

slack_client = SlackClient(TOKEN)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    command = command.lower()
    response = "Not sure what you mean. Try the {} command with numbers, delimited by spaces.".format(EXAMPLE_COMMAND)
    if command.startswith('do'):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith('what'):
        response = "Sure...write some more code then I can do that!"
    elif command.startswith('calculate'):
        response = "Sure...write some more code then I can do that!"

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def handle_keyword(message, channel):
    """
        looks for keywords and chats back
    """
    message = message.lower()
    response = None
    for lunch_key in lunch_keywords:
        if lunch_key in message:
            trigger_roll = random.randint(0, 99)
            if trigger_roll < KEYWORD_TRIGGER_PERCENT:
                response = random.SystemRandom().choice(lunch_responses)
            else:
                print('The almighty Rand Don has blocked this message')

    if response:
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    #print(output_list)
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and 'bot_id' not in output:
                if AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return 'command', output['text'].split(AT_BOT)[1].strip().lower(), output['channel'], output['user']
                else:
                    for keyword in KEYWORDS:
                        if keyword in output['text']:
                            return 'keyword', output['text'], output['channel'], output['user']
    return None, None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Slackmate connected and running!")
        api_call = slack_client.api_call("users.list")
        if api_call.get('ok'):
            # retrieve all users so we can find our bot
            users = api_call.get('members')
            for user in users:
                if 'name' in user and user.get('name') == BOT_NAME:
                    print("Bot ID for '{}' is {}".format(user['name'], user.get('id')))
        else:
            print("could not find bot user with the name {}".format(BOT_NAME))
        while True:
            trigger, command, channel, user = parse_slack_output(slack_client.rtm_read())
            if trigger and channel:
                if trigger == 'keyword':
                    handle_keyword(command, channel)
                elif trigger == 'command':
                    handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
