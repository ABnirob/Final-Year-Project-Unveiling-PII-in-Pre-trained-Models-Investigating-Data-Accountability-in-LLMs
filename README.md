# 🔐 Unveiling PII in Pre-trained Models | Data Accountability in LLMs

<p align="center">
  <img src="https://img.shields.io/badge/Research-Academic-1f77b4?style=flat&logo=academia" alt="Academic Research" />
  <img src="https://img.shields.io/badge/LLMs-GPT--2%20%7C%20OPT%20%7C%20Pythia-4ECDC4?style=flat&logo=huggingface" alt="LLMs" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/PyTorch-2.0-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?logo=huggingface&logoColor=black" alt="HuggingFace" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT" />
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen" alt="Status: Completed" />
</p>

---

## 📋 Executive Summary

Large Language Models (LLMs) like GPT, BERT, and OPT have revolutionized natural language processing. However, these models are often trained on massive datasets scraped from the web **without proper filtration**, leading to the inadvertent memorization of **Personally Identifiable Information (PII)** — names, email addresses, phone numbers, and other sensitive data.

This research project investigates methodologies to **detect the presence of PII in LLM pre-training datasets** and proposes a **novel unlearning technique** to mitigate privacy risks. We introduce **Token Probability and Frequency Scoring (TPFS)** — our own novel method — alongside existing approaches like Min-K% and Min-K%++, across multiple LLM architectures.

> **Key Achievement:** Successfully demonstrated that detecting and unlearning sensitive data is feasible, laying the groundwork for ethical AI practices and GDPR compliance.

---

## 🎯 Research Objectives

| # | Objective | Status |
|---|-----------|--------|
| 1 | Develop a novel methodology (TPFS) to detect PII memorization in pre-trained LLMs | ✅ Achieved |
| 2 | Compare TPFS against baseline methods (Min-K%, Min-K%++) across multiple models | ✅ Achieved |
| 3 | Quantify the privacy leakage risk in popular LLMs (GPT-2, OPT, GPT-Neo, Pythia) | ✅ Achieved |
| 4 | Propose and validate a negative sampling-based machine unlearning approach | ✅ Achieved |
| 5 | Contribute to data accountability and ethical AI practices | ✅ Achieved |

---

## 🔬 Methodology Overview

### 1. Detection Methods Evaluated

| Method | Description | Key Insight |
|--------|-------------|-------------|
| **Min-K%** | Uses log-probability scores; selects lowest K% of tokens. Baseline method. | Simple but biased toward common tokens |
| **Min-K%++** | Normalizes token probabilities via z-scores before selection. | More robust than Min-K% |
| **TPFS (Ours)** | Combines model probabilities with external token frequency distributions from reference corpus. | **Balanced detection** — common tokens are not falsely flagged |


---
### 2. TPFS Workflow
Input Name → Tokenization → Model Probability Calculation
↓
Log-Odds Computation (Model Prob × Frequency)
↓
TPFS Score Aggregation → Memorization Decision


---

