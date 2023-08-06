from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution

from dkist_header_validator.exceptions import *
from dkist_header_validator.spec_validators import *

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "unknown"
