"""
Validators configured for specific Fits Specs
"""
from dkist_fits_specifications import spec122
from dkist_fits_specifications import spec214
from dkist_fits_specifications.spec214 import level0

from dkist_header_validator.base_validator import SpecValidator
from dkist_header_validator.exceptions import SpecSchemaDefinitionException
from dkist_header_validator.exceptions import SpecValidationException

__all__ = [
    "spec122_validator",
    "Spec122ValidationException",
    "spec214_validator",
    "spec214_l0_validator",
    "Spec214ValidationException",
]


############
# SPEC-122 #
############


class Spec122ValidationException(SpecValidationException):
    """
    Exception when validating a spec 122 file
    """


spec122 = list(spec122.load_spec122().values())

spec122_validator = SpecValidator(
    spec_schema=spec122,
    SchemaValidationException=Spec122ValidationException,
)


############
# SPEC-214 #
############
class Spec214ValidationException(SpecValidationException):
    """
    Exception when validating a spec 214 file
    """


spec214_l0 = list(level0.load_level0_spec214().values())

spec214_l0_validator = SpecValidator(
    spec_schema=spec214_l0,
    SchemaValidationException=Spec214ValidationException,
)

spec214 = list(spec214.load_spec214().values())


spec214_validator = SpecValidator(
    spec_schema=spec214,
    SchemaValidationException=Spec214ValidationException,
)
