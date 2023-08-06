class ParsingAccount:
    def __init__(self, login, password, cooldown, logger):
        self.login = login
        self.password = password
        self.token = None
        self.cooldown = cooldown
        self.logger = logger
        self.can_single = False
        self.can_bucket = False

    def __hash__(self):
        return hash((self.login, self.token))

    def auth(self):
        pass

    def check(self):
        pass

    def error_filter(self, error):
        pass
 
    def method(self, method_name, args={}):
        pass
