"""This module is for  for sending alerts and monitoring stats to a slack channel"""

import os
from slack_sdk import WebClient
from custom_utils.exceptions import SlackError

class Slack:
    """Class for sending alerts and monitoring stats to a slack channel"""

    def __init__(self, token=None):
        try:
            if token is not None:
                self.client = WebClient(token)
            else:
                self.client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
        except Exception as err:
            raise SlackError(err)  from err

    def send_alert(self, channel:str, message:str, uids:list=[]):
        """
        This function send alert to a target channel tagging a user
                            with a alert message and traceback error.
        args:
            channel     : Name of the channel (ex : #channel_name)
            message     : Pass the message to be displayed in the channel
            uids        : List of Slack user_ids  who needs to be tagged

        returns: Nothing
        """

        uids = [f"<@{uid}>" for uid in uids]
        uids = " ".join(uids)
        message = f'{uids}  {message}'
        print(message)
        self.client.chat_postMessage(channel=channel, text=message)


