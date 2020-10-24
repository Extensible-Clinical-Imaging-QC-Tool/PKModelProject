import numpy as np

class Protocol(object):
	"""
	A Pharmokinetic (PK) protocol

	Parameters:

	quantity: drug quantity to inject 
	k : increment for drug quantity to inject
	t_start: starting time of protocol
	t_end: ending time of protocol
	n: time steps in hours 
	t: time duration of protocol
	
	-----------

	1) Instantaneous dose injection

	Parameters: 
	
	T1: first time point of injection
	T2: second time point of injection 
	
	Possibility to add other time points if needed ie: add a T3 variable  
	
	-----------
	
	2) Steady dose injection 
	This protocol represents a constant injection of drug quantity over time.
	The parameter to set in the initialisation is the quantity.
	
	-----------
		
	3) Linear dose injection 
	This protocol is a linear increase (+ quantity) or decrease (- quantity) of drug over time. 

	"""
	
	def __init__(self, quantity = 43, t_start = 0, t_end = 10, n = 1000):

		self.quantity = quantity
		self.t_start = t_start  
		self.t_end = t_end 
		self.n = n
		self.t = np.linspace(t_start, t_end, n)
	
	# Protocol 1: Instantaneous drug dose injection
	
	def instantaneous_dose(self,k = 1,T1 = 2,T2 = 8,sigma = 1):
	
		quantity, t= self.quantity, self.t
		self.k = k
		self.T1 = T1
		self.T2 = T2
		self.sigma = sigma
		X=np.zeros_like(t)
	     
		from scipy.stats import norm
		
		for i,time in enumerate(t):
			if ((time>T1-3*sigma) and (time<T1+3*sigma)):
				X[i] =  quantity * np.sqrt(2*np.pi) * sigma * norm.pdf(time,T1,sigma) 
			elif ((time>T2-3*sigma) and (time<T2+3*sigma)):
				X[i] =  k * quantity * np.sqrt(2*np.pi) * sigma * norm.pdf(time,T2,sigma) 
			if ((time>T1-3*sigma) and (time<T2+3*sigma)): 
				X[i] =  k * quantity * np.sqrt(2*np.pi) * sigma * (norm.pdf(time,T1,sigma) + norm.pdf(time,T2,sigma))
		return X
		
	# Protocol 2: Steady injection of drug over time 
		
	def steady_dose(self,quantity):
		
		t = self.t
		self.quantity = quantity
		X = quantity * np.ones_like(t)
		return X
		
	# Protocol 3: Linear injection of drug over time 
	
	def linear_dose(self,quantity):
		
		
		t = self.t
		self.quantity = quantity
		X = quantity * t
		return X
     
	
	


	
