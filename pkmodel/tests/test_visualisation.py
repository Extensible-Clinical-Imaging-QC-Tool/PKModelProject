import pkmodel as pk
import unittest
from unittest.mock import patch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class VisualisationTest(unittest.TestCase):
    """
    Tests the :class:`Visualisation` class.
    """

    @patch("pandas.read_csv")
    def test_initialisation(self, read_csv_mock):
        """
        Tests the initialisation of the public and
        private attributes
        """

        test_array = np.array( [[1,2,3,4], [5,6,7,8]] )
        read_csv_mock.return_value = pd.DataFrame( test_array )

        data_file_paths = ['', '']
        data_labels = ['beautiful model', 'fantastic model']
        dose_types = ['sc', 'iv']
        compartment_num = np.shape(test_array)[1] - 1 

        plots = pk.Visualisation(data_file_paths, 
                                    data_labels,
                                    dose_types)
        
        for k, label in enumerate(data_labels):

            self.assertEqual(plots._data_labels[k], label )
            self.assertEqual(plots._compartment_num[label], compartment_num )
            
            for (i,j), element in np.ndenumerate(test_array):
                if (j==0):
                    self.assertEqual(plots._time[label][i], element )
                else:
                    self.assertEqual(plots._quantity[label][i,j-1], element )

            if dose_types[k] == 'sc':
                self.assertEqual(plots.plot_labels[label][0], label + ' $q_0$')
                self.assertEqual(plots.plot_labels[label][1], label + ' $q_c$')
                [self.assertEqual(plots.plot_labels[label][1+i], 
                                    label + ' $q_{p%d}$' %(i))
                                    for i in range(1, compartment_num - 1) ]

            elif dose_types[k] == 'iv':
                self.assertEqual(plots.plot_labels[label][0], label + ' $q_c$')
                [self.assertEqual(plots.plot_labels[label][i], 
                                    label + ' $q_{p%d}$' %(i))
                                    for i in range(1, compartment_num) ]

    @patch("pandas.read_csv")
    def test_initialisation_errors(self, read_csv_mock):
        """
        Tests the errors in the initialisation
        """

        test_array = np.array( [[1,2,3,4], [5,6,7,8]] )
        read_csv_mock.return_value = pd.DataFrame( test_array )

        data_file_paths = ['', '']

        # Tests the error when the length of data_file_labels is not equal 
        # to the length of the data_file_paths
        with self.assertRaises(ValueError):
            data_labels = ['beautiful model']
            dose_types = ['sc', 'iv']
            pk.Visualisation(data_file_paths, 
                                data_labels,
                                dose_types)
        

        # Tests the error when the length of dose_types is not equal to the
        # length of the data_file_paths
        with self.assertRaises(ValueError):
            data_labels = ['beautiful model', 'fantastic model']
            dose_types = ['sc']
            pk.Visualisation(data_file_paths, 
                                data_labels,
                                dose_types)

        # Tests the error when the dose_types elements are not a subset of
        # set(['sc', 'iv'])
        with self.assertRaises(ValueError):
            data_labels = ['beautiful model', 'fantastic model']
            dose_types = ['sc', 'illegal dosing type']
            pk.Visualisation(data_file_paths, 
                                data_labels,
                                dose_types)

    @patch("pandas.read_csv")
    def test_visualise_errors(self, read_csv_mock):
        """
        Tests the errors in the visualise method
        """

        test_array = np.array( [[1,2,3,4], [5,6,7,8]] )
        read_csv_mock.return_value = pd.DataFrame( test_array )

        data_file_paths = ['', '']
        data_labels = ['beautiful model', 'fantastic model']
        dose_types = ['sc', 'iv']

        plots = pk.Visualisation(data_file_paths, 
                                data_labels,
                                dose_types)

        # Tests the error when the elements of labels_of_data_to_visualise 
        # are not elements of the data_labels list from the class 
        # initialisation
        with self.assertRaises(ValueError):
            plots.visualise(['beautiful model', 'terrible model'])

    @patch("pandas.read_csv")
    def test_visualise_plot(self, read_csv_mock):
        """
        Tests whether or not the visualise method produces a plot
        (More specifically whether plt.show is successfully called
        which occurs at the very end of the file)
        """

        test_array = np.array( [[1,2,3,4], [5,6,7,8]] )
        read_csv_mock.return_value = pd.DataFrame( test_array )

        data_file_paths = ['', '']
        data_labels = ['beautiful model', 'fantastic model']
        dose_types = ['sc', 'iv']

        plots = pk.Visualisation(data_file_paths, 
                                data_labels,
                                dose_types)

        with patch("matplotlib.pyplot.show") as show_mock:
            plots.visualise(['beautiful model', 'fantastic model'])
            assert show_mock.called
        
    @patch("pandas.read_csv")
    def test_visualise_save_file(self, read_csv_mock):
        """
        Tests whether or not the visualise method saves a plot
        (More specifically whether plt.savefig is successfully called)
        """

        test_array = np.array( [[1,2,3,4], [5,6,7,8]] )
        read_csv_mock.return_value = pd.DataFrame( test_array )

        data_file_paths = ['', '']
        data_labels = ['beautiful model', 'fantastic model']
        dose_types = ['sc', 'iv']

        plots = pk.Visualisation(data_file_paths, 
                                data_labels,
                                dose_types)

        with patch("matplotlib.pyplot.savefig") as savefig_mock:
            plots.visualise(['beautiful model', 'fantastic model'],
                            save_file_path='/path/to/file.pdf')
            assert savefig_mock.called

if __name__ == '__main__':
    unittest.main()
