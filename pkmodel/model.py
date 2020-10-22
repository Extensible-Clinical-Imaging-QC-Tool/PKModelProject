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
         'CL' : 0.0
        }    
        

    :param dose_type: str 
        'sc' = subcutaneous
        'iv' = intravenous

    

    """
    def __init__(self, components,model_args,dose_type):
        if (len(model_args.keys()) != 2*(components + 1) and dose_type == 'iv' \
            or len(model_args.keys()) != 2*(components + 1) + 1 and dose_type =='sc'):

            ValueError("ERROR: Model not fully defined")

        self.components = components
        self.model_args = model_args
        self.dose_type = dose_type

    
    def make_args(self):
        # creates a list of arguments which will
        # be used to call rhs in solution.py

        CL = self.model_args['CL']
        Q_rates = []
        vols = [self.model_args['V_c']]

        for i in range(1,self.components + 1):
            key_a = 'V_p' + str(i)
            key_b = 'Q_p' + str(i)
            
            vols.append(self.model_args[key_a])
            Q_rates.append(self.model_args[key_b])

        if self.dose_type == 'sc':
            args = [k_a,vols,Q_rates,CL]
            return args
            
        else:
            args = [vols,Q_rates,CL]
            print(args)
            return args


    def get_peripheral_rates(self,v_x,q_x,Q_px):
        # Calculate dqpx_dt for all components present
        total = []
        for i in range(1,len(v_x)):
            total.append(Q_px[i-1]*(q_x[0]/v_x[0] - q_x[i]/v_x[i]))

        return total

    def dose(self,t, X=1):
        return X

    #if self.dose_type == 'sc':
    ## Define the system of equations based on the type of dose 
    ## intake
#
    #    def rhs(t,y,k_a,v_x,Q_px,CL,dose):
    #        q_0,q_x = y[0],y[1:]
    #        dq0_dt = dose(t,X) - k_a*q_0
    #        transitions = get_peripheral_rates(q_x,v_x,Q_px)
    #        dqc_dt = k_a*q_0 - (q_x[0]/v_x[0])*CL - sum(transitions)
    #        
    #        return [dq0_dt,dqc_dt] + transitions
    #else:
    def rhs(self,t,y,args): #v_x,Q_px,CL,dose):
        v_x = args[0]
        Q_px = args[1]
        CL = args[2]

        q_x  = y
        transitions = self.get_peripheral_rates(v_x,q_x,Q_px)
        dqc_dt = self.dose(t) - (q_x[0]/v_x[0])*CL# - sum(transitions)

        return [dqc_dt] + transitions



