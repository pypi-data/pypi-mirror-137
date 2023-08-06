from typing import Tuple
import numpy as np

from numpy.linalg import svd

class Euclidean:
    def __init__(self, var_shape: Tuple) -> None:
        
        self.dim = np.prod(var_shape)
        self.var_shape = var_shape
        self.zero_X = np.zeros(self.var_shape)





    def Feas_correction(self, X):
        return X 


    def A(self, X):
        return X


    def JA(self, X, G):
        return G
    

    def JA_approx(self, X, G):
        return G


    def JC(self, X, Lambda):
        return self.zero_X

    
    def JC_transpose(self, X, D):
        return 0

    

    def C(self, X):
        return 0

    def Feas_eval(self, X):
        return 0

    def Init_point(self, Xinit = None):
        if Xinit == None:
            Xinit = np.random.randn(*self.var_shape)
            
        return Xinit



    def Post_process(self,X):
        
        return X
