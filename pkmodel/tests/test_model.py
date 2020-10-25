import unittest

import pkmodel as pk
from pkmodel import Model,Visualisation,Solution,Protocol

class ModelTest(unittest.TestCase):
    """
    Tests the :class:`Model` class.
    """
    
    def test_model_instantiation(self):
        """
        Tests Model instantiation.

        """

        test_args_sc3 = {
            'name': 'test_model',
            'V_c': 1.0,
            'Q_p1': 2.0,
            'V_p1': 3.0,
            'CL': 4.0,
            'k_a':5.0
        }

        test_args_iv1 = {
            'name': 'test_model',
            'V_c': 1.0,
            'CL': 2.0
        }
        
        test_args_nve = {
            'name': 'test_model',
            'V_c': -1.0,
            'CL': 2.0
        }

        # Negative value in the component properties
        with self.assertRaises(AssertionError):
            obj = pk.Model(1,test_args_nve,'iv',0)

        # Unavailable type of injection
        with self.assertRaises(ValueError):
            obj = pk.Model(0,test_args_iv1,'jk',0)

        # Too few components for subcutaneous injections
        with self.assertRaises(ValueError):
            obj = pk.Model(1,test_args_iv1,'sc',0)

        # Number of components and model keys do not match
            # sc
        with self.assertRaises(ValueError):
            obj = pk.Model(2,test_args_sc3,'sc',0)

            # iv
        with self.assertRaises(ValueError):
            obj = pk.Model(3,test_args_iv1,'iv',0) 


    def test_model_definition(self):
        """
        Tests Model definition.

        """

        test_args_sc3 = {
            'name': 'test_model',
            'V_c': 1.0,
            'Q_p1': 2.0,
            'V_p1': 3.0,
            'CL': 4.0,
            'k_a':5.0
        }

        test_args_iv1 = {
            'name': 'test_model',
            'V_c': 1.0,
            'CL': 2.0
        }
        
        # test correct definition of 1 comp iv

        obj1 = pk.Model(1,test_args_iv1,'iv',[0])
        args = obj1.make_args()
        assert len(args[0]) == 1 , 'Volumes incorrectly defined'
        assert len(args[1]) == 0 , 'Transitions incorrectly defined'
        assert type(args[2]) == float , 'CL incorrectly defined'

        rates = obj1.rhs(t = 0, y = [0], args = args)
        assert len(rates) == 1, 'iv ODE system incorrectly defined'
        
        # test correct definition of 3 comp sc
        obj1 = pk.Model(3,test_args_sc3,'sc',[0])
        args = obj1.make_args()
        assert type(args[0]) == float , 'k_a incorrectly defined'
        assert len(args[1]) == 2 , 'Volumes incorrectly defined'
        assert len(args[2]) == 1 , 'Transitions incorrectly defined'
        assert type(args[3]) == float , 'CL incorrectly defined'

        rates = obj1.rhs(t = 0, y = [0,0,0],args = args)
        assert len(rates) == 3, 'sc ODE system incorrectly defined'


