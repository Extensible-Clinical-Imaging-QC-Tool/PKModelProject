import unittest
import numpy as np
import numpy.testing as npt
import pytest
import Dose

"""
Testing of the Protocol class from the Dose.py file 

"""

class ProtocolTest(unittest.TestCase):
    """
    Tests the Protocol class.
    """
    def test_steady_dose(self):
        """
        Unittests of the steady dose function
        """
        protocol = Dose.Protocol()
        self.assertEqual(protocol.steady_dose().any(), 43)


"""
Multiple unittests of the steady dose function
"""
@pytest.mark.parametrize("test, expected", [(43, 43), (-20, 43)])
def tests_steady_dose(test,expected):
    protocol = Dose.Protocol()
    npt.assert_array_equal(protocol.steady_dose(), expected)


class ProtocolInput(object):
    
     def test_instantaneous_dose_string(self):
        """
        Test for TypeError when passing strings in the instantaneous dose function
        """
        
        protocol = Dose.Protocol()
        with pytest.raises(TypeError):
             protocol.instantaneous_dose('hello world')


