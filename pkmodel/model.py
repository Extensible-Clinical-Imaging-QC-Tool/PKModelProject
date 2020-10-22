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
    :param dose_type: str 

    

    """
    def __init__(self, components: int,model_args: dict,dose_type: str):
        if (len(model_args.keys()) != 2*components + 1 and dose_type == 'iv') \
            or len(model_args.keys()) != 2*(components + 1) and dose_type =='sc'):

            return "ERROR: Model not fully defined"

        self.components = components
        self.model_args = model_args
        self.dose_type = dose_type


    def get_peripheral_rates(q_x,v_x,Q_px):
        # Calculate dqpx_dt for all components present
        total = []
        for i in range(1,len(v_x)):
            total.append(Q_px[i-1]*(q_x[0]/v_x[0] - q_x[i]/v_x[i]))

        return total


    if self.dose_type == 'sc'
    # Define the system of equations based on the type of dose 
    # intake
        def rhs(t,y,k_a,v_x,Q_px,dose):
            q_0,q_x = y[0],y[1:]
            dq0_dt = dose(t,X) - k_a*q_0
            transitions = get_peripheral_rates(q_x,v_x,Q_px)
            dqc_dt = k_a*q_0 - (q_x[0]/v_x[0])*CL - sum(transitions)
            
            return [dq0_dt,dqc_dt] + transitions
    else:
        def rhs(t,y,v_x,Q_px,dose):
            q_x  = y
            transitions = get_peripheral_rates(q_x,v_x,Q_px)
            dqc_dt = dose(t,X) - (q_x[0]/v_x[0])*CL - sum(transitions)

            return [dqc_dt] + transitions



hey = 4
hey = hey * 2

