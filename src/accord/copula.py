import numpy as np
from scipy.stats import norm, multivariate_normal
from typing import List, Tuple

class GaussianCopulaEstimator:
    def __init__(self, n_agents: int):
        self.n_agents = n_agents
        self.sigma = np.eye(n_agents)
        
    def estimate_sigma(self, error_matrix: np.ndarray):
        """
        Estimates the Gaussian copula correlation matrix from agent errors.
        error_matrix: (m_claims, n_agents) binary array of errors.
        """
        # Convert binary errors to normal scores using inverse CDF
        # Handling edge cases (all zeros/ones) with a small epsilon
        eps = 1e-6
        # Marginal error rates (p_i)
        p_i = np.mean(error_matrix, axis=0)
        p_i = np.clip(p_i, eps, 1 - eps)
        
        # Mapping binary error to latent standard normal space
        # A simple empirical mapping: 0 -> qnorm(eps), 1 -> qnorm(1-eps)
        # More robustly, we use the rank-based Spearman's rho or Kendall's tau 
        # and convert it to Pearson correlation for the Gaussian copula.
        
        # Pearson correlation of binary indicators is a common proxy for Sigma
        self.sigma = np.corrcoef(error_matrix, rowvar=False)
        # Ensure it's positive semi-definite and symmetric
        self.sigma = (self.sigma + self.sigma.T) / 2
        np.fill_diagonal(self.sigma, 1.0)
        
        # Add a small shrinkage to ensure PD
        self.sigma = (1 - 1e-5) * self.sigma + 1e-5 * np.eye(self.n_agents)
        
    def get_joint_failure_prob(self, marginals: np.ndarray) -> float:
        """
        Calculates P(all agents wrong) using the Gaussian copula.
        marginals: array of P(agent i is wrong).
        """
        # Map marginals to latent standard normal values z_i = Phi^{-1}(p_i)
        eps = 1e-7
        marginals = np.clip(marginals, eps, 1 - eps)
        z = norm.ppf(marginals)
        
        # Multivariate normal CDF at z with correlation sigma
        # This represents P(U_1 <= u_1, ..., U_n <= u_n)
        return multivariate_normal.cdf(z, mean=np.zeros(self.n_agents), cov=self.sigma)
