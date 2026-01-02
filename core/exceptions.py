class BusinessError(Exception):
    code: str = "BUSINESS_ERROR"

    def __init__(self, message: str = ""):
        super().__init__(message)
        self.message = message
