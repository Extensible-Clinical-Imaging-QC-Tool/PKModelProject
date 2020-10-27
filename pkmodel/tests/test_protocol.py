

import unittest
from unittest import TestCase
import pkmodel import Protocol


class ProtocolTest(unittest.TestCase):
    
    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def tests_steady_dose(self):
        
        """
        Test the steady dose function X as a function of time t:
        X(t) = quantity, 
        where quantity is the specified drug quantity to inject [ng]
        """
        param_list_tests_1 = [(44,44), (-20,44),(100,44)]
        for test, expected in param_list_tests_1:
            protocol = Protocol(quantity = test)
            with self.subTest():
                try: self.assertEqual(protocol.steady_dose()[0], expected)
                except AssertionError as e: self.verificationErrors.append(str(e))
    
    def tests_linear_dose(self):

        """
        Test the linear dose function X as a function of time t:
        X(t) = quantity*t, 
        where quantity is the specified drug quantity to inject [ng]
        """
        param_list_tests_2 = [(0, 0), (100, 100), (100, 2)]
        for test, expected in param_list_tests_2:
            protocol = Protocol(quantity = test)
            with self.subTest():
                try: self.assertEqual(protocol.linear_dose()[10], expected)
                except AssertionError as e: self.verificationErrors.append(str(e))
                
    
    
    def tests_instantantaneous_dose(self):

        """
        Test the instantaneous dose function X ~ N(t,1) where t is the specified time of injection (hrs)
        """
        param_list_tests_3 = [(43, 0), (43, 43)]
        for test, expected in param_list_tests_3:
            protocol = Protocol(quantity = test)
            with self.subTest():
                try: self.assertEqual(protocol.instantaneous_dose()[799], expected)
                except AssertionError as e: self.verificationErrors.append(str(e))

    def test_instantaneous_dose_string(self):

        """
        Test for TypeError when passing strings in the instantaneous dose function
        """  
        with self.assertRaises(TypeError):
            protocol = Protocol()
            protocol.instantaneous_dose("hello world")




if __name__ == '__main__':
    unittest.main()
