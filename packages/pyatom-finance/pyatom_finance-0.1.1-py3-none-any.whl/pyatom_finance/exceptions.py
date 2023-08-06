"""Custom exceptions"""


class StockCollectorRequesterError(Exception):
    """General exception for HTTP/HTTPS requests"""

    def __init__(self, reason, message, **kwargs):
        """Exception Init."""
        super(StockCollectorRequesterError, self).__init__(kwargs)
        self.reason = reason
        self.message = message

    def __str__(self):
        """Exception __str__."""
        return f"{self.__class__.__name__}: {self.reason}: {self.message}"


class AtomLoginError(Exception):
    """Atom login error exception"""

    def __init__(self, reason, message, **kwargs):
        """Exception Init."""
        super(AtomLoginError, self).__init__(kwargs)
        self.reason = reason
        self.message = message

    def __str__(self):
        """Exception __str__."""
        return f"{self.__class__.__name__}: {self.reason}: {self.message}"
