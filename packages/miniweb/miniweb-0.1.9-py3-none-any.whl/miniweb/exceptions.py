
class MiniwebFrameworkException(Exception):
    pass

class PayloadTooLarge(MiniwebFrameworkException):
    pass

class LengthRequired(MiniwebFrameworkException):
    pass
