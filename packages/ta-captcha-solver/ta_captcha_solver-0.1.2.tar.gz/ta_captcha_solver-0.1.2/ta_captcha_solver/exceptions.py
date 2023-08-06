class APICaptchaNotReady(Exception):
    """
    API: Captcha is still being solved
    """

    pass


class APICaptchaUnsolvable(Exception):
    """
    API: Error that captcha cannot be solved
    """

    pass


class UICaptchaNotSolved(Exception):
    """
    UI: Cannot find xpath that indicates solved captcha
    """

    pass

class ImageCaptchaNotSolved(Exception):
    """
    UI: Cannot find image source for solve captcha
    """

    pass


class ParamsException(Exception):
    """
    Some params are missing for captcha resolving
    """

    pass


class LowBalanceException(Exception):
    """
    API tool balance is low
    """

    pass
