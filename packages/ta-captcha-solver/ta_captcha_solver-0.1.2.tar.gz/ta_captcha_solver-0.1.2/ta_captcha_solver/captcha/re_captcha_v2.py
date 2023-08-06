import logging

from .captcha import Captcha


class ReCaptchaV2(Captcha):
    """
    Google reCaptchaV2 solver
    """

    def solve(self):
        """
        Core method that performs solving according to previously provided settings

        :return: True if solved
        """
        self._get_data()
        self.api_provider.get_in(self.site_key, self.page_url)
        self.token = self.api_provider.get_res()
        self._put_token()

        if self.callback_function:
            self._execute_callback()

        if self.params["click_xpath"]:
            self.click_solve_captcha()

        if self.params["check_xpath"]:
            self.check_captcha()

        return True

    def _execute_callback(self):
        """
        One of the parts of solving workflow after token put to appropriate HTML tag
        """
        self.browser.execute_javascript(
            "{}('{}')".format(self.callback_function, self.token)
        )

    def _put_token(self):
        """
        Put token to appropriate HTML tag
        """
        self.browser.execute_javascript(
            "document.getElementById('g-recaptcha-response').innerHTML='{}'".format(
                self.token
            )
        )

    def _get_data(self):
        """
        Get all Google reCatpcha info. Obtains info for v2 and v3 captchas
        """
        data = self.browser.execute_javascript(
            """
        function findRecaptchaClients() {
  // eslint-disable-next-line camelcase
  if (typeof (___grecaptcha_cfg) !== 'undefined') {
    // eslint-disable-next-line camelcase, no-undef
    return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {
      const data = { id: cid, version: cid >= 10000 ? 'V3' : 'V2' };
      const objects = Object.entries(client).filter(([_, value]) => value && typeof value === 'object');

      objects.forEach(([toplevelKey, toplevel]) => {
        const found = Object.entries(toplevel).find(([_, value]) => (
          value && typeof value === 'object' && 'sitekey' in value && 'size' in value
        ));

        if (typeof toplevel === 'object' && toplevel instanceof HTMLElement && toplevel['tagName'] === 'DIV'){
            data.pageurl = toplevel.baseURI;
        }

        if (found) {
          const [sublevelKey, sublevel] = found;

          data.sitekey = sublevel.sitekey;
          const callbackKey = data.version === 'V2' ? 'callback' : 'promise-callback';
          const callback = sublevel[callbackKey];
          if (!callback) {
            data.callback = null;
            data.function = null;
          } else {
            data.function = callback;
            const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `['${key}']`).join('');
            data.callback = `___grecaptcha_cfg.clients${keys}`;
          }
        }
      });
      return data;
    });
  }
  return [];
}

let res = findRecaptchaClients();
return res
        """
        )
        logging.info(data)
        self.site_key = data[0]["sitekey"]
        self.page_url = data[0]["pageurl"]
        self.callback_function = data[0]["function"]
