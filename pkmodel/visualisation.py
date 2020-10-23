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
        to be visualised. The solution data should be the output
        of a method in the Solution class as a .csv file.

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

    """

    def __init__(self, data_file_paths, data_labels):
        self.time = {}
        self.quantity = {}

        for i, file_path in enumerate(data_file_paths):
            label = data_labels[i]
            self.time[label] = pd.read_csv(file_path, sep=',', header=None).loc[:, 0]
            self.quantity[label] = pd.read_csv(file_path, sep=',', header=None).loc[:, 1]

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

        # Colour map for the figure
        # A perceptually uniform colour map suitable for the most common
        # types of colour-blindness
        cmap = cm.get_cmap('viridis')

        ### Figure ###
        fig, ax = plt.subplots(1, 1)

        # Plotting
        l = len(labels_of_data_to_visualise)

        if l == 1:
            for i, label in enumerate(labels_of_data_to_visualise):
                ax.plot(self.time[label], self.quantity[label], 
                        color=cmap(0.4), label=label )
        else:
            for i, label in enumerate(labels_of_data_to_visualise):
                ax.plot(self.time[label], self.quantity[label], 
                        color=cmap(i * 0.8 / (l - 1) ), label=label )

        # Formatting
        ax.set_xlabel(r'time / hr')
        ax.set_ylabel(r'quantity / ng')
        ax.legend(loc=0)

        # Saving the figure
        if save_file_path is not None:
            fig.savefig(save_file_path, bbox_inches='tight')

        plt.show()