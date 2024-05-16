import numpy as np
import scipy.sparse as sp

np.random.seed(12345)


class EASE:
    def __init__(self, l2: float):
        self.l2 = l2
        self.B = None

    def fit(self, X: sp.csr_matrix, density=0.01):
        n_items = X.shape[1]
        print("Constructing G...")
        G = X.T @ X + self.l2 * sp.eye(n_items, dtype=X.dtype)
        print(f"Density of G: {G.nnz/(G.shape[1]**2):.4%}")
        G = G.toarray()
        print("Inverting G...")
        P = np.linalg.inv(G)
        self.B = np.eye(n_items, dtype=X.dtype) - P / np.diag(P)

        # prune to specified density
        keep_threshold = np.quantile(np.abs(self.B), 1-density)
        self.B[np.abs(self.B) < keep_threshold] = 0
        nonzero_x, nonzero_y = self.B.nonzero()
        nonzero_values = self.B[nonzero_x, nonzero_y]
        self.B = sp.csr_matrix((nonzero_values, (nonzero_x, nonzero_y)), shape=self.B.shape)

    def recommend(self, X: sp.csr_matrix):
        n_users = X.shape[0]
        S = X @ self.B
        S = S.toarray()
        # set scores for input items to zero
        S[X.nonzero()] = 0
        return S


class AbsEASE(EASE):
    def fit(self, X: sp.csr_matrix, density=0.01):
        super().fit(X)
        self.B.data *= np.sign(self.B.data)