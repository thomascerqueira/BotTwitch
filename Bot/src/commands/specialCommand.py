class SpecialCommand():
    def __init__(self):
        pass
    
    def help(self):
        raise NotImplementedError
    
    def execute(self, ws, message, **kwargs):
        raise NotImplementedError