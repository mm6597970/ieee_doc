# ACCORD: Formal Mathematical Proofs (Markdown Format)

This document provides the formal mathematical foundations for the ACCORD framework, supporting the IEEE/Springer Research Paper submission.

---

## Proposition 1: Bias of Independence-Assuming Consensus
**Theorem Statement:** Under the Gaussian copula model with correlation matrix $\Sigma$ and agent reliability vector $\Theta$, the independence-assuming majority vote posterior overestimates claim correctness probability.

**Proof Sketch:**
Let $\epsilon_i$ be the error for agent $i$.
Under independence, $P(\text{all wrong}) = \prod P(\epsilon_i)$.
Under the Gaussian copula, as correlation $\kappa \to 1$, the joint error probability approaches the error rate of a single agent:
$$P(\epsilon_1, \dots, \epsilon_n) \to \min_i P(\epsilon_i)$$
Since $\prod P(\epsilon_i) \ll \min P(\epsilon_i)$, the independence assumption systematically underestimates joint failure, leading to a massive overestimation of correctness probability.

---

## Theorem 1: Consistency of ACCORD Estimator
**Theorem Statement:** Under regularity conditions (bounded correlation and acyclic graph $G$), the ACCORD estimator is consistent:
$$\hat{P}(y_c = 1 \mid \dots) \to P(y_c = 1) \text{ as } n \to \infty$$

**Proof Sketch:**
ACCORD is an extension of the Dawid-Skene model. Consistency follows from the strict concavity of the copula-corrected log-likelihood function. Since the correlation $\Sigma$ is bounded and the Claim Dependency Graph (CDG) is a DAG, belief propagation messages converge to the true marginals, ensuring that the estimator converges to the ground truth labels as agent evidence accumulates.

---

## Theorem 2: Conformal Hallucination Rate Control
**Theorem Statement:** Given a calibration set, there exists a threshold $\lambda^*$ such that the hallucination risk $R$ satisfies:
$$P(R_{ACCORD}(\lambda^*) \le \delta) \ge 1 - \alpha$$

**Proof Sketch:**
We apply the Conformal Risk Control (CRC) framework. The loss function $L(c) = 1$ if a hallucination is accepted. Since the ACCORD posterior is monotonic (higher probability $\to$ lower risk), we can find a threshold $\lambda^*$ on a small calibration set that provides a distribution-free guarantee on the total error rate of accepted claims.

---

## Proposition 2: POMDP Pareto Dominance
**Theorem Statement:** The optimal POMDP policy $\pi^*$ Pareto-dominates any fixed-threshold policy on the (accuracy, cost) frontier.

**Proof Sketch:**
A fixed-threshold policy (e.g., "accept if score > 0.9") is a degenerate (simple) version of a POMDP policy. Since the POMDP solver searches the entire space of policies, and the fixed-threshold rule is within that space, the optimal POMDP policy must perform at least as well as, or better than, any fixed-threshold rule.

---

## Corollary: CHR-κ Relationship
**Theorem Statement:** For homogeneous agents, Correlated Hallucination Risk (CHR) increases monotonically with agent correlation $\kappa$.

**Proof Sketch:**
Under independence, CHR is $p^n$ (where $p$ is error rate). Under the copula, CHR approaches $p$ as $\kappa \to 1$. The gap between the two represents the "unanimous wrong" scenario where all agents fail together. As agents become more similar, the diversity benefit disappears, and CHR rises toward the single-agent failure rate.
