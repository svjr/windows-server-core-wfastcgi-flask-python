class ApplicationConfiguration:

    def __init__(self, token_secret=None, max_mb_file_upload=100, refresh_time_monitor=120, username=None,
                 password=None):
        self.__token_secret = token_secret
        self.__max_mb_file_upload = max_mb_file_upload
        self.__refresh_time_monitor = refresh_time_monitor
        self.__username = username
        self.__password = password

    def configure_build(self, cfg):
        self.__token_secret = cfg["app"]["token_secret"]
        self.__max_mb_file_upload = cfg["app"]["max_mb_file_upload"]
        self.__refresh_time_monitor = cfg["app"]["refresh_time_monitor"]
        self.__username = cfg["app"]["username"]
        self.__password = cfg["app"]["password"]

    @property
    def token_secret(self):
        return self.__token_secret

    @token_secret.setter
    def token_secret(self, token_secret):
        self.__token_secret = token_secret

    @property
    def max_mb_file_upload(self):
        return self.__max_mb_file_upload

    @max_mb_file_upload.setter
    def max_mb_file_upload(self, max_mb_file_upload):
        self.__max_mb_file_upload = max_mb_file_upload

    @property
    def refresh_time_monitor(self):
        return self.__refresh_time_monitor

    @refresh_time_monitor.setter
    def refresh_time_monitor(self, refresh_time_monitor):
        self.__refresh_time_monitor = refresh_time_monitor

    @property
    def username(self):
        return self.__username

    @username.setter
    def user(self, username):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password
