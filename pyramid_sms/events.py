from pyramid.request import Request


class SMSEvent:
    """Base class for SMS events.

    All events are fired within the web application process.
    """
    def __init__(self, request: Request, receiver: str, text_body: str, sender: str, user_dialog: bool):
        self.request = request
        self.receiver = receiver
        self.text_body = text_body
        self.sender = sender
        self.user_dialog = user_dialog


class SMSSent(SMSEvent):
    """Outbound SMS sent."""



