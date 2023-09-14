import logging
from datetime import datetime

log = logging.getLogger("user_activity")

class LoggingMiddleware: 
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dash = "- " * 30
        equal = "=" * 50
        timestamp = "[{}]".format(datetime.now().strftime("%c"))
        user_details = "User: {}".format(request.user)
        request_details = "Request: {} {}".format(request.method, request.path)
        log.info(timestamp)
        log.info(user_details)
        log.info(request_details)
        if request.POST:
            log.info("Form Data:")
            for key, val in request.POST.items():
                log.info("  " + key + " - " + val)

        response = self.get_response(request)
        response_details = "Response: {} {}".format(response.status_code, response.closed)
        log.info(response_details)
        log.info(equal)
        return response