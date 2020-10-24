import pytest
import numpy as np
import numpy.testing as npt
import pkmodel as pk
from pkmodel import Protocol


 
"""
Test the steady dose function X as a function of time t:
X(t) = quantity, 
where quantity is the specified drug quantity to inject [ng]
"""

@pytest.mark.parametrize("test,expected", [(44,44), (-20,44),(100,44)])
def tests_steady_dose(test,expected):
    protocol = Protocol(quantity = test)
    npt.assert_array_equal(protocol.steady_dose()[0], expected) 


"""
Test the linear dose function X as a function of time t:
X(t) = quantity*t, 
where quantity is the specified drug quantity to inject [ng]
"""

@pytest.mark.parametrize("test, expected", [(0, 0), (100, 100), (100, 2)])
def tests_linear_dose(test,expected):
    protocol = Protocol(quantity=test)
    npt.assert_array_equal(protocol.linear_dose()[10], expected) 


"""
Test the instantaneous dose function X ~ N(t,1) where t is the specified time of injection (hrs)
"""

@pytest.mark.parametrize("test, expected", [(43, 0), (43, 43)])
def tests_instantaneous_dose(test,expected):
    protocol = Protocol(quantity=test)
    npt.assert_array_equal(protocol.instantaneous_dose()[799], expected) 


    """
    Test for TypeError when passing strings in the instantaneous dose function
    """  

    def test_instantaneous_dose_string():

        with pytest.raises(TypeError):
            protocol = Protocol()
            protocol.instantaneous_dose("hello world")
            

 
if __name__ == '__main__':
    pytest.main()
