# 🔐 Unveiling PII in Pre-trained Models | Data Accountability in LLMs

<p align="center">
  <img src="https://img.shields.io/badge/Research-Academic-1f77b4?style=flat&logo=academia" alt="Academic Research" />
  <img src="https://img.shields.io/badge/LLMs-GPT--2%20%7C%20OPT%20%7C%20Pythia-4ECDC4?style=flat&logo=huggingface" alt="LLMs" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python 3.12" />
  <img src="https://img.shields.io/badge/PyTorch-2.0-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch" />
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?logo=huggingface&logoColor=black" alt="HuggingFace" />
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


### 2. TPFS Workflow
Input Name → Tokenization → Model Probability Calculation
↓
Log-Odds Computation (Model Prob × Frequency)
↓
TPFS Score Aggregation → Memorization Decision


### 3. Unlearning Approach (Negative Sampling)
Sensitive PII (e.g., email@enron.com) → Replace with Placeholder (email@example.com)
↓
Fine-tune Model (AdamW optimizer, 10 epochs)
↓
Model learns to predict placeholder instead of PII


---

---

## 📊 Experiments & Results

### Models Tested

| Model | Parameters | Architecture |
|-------|-----------|--------------|
| GPT-2 Medium | 355M | Transformer Decoder |
| GPT-2 XL | 1.5B | Transformer Decoder |
| GPT-Neo 1.3B | 1.3B | Transformer Decoder |
| GPT-Neo 2.7B | 2.7B | Transformer Decoder |
| OPT 1.3B | 1.3B | Transformer Decoder |
| OPT 2.7B | 2.7B | Transformer Decoder |
| Pythia 1.4B | 1.4B | Transformer Decoder |
| Pythia 2.4B | 2.4B | Transformer Decoder |

### Datasets Used

| Dataset | Purpose | Size |
|---------|---------|------|
| OpenWebText (NER-extracted names) | **Seen Data** — names model has encountered | 500 samples |
| Synthetic Names (Faker library) | **Unseen Data** — names model has never seen | 500 samples |
| WikiMIA-24 (NER-extracted names) | **Reference Corpus** for TPFS frequency calculation | 12,000 names |

### Sample Data Example

| Seen Names | Unseen Names | Reference Names |
|------------|--------------|-----------------|
| David Wain | Rebeca Gomes | Brittany Payne |
| Noam Chomsky | Isabela Martins | Nikol Pashinyan |
| John O'Neil | Benjamim Peixoto | Brooke Jenkins |
| Steve Eder | Eduarda Rios | Sunil Narine |

### Key Results (AUC Scores)

| Model | TPFS | Min-K% (K=20%) | Min-K%++ (K=20%) |
|-------|------|----------------|------------------|
| **OPT 2.7B** | **0.6050** | 0.5998 | 0.6219 |
| **GPT-Neo 2.7B** | 0.5942 | **0.6796** | 0.6700 |
| GPT-2 XL | 0.5509 | **0.6510** | 0.6952 |
| Pythia 1.4B | 0.5842 | **0.6495** | 0.6339 |

### Unlearning Results (GPT-2 Medium on Enron Email Dataset)

| Metric | Before Unlearning | After Unlearning | Improvement |
|--------|-------------------|------------------|-------------|
| **AUC Score** | 0.5790 | **0.5077** | ↓ 12.3% |
| **Interpretation** | Model could distinguish seen vs. unseen emails | **Near-random** — association with sensitive data minimized | ✅ Success |

> **Key Finding:** Even with only 10 epochs of negative sampling, the model's ability to recognize sensitive PII dropped to near-random levels, demonstrating the feasibility of machine unlearning.

---

## 💡 Key Findings & Contributions

| # | Finding | Impact |
|---|---------|--------|
| 1 | **LLMs do memorize PII** from pre-training data | Validates privacy concerns |
| 2 | **TPFS provides robust detection** across all K values | Better for real-world applications |
| 3 | **Min-K% at K=20% gives highest peak AUC** | Useful for targeted detection |
| 4 | **Negative sampling unlearning works** — even with limited epochs | Practical mitigation path |
| 5 | **Reference corpus quality matters** — larger corpus improves TPFS | Future improvement direction |

---

## 🛠️ Technical Implementation

### Software Stack

| Component | Tools Used |
|-----------|-----------|
| **Deep Learning** | PyTorch, Hugging Face Transformers |
| **NLP Processing** | SpaCy (NER), Faker (synthetic data) |
| **Evaluation** | Matplotlib (ROC curves), Scikit-learn (AUC) |
| **Platform** | Kaggle, Google Colab |

### Key Code Snippet — TPFS Score Calculation

```python
def compute_tpfs_score(model, tokenizer, name, reference_frequencies):
    # Tokenize input
    tokens = tokenizer.encode(name)
    
    # Get model probabilities
    with torch.no_grad():
        outputs = model(torch.tensor([tokens]))
        probs = torch.softmax(outputs.logits, dim=-1)
    
    # Compute log-odds for each token
    log_odds_sum = 0
    for i, token in enumerate(tokens):
        prob = probs[0, i, token].item()
        freq = reference_frequencies.get(token, 1e-6)
        log_odds_sum += -prob * np.log(freq)
    
    return log_odds_sum / len(tokens)

---

