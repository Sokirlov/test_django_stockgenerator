from rest_framework.throttling import BaseThrottle
import time

class CreationPriceThrottle(BaseThrottle):
    """
    Price throttle to limit object creation to once every 5 seconds.
    For correct time use waite_time property
    """
    cache = {}
    waite_time = 5
    def allow_request(self, request, view):
        if request.method != self.request_method:
            return True
        user_identifier = self.get_ident(request)
        current_time = time.time()
        if user_identifier in self.cache:
            last_request_time = self.cache[user_identifier]
            if current_time - last_request_time < self.waite_time:
                return False
        self.cache[user_identifier] = current_time
        return True

    def __init__(self, request_method='POST'):
        super().__init__()
        self.request_method = request_method

    def wait(self):
        return self.waite_time
