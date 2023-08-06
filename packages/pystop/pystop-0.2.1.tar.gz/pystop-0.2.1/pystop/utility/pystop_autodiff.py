import numpy as np
import autograd as ag

def fun_autodiff(obj_fun):
    grad_local = ag.grad(obj_fun)
    def fungrad(X):
        return obj_fun(X), grad_local(X)

    return grad_local, fungrad