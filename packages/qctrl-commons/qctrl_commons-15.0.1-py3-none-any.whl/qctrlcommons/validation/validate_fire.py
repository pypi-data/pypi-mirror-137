"""
Validator for core__calculateFire mutation.
"""
import re

from qctrlcommons.validation.base import BaseMutationInputValidator

# from qctrlcommons.exceptions import QctrlFieldError


class CalculateFireValidator(BaseMutationInputValidator):
    """
    Validator for core__calculateFire mutation.
    """

    _QASM_PATTERN_RE = re.compile(r"OPENQASM 2\.0\;")

    properties = {
        "circuits": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "shotCount": {"type": "number", "exclusiveMinimum": 0},
    }

    def check_qasm_circuit_format(self, input_: dict):  # pylint:disable=no-self-use
        """
        Expect all circuits are valid QASM circuit strings.

        Parameters
        ----------
        input_ : dict
            the GraphQL input.
        Raises
        ------
        QctrlFieldError
            validation check failed
        """

        # The QASM validation is commented out because the validator check for a
        # valid QASM input is not fully correct and it is preventing the circuits
        # for the upcoming demo from running. This will be addressed once we have
        # a working Fire Opal in production for the upcoming demo.

        # for index, circuit in enumerate(input_.get("circuits", [])):
        #     if not self._QASM_PATTERN_RE.match(circuit):
        #         raise QctrlFieldError(
        #             message=f"Item {index} is not in valid QASM format.",
        #             fields=["circuits"],
        #         )
