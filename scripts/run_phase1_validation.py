import sys
import os
import numpy as np
import pandas as pd
from typing import List

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.accord.aggregator import ACCORDBaseAggregator
from src.agents.mock_agents import create_correlated_agents

def calculate_chr(predictions: np.ndarray, labels: np.ndarray) -> float:
    """
    Correlated Hallucination Risk (CHR): 
    Probability that all agents agree (on correctness or hallucination) and are WRONG.
    Specifically for hallucinations: P(unanimous agreement on wrong claim).
    """
    # predictions: (m_claims, n_agents) binarized predictions
    # labels: (m_claims,) true binary labels
    
    # All agents agree
    unanimous = np.all(predictions == predictions[:, [0]], axis=1)
    
    # Wrong (assuming we are interested in unanimous wrong claims)
    wrong = predictions[:, 0] != labels
    
    chr_val = np.mean(unanimous & wrong)
    return chr_val

def run_validation():
    print("=== ACCORD Phase 1: Fast Validity Check ===")
    
    # 1. Setup Simulation (Target: VERY High Correlation κ -> 1)
    n_claims = 2000
    n_agents = 6
    target_accuracy = 0.70
    target_kappa = 0.9  # Very high inter-agent correlation
    
    # True labels
    y_true = np.random.randint(0, 2, n_claims)
    
    # Latent correlation signal (shared noise)
    shared_noise = np.random.randn(n_claims)
    
    # 2. Generate Agent Predictions
    agents = create_correlated_agents(n_agents, target_accuracy, target_kappa)
    agent_beliefs = np.array([agent.predict(y_true, shared_noise) for agent in agents]).T
    agent_binarized = (agent_beliefs > 0.5).astype(int)
    
    # 3. Baseline: Single Agent
    chr_single = calculate_chr(agent_binarized[:, [0]], y_true)
    
    # 4. Baseline: Majority Vote
    majority_vote = (np.mean(agent_binarized, axis=1) > 0.5).astype(int)
    # Majority vote chr is special: we look at cases where the consensus is unanimous
    chr_mv = calculate_chr(agent_binarized, y_true)
    
    # 5. ACCORD Aggregator
    # Calibrate on a subset (100 examples)
    cal_size = 100
    aggregator = ACCORDBaseAggregator(n_agents)
    aggregator.calibrate(agent_beliefs[:cal_size], y_true[:cal_size])
    
    # Test on remaining
    test_beliefs = agent_beliefs[cal_size:]
    test_labels = y_true[cal_size:]
    
    accord_posteriors = np.array([aggregator.aggregate(b) for b in test_beliefs])
    accord_binarized = (accord_posteriors > 0.5).astype(int)
    
    # Calculate CHR for ACCORD
    # ACCORD "reduces CHR by explicitly modeling κ and discounting consensus confidence"
    # To measure CHR for ACCORD, we look at the binarized final decision
    chr_accord = np.mean((accord_binarized != test_labels) & (np.all(agent_binarized[cal_size:] == agent_binarized[cal_size:, [0]], axis=1)))

    # Metrics
    mv_acc = np.mean(majority_vote[cal_size:] == test_labels)
    accord_acc = np.mean(accord_binarized == test_labels)
    
    print(f"\nSimulation Results (κ={target_kappa}):")
    print(f"{'Method':<20} | {'Accuracy':<10} | {'CHR':<10}")
    print("-" * 45)
    print(f"{'Single Agent':<20} | {target_accuracy:<10.4f} | {chr_single:<10.4f}")
    print(f"{'Majority Vote':<20} | {mv_acc:<10.4f} | {chr_mv:<10.4f}")
    print(f"{'ACCORD (Ours)':<20} | {accord_acc:<10.4f} | {chr_accord:<10.4f}")
    
    reduction = (chr_mv - chr_accord) / max(chr_mv, 1e-10) * 100
    print(f"\nRelative CHR Reduction: {reduction:.2f}%")
    
    if reduction >= 15:
        print("\nSUCCESS: Phase 1 Validation target (>15% CHR reduction) met.")
    else:
        print("\nWARNING: Phase 1 Validation target not met. Check Σ estimation.")

if __name__ == "__main__":
    run_validation()
