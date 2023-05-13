from collections.abc import Callable, Iterable, Mapping
import threading
from typing import Any

class EmailTread(threading.Thread):

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
