#
# Model class
#

class Model:
    """A Pharmokinetic (PK) model

    Allows users to define a PK model with the 
    desired number of components, component properties
    and the method of dose intake

    Parameters
    ----------
    :param components: integer
    :param model_args: dict

        {'name': 'model_name',
         'V_c' : 0.0,
         'V_p1' : 0.0,
           .
           .
         'V_pN' : 0.0,
         'Q_p1' : 0.0,
           .
           .
         'Q_pN' : 0.0,
         'CL' : 0.0,
         ('k_a') : 0.0
        }    
        

    :param dose_type: str 
        'sc' = subcutaneous
        'iv' = intravenous

    """
    def __init__(self, components,model_args,dose_type,dose_t):
        # Preconditions to ensure that the correct number of properties are provided
        # for the desired model and that the inputs are correct.
        if dose_type == 'sc' and components < 2:
            raise ValueError("A model of subcutaneous injection must posses at\
                lease two components: Skin and Central")

        if ((dose_type == 'iv' and len(model_args.keys()) != 2*components + 1) \
            or (dose_type =='sc'and len(model_args.keys()) != 2*components)):
            
            raise ValueError("Model incorrectly defined. Please ensure all\
                components are defined")

        if dose_type != 'sc' and dose_type!='iv':
           raise ValueError("Not a valid form of injection. 'sc' or 'iv' required")

        values = list(model_args.values())
        assert all(value >= 0 for value in values[1:]), 'All model properties\
            must be >= 0'

        self.components = components
        self.model_args = model_args
        self.dose_type = dose_type
        self.dose_t = dose_t
        self.counter = 0

    
    def make_args(self):
        # Creates a list of arguments that define the system of equations.
        # The arguments will be used to call rhs in solution.py

        CL = self.model_args['CL']
        Q_rates = []
        vols = [self.model_args['V_c']]

        if self.dose_type == 'sc':
            iter_range = range(1,self.components - 1)
            k_a = self.model_args['k_a']
            args = [k_a,vols,Q_rates,CL]
        else:
            iter_range = range(1,self.components)
            args = [vols,Q_rates,CL]

        for i in iter_range:
            key_a = 'V_p' + str(i)
            key_b = 'Q_p' + str(i)
            
            vols.append(self.model_args[key_a])
            Q_rates.append(self.model_args[key_b])

        return args


    def get_peripheral_rates(self,v_x,q_x,Q_px):
        # Calculate dqpx_dt for all components present
        total = []
        for i in range(1,len(Q_px) + 1):
            total.append(Q_px[i-1]*(q_x[0]/v_x[0] - q_x[i]/v_x[i]))

        return total


    def dose(self):
        # Return the dose at time t
        X = self.dose_t[self.counter]
        self.counter += 1
        return X


    def rhs(self,t,y,args):
    # Define the system of equations based on the type of dose 
    # intake
        if self.dose_type == 'sc':
            k_a, v_x, Q_px, CL  = args[0], args[1], args[2], args[3]
            q_0, q_x = y[0], y[1:]

            dq0_dt = self.dose() - k_a*q_0
            transitions = self.get_peripheral_rates(v_x,q_x,Q_px)
            dqc_dt = k_a*q_0 - (q_x[0]/v_x[0])*CL - sum(transitions)
            
            return [dq0_dt,dqc_dt] + transitions

        else:
            v_x, Q_px, CL  = args[0], args[1], args[2]
            q_x  = y
            transitions = self.get_peripheral_rates(v_x,q_x,Q_px)
            dqc_dt = self.dose() - (q_x[0]/v_x[0])*CL - sum(transitions)

            return [dqc_dt] + transitions

