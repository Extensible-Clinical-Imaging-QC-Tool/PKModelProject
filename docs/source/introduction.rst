
Pharmacokinetics: Definition
==============================

Pharmacokinetics (PK) is the quantification of drug absorption, distribution and elimination in order to predict blood concentration-time profiles.
The aim of PK is to maintain a sufficient concentration of the drug in the body while ensuring that the concentration levels do not exceed the pre-established toxic threshold.

Mathematical Problem
====================

PK models have varying levels of complexity. In this project, we adopt a compartmental approach. The body can be modelled with one or more compartments. The drug is administered and excreted from the body via the central compartment, the latter may be combined with one or more peripheral compartments to which the drug can be distributed in a forward-reverse relationship. Each of the peripheral compartment(s) is only connected to the central compartment.

Intravenous bolus model
------------------------

A two-compartment model with a linear clearance from the central compartment.
We address this two-compartment model by solving the following set of 1st order differential equations for the drug quantity in the central and peripheral compartments, :math:`q_{c}` and :math:`q_{p_{1}}` (units [ng]) respectively: 

 .. math:: 
      
      \frac { dq_{c} }{ dt } &= Dose(t)- \frac { q_{c} }{V_{c} }  CL - Q_{p_{1}} ( \frac { q_{c} }{V_{c} } - \frac { q_{p_{1}} }{V_{p_{1}} } ) 
            
      \frac { dq_{p_{1}} }{ dt } &= Q_{p_{1}} ( \frac { q_{c} }{V_{c} } - \frac { q_{p_{1}} }{V_{p_{1}} } )


 * The dose function Dose(t) consists of instantaneous doses of X ng of the drug at one or more time points, a steady or constant application of X ng per hour over a given time period

 * :math:`V_{c}` [mL] is the volume of the central compartment 

 * :math:`V_{p_{1}}` is the volume of the first peripheral compartment

 * CL [mL/h] is the clearance/elimination rate from the central compartment

 * :math:`Q_{p_{1}}` [mL/h], the transition rate between central compartment and first peripheral compartment   


Subcutaneous model
------------------------

This time the dose is injected via another route, in the flat layer between the skin and the muscle.
We describe a three-compartment model with the addition of another compartment from which the drug is absorbed to the central compartment. We add the drug quantity in the third compartment :math:`q_{0}` (units [ng]):

.. math:: 
      
      \frac { dq_{0} }{ dt } &= Dose(t) - k_{a} q_{0}

      \frac { dq_{c} }{ dt } &= Dose(t)- \frac { q_{c} }{V_{c} }  CL - Q_{p_{1}} ( \frac { q_{c} }{V_{c} } - \frac { q_{p_{1}} }{V_{p_{1}} } ) 
            
      \frac { dq_{p_{1}} }{ dt } &= Q_{p_{1}} ( \frac { q_{c} }{V_{c} } - \frac { q_{p_{1}} }{V_{p_{1}} } )

* :math:`k_{a}` [/h] is the “absorption” rate 