# Minimalist communication protocal

class BaseMessage:
    '''minimal class which may be used for writing custom Message implementations
    '''
    def __init__(self, data, *args, **kwargs):
        pass
        
class Message(BaseMessage):
    pass

