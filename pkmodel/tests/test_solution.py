import unittest
from unittest.mock import Mock, patch, PropertyMock
import numpy as np
import pkmodel as pk
import math

class SolutionTest(unittest.TestCase):
    """
    Tests the :class:`Solution` class.
    """
    @patch('pkmodel.Model')
    def test_create_solution(self, mock_class):
        """
        Tests Solution creation.
        """
        test_model = mock_class
        test_model.configure_mock(components = 2)
        test_model.configure_mock(model_args = {'name': 'test_model'})
        model_list = [test_model]
        t_eval = [0, 1, 2, 3, 4, 5]
        y0 = [[0, 0]]
        solution = pk.Solution(model_list, t_eval, y0)
        self.assertEqual(solution.models, model_list)
        self.assertEqual(solution.t_eval, t_eval)
        self.assertEqual(solution.y0, y0)

        test_model_bad_dimension = mock_class
        test_model_bad_dimension.configure_mock(components = 3)
        model_list2 = [test_model_bad_dimension]

        # Test that the solution class catches the error when y0 and #compartments do not match
        with self.assertRaises(ValueError):
            solution2 = pk.Solution(model_list2, t_eval, y0)
   
    @patch.object(pk.Model, 'make_args', return_value= None)
    def test_analyse_models(self, mock_class):
        """
        Test creation of a list  containing a solution of each model.

        """
        # Create a Solution object
        model1 = mock_class
        model2 = mock_class
        mock_class.configure_mock(components = 2)
        model_list = [model1, model2]
        t_eval = [0, 1, 2, 3, 4, 5]
        y0 = [[0, 0], [1, 1]]
        solution = pk.Solution(model_list, t_eval, y0)

        # Set mock functions and properties
        solution._integrate = Mock(return_value = mock_class)
        t = PropertyMock(return_value = 't')
        type(mock_class).t = t
        solution._save_to_csv = Mock(return_value = 'save_csv')
        
        sol_list = solution.analyse_models()
        self.assertEqual(sol_list, [mock_class,mock_class])
    
    @patch('pkmodel.Model')
    def test_integrate(self, mock_class):
        """
        Test integration of a given model.
        """
        def test_solution(t):
            """
            Create the analytical solution of the test_rhs model.
            """
            y_sol =  -1*math.exp(-3*t/2)
            return y_sol
        
        def test_rhs(t, y, args):
            """
            A test model for the ODE solver.
            """
            x, z = y
            dx_dt = -x + 1/4*z
            dz_dt = x - z
            return [dx_dt, dz_dt]
        
        # Create a Solution object
        y_0 = [[-1, 2]]
        test_model = mock_class
        test_model.configure_mock(components = 2)
        t_eval = np.linspace(0,100,1000)
        testsol = pk.Solution([test_model], t_eval, y_0)

        # Set the behaviour of the mock rhs method to the test model
        test_model.rhs.side_effect = test_rhs

        args = [-1, 1/4]
        sol = testsol._integrate(test_model, args, np.array(y_0[0]))

        # Obtain y values for the analytical solution
        y_sol = np.array([test_solution(x) for x in t_eval])
        self.assertIsNone(np.testing.assert_almost_equal(sol.y[0], y_sol, decimal = 3))
    




