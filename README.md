# 🔐 Unveiling PII in Pre-trained Models | Data Accountability in LLMs

<p align="center">
  <img src="https://img.shields.io/badge/Research-Academic-1f77b4?style=flat&logo=academia" />
  <img src="https://img.shields.io/badge/LLMs-GPT--2%20%7C%20OPT%20%7C%20Pythia-4ECDC4?style=flat&logo=huggingface" />
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyTorch-2.0-EE4C2C?logo=pytorch&logoColor=white" />
  <img src="https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?logo=huggingface&logoColor=black" />
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen" />
</p>

---

## 📋 Executive Summary

Large Language Models (LLMs) like GPT, BERT, and OPT have revolutionized natural language processing. However, these models are often trained on massive datasets scraped from the web **without proper filtration**, leading to the inadvertent memorization of **Personally Identifiable Information (PII)** — names, email addresses, phone numbers, and other sensitive data.

This research project investigates methodologies to **detect the presence of PII in LLM pre-training datasets** and proposes a **novel unlearning technique** to mitigate privacy risks. We introduce **Token Probability and Frequency Scoring (TPFS)** — our own novel method — alongside existing approaches like Min-K% and Min-K%++, across multiple LLM architectures.

> **Key Achievement:** Successfully demonstrated that detecting and unlearning sensitive data is feasible, laying the groundwork for ethical AI practices and GDPR compliance.

---

## 🎯 Research Objectives

| # | Objective                                                                         | Status     |
| - | --------------------------------------------------------------------------------- | ---------- |
| 1 | Develop a novel methodology (TPFS) to detect PII memorization in pre-trained LLMs | ✅ Achieved |
| 2 | Compare TPFS against baseline methods (Min-K%, Min-K%++) across multiple models   | ✅ Achieved |
| 3 | Quantify the privacy leakage risk in popular LLMs (GPT-2, OPT, GPT-Neo, Pythia)   | ✅ Achieved |
| 4 | Propose and validate a negative sampling-based machine unlearning approach        | ✅ Achieved |
| 5 | Contribute to data accountability and ethical AI practices                        | ✅ Achieved |

---

## 🔬 Methodology Overview

### 1. Detection Methods Evaluated

| Method          | Description                                                                                     | Key Insight                                                    |
| --------------- | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Min-K%**      | Uses log-probability scores; selects lowest K% of tokens. Baseline method.                      | Simple but biased toward common tokens                         |
| **Min-K%++**    | Normalizes token probabilities via z-scores before selection.                                   | More robust than Min-K%                                        |
| **TPFS (Ours)** | Combines model probabilities with external token frequency distributions from reference corpus. | **Balanced detection** — common tokens are not falsely flagged |

---

### 2. TPFS Workflow

```text
Input Name → Tokenization → Model Probability Calculation
↓
Log-Odds Computation (Model Prob × Frequency)
↓
TPFS Score Aggregation → Memorization Decision
```

---

### 3. Unlearning Approach (Negative Sampling)

```text
Sensitive PII (e.g., email@enron.com) → Replace with Placeholder (email@example.com)
↓
Fine-tune Model (AdamW optimizer, 10 epochs)
↓
Model learns to predict placeholder instead of PII
```

---

## 📊 Experiments & Results

### Models Tested

| Model        | Parameters | Architecture        |
| ------------ | ---------- | ------------------- |
| GPT-2 Medium | 355M       | Transformer Decoder |
| GPT-2 XL     | 1.5B       | Transformer Decoder |
| GPT-Neo 1.3B | 1.3B       | Transformer Decoder |
| GPT-Neo 2.7B | 2.7B       | Transformer Decoder |
| OPT 1.3B     | 1.3B       | Transformer Decoder |
| OPT 2.7B     | 2.7B       | Transformer Decoder |
| Pythia 1.4B  | 1.4B       | Transformer Decoder |
| Pythia 2.4B  | 2.4B       | Transformer Decoder |

---

### Datasets Used

| Dataset                           | Purpose          | Size         |
| --------------------------------- | ---------------- | ------------ |
| OpenWebText (NER-extracted names) | Seen Data        | 500 samples  |
| Synthetic Names (Faker library)   | Unseen Data      | 500 samples  |
| WikiMIA-24                        | Reference Corpus | 12,000 names |

---

### Key Results (AUC Scores)

| Model        | TPFS       | Min-K% (K=20%) | Min-K%++ (K=20%) |
| ------------ | ---------- | -------------- | ---------------- |
| OPT 2.7B     | **0.6050** | 0.5998         | 0.6219           |
| GPT-Neo 2.7B | 0.5942     | **0.6796**     | 0.6700           |
| GPT-2 XL     | 0.5509     | **0.6510**     | 0.6952           |
| Pythia 1.4B  | 0.5842     | **0.6495**     | 0.6339           |

---

### Unlearning Results (GPT-2 Medium on Enron Email Dataset)

| Metric    | Before | After      | Improvement |
| --------- | ------ | ---------- | ----------- |
| AUC Score | 0.5790 | **0.5077** | ↓ 12.3%     |

---

## 📸 Output (Results Visualization)

### ROC Curve Example
<img width="1638" height="516" alt="roc curve" src="https://github.com/user-attachments/assets/4faec4b1-56e3-44e0-b12d-84a17dbb1b78" />

### GPT-Neo ROC
<img width="1401" height="461" alt="gpt neo" src="https://github.com/user-attachments/assets/9ea8f29c-565d-4ebb-b3dc-3ea009fc34e8" />

### Unlearning Comparison
<img width="1331" height="505" alt="unlearning" src="https://github.com/user-attachments/assets/f724fb73-de4a-45a6-8b4c-37255e4001ec" />

## 📌 Capstone Poster
<img width="3179" height="4494" alt="Scientific Method Educational Poster (84 1 x 118 9 cm)_1" src="https://github.com/user-attachments/assets/f44eb70f-3d1d-4c2e-8dc0-ccafc284edd7" />
 

---

## 💡 Key Findings & Contributions

* LLMs memorize PII
* TPFS provides robust detection
* Min-K% performs best at K=20%
* Negative sampling unlearning works
* Reference corpus quality impacts TPFS

---

## 🛠️ Technical Implementation

### Software Stack

* PyTorch
* Hugging Face Transformers
* SpaCy
* Faker
* Matplotlib
* Scikit-learn

---

### Run the Project

```bash
git clone https://github.com/ABnirob/Final-Year-Project-Unveiling-PII-in-Pre-trained-Models-Investigating-Data-Accountability-in-LLMs.git
cd Final-Year-Project-Unveiling-PII-in-Pre-trained-Models-Investigating-Data-Accountability-in-LLMs
pip install -r requirements.txt
python detect_pii.py
```

---

## 📁 Repository Structure

```text
project/
├── detection/
├── unlearning/
├── data/
├── results/
├── images/
└── README.md
```

---

## 📝 Conclusion

* Privacy leakage is real
* Detection is possible
* Unlearning reduces risk
* Ethical AI is achievable

---

## 👨‍💻 Authors

1. Adnan Bakth Mazmader
2. Md. Abul Bashar Nirob

---

## 🎓 Supervisor

Dr. Mohammad Ashrafuzzaman Khan

---
 
