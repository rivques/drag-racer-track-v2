class ErrorType:
    NONE = 0
    RECOVERABLE = 1
    FATAL = 2

class Error:
    def __init__(self, error_code, short_msg):
        self.error_code = error_code
        self.short_msg = short_msg