"""YoonikApiException module
"""


class YoonikApiException(Exception):
    """Custom Exception for the YooniK APIs."""
    def __init__(self, status_code: int, message: str):
        """ Class initializer.
        :param status_code: HTTP responde status code.
        :param message: Error message.
        """
        super(YoonikApiException, self).__init__()
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return ('Error when calling YooniK API:\n'
                '\tstatus_code: {}\n'
                '\tmessage: {}\n').format(self.status_code, self.message)