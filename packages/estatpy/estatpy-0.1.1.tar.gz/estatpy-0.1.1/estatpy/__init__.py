import logging
from logging import NullHandler

__title__ = "estatpy"
__description__ = "e-Stat API Client"
__url__ = "https://github.com/poyo46/estatpy"
__version__ = "0.1.1"
__author__ = "poyo46"
__author_email__ = "poyo4rock@gmail.com"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2022 poyo46"

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
