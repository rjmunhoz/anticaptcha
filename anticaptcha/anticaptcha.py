import json
import logging
import time
from base64 import b64encode

from . import session

TIMEOUT = 60  # max seconds to wait for result
WAIT_BEFORE_REQUESTS = 5  # wait seconds before starting to request for result
WAIT_BETWEEN_REQUESTS = 1


class Anticaptcha:
    def __init__(self, API_KEY):
        self.clientKey = API_KEY
        self.base_url = 'http://api.anti-captcha.com/'
        self.logger = logging.getLogger(__name__)

    def getBalance(self):
        """sends JSON data in POST request -> dict"""
        self.logger.info('[ANTICAPTCHA] GET BALANCE')
        url = self.base_url + 'getBalance'
        data = {'clientKey': self.clientKey}
        response = session.post(url, data=json.dumps(data)).json()
        self.logger.info('[ANTICAPTCHA] RESPONSE TO GET BALANCE: {}'.format(
            response))
        return response

    def createTask(self, bin_str):
        """binary content of file -> id of task in dict"""
        self.logger.info('[ANTICAPTCHA] CREATE TASK')
        url = self.base_url + 'createTask'
        img_str = b64encode(bin_str).decode('ascii')
        task = {'type': 'ImageToTextTask', 'body': img_str}
        data = {'clientKey': self.clientKey, 'task': task}
        response = session.post(url, data=json.dumps(data)).json()
        self.logger.info('RESPONSE TO CREATE TASK: {}'.format(response))
        return response

    def getTaskResult(self, task_id):
        """ -> dict with solution and extra info about task OR None"""
        self.logger.info('GET TASK RESULT')
        url = self.base_url + 'getTaskResult'
        time.sleep(WAIT_BEFORE_REQUESTS)
        total_sec = WAIT_BEFORE_REQUESTS
        data = {'clientKey': self.clientKey, 'taskId': task_id}
        while total_sec <= TIMEOUT:
            response = session.post(url, data=json.dumps(data)).json()
            if response.get('status') == 'processing':
                time.sleep(WAIT_BETWEEN_REQUESTS)
                total_sec += WAIT_BETWEEN_REQUESTS
                continue
            else:
                break
        else:
            return
        self.logger.info(
            '[ANTICAPTCHA] RESPONSE TO GET TASK RESULT: {}'.format(response))
        return response
