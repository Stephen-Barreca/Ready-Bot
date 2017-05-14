import os
import time
import random
from slackclient import SlackClient

# constants
BOT_ID = os.environ.get('bot_id')
TOKEN = os.environ.get('token')
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"
BOT_NAME = 'slackmate'
COMMANDS = ['do', 'what']
KEYWORDS = ['lunch']

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

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def handle_keyword(command, channel):
    """
        interperets keywords
    """
    response = None
    for lunch_key in ['lunch', 'ht?', 'harris teeter', ' ht', 'chipotle']:
        if lunch_key in command.lower():
            lunch_responses = ['Lunch! Did somebody say lunch?!',
                               'Sure let me just commit these changes',
                               "No thank. I'm pretty full on all this success we are having",
                               'https://media.tenor.co/images/8a01457a623ccd7582c6331b04194bf3/tenor.gif',
                               'http://stream1.gifsoup.com/view3/1860304/office-lunch-tray-o.gif',
                               'https: // media.giphy.com / media / v2StD0rQVBJni / giphy.gif',
                               'https://m.popkey.co/3b4c61/ldGm6_s-200x150.gif']
            response = random.SystemRandom().choice(lunch_responses)

    if response:
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                if AT_BOT in output['text']:
                    # return text after the @ mention, whitespace removed
                    return 'command', output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
                else:
                    for keyword in KEYWORDS:
                        if keyword in output['text']:
                            return 'keyword', output['text'], output['channel']
    return None, None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Slackmate connected and running!")
        while True:
            trigger, command, channel = parse_slack_output(slack_client.rtm_read())
            if trigger and channel:
                if trigger == 'keyword':
                    handle_keyword(command, channel)
                elif trigger == 'command':
                    handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
