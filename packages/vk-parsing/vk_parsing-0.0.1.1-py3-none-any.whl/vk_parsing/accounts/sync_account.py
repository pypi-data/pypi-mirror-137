from .account import ParsingAccount
from vk_parsing.exceptions import *
import vk_api
import os
import datetime
import time
import random

VK_CONFIG_PATH = "parser.vk_config.v2.json"

def forward(response):
    return response

def captcha_handler(captcha): # TODO: that is cringe
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)

class VkApiAccount(ParsingAccount):
    def __init__(self, login, password, cooldown, logger):
        self.vk_session = None
        self.last_access = None
        super().__init__(login, password, cooldown, logger)    

    def auth(self):
        os.system("rm ./" + VK_CONFIG_PATH)
        self.vk_session = vk_api.VkApi(
            self.login, self.password,
            captcha_handler=captcha_handler,
            config_filename=VK_CONFIG_PATH
        )
        self.vk_session.http.headers['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0'
        self.vk_session.auth(token_only=True)

    def check(self):
        if (self.vk_session == None):
            raise RuntimeError("Auth() was not called") 
        try:
            self.method("account.getInfo")
            self.can_single = True
        except Exception as ex:
            self.logger.debug(f"{self.login} can_single failed: {str(ex)}")
            self.can_single = False 
        try:
            self.method("execute", {"code": "return [API.account.getInfo()];"})
            self.can_bucket = True
        except Exception as ex:
            self.logger.debug(f"{self.login} can_bucket failed: {str(ex)}")
            self.can_bucket = False
    
    def error_filter(self, ex):
        try:
            if not ex.code in [6, 9, 14, 29]:
                raise ex
            if ex.code in [5, 37]:
                raise StopParsingError(f"Parsing stopped on account {self.login}, error: {str(ex)}")
        except Exception:
            raise ex
        return

    def _obey_cooldown(self):
        if (self.last_access == None):
            self.last_access = datetime.datetime.now()
        now_time = datetime.datetime.now()
        difftime = now_time - self.last_access
        if (difftime.total_seconds() < self.cooldown):
            time.sleep(self.cooldown + self._exactly_small_random(self.cooldown) - difftime.total_seconds())
        self.last_access = datetime.datetime.now()

    def _exactly_small_random(self, core_value):
        return core_value / random.randint(1, 100)

    def method(self, method_name, method_args={}, callback=forward, callback_args=(), callback_kwargs={}):
        self._obey_cooldown()
        if (self.vk_session == None):
            raise RuntimeError("Auth() was not called")
        drop = False
        try:
            try:
                vk_response = self.vk_session.method(method_name, values=method_args)
            except Exception as ex:
                self.logger.debug(f"Error with {self.login}: {str(ex)}, trying again")
                self.error_filter(ex)
                self.logger.debug("This error passed filter, dropping account")
                drop = True
        except Exception as ex: # Case we raise the error
            self.logger.debug("This error didn't pass filter, raising this")
            raise
        if drop: # Case we drop the account
            raise BrokenAccountError("")
        try: # Case we call the callback
            return callback(vk_response, *callback_args, **callback_kwargs)
        except Exception as ex:
            self.logger.error(f"Error while calling callback: {str(ex)}")
            raise
