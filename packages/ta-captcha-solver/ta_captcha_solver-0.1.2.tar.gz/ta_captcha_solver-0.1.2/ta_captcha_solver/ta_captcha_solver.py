from collections import defaultdict

from .captcha.image_captcha import ImageCaptcha
from .captcha.re_captcha_v2 import ReCaptchaV2

from .exceptions import ParamsException


class TACaptchaSolver(object):
    """
    Main interface for package users

    Example:
        captcha = TACaptchaSolver.get(
            captcha_type="v2",
            browser=self.browser,
            captcha_guru_api_key=self.captcha_guru_api_key,
            click_xpath="//input[@id='recaptcha-demo-submit']",
            check_xpath="//div[@class='recaptcha-success']",
        )
        captcha.solve()
    """

    @staticmethod
    def get(**params):
        """
        Return instance of captcha according to provided params

        :param params: Captcha settings. Possible values:
            - captcha_type: 'v2' or 'image'. Required
            - browser: Instance of RPA.Browser.Selenium.Selenium(). Required for 'v2' and 'image' captcha in case image_source is not provided
            - captcha_guru_api_key: Valid api key. Required
            - image_xpath: Image with captcha. Required for image captcha if browser is provided.
            - input_xpath: Input token to this input field. Valid for image captcha
            - click_xpath: Click button after captcha solved
            - check_xpath: Search for locator after captcha submitted
            - upper: make Solved token.upper() for image captcha. Valid for image captcha
            - image_source: path to image file. Required for 'image' captcha if browser is not provided. 
        :raises ParamsException: if 'captcha_type' has unexisting captcha type
        """
        params = TACaptchaSolver.validate_params(**params)
        if "image" in params["captcha_type"]:
            return ImageCaptcha(**params)
        elif "v2" in params["captcha_type"]:
            return ReCaptchaV2(**params)
        else:
            raise ParamsException(
                "Incorrect captcha_type provided. Dont know what captcha need to solve!"
            )

    @staticmethod
    def validate_params(**params):
        """
        Check all provided params

        :return: validated params
        :raises ParamsException: if some param has incorrect value or required param doesnt exist
        """
        params = defaultdict(str, params)

        if not params["captcha_type"] or not isinstance(params["captcha_type"], str):
            raise ParamsException(
                "No captcha_type provided or incorrect data type. Dont know what captcha need to solve!"
            )
        if params["captcha_type"] == 'image':
            if not params["browser"] and (not params["image_source"]):
                raise ParamsException(
                    "No browser or image source provided. Cannot work without neither!"
                )
                
            elif params["browser"] and params["image_source"]:
                raise ParamsException(
                    "Browser and image source both provided. Dont know what source use to solve captcha! Please submit just one."
                )

            elif params["browser"] and (not params["image_xpath"]):
                raise ParamsException(
                    "No image_xpath provided. Cannot work witouht image with captcha!"
                )
        
            elif not (".jpg" in params["image_source"] or ".png" in params["image_source"]) and (not params["browser"]):
                raise ParamsException(
                    "No image path valid provided on image_source. Cannot work without a valid path!"
                )

        if params["captcha_type"] == 'v2':
            if not params["browser"]:
                raise ParamsException(
                    "No browser provided. Cannot work without any browser!"
                )
        if not params["captcha_guru_api_key"] or not isinstance(
            params["captcha_guru_api_key"], str
        ):
            raise ParamsException(
                "No api key provided or incorrect data type. Cannot work without third party API tool!"
            )

        return params
