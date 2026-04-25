import numpy as np
from typing import List

class MockAgent:
    def __init__(self, accuracy: float, correlation_with_others: float = 0.0):
        self.accuracy = accuracy
        self.correlation = correlation_with_others
        
    def predict(self, labels: np.ndarray, latent_correlation_signal: np.ndarray = None) -> np.ndarray:
        """
        Predicts binary truths with some accuracy and correlation.
        latent_correlation_signal: (m_claims,) noise signal common across agents.
        """
        m = len(labels)
        # Random noise + latent correlation signal
        if latent_correlation_signal is None:
            latent_correlation_signal = np.zeros(m)
            
        noise = (1 - self.correlation) * np.random.randn(m) + self.correlation * latent_correlation_signal
        # Threshold for noise to achieve target accuracy
        # If noise > threshold, predict correctly.
        threshold = np.percentile(noise, (1 - self.accuracy) * 100)
        
        predictions = labels.copy().astype(float)
        # Introduce errors where noise <= threshold
        error_mask = noise <= threshold
        predictions[error_mask] = 1 - predictions[error_mask]
        
        # Convert to soft beliefs (e.g., 0.9 for correct-looking, 0.1 for incorrect-looking)
        # Simulating well-calibrated but imperfect agents
        soft_beliefs = np.where(predictions == 1, 
                                np.random.uniform(0.6, 0.95, m), 
                                np.random.uniform(0.05, 0.4, m))
        
        return soft_beliefs

def create_correlated_agents(n_agents: int, accuracy: float, correlation: float) -> List[MockAgent]:
    """Creates a pool of agents with a shared error correlation signal."""
    return [MockAgent(accuracy, correlation) for _ in range(n_agents)]
