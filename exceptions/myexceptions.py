

class MyException(Exception):
    def __init__(self, *args):
       self.args = args


class PageNumberError(MyException):
    def __init__(self, message="页码必须是整数同时大于0", arges=("页码错误")):
        self.message = message


class PageOutOFNumberError(MyException):
    def __init__(self, message="页码溢出", arges= ("页码错误")):
        self.message = message
