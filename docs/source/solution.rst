Solution Class
==============================
The solution class uses scipy's `solve_ivp <https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html>`_  method to solve a PK model 
with specified initial conditions.

Class parameters and methods
----------------------------
.. automodule:: solution
    :members:

How to use
----------------------------
Once a dosing protocol and a model has been specified, you need to firstly create a solution class.
Remember to specify initial conditions for all models and all compartments, as well as a time span for model evaluation.
Ensure that models are specified as a list of models.

.. code-block:: python

    models = [model_1,model_2]
    trial_sol = pk.Solution(models, t_eval = np.linspace(t_0, t_end, precison),y0=[[0,0],[0,0]])

To obtain the solution run the following method:

.. code-block:: python

    trial_sol.analyse_models()

Issues
----------------------------
*I get an error saying my initial conditions do not match the model components*

Please ensure you have specified initial conditions for ALL compartments - i.e. for analysing one model
with three comparments (including main compartments and subcatenous compartment if applicable)
your y0 should look like this:

.. code-block:: python

    y0 = [[0,0,0]]

*I get an error saying that the Model object is not iterable*

You need to specify your models as a list. Even if you are only analysing one model it should still
be specified as a list, i.e:

.. code-block:: python

    list_of_models = [model1]

*When I try to run my solution I get an error related to my t_span: int object is not subscriptable*

You need to specify your time points (t_eval) as an array.

*I have a different issue*

Please contact one of the contributors or raise an issue on the github repository.