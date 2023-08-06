import logging
import json
import requests

from retry import retry

from ..exceptions import (
    APICaptchaNotReady,
    APICaptchaUnsolvable,
    ParamsException,
    LowBalanceException,
)


class CaptchaGuru(object):
    """
    API Interface for captcha.guru captcha solving provider.

    http://learn.captcha.guru/#/
    """

    def __init__(self, api_key):
        """
        Check captcha.guru account money balance before initialization

        :param str api_key: Valid captcha.guru api key
        """
        self.api_key = api_key
        self.api_request_id = None

        self.check_balance()

    def check_balance(self):
        """
        Check captcha.guru account money balance

        :raises ParamsException: if incorrect 'captcha_guru_api_key' provided
        :raises LowBalanceException: if money account balance is low
        """
        response = requests.get(
            "http://api.captcha.guru/res.php?action=getbalance&key={}&json=1".format(
                self.api_key
            )
        )
        json = response.json()
        logging.info(json)

        if json["request"] == "ERROR_WRONG_USER_KEY":
            raise ParamsException(
                "Incorrect captcha_guru_api_key provided. Cannot get data!"
            )
        if int(json["request"]) <= 10:
            raise LowBalanceException(
                "Captcha guru money balance is very low: {}! Put something there".format(
                    json["request"]
                )
            )

    def get_in(self, site_key, page_url):
        """
        Send GET to in.php endpoint. Obtain request id that should be used in get_res

        :param str site_key: reCaptcha site_key value
        :param str page_url: reCaptcha page_url value
        """
        response = requests.get(
            "http://api.captcha.guru/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}&json=1".format(
                self.api_key, site_key, page_url
            )
        )
        json = response.json()
        logging.info(json)
        self.api_request_id = json["request"]

    def post_in(self, post_body):
        """
        Send POST to in.php endpoint. Obtain request id that should be used in get_res

        :param str post_body: base64 encoded image
        """
        data = {
            "key": self.api_key,
            "method": "base64",
            "body": post_body,
            "json": 1,
        }
        response = requests.post("http://api.captcha.guru/in.php", data)
        json = response.json()
        logging.info(json)
        self.api_request_id = json["request"]

    @retry(APICaptchaNotReady, delay=3, tries=30)
    def get_res(self):
        """
        Send GET to res.php endpoint. Return token for request id

        :return: captcha token
        :raises APICaptchaNotReady: if CAPCHA_NOT_READY response
        :raises APICaptchaUnsolvable: if ERROR_CAPTCHA_UNSOLVABLE response
        """
        response = requests.get(
            "http://api.captcha.guru/res.php?key={}&action=get&id={}&json=1".format(
                self.api_key, self.api_request_id
            )
        )
        json = response.json()
        logging.info(json)
        if json["request"] == "CAPCHA_NOT_READY":
            raise APICaptchaNotReady()

        if json["request"] == "ERROR_CAPTCHA_UNSOLVABLE":
            raise APICaptchaUnsolvable()

        if json["status"] == 1:
            return json["request"]
