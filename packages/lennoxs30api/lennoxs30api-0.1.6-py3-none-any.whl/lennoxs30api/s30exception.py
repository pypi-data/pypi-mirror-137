EC_AUTHENTICATE = 1
EC_LOGIN = 2
EC_NEGOTIATE = 3
EC_SUBSCRIBE = 4
EC_RETRIEVE = 5
EC_REQUEST_DATA_HELPER = 6
EC_BAD_PARAMETERS = 7
EC_SETMODE_HELPER = 8
EC_PUBLISH_MESSAGE = 9
EC_PROCESS_MESSAGE = 10
EC_COMMS_ERROR = 11
EC_NO_SCHEDULE = 12
EC_HTTP_ERR = 13
EC_LOGOUT = 14
EC_CONFIG_TIMEOUT = 15
EC_UNAUTHORIZED = 401


class S30Exception(Exception):
    def __init__(self, value: str, error_code: int, reference: int) -> None:
        """Initialize error."""
        super().__init__(self, value)
        self.message = value
        self.error_code = error_code
        self.reference = reference

    def as_string(self) -> str:
        return f"Code [{self.error_code}] Reference [{self.reference}] [{self.message}]"

    pass
