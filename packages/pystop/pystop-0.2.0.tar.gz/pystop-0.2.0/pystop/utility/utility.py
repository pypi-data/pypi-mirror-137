import numpy as np
import scipy as sp


def prox_l1(X_input, eta, gamma = 0):
    # np.max(X_input, 0)
    # return the proximal operator of \gamma * ||X||_1
    return np.maximum(X_input - gamma * eta, 0 ) + np.minimum(X_input + gamma * eta, 0 )


def prox_l21(X_input, eta, gamma = 0):
    # np.max(X_input, 0)
    # return the proximal operator of \gamma * ||X||_{2,1}
    X_ref = np.sqrt(np.sum(X_input** 2, axis= 1, keepdims= True))
    X_ref_reduce = np.maximum(X_ref - gamma * eta, 0 )
    return X_ref_reduce/(X_ref + 1e-14) * X_input