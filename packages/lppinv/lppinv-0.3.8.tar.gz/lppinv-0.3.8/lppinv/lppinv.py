"""
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
"Hybrid" LS-LP model pseudoinverse-based (SVD-based) solving algorithm
© econcz, 2022
––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

Overview:
–––––––––
The algorithm solves "hybrid" least squares linear programming (LS-LP) problems
with the help of the Moore-Penrose inverse (pseudoinverse), calculated using
singular value decomposition (SVD), with emphasis on estimation of non-typical
constrained OLS (cOLS), Transaction Matrix (TM) [1], and custom (user-defined)
cases. The pseudoinverse offers a unique solution and may be the best linear
unbiased estimator (BLUE) for a group of problems under certain conditions [2].

Example of a non-typical cOLS problem:
- Estimate the trend and the cyclical component of a country's GDP given
  the textbook or any other definition of its peaks, troughs, and saddles.

Example of an TM problem:
- Estimate the input-output table or a matrix of trade / investment / etc.,
  the technical coefficients or (country) shares of which are unknown.

Mechanism:
––––––––––
The problem is written as a matrix equation `a @ x = b` where `a` consists of
coefficients for CONSTRAINTS and for SLACK VARIABLES (the upper part) as well
as for MODEL (the lower part) as illustrated in Figure 1. Each part of `a` can
be omitted to accommodate a special case:
- cOLS problems require no case-specific CONSTRAINTS;
- TM problems require case-specific CONSTRAINTS, no problem CONSTRAINTS, and
  an optional MODEL;
- SLACK VARIABLES are non-zero only for inequality constraints and are omitted
  if problems don't include any;
...

Figure 1: Matrix equation `a @ x = b`
                             `a`                            |       `b`
+–––––––––––––––––––––––––––––––––––––––––+–––––––––––––––––+–––––––––––––––––+
|  CONSTRAINTS (PROBLEM + CASE-SPECIFIC)  | SLACK VARIABLES |   CONSTRAINTS   |
+–––––––––––––––––––––––––––––––––––––––––+–––––––––––––––––+–––––––––––––––––+
|                           MODEL                           |      MODEL      |
+–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––+–––––––––––––––––+
                                                            |
Source: self-prepared

The solution of the equation, `x = pinv(a) @ b`, is calculated with the help
of numpy.linalg.lstsq(). To check if `a` is within computational limits, its
(maximum) dimensions can be calculated using the formulas:

- (2 * N) x (K + K*    )    cOLS without slack variables;
- (2 * N) x (K + K* + 1)    cOLS with slack variables;
- (M * N) x (M * N)         TM without slack variables;
- (M * N) x (M * N + 1)     TM with slack variables;
- M x N                     custom without slack variables;
- M x (N + 1)               custom with slack variables;

where, in cOLS problems, K is the number of independent variables in the model
(including the constant), K* (K* \not \in K) is the number of extra variables
in CONSTRAINTS, and N is the number of observations; in TM problems, M and N
are the dimensions of the transaction matrix; and in custom cases, M and N or
M x (N + 1) are the dimensions of `a` (fully user-defined).

Parameters:
–––––––––––
    # LS-LP type and input
    lp        : str or unicode, optional
                'cOLS' (Constrained OLS), 'TM' (Transaction Matrix), or
                'custom' (user-defined case).
    lhs       : sequence of array_like
                Left-hand side of the problem (NB 3D iterable for lp='cOLS').
    rhs       : sequence of array_like
                Right-hand side of the problem (NB row sums first for lp='TM').
    svar      : array_like
                Slack variables.
    # `a` and estimation
    diag      : bool, optional
                Diagonal of M x N (NB for lp='TM').
    rcond     : float, optional
                Cut-off ratio for small singular values of a. For the purposes
                of rank determination, singular values are treated as zero if
                they are smaller than rcond times the largest singular value
                of a in `numpy.linalg.lstsq(a, b, rcond=rcond)`.

Returns:
––––––––
    x         : {(N,), (N, K)} ndarray
                Least-squares solution. If b is two-dimensional, the solutions
                are in the K columns of x.
    nrmse     : float
                Square root of sums of squared residuals normalized by variance
                of b.
    a         : (ndarray, int) tuple
                Matrix `a', Rank of a.
    s         : (min(M, N),) ndarray
                Singular values of a.

Raises:
–––––––
    LPpinvError  If the LS-LP problem is incorrectly specified.
    LinAlgError  If computation does not converge.

Notes:
––––––
[1] Transaction Matrix (TM) of size M x N is a formal model of transactions
    between M and N elements in a system.
    For example,
    - an input-output table (IOT) is a type of TM where M = N and the elements
      are industries;
    - a matrix of trade / investment / etc. is a type of TM where M = N and
      the elements are countries or (macro)regions in which diagonal elements
      can, in some cases, all be equal to zero.

[2] For example, consult Albert, A., 1972. Regression And The Moore-Penrose
    Pseudoinverse. New York: Academic Press. Chapter VII.
"""

import numpy as np

class LPpinvError(Exception): # ---------------------------------------------- #
    """error class"""
    pass

def solve(
    # Function arguments (parameters) ---------------------------------------- #
    lp='custom', lhs=[[]], rhs=[[]], svar=[],          # LS-LP type and input
    diag=None, rcond=None,                             # `a` and estimation
    *args, **kwargs
):
    """main function"""
    # Check for errors ------------------------------------------------------- #
    if lp not in ('cOLS', 'TM', 'custom'):             # LS-LP type
        raise LPpinvError("Unknown LS-LP problem type")

    # Construct `b` and `a` -------------------------------------------------- #
    try:
        b = (np.row_stack([np.array(l).reshape(len(l), 1) for l in rhs])
             if lp != 'custom' else np.array(rhs))
        if lp == 'cOLS':                               # LS-LP type: cOLS
            a = np.row_stack([np.vstack(l).T for l in lhs])
        if lp == 'TM':                                 # LS-LP type: TM
            r, c = (len(l) for l in rhs[0:2])
            a = np.row_stack([
                np.kron(np.identity(r), np.ones(c)),   # row sums
                np.kron(np.ones(r), np.identity(c)),   # column sums
            ])
            if diag:                                   # diagonal of `a`
                a = np.row_stack([a, [
                    np.kron(
                        np.identity(min(r, c))[i], np.identity(max(r, c))[i]
                    ) for i in range(min(r, c))
                ]])
            if np.array(lhs[0]).size:
                a = np.row_stack([a, np.array(lhs)])
        if lp == 'custom':                             # LS-LP type: custom
            a = np.array(lhs)
        if np.array(svar).size:                        # slack variables
            a = np.column_stack([a, (
                np.concatenate([
                    np.array(svar), np.zeros(b.size - np.array(svar).size)
                ]) if lp == 'cOLS' else np.array(svar)
            ).T])
        assert a.size                                  # check for `a`
    except:
        raise LPpinvError("Misspecified LHS, RHS, or SVAR")

    # Obtain an SVD-based solution ------------------------------------------- #
    soln = list(np.linalg.lstsq(a, b, rcond))
    soln[1] = np.sqrt(
        np.sum(np.square(b - a @ soln[0])) /           # normalized RMSE
        len(b) / np.var(b)
    )
    if np.array(svar).size:                            # slack variables
        if lp == 'cOLS':
            soln[0] = soln[0][0:-1]
        if lp == 'TM':
            soln[0] = soln[0][0:r * c]
    if lp == 'TM':                                     # LS-LP type: TM
        soln[0] = soln[0].reshape(r, c)
    soln[2] = a, soln[2]

    # Return the solution ---------------------------------------------------- #
    return soln
