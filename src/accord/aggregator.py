import numpy as np
from typing import List, Dict, Tuple
from .copula import GaussianCopulaEstimator

class ACCORDBaseAggregator:
    def __init__(self, n_agents: int):
        self.n_agents = n_agents
        self.copula_estimator = GaussianCopulaEstimator(n_agents)
        self.agent_reliabilities = np.ones(n_agents) * 0.8  # Initial prior on agent accuracy
        
    def calibrate(self, calibration_data: np.ndarray, calibration_labels: np.ndarray):
        """
        Calibrates the aggregator on a calibration set.
        calibration_data: (m_claims, n_agents) agent beliefs A_i(c).
        calibration_labels: (m_claims,) true binary labels.
        """
        # error_matrix = I(A_i(c) != y_c)
        # For simplicity, we binarize agent predictions at 0.5 threshold for correlation estimation
        # In a real system, we'd use soft-calibrated error residuals.
        error_matrix = (calibration_data > 0.5).astype(int) != calibration_labels[:, None].astype(int)
        self.copula_estimator.estimate_sigma(error_matrix)
        
        # Update reliabilities (p_i accuracy = 1 - error_rate)
        self.agent_reliabilities = 1 - np.mean(error_matrix, axis=0)
        
    def aggregate(self, agent_beliefs: np.ndarray) -> float:
        """
        Aggregates agent beliefs A_i(c) into a single posterior P(y_c=1).
        agent_beliefs: (n_agents,) array of soft beliefs in [0, 1].
        """
        # Calculate Effective Sample Size (ESS) based on average correlation
        sigma = self.copula_estimator.sigma
        # Average off-diagonal correlation
        n = self.n_agents
        if n > 1:
            avg_corr = (np.sum(sigma) - n) / (n * (n - 1))
            avg_corr = max(0, avg_corr)
            # Effective Sample Size formula for correlated observations
            ess = n / (1 + (n - 1) * avg_corr)
        else:
            ess = 1.0
            
        # Naive Bayes posterior log-odds
        eps = 1e-9
        beliefs = np.clip(agent_beliefs, eps, 1 - eps)
        log_odds = np.log(beliefs / (1 - beliefs))
        
        # ACCORD Correction: Scale total log-odds by (ESS / n)
        # Instead of summing N independent pieces of evidence, 
        # we treat them as ESS pieces of evidence.
        aggregated_log_odds = np.sum(log_odds) * (ess / n)
        
        corrected_posterior = 1 / (1 + np.exp(-aggregated_log_odds))
        
        return np.clip(corrected_posterior, 0.0, 1.0)

class ConformalAggregator(ACCORDBaseAggregator):
    def __init__(self, n_agents: int, delta: float = 0.05, alpha: float = 0.1):
        super().__init__(n_agents)
        self.delta = delta  # Max allowed hallucination rate
        self.alpha = alpha  # Confidence level (1 - alpha)
        self.lambda_star = 0.5  # Default threshold
        
    def calibrate_crc(self, calibration_data: np.ndarray, calibration_labels: np.ndarray):
        """
        Computes the CRC threshold lambda* to bound the hallucination rate.
        Following Angelopoulos et al. (2022) with Hoeffding-like correction.
        """
        self.calibrate(calibration_data, calibration_labels)
        posteriors = np.array([self.aggregate(b) for b in calibration_data])
        
        lambdas = np.linspace(0.5, 0.99, 100)
        n = len(calibration_labels)
        
        # Risk target delta_target with confidence correction
        # We want P(Risk > delta) <= alpha
        # Using a simple (n+1)/n correction for CRC
        corrected_delta = (n / (n + 1)) * self.delta
        
        for l in lambdas:
            accepted = posteriors >= l
            if np.sum(accepted) == 0:
                self.lambda_star = l
                break
            
            # Empirical risk on accepted claims
            hallucinated = (calibration_labels == 0) & accepted
            risk = np.sum(hallucinated) / n
            
            if risk <= corrected_delta:
                self.lambda_star = l
                break
        
        print(f"CRC Calibration Complete. Lambda* set to: {self.lambda_star:.4f} for delta={self.delta}")

    def detect_patient_zero(self, claim_ids: List[int], graph_edges: List[Tuple[int, int]], beliefs: List[float]) -> int:
        """
        Identifies the 'Patient Zero' root claim that likely caused downstream errors.
        Uses a heuristic based on belief propagation influence.
        """
        # Simple influence heuristic: Root nodes with low beliefs are likely Patient Zeroes
        parents = {target for _, target in graph_edges}
        roots = [c for c in claim_ids if c not in parents]
        
        if not roots: return claim_ids[0]
        
        # Patient zero is the root with the lowest belief (highest error probability)
        root_beliefs = {c: beliefs[claim_ids.index(c)] for c in roots}
        return min(root_beliefs, key=root_beliefs.get)

    def predict_safe(self, agent_beliefs: np.ndarray) -> Tuple[int, float]:
        """
        Returns (prediction, posterior) if the claim is accepted by CRC, else (0, posterior).
        """
        posterior = self.aggregate(agent_beliefs)
        if posterior >= self.lambda_star:
            return 1, posterior
        else:
            return 0, posterior # Rejected/Abstained
