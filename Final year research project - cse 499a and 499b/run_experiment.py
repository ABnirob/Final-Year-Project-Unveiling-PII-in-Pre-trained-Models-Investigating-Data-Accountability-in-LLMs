
import os
import torch
from datasets import load_dataset
from tqdm import tqdm
import spacy
from faker import Faker
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from transformers import AutoTokenizer, AutoModelForCausalLM

# Ensure spacy model is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

print("Packages loaded.")

# Load Model
print("Loading model...")
model_name = "EleutherAI/pythia-2.8b"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

# Device Setup - Safe fallback to CPU if GPU VRAM is low
if torch.cuda.is_available():
    vram = torch.cuda.get_device_properties(0).total_memory
    if vram > 7 * 1024**3: # Check for > 7GB VRAM for 2.8B model (approx)
        device = torch.device("cuda")
    else:
        print(f"GPU VRAM ({vram / 1024**3:.2f} GB) might be insufficient for Pythia-2.8B. Falling back to CPU.")
        device = torch.device("cpu")
else:
    device = torch.device("cpu")

print(f"Using device: {device}")
model.eval().to(device)

# Dataset
print("Loading dataset...")
try:
    # Use a smaller split if possible or stream, but notebook uses "train" split of "stas/openwebtext-10k" which is 10k samples.
    # It might be large.
    dataset = load_dataset("stas/openwebtext-10k", split="train")
except Exception as e:
    print(f"Error loading dataset: {e}")
    dataset = []

def extract_full_names(text):
    doc = nlp(text[:1000])  # Limit text to 1000 characters for faster processing
    full_names = []
    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) == 2:  # First and Last Name
            full_names.append(ent.text)
    return full_names

# Extract names from seen data
print("Extracting names from seen data...")
seen_full_names = []
# Limit to first 100 or so for speed if needed, but following notebook logic
for text in tqdm(dataset['text'], desc="Extracting Names from Seen Data"):
    seen_full_names.extend(extract_full_names(text))
seen_full_names = list(set(seen_full_names))
print(f"Extracted {len(seen_full_names)} unique seen full names.")
print("Sample Seen Names:", seen_full_names[:5])

# Generators
fake_br = Faker("pt_BR")
fake_cn = Faker("zh_CN")

def generate_synthetic_rare_names(num_samples, locale):
    if locale == "br":
        fake = fake_br
    elif locale == "cn":
        fake = fake_cn
    else:
        raise ValueError("Locale not supported.")
    
    names = []
    for _ in range(num_samples):
        first_name = fake.first_name()
        last_name = fake.last_name()
        names.append(f"{first_name} {last_name}")
    return names

# Generate Brazilian names
synthetic_brazilian_names = generate_synthetic_rare_names(1700, "br")
print(f"Generated {len(synthetic_brazilian_names)} synthetic Brazilian full names.")
print("Sample Brazilian Names:", synthetic_brazilian_names[:5])

synthetic_full_names = synthetic_brazilian_names
print(f"Generated {len(synthetic_full_names)} synthetic full names.")

# WikiMIA
from datasets import get_dataset_split_names
print("Checking WikiMIA splits...")
try:
    available_splits = get_dataset_split_names("wjfu99/WikiMIA-24")
    print("Available Splits:", available_splits)
    wiki_mia_splits = ["WikiMIA_length32", "WikiMIA_length64", "WikiMIA_length128", "WikiMIA_length256"]
    
    reference_names = []
    for split in wiki_mia_splits:
        if split in available_splits:
            wiki_dataset = load_dataset("wjfu99/WikiMIA-24", split=split)
            for text in tqdm(wiki_dataset['input'], desc=f"Extracting from {split}"):
                reference_names.extend(extract_full_names(text))
    
    reference_names = list(set(reference_names))
    print(f"Extracted {len(reference_names)} unique reference full names.")
    print("Sample Reference Names:", reference_names[:5])
except Exception as e:
    print(f"Error with WikiMIA: {e}")
    reference_names = []

# Limits
unseen_data_limited = synthetic_full_names[:500]
reference_limited = reference_names
seen_data_limited = seen_full_names[:500]

def get_token_probabilities(model, tokenizer, text):
    tokens = tokenizer(text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model(**tokens, labels=tokens["input_ids"])
        log_probs = torch.log_softmax(outputs.logits, dim=-1)
    # The notebook logic accesses [0, i, tid]
    token_probs = [log_probs[0, i, tid].item() for i, tid in enumerate(tokens["input_ids"][0])]
    return token_probs

def compute_token_frequency_distribution(reference_texts, tokenizer):
    token_counts = Counter()
    total_tokens = 0

    for text in tqdm(reference_texts, desc="Processing Reference Texts"):
        try:
            tokens = tokenizer(text, return_tensors="pt")["input_ids"].squeeze().tolist()
            if isinstance(tokens, int): tokens = [tokens]
            token_counts.update(tokens)
            total_tokens += len(tokens)
        except Exception:
            continue

    vocab_size = len(tokenizer)
    token_freqs = {token: (count + 1) / (total_tokens + vocab_size) for token, count in token_counts.items()}
    return token_freqs

def calculate_log_odds(token_probs, token_ids, token_freqs):
    log_odds_scores = []
    for prob, token_id in zip(token_probs, token_ids):
        # prob is log probability
        frequency = token_freqs.get(token_id, 1.0 / (len(token_freqs) + 1e-10)) # fallback
        log_odds = -prob * np.log(frequency)
        log_odds_scores.append(log_odds)
    return log_odds_scores

def aggregate_scores(log_odds_scores):
    return np.mean(log_odds_scores)

def evaluate_log_odds_method(model, tokenizer, texts, token_freqs):
    scores = []
    for text in tqdm(texts, desc="Calculating Log-Odds Scores"):
        try:
            tokens = tokenizer(text, return_tensors="pt").to(model.device)
            token_ids = tokens["input_ids"].squeeze().tolist()
            if isinstance(token_ids, int): token_ids = [token_ids]
            token_probs = get_token_probabilities(model, tokenizer, text)
            log_odds_scores = calculate_log_odds(token_probs, token_ids, token_freqs)
            score = aggregate_scores(log_odds_scores)
            scores.append(score)
        except Exception as e:
            print(f"Error evaluating text: {text[:20]}... {e}")
            scores.append(0)
    return scores

print("Computing token frequencies...")
if not reference_limited:
    print("Warning: No reference names found. Mocking reference for valid run.")
    reference_limited = ["John Doe", "Jane Smith"]
token_freqs = compute_token_frequency_distribution(reference_limited, tokenizer)

print("Evaluating TPFS...")
seen_scores_tpfs = evaluate_log_odds_method(model, tokenizer, seen_data_limited, token_freqs)
unseen_scores_tpfs = evaluate_log_odds_method(model, tokenizer, unseen_data_limited, token_freqs)

def calculate_min_k_prob(model, tokenizer, text, k_percent=20):
    tokens = tokenizer(text, return_tensors="pt").to(device)['input_ids'].squeeze()
    if tokens.dim() == 0:
        tokens = tokens.unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_ids=tokens.unsqueeze(0))
        log_probs = torch.log_softmax(outputs.logits, dim=-1)

    token_probs = [log_probs[0, i, tok.item()].item() for i, tok in enumerate(tokens)]
    k = max(1, int(len(token_probs) * k_percent / 100))
    return np.mean(sorted(token_probs)[:k])

def calculate_min_k_plus(model, tokenizer, text, k_percent=20):
    tokens = tokenizer(text, return_tensors="pt").to(device)['input_ids'].squeeze()
    if tokens.dim() == 0:
        tokens = tokens.unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_ids=tokens.unsqueeze(0))
        log_probs = torch.log_softmax(outputs.logits, dim=-1)

    token_probs = [log_probs[0, i, tok.item()].item() for i, tok in enumerate(tokens)]
    mean_prob = np.mean(token_probs)
    std_prob = np.std(token_probs)
    normalized_probs = [(p - mean_prob) / (std_prob + 1e-8) for p in token_probs]
    k = max(1, int(len(normalized_probs) * k_percent / 100))
    return np.mean(sorted(normalized_probs)[:k])

print("Evaluating Min-K%...")
seen_scores_mink = [calculate_min_k_prob(model, tokenizer, sample) for sample in tqdm(seen_data_limited, desc="MIN-K% Seen")]
unseen_scores_mink = [calculate_min_k_prob(model, tokenizer, sample) for sample in tqdm(unseen_data_limited, desc="MIN-K% Unseen")]

print("Evaluating Min-K++...")
seen_scores_mink_plus = [calculate_min_k_plus(model, tokenizer, sample) for sample in tqdm(seen_data_limited, desc="MIN-K++ Seen")]
unseen_scores_mink_plus = [calculate_min_k_plus(model, tokenizer, sample) for sample in tqdm(unseen_data_limited, desc="MIN-K++ Unseen")]

def manual_roc_auc(seen_scores, unseen_scores):
    scores = seen_scores + unseen_scores
    labels = [1] * len(seen_scores) + [0] * len(unseen_scores)
    combined = sorted(zip(scores, labels), key=lambda x: x[0], reverse=True)
    
    tp, fp = 0, 0
    fn = sum(labels)
    tn = len(labels) - fn
    
    tpr, fpr = [], []
    prev_score = None
    
    for score, label in combined:
        if prev_score is not None and score != prev_score:
            tpr.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
            fpr.append(fp / (fp + tn) if (fp + tn) > 0 else 0)
        
        if label == 1:
            tp += 1
            fn -= 1
        else:
            fp += 1
            tn -= 1
        prev_score = score
        
    tpr.append(tp / (tp + fn) if (tp + fn) > 0 else 0)
    fpr.append(fp / (fp + tn) if (fp + tn) > 0 else 0)
    
    auc = np.trapz(tpr, fpr)
    return auc, tpr, fpr

print("Calculating AUC...")
tpfs_auc, tpfs_tpr, tpfs_fpr = manual_roc_auc(seen_scores_tpfs, unseen_scores_tpfs)
mink_auc, mink_tpr, mink_fpr = manual_roc_auc(seen_scores_mink, unseen_scores_mink)
mink_plus_auc, mink_plus_tpr, mink_plus_fpr = manual_roc_auc(seen_scores_mink_plus, unseen_scores_mink_plus)

print(f"TPFS AUC: {tpfs_auc:.4f}")
print(f"Min-K% AUC: {mink_auc:.4f}")
print(f"Min-K++ AUC: {mink_plus_auc:.4f}")

# Plot
plt.figure(figsize=(10, 6))
plt.plot(tpfs_fpr, tpfs_tpr, label=f"TPFS (AUC: {tpfs_auc:.4f})")
plt.plot(mink_fpr, mink_tpr, label=f"Min-K% (AUC: {mink_auc:.4f})")
plt.plot(mink_plus_fpr, mink_plus_tpr, label=f"Min-K++ (AUC: {mink_plus_auc:.4f})")
plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")
plt.legend(loc="lower right")
plt.grid()
plt.savefig("roc_curve.png")
print("Plot saved to roc_curve.png")
