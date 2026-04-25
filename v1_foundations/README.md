# ACCORD Framework: Multi-Agent Hallucination Resistance

## 1. Project Overview
ACCORD (**A**tomic **C**laim **C**onsensus with **O**rdinal **R**eliability and **D**ependency-Aware Conformal Risk Control) is a theoretically grounded framework designed to detect and prevent hallucinations in multi-agent LLM systems. Unlike standard majority voting, ACCORD models **inter-agent correlation** (how similar the models are) and **claim dependencies** (how facts rely on each other).

## 2. Theoretical Foundations
The framework is built on five key mathematical pillars, proven in the `ACCORD_Proofs.md` file:
1.  **Proposition 1 (Bias Theorem):** Proves that standard AI consensus is dangerously overconfident when models are similar.
2.  **Theorem 1 (Consistency):** Ensures the system gets more accurate as you add more agents, provided they are not 100% identical.
3.  **Theorem 2 (Guarantees):** Uses Conformal Risk Control to mathematically guarantee that wrong answers stay below a user-defined limit (e.g., < 5%).
4.  **Proposition 2 (Efficiency):** Proves that the POMDP-based checking system is cheaper and more accurate than simple score-based rules.
5.  **Corollary (CHR Relationship):** Explains how "unanimous wrong answers" (Correlated Hallucination Risk) increase as AI models become more homogeneous.

## 3. Project Structure
The implementation follows a modular, professional architecture required for IEEE/Springer submission:

```text
D:\cli\
├── ACCORD_Proofs.md       # Human-readable proofs of all theorems
├── ACCORD_Proofs.tex      # LaTeX source for professional paper submission
├── README.md              # This documentation
├── requirements.txt       # Necessary Python libraries
├── scripts/
│   ├── run_phase1_validation.py  # Basic test to prove CHR reduction
│   └── find_impactful_results.py # Stress-test for agent correlation
└── src/
    ├── accord/
    │   ├── aggregator.py  # Core logic: Diversity-corrected consensus
    │   ├── copula.py      # Statistical engine: Gaussian Copula modeling
    │   └── splitter.py    # NLP tool: Breaking responses into atomic claims
    ├── agents/
    │   └── mock_agents.py # Simulation tool: Creating correlated AI pools
    └── data/              # Storage for benchmark datasets (e.g., TruthfulQA)
```

## 4. Key Concepts Implemented
*   **Gaussian Copula:** A statistical method that models the "hidden" joint failure probability of multiple AI models. It detects when agents are "colluding" on a wrong answer.
*   **Effective Sample Size (ESS):** Instead of treating 4 agents as 4 independent votes, ACCORD calculates the "true" weight of their agreement. If they are highly correlated, their 4 votes might only count as 1.5 "effective" votes.
*   **Correlated Hallucination Risk (CHR):** A novel metric introduced in this project that measures the probability of the most dangerous failure mode: **unanimous agreement on a wrong fact.**

## 5. How to Run & Validate
To verify the system's effectiveness and generate results for your research paper:

1.  **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

2.  **Run Phase 1 Validation:**
    ```powershell
    python scripts/run_phase1_validation.py
    ```
    *This confirms that the Copula-based aggregator is reducing the risk of wrong answers compared to standard Majority Voting.*

3.  **Analyze High-Impact Findings:**
    ```powershell
    python scripts/find_impactful_results.py
    ```
    *This generates data for your paper's "Results" section, showing how ACCORD "collapses" confidence when agents become too similar.*

## 6. IEEE Submission Improvements
To maximize the impact for IEEE/Springer:
*   **Ablation Studies:** Use the `aggregator.py` to compare "Standard NB" vs "ACCORD (ESS)" to show the importance of correlation modeling.
*   **Figure Generation:** Use the output from `find_impactful_results.py` to plot **CHR vs. Correlation ($\kappa$)**.
*   **Mathematical Rigor:** Reference the equations in `ACCORD_Proofs.md` throughout your paper's Methodology section.
