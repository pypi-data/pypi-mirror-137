import numpy as np


class Product_manifold:
    def __init__(self, list_of_manifold) -> None:

        self.var_shape = tuple( M.var_shape for M in list_of_manifold  )

        self.var_dim_list = tuple( np.prod(M_shape) for M_shape in self.var_shape  )

        self.var_dim_split_list = tuple(  np.sum(self.var_dim_list[:i+1]) for i in range( len(self.var_dim_list) -1 )  )
        
        self.dim = np.sum( self.var_dim_list )
        self.list_manifold = list_of_manifold



    def v2m(self, x_vec):
        x_tuple_tmp = np.split(x_vec, self.var_dim_split_list)
        return tuple( np.reshape(x_local, shape_local ) for x_local, shape_local in zip(x_tuple_tmp, self.var_shape)  )



    def m2v(self, X_tuple):
        return np.concatenate(tuple( var.flatten() for var in X_tuple ), axis = 0)



    def Feas_correction(self, x_vec):
        X_list = self.v2m(x_vec)
        return self.m2v(tuple( self.list_manifold[i].Feas_correction(X) for i, X in enumerate(X_list) ))


    def A(self, x_vec):
        X_list = self.v2m(x_vec)
        return self.m2v(tuple( self.list_manifold[i].A(X) for i, X in enumerate(X_list) ))


    # def JA(self, X, G):
    #     XX = X.T @X 
    #     return 1.5 * G - 0.5 * G@( XX ) - X @ self.Phi(X.T @ G)
    

    def JA(self, x_vec, g_vec):
        X_list = self.v2m(x_vec)
        G_list = self.v2m(g_vec)
        return  self.m2v(tuple(M.JA(X, G) for M, X, G in zip(self.list_manifold, X_list, G_list) ))


    def JC(self, x_vec, Lambda_list):
        X_list = self.v2m(x_vec)
        # Lambda_list = self.v2m(lambda_vec)
        return self.m2v(tuple( M.JC(X,Lambda) for M, X, Lambda in zip(self.list_manifold, X_list, Lambda_list) ))

    
    def C_quad_penalty(self, x_vec):
        X_list = self.v2m(x_vec)
        return np.sum( tuple( np.sum(M.C(X) ** 2) for M, X in zip(self.list_manifold, X_list)) )


    

    def C(self, x_vec):
        X_list = self.v2m(x_vec)
        return tuple(M.C(X) for M, X in zip(self.list_manifold, X_list) )

    def Feas_eval(self, X_list):
        return np.sqrt( self.C_quad_penalty(X_list) )

    def Init_point(self, Xinit = None):
        x_vec = Xinit
        if x_vec is None:
            return self.m2v(tuple(M.Init_point() for M in self.list_manifold))
        else:
            X_list = self.v2m(x_vec)
            return self.m2v(tuple(M.Init_point(Xinit) for M, Xinit in zip(self.list_manifold, X_list)))



    def Post_process(self,x_vec):
        X_list = self.v2m(x_vec)
        return self.m2v(self.m2v(tuple(M.Post_process(X) for M, X in zip(self.list_manifold, X_list) )))



    def vectorize_fun(self, obj_fun):
        '''
        Input: obj_fun(X1, X2,... X_m) -> float
        '''
        return lambda x_vec: obj_fun( *self.v2m(x_vec) )



    def vectorize_fungrad(self, obj_fungrad):
        '''
        Input: obj_fun(X1, X2,... X_m) -> ( float, tuple of nd array)
        '''
        def local_fun(x_vec):
            fval, grad_mesh = obj_fungrad(*self.v2m(x_vec))
            return fval, self.m2v(grad_mesh)

        return local_fun
