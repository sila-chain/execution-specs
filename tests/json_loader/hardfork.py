"""
Test-specific Hardfork subclass.

Extends the base Hardfork class with test infrastructure properties.
"""

from sila_spec_tools.forks import Hardfork


class TestHardfork(Hardfork):
    """
    Hardfork subclass with test-specific properties.

    This class extends the base Hardfork class with properties needed
    for test infrastructure, keeping test-specific concerns separated
    from the core fork metadata.
    """

    @property
    def json_test_name(self) -> str:
        """
        Name of the hard fork in the test json fixtures.
        """
        if self.title_case_name == "Tangerine Whistle":
            return "SIP150"
        elif self.title_case_name == "Spurious Dragon":
            return "SIP158"
        elif self.title_case_name == "Constantinople":
            return "ConstantinopleFix"
        else:
            return self.title_case_name
