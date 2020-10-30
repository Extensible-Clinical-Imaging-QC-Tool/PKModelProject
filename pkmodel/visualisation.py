#
# Visualiser class
#

# Packages

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

from matplotlib import cm 

#Class

class Visualisation:
    """
    A Pharmokinetic (PK) model solution visualiser

    Parameters
    ----------

    data_file_paths: list of str or PathLike or file-like objects, required
        Specifies the file paths or file names of the solution data
        to be visualised. The solution data should be a two column .csv 
        file, where the first column is the time steps and second column 
        is the quantity at each time step. The output .csv file generated 
        from the _save_to_csv method of the Solution class is of the 
        correct format.


        e.g. ['../path/to/beautiful_model_data.csv',
                '../path/to/fantastic_model_data.csv'
                '../path/to/remarkable_model_data.csv']

    data_file_labels: list of str, required
        Specifies the labels of the solution data.
        The order of the labels should correspond to the order
        of the file paths in the data_file_paths parameter.

        e.g. ['beautiful model', 
                'fantastic model', 
                'remarkable model']

    dose_types: list of str, required
        Specifies the types of dosing models for the solution data. 
        The order of the types should correspond to the order
        of the file paths in the data_file_paths parameter.
        Elements must be one of:

        'sc' = subcutaneous dosing
        'iv' = intravenous dosing

    Attributes
    ----------

    .plot_labels: a dict with str values
        A dictionary of plot labels for each quantity in each data file, 
        automatically generated after the class initialisation. The keywords
        are the data_file_labels provided during the initialisation.

    """

    def __init__(self, data_file_paths, data_labels, dose_types):

        if len(data_file_paths) != len(data_labels):
            raise ValueError( ("The length of data_labels must be "
                                "the same as the length of "
                                "data_file_paths.") )

        if len(data_file_paths) != len(dose_types):
            raise ValueError( ("The length of data_labels must be "
                                "the same as the length of "
                                "dose_types.") )

        if set(dose_types).issubset(['sc', 'iv']) is False:
           raise ValueError( ("Not a valid form of dosing types. "
                                "Elements must be 'sc' or 'iv'.") )
        
        self._data_labels = data_labels
        self._time = {}
        self._quantity = {} 
        self._compartment_num = {}
        self.plot_labels = {}

        for i, file_path in enumerate(data_file_paths):
            label = self._data_labels[i]

            self._time[label] = pd.read_csv(file_path, sep=',', 
                                                header=None
                                                ).loc[:, 0].to_numpy()
            self._quantity[label] = pd.read_csv(file_path, sep=',', 
                                                    header=None
                                                    ).loc[:, 1:].to_numpy()
            self._compartment_num[label] = np.shape(self._quantity[label])[1]
            self.plot_labels[label] = [None] * self._compartment_num[label]

            if dose_types[i] == 'sc':
                self.plot_labels[label][0] = label + ' $q_0$'
                self.plot_labels[label][1] = label + ' $q_c$'
                self.plot_labels[label][2:] = [label + ' $q_{p%d}$' %(i)
                                                for i in range(1, 
                                                self._compartment_num[label] 
                                                - 1) ]

            elif dose_types[i] == 'iv':
                self.plot_labels[label][0] = label + ' $q_c$'
                self.plot_labels[label][1:] = [label + ' $q_{p%d}$' %(i)
                                                for i in range(1, 
                                                self._compartment_num[label]
                                                ) ]


    def visualise(self, labels_of_data_to_visualise, save_file_path=None):
        """
        Generates a plot of the provided data. If multiple data are provided
        then multiple plots will be overlaid on the same figure. The figure
        will be scaled to the datum which covers the largest time interval.

        Parameters
        ----------

        labels_of_data_to_visualise: list of str, required
            Specifies the labels of the solution data to visualise.
            These labels must be a subset of the data_labels provided
            in the class initialisation.

            e.g. ['beautiful model', 
                    'fantastic model']

        save_file_path: None or str or PathLike or file-like object, optional
            If None then the figure will not be saved.
            If str or PathLike or file-like object, then it will be used 
            as the file path or file name of the saved figure.

            e.g. '../path/to/stunning_plot.pdf'

        """

        if set(labels_of_data_to_visualise).issubset(self._data_labels) is False:
           raise ValueError( ("Not a valid form of labels_of_data_to_visualise. " 
                                "Elements must be in the the data_labels list " 
                                "provided in the class initialisation.") )
        
        # Colour map for the figure
        # A perceptually uniform colour map suitable for the most common
        # types of colour-blindness
        cmap = cm.get_cmap('viridis')

        ### Figure ###
        fig, ax = plt.subplots(1, 1)

        # Plotting
        def width(length):
            # width of the partitions for the argument of the
            # colour map
            output = 0

            if length > 1:
                output = length - 1
            elif length <= 1:
                output = 1

            return output
        
        L = len(labels_of_data_to_visualise)

        for i, label in enumerate(labels_of_data_to_visualise):
            N = self._compartment_num[label]

            for j in range(N):
                ax.plot( self._time[label], self._quantity[label][:, j], 
                    color=cmap((i * N + j) * 0.9 / width(L * N) ), 
                    label=self.plot_labels[label][j] )

        # Formatting
        ax.set_xlabel(r'time / hr')
        ax.set_ylabel(r'quantity / ng')
        ax.legend(loc=0)

        # Saving the figure
        if save_file_path is not None:
            plt.savefig(save_file_path, bbox_inches='tight')

        plt.show()