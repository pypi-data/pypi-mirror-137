from .accounts.sync_account import VkApiAccount
from .task import ParsingTask
from .lconfig import *
from .exceptions import *
import logging.config

DEFAULT_SLEEP_TIME = 0.4
DEFAULT_BUCKET_SIZE = 25

def forward(response):
    return response

class Parser:
    # TODO: other ways to authorize
    def __init__(self, logins, passwords, account_klass = VkApiAccount, need_all = False, sleep_time = DEFAULT_SLEEP_TIME, bucket_size_limit = DEFAULT_BUCKET_SIZE, logger = None, need_logging = True):
        if not need_logging:
            logging.config.dictConfig(SILENT_CONFIG)
            self.logger = logging.getLogger(list(SILENT_CONFIG["loggers"].keys())[0])
        elif logger == None:
            logging.config.dictConfig(LOGGING_CONFIG)
            self.logger = logging.getLogger(list(LOGGING_CONFIG["loggers"].keys())[0]) 
        else:
            self.logger = logger
        self.logger.debug("Parser was created, logging enabled")
        self.bucket_size_limit = bucket_size_limit
        self.current_account_index = -1
        self.tasks = []
        self.accounts = []
        if bucket_size_limit > DEFAULT_BUCKET_SIZE:
            raise RuntimeError("Too large bucket_size_limit")
        if len(logins) != len(passwords):
            self.logger.error("Weird list lengths, aborting")
            raise RuntimeError("No match login-password: different lengths")
        for login, password in zip(logins, passwords):
            if (not isinstance(login, str)) or (not isinstance(password, str)):
                self.logger.error("Strings were expected, aborting")
                raise RuntimeError("Strings were expected")
        temp_accounts = []
        for login, password in zip(logins, passwords):
            temp_accounts.append(account_klass(login, password, sleep_time, self.logger))
        for account in temp_accounts:
            try:
                account.auth()
                account.check()
                self.accounts.append(account)
            except Exception as ex:
                if need_all:
                    self.logger.error(f"Account {account.login} auth[or the first request] failed with error: {str(ex)}")
                    raise
                self.logger.warning(f"Account {account.login} auth[or the first request] missed with error: {str(ex)}")
        
        # TODO
        # self.missed_percent / strategy
        # self.asynchronous = asynchronous
        # self.hold_accounts = hold_accounts
    
    def _get_next_account(self, need_single = False, need_bucket = False):
        if len(self.accounts) == 0:
            self.logger.error("No more accounts in Parser, aborting")
            raise RuntimeError("No more accounts at all")
        for i in range(len(self.accounts)):
            self.current_account_index += 1
            self.current_account_index %= len(self.accounts)
            account = self._get_current_account()
            acceptable = True
            if (need_single and not account.can_single):
                acceptable = False
            if (need_bucket and not account.can_bucket):
                acceptable = False
            if (acceptable):
                return account
        self.logger.error(f'No more accounts with need_single={need_single}, need_bucket={need_bucket}')
        raise RuntimeError(f'No more accounts with need_single={need_single}, need_bucket={need_bucket}')

    def _get_current_account(self):
        if len(self.accounts) == 0:
            self.logger.error("No more accounts in Parser, aborting")
            raise StopParsingError("No more accounts at all")
        return self.accounts[self.current_account_index]

    def _find_account_by_hash(self, hsh):
        for account in self.accounts:
            if (hsh == hash(account)):
                return account
        raise RuntimeError("No such account.")

    def _drop_current_account(self):
        self.logger.debug(f"Erasing {self._get_current_account().login}")
        self.accounts.pop(self.current_account_index)
        if len(self.accounts) == 0:
            self.logger.error("No more accounts in Parser, aborting")
            raise StopParsingError("No more accounts at all")
        self.current_account_index %= len(self.accounts)

    def direct_call(self, method, method_args = {}, callback = forward, callback_args=(), callback_kwargs={}):
        while(True):
            current_account = self._get_next_account(need_single=True, need_bucket=(True if (method == "execute") else False))
            
            try:
                return current_account.method(method, method_args, callback, callback_args, callback_kwargs)
            except BrokenAccountError as ex:
                self._drop_current_account() # Could raise StopParsingError
                continue

    def add_task(self, method, method_args, callback, callback_args=(), callback_kwargs={}):
        self.tasks += [ParsingTask(method, method_args, callback, callback_args, callback_kwargs)]
        if (len(self.tasks) > self.bucket_size_limit):
            raise StopParsingError("Bucket was somehow overloaded")
        if (len(self.tasks) == self.bucket_size_limit):
            while (len(self.tasks) > 0):
                self.execute_tasks()

    def execute_tasks(self):
        if (len(self.tasks) == 0):
            return
        code = "return ["
        for task in self.tasks:
            code += "API." + task.method + "(" + str(task.method_args) + "), " 
        code = code[:-2]
        code += "];"
        correct = self.direct_call("execute",
                        {"code": code},
                        self._execute_callbacks,
        )
        if not correct:
            self.logger.debug(f"Trying to understand if account needs mark can_backet=False with direct_calls")
            need_make_impotent = False
            hsh = hash(self._get_current_account())
            while self.tasks:
                task = self.tasks[0]
                self.tasks.pop(0)
                try:
                    self.direct_call(task.method, task.method_args, task.callback, task.callback_args, task.callback_kwargs)
                    need_make_impotent = True
                    break
                except StopParsingError as ex:
                    raise
                except Exception as ex:
                    pass
            if need_make_impotent:
                self.logger.debug("Result: can_bucket=False")
                try:
                    self._find_account_by_hash(hsh).can_bucket = False
                except Exception as ex:
                    print(ex)
                    pass
            else:
                self.logger.debug("Result: can_bucket=True")
        else:
            self.tasks = []

    def _execute_callbacks(self, response):
        size = len(self.tasks)
        for i in range(len(self.tasks)):
            if (isinstance(response[i], bool) and not response[i]):
                size -= 1
        if (size == 0):
            self.logger.debug("Whole bucket request failed (response[i] = False)") 
            return False

        for i in range(len(self.tasks)):
            if (isinstance(response[i], bool) and not response[i]):
                continue
            self.tasks[i].callback(response[i], *self.tasks[i].callback_args, **self.tasks[i].callback_kwargs)
        return True
