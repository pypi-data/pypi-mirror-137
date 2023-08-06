import numpy as np

"""
Diffeomorphisms
"""

def hypercube_to_simplex(X, scale):
    """
    Sends the interval (0,1)^n to a rectangular simplex of dimension n with
    legs specified by scale.

    Source: https://math.stackexchange.com/a/1945720

    X: Points in the interval (0,1)^n.
        numpy.array
    scale: Matrix of two columns specifying bounds of the simplex
            in the form [[a^0_min,...,a^{n-1}_min],[a^0_max,...,a^{n-1}_max]]
        numpy.array
    """
    n = X.shape[1]
    r = np.ones(n)
    T = np.tensordot(1-X, r, axes=0) #Repeats rows of 1-X n times in a tensor of shape (m,n,n)
    T = T*(1-np.eye(n)) + np.eye(n) #Fills diagonals with ones for each row: (:,n,n)
    T = T.prod(axis=1) #Multiply over columns (m,n)
    S = X*T #Coords in an unitary rectangle simplex
    S = scale[0,:]*S + scale[1,:]*(1-S)#scaling
    return S
