"""This module is for  for sending alerts and monitoring stats to a slack channel"""

import json
import time
import traceback
import psutil
import requests

class Slack:
    """Class for sending alerts and monitoring stats to a slack channel"""

    @staticmethod
    def send_alert(message:str, url:str, user_id:str=None, send_error:bool=False):
        """
        This function send alert to a target channel tagging a user
                           with a alert message and traceback error.
        args:
                message     : Pass the message to be displayed in the channel
                url         : Pass webhook of target channel
                user_id     : Slack user_id of user who needs to be tagged (
                send_error  : This should be set True,
                             if slack_alert is called while catching exception
        returns: Nothing
        """

        if send_error is True:
            message = f"{message}\n{traceback.format_exc()}"
        if user_id is not None:
            payload = {"text": f'<@{user_id}> : {message}'}
        else:
            payload = {"text": f'{message}'}
        requests.post(url=url, data=json.dumps(payload))

    @staticmethod
    def start_monitoring():
        """function for initiating monitoring"""

        tic = time.time()
        initial_ram = psutil.virtual_memory().used/(1024*1000000)
        return (tic, initial_ram)

    @staticmethod
    def stop_monitoring():
        """function for end monitoring"""

        toc = time.time()
        final_ram = psutil.virtual_memory().used/(1024*1000000)
        return (toc, final_ram)

    @staticmethod
    def send_monitoring_stats(start:tuple, stop:tuple,message:str, url:str, user_id:str=None):

        """
        This function send run time and RAM usage for a cronjob
        to a target channel tagging a user with a  message

        Args:
                message : Pass the message to be displayed in the channel
                url : Pass webhook of target channel
                user_id : Slack user_id of user who needs to be tagged
                start : this should be set to output of start_monitoring function
                stop : this should be set to output of start_monitoring function
        """

        tic, initial_ram = start
        toc, final_ram = stop
        run_time = round(toc-tic)
        memory_usage = round(final_ram-initial_ram, 2)
        message = (f"{message}\n"
                   f"Total time taken : {run_time} sec\n"
                   f"Total RAM usage : {memory_usage} gb")
        if user_id is not None:
            payload = {"text": f'<@{user_id}> : {message}'}
        else:
            payload = {"text": f'{message}'}
        requests.post(url=url, data=json.dumps(payload))
