
import sys


def patch():
    module = __import__('ftl_module_utils')
    sys.modules['ansible'] = module
