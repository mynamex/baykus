import logging

from apps.staff.models import Log


class LoggingHandler(logging.Handler):
    """Save log messages to MongoDB
    """
    def emit(self, record):

        Log.objects.create(
            message=self.format(record),
        )
