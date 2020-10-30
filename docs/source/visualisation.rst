 Visualisation Class
==============================
The class uses the Python libraries numpy, matplotlib and pandas. 

It is designed to create figures of the solutions (loaded from csv files)
from the Solution class. The figures display plots of the quantities of each 
compartment as a function of time.

The solutions of multiple models may be compared by plotting all of their 
quantities on the same figure.

Class parameters and methods
----------------------------
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


How to use
----------------------------
First import the package.

.. code-block:: python
    import pkmodel as pk

Create an instance of the class. You must specify the data you want to use for 
visualisation as a list of file paths. Even if you want to visualise only one
data file you must provide the file path as a list with one element. You must
also provide the names of the models associated with each data file. These
names will be used to generate the plot labels associated with each data set.
The model names must be provided as a list of strings of the same length as the
list of file paths. Finally, you must provide a list of dosing types associated
with each model. This is used to ensure that the plot labels correctly label
the additional compartment present in the subcatenous dosing type.

.. code-block:: python
    plots = pk.Visualisation(['/path/to/data_1.csv', '/path/to/data_2.csv', '/path/to/data_3.csv'], 
                               ['beautiful model', 'fantastic model', 'controversial model'],
                               ['sc', 'iv', 'iv'])

To visualise the solutions from these csv files you must call the visualise()
method of the class. You must provide a list of strings of names of the models
you want to visualise. This list must be a subset of the list of model names
you provided in the class inialisation. Optionally, you may provide a file
path of where you would like to save the figure. You have the freedom to 
choose the image format extension of your saved figure.

.. code-block:: python
    plots.visualise(['beautiful model', 'fantastic model'],
                       save_file_path='/path/to/fun_figure.pdf')

After running this you should have generated a single figure and saved it to 
the chosen file path.
 

Issues
----------------------------
The class has a few errors coded that explain what specifically went wrong
within the context of the class.
This is a non-exhaustive list of errors you may encounter which are not coded
specifically for the Visualisation class, but arise from methods called from 
other classes within the Visualisation class. Most arise from inputting
parameters in an incorrect format.

*I get an error using the visualise() method saying ValueError.
Format 'df' is not supported (supported formats: eps, jpeg, jpg, pdf, pgf, 
png, ps, raw, rgba, svg, svgz, tif, tiff)*

You provided a save_file_path which included an extension for an image file
format which is not supported. Please use one of the supported formats.

*I get an error using the visualise() method saying FileNotFoundError.
No such file or directory: '/non/existent/path/to/fun_figure.pdf' *

You provided a save_file_path which included a non-existent directory. Please
amend the file path to save the figure in a pre-existing directory.

*I get an error inialisating the class saying FileNotFoundError.
No such file or directory: '/path/to/non/existent/file.csv' *

You provided a file path to a non-existent data file. Please change the file
path to a pre-existing data file or use a method in the Solution class to 
generate and save a new data csv file.

*I get an error inialisating the class saying ValueError.
Invalid file path or buffer object type: <class 'int'> *

You provided a file path of the incorrect format. (In this case an integer.)
Please provide the file path in the correct format.

*I get an error inialisating the class saying TypeError.
unsupported operand type(s) for +: 'int' and 'str' *

You provided a list of model name with elements of the incorrect format. (In 
this case an integer and not a string.) The elements must be strings so that 
the automatic plot compartment plot labels may be generated using string 
addition.

*I have an issue not covered here*

Please contact one of the contributors and we will try to help.