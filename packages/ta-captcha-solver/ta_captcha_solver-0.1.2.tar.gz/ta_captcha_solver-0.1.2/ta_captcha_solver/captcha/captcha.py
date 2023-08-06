from abc import ABC, abstractmethod
from collections import defaultdict


from ..exceptions import (
    UICaptchaNotSolved,
    ParamsException,
)

from ..browser.browser import Browser
from ..api.captcha_guru import CaptchaGuru


class Captcha(ABC):
    """
    Abstract base class for all captchas in this package
    """

    def __init__(self, **params):
        """
        :param params: Captcha settings. Possible values:
            - captcha_type: 'v2' or 'image'. Required
            - browser: Instance of RPA.Browser.Selenium.Selenium().  Required for 'v2' and 'image' captcha in case image_source is not provided
            - captcha_guru_api_key: Valid api key. Required
            - image_xpath: Image with captcha. Required if browser is provided
            - input_xpath: Input token to this input field. Valid for image captcha
            - click_xpath: Click button after captcha solved
            - check_xpath: Search for locator after captcha submitted
            - image_source: path to image file. Required for 'image' captcha if browser is not provided. 
            - upper: make Solved token.upper() for image captcha. Valid for image captcha
        """
               
        self.api_provider = CaptchaGuru(params["captcha_guru_api_key"])

        self.params = defaultdict(str, params)
  
        if not self.params["image_source"]:
            self.browser = Browser(params["browser"])

        self.token = None

    @abstractmethod
    def solve(self):
        """
        Core method that actually solves captcha according to settings
        """
        pass

    def click_solve_captcha(self):
        """
        Click 'click_xpath' element after captcha solved
        """
        self.browser.click_element_when_visible(self.params["click_xpath"])

    def check_captcha(self):
        """
        Check page contains 'check_xpath'. The last step of captcha solving workflow

        :raises UICaptchaNotSolved: if 'check_xpath' not found. This means that captcha is not solved
        """
        try:
            self.browser.wait_until_page_contains_element(
                self.params["check_xpath"], timeout=5
            )
        except:
            raise UICaptchaNotSolved()
