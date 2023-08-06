import numpy as np
from numpy.linalg import norm



def PenCF(Xinit, obj_fun,  manifold, beta = None, maxit= 100, gtol = 1e-5, post_process = True, verbosity = 2, **kwargs):
    kkts = []
    feas = []
    fvals = []

    



    n = manifold._n
    p = manifold._p

    X = Xinit

    X_p = np.zeros( (n,p) )

    fval, gradf = obj_fun(X)

    
    if beta == None:
        beta = 0.1* np.linalg.norm(gradf,'fro')
    



    
    gradr = manifold.JA(X, gradf) + beta * manifold.JC(X, manifold.C(X))


    L = np.linalg.norm(gradf,'fro') + np.linalg.norm(gradr,'fro')

    for jj in range(maxit):

        

        

        if jj < 3:
            stepsize = 0.01/L
        else:
            stepsize = np.abs( np.sum( S * Y ) / np.sum( Y* Y ) )
            stepsize = np.min( (stepsize, 1e10) )

        X_p = X

        X = X - stepsize * gradr

        XX = X.T @ X
        feas_tmp = manifold.Feas_eval(X)
        if feas_tmp > 1e-1:
            if feas_tmp < 0.5:
                X = 1.5 * X - X @ (XX /2)
            else:
                X = np.linalg.solve( ( XX + np.eye(p) ) /2, X.T  ).T
        
        if np.linalg.norm(X,'fro') > 1.001 * np.sqrt(p):
            X = X *(1.001 * np.sqrt(p)/ np.linalg.norm(X,'fro') )

        S = X - X_p

        fval, gradf = obj_fun(X)
        gradr_p = gradr
        gradr = manifold.JA(X, gradf) + beta * manifold.JC(X, manifold.C(X))
        Y = gradr - gradr_p

        substationarity = np.linalg.norm(gradr, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity == 2 and np.mod(jj,20) == 0:
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

        kkts.append( substationarity )
        feas.append( feasibility )
        fvals.append( fval )



        if substationarity < gtol:
            if verbosity >= 1:
                print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))

            break

    if post_process:
        X = manifold.Post_process(X)
        fval, gradf = obj_fun(X)
        gradr = manifold.JA(X, gradf)
        substationarity = np.linalg.norm(gradr, 'fro')
        feasibility = manifold.Feas_eval(X)

        if verbosity >= 1:
            print("Post-processing")
            print("Iter:{}    fval:{:.3e}   kkts:{:.3e}    feas:{:3e}".format(jj,fval, substationarity, feasibility))


        kkts[-1] = substationarity
        feas[-1] = feasibility
        fvals[-1] = fval


    output_dict = { 'kkts': kkts, 'fvals': fvals, 'fea': feasibility, 'kkt': substationarity, 'fval': fval, 'feas': feas}

    return X, output_dict







