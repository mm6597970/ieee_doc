# 🏛️ ACCORD Project: Comprehensive Master Record

This document provides a unified overview of the ACCORD framework, synthesizing research findings, technical architecture, and the evolutionary history of the project.

---

## 1. 🚀 Executive Summary
**ACCORD** (Agent-Correlation-Conscious Output Reliability & Detection) is a framework designed to manage multi-agent consensus in LLM systems. It specifically addresses the critical safety issue of **Overconfidence in Correlated Pools**—where models with shared training data (ancestors) fail simultaneously while reporting high confidence.

### Core Value Propositions:
- **Safety**: Uses Gaussian Copulas and Conformal Risk Control (CRC) to guarantee hallucination bounds.
- **Utility**: Automatically detects and leverages "The Heterogeneity Dividend" from diverse model families.
- **Interpretability**: Traces errors back to "Patient Zero" in reasoning chains.

---

## 2. 🧬 Technical Architecture

### 📊 The Statistical Engine (`src/accord/copula.py`)
- **Gaussian Copula**: Models the joint error distribution of agents.
- **Shrinkage-Regularization**: Uses Ledoit-Wolf shrinkage to ensure stability with sparse calibration data.
- **Spectral Analysis**: Analyzes eigenvalues ($\lambda$) of the correlation matrix ($\Sigma$) to detect "Architectural Incest."

### ⚙️ The Aggregator (`src/accord/aggregator.py`)
- **Effective Sample Size (ESS)**: Corrects naive voting by treating $N$ correlated agents as $ESS$ independent agents.
- **Conformal Risk Control (CRC)**: Dynamically adjusts acceptance thresholds to maintain a user-defined risk target (e.g., < 5% error).
- **Patient Zero Detection**: Heuristic-based root-cause analysis for reasoning dependencies.

### 📝 The Splitter (`src/accord/splitter.py`)
- **Atomic Claim Extraction**: Uses NLTK-based sentence tokenization to break complex responses into verifiable units.

---

## 3. 📉 Key Research Findings

### 🌟 The Heterogeneity Dividend
- **Homogeneous Pools ($\kappa > 0.8$):** ACCORD triggers a **"Confidence Collapse,"** dropping its surety rate to ~3.4% to prevent false positives.
- **Heterogeneous Pools ($\kappa < 0.3$):** ACCORD increases surety to ~67.0%, providing a **19.7x Utility Dividend** over homogeneous setups.

### 💀 The Spectral Signature of Incest
The primary eigenvalue ($\lambda_1$) of $\Sigma$ serves as a safety warning. If $\lambda_1$ explains $>80\%$ of variance, the pool is redundant and unsafe for high-stakes tasks.

---

## 4. 📅 Version History & Evolution

| Version | Focus | Key Addition |
| :--- | :--- | :--- |
| **v1** | Foundations | Math proofs for 5 core theorems. |
| **v2** | Validation | Benchmarks on TruthfulQA, FEVER, and HotpotQA. |
| **v3** | Publication | IEEE Submission-ready LaTeX drafts. |
| **v4** | CRC & Attribution | Implementation of Conformal Risk Control. |
| **v5** | Ancestry & Stability | Detection of "Architectural Incest" and shrinkage stability. |
| **v6** | Spectral Reliability | Spectral Entropy metrics and Spectral Signature discovery. |

---

## 🧪 5. Experimental Performance Summary

| Dataset | ACCORD Acc | ACCORD CHR (Risk) | Benefit vs. Majority Vote |
| :--- | :--- | :--- | :--- |
| **TruthfulQA** | 81.2% | 0.004 | **Safety-Gated Failure** |
| **FEVER** | 87.4% | 0.000 | **Hallucination Suppression** |
| **HotpotQA** | 91.8% | 0.000 | **Diversity-Aware Consensus** |

*Note: Data taken from `experimental_results.csv` at $\kappa=0.2$ (Heterogeneous).*

---

**DOCUMENT END: This record serves as the definitive source for the ACCORD Project status as of May 2026.**
