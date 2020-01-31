"""Computes the realignment of a bipartite operator."""
import numpy as np
import operator
import functools
from toqito.perms.swap import swap
from toqito.super_operators.partial_transpose import partial_transpose


def realignment(input_mat: np.ndarray, dim=None) -> np.ndarray:
    """
    Compute the realignment of a bipartite operator.

    Gives the realignment of the matrix INPUT_MAT, where it is assumed that
    the number of rows and columns of INPUT_MAT are both perfect squares and
    both subsystems have equal dimension. The realignment is defined by mapping
    the operator |ij><kl| to |ik><jl| and extending linearly.

    If INPUT_MAT is non-square, different row and column dimensions can be
    specified by putting the row dimensions in the first row of DIM and the
    column dimensions in the second row of DIM.

    :param input_mat: The input matrix.
    :param dim: Default has all equal dimensions.
    :return: The realignment map matrix.
    """
    eps = np.finfo(float).eps
    dX = input_mat.shape
    round_dim = np.round(np.sqrt(dX))
    if dim is None:
        dim = np.transpose(np.array([round_dim]))
    if isinstance(dim, list):
        dim = np.array(dim)

    if isinstance(dim, int):
        dim = np.array([[dim], [dX[0]/dim]])
        if np.abs(dim[1] - np.round(dim[1])) >= 2*dX[0]*eps:
            raise ValueError("InvalidDim:")
        dim[1] = np.round(dim[1])
        dim = np.array([[1], [4]])

    if min(dim.shape) == 1:
        dim = dim[:].T
        print(dim)
        dim = functools.reduce(operator.iconcat, dim, [])
        dim = np.array([dim, dim])
        #dim = functools.reduce(operator.iconcat, dim, [])
        print(dim)

    dim_x = np.array([[dim[0][1], dim[0][0]], [dim[1][0], dim[1][1]]])
    dim_y = np.array([[dim[1][0], dim[0][0]], [dim[0][1], dim[1][1]]])
    swapped_input = swap(input_mat, [1, 2], dim, True)
    print(swapped_input)

    return swap(partial_transpose(swapped_input, sys=1, dim=dim_x), [1, 2], dim_y, True)