from typing import List

from django.apps import AppConfig
from django.utils.functional import cached_property


class MeduxPluginAppConfig(AppConfig):
    """Common base class for all MedUX AppConfigs.

    All MedUX apps' AppConfigs must inherit from this class (or must at least implement this interface).
    """

    def initialize(self):
        """Initializes the application at setup time.

        This method is called from the "initialize" management command.
        It should set up basic data in the database etc., and needs to be idempotent.
        """

    @cached_property
    def compatibility_errors(self) -> List[str]:
        """checks for compatibility issues that can't be ignored for correct application function,
         and returns a list of errors.
        :returns a list of error strs"""

        return []

    @cached_property
    def compatibility_warnings(self) -> List[str]:
        """checks for compatibility issues that can be accepted for continuing, and returns a list of warnings.
        :returns a list of warning strs"""

        return []
