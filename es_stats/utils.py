from dotmap import DotMap
import re
import logging

logger = logging.getLogger(__name__)

def fix_key(key):
    """Convert dotted key to dict structure."""
    return '[\'' + re.sub('\.', '\'][\'', key) + '\']'

def status_map(state):
    """Return a numeric value in place of the string value for state"""
    if state == 'green':
        return 0
    elif state == 'yellow':
        return 1
    elif state == 'red':
        return 2
    elif state == 'red':
        return 2
    else:
        return 3 # fail

def get_value(dotted, notation):
    """
    Return value from DotMap dictionary, accessed by dotted or dict notation
    """
    return eval("dotted" + notation)
