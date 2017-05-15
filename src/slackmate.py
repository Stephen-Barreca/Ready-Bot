import os
import time
import random

from keywords import keywords, gifs
from slackclient import SlackClient

# constants
BOT_ID = os.environ.get('bot_id')
TOKEN = os.environ.get('token')
AT_BOT = "<@{}>".format(BOT_ID)
EXAMPLE_COMMAND = "do"
BOT_NAME = 'slackmate'
COMMANDS = ['do', 'what', 'calculate']
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

def handle_keyword(keyword, channel):
    """
        looks for keywords and chats back
        Keywords and responses are stored in responses.py
        make sure that you only responding to some (not all) off the keyword hits
        otherwise slackmate becomes really annoying, really fast.
    """
    ktp = KEYWORD_TRIGGER_PERCENT
    response = None
    trigger_roll = random.randint(0, 99)
    if trigger_roll < ktp:
        response = random.SystemRandom().choice(keywords[keyword])
    else:
        print('The almighty Rand Don has blocked this message')

    if response:
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def handle_gif(message, channel):
    """
    posts gifs that express the idea of the previous messages
    :param message:
    :param channel:
    :return:
    """
    ktp = KEYWORD_TRIGGER_PERCENT * 10
    message = message.lower()
    response = None
    trigger_roll = random.randint(0, 99)
    if trigger_roll < ktp:
        response = random.SystemRandom().choice(gifs[message])
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
                    return 'command', output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel'], output['user']

                elif output['text'] in gifs.keys():
                    return 'gif', output['text'], output['channel'], output['user']

                else:
                    for keyword in keywords.keys():
                        if keyword in output['text'].lower():
                            return 'keyword', keyword, output['channel'], output['user']
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
                elif trigger == 'gif':
                    handle_gif(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
