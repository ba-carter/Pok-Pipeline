import logging
import time
from utils.config import Config
import os

def get_request_delay():
    delay = Config.REQUEST_DELAY
    return float(delay)
