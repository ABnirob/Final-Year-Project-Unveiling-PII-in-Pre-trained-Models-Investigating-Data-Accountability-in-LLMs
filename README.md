🔐 Unveiling PII in Pre-trained Models
🧠 Investigating Data Accountability in Large Language Models (LLMs)
<p align="center"> <img src="https://img.shields.io/badge/AI-Privacy%20Research-blueviolet?style=for-the-badge"/> <img src="https://img.shields.io/badge/Focus-LLM%20Security-critical?style=for-the-badge"/> <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge"/> <img src="https://img.shields.io/badge/Made%20With-PyTorch-red?style=for-the-badge"/> </p> <p align="center"> <b>⚠️ Detecting Privacy Leakage in LLMs | 🔍 Novel TPFS Method | 🧹 Machine Unlearning</b> </p>
🚀 Project Highlights

✨ First-of-its-kind undergraduate research exploring PII memorization in LLMs
🧠 Introduces TPFS (Token Probability & Frequency Scoring)
📊 Benchmarks across multiple state-of-the-art models
🔐 Demonstrates practical machine unlearning for privacy protection

🎬 Project Visualization
<p align="center"> <img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake.svg" alt="animation"/> </p>

🔁 Replace this with your own GIF later (e.g., TPFS workflow or ROC curve animation)

📌 Problem Statement

Large Language Models are trained on massive internet data.

👉 But what if they memorize sensitive personal information (PII)?

This project answers:

❓ Do LLMs leak private data?
❓ Can we detect memorized PII?
❓ Can we make models forget it?
🧠 Core Idea
⚡ We combine:
Model token probability
Real-world token frequency

➡️ To detect abnormal confidence = possible memorization

🏗️ System Architecture
🧪 Methodology
📊 Dataset Design
Type	Source	Purpose
Seen	OpenWebText (NER via SpaCy)	Known to model
Unseen	Faker-generated names	Unknown data
Reference	WikiMIA dataset	Frequency baseline
⚙️ Detection Methods
Method	Description
Min-K%	Uses lowest probability tokens
Min-K%++	Normalized variant
TPFS (Proposed)	Combines probability + frequency
💡 TPFS — The Innovation
TPFS(x)=
n
1
	​

i=1
∑
n
	​

log
P(x
i
	​

∣D
′
)
P(x
i
	​

∣M)
	​


✔ Penalizes common tokens
✔ Highlights memorized rare tokens
✔ More robust than existing methods

📈 Results
🔍 Key Insights
🥇 Min-K% performs best at low K (20%)
📉 Performance drops as K increases
⚖️ TPFS remains stable and unbiased
🧠 Better handling of real-world language patterns
📊 Performance Snapshot
Model	TPFS	Min-K% (20%)
GPT-Neo 2.7B	0.5942	0.6796
OPT 2.7B	0.6050	0.5998
GPT-2 Medium	0.5132	0.5929
🧹 Machine Unlearning
⚙️ Approach
Replace sensitive data with placeholders
Fine-tune model using negative sampling
📉 Impact
Stage	AUC
Before	0.5790
After	0.5077

✅ Reduced memorization
✅ Improved privacy safety

🛠️ Tech Stack
<p align="center"> <img src="https://skillicons.dev/icons?i=python,pytorch" /> </p>
🤗 Transformers
🔥 PyTorch
🧠 SpaCy (NER)
🎭 Faker
📊 Matplotlib
📦 Hugging Face Datasets
📂 Project Structure
📁 project-root
├── data/
├── models/
├── experiments/
├── tpfs/
├── unlearning/
├── results/
└── README.md
🌍 Impact
🧑‍🤝‍🧑 Societal
Prevents privacy leakage
Builds trust in AI systems
⚖️ Legal
Supports GDPR compliance
Encourages AI auditing
🌱 Ethical AI
Promotes responsible AI development
⚠️ Limitations
Small reference corpus affects TPFS
Limited large-scale model testing
Unlearning tested on smaller models
🔮 Future Work
🚀 Scale to GPT-4 level models
📊 Improve TPFS with larger corpus
🔍 Extend to financial/medical PII
⚙️ Build automated privacy filters
👨‍💻 Authors

Md. Abul Bashar Nirob
Adnan Bakth Mazmader

🎓 North South University, Bangladesh

🎓 Supervisor

Dr. Mohammad Ashrafuzzaman Khan
Associate Professor, ECE Department

⭐ Support This Work

If you find this project valuable:

🌟 Star the repo
🍴 Fork it
📢 Share it

🧠 Final Thought

“Powerful AI demands powerful responsibility.”

This project is a step toward privacy-aware, accountable AI systems.
