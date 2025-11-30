# Pustu Chatbot - Anamnesis NLP (From Scratch)

This repository contains a small NLP-from-scratch project to build a naive-anamnesis chatbot for Puskesmas (Pustu). It follows the development guide `panduan_pustu_chatbot.md`.

## Quick Start

1. Create and activate a Python virtual environment (recommended).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Generate dataset and visuals:

```powershell
python generate_data.py
```

4. Train or use the chatbot via `pustu_chatbot.py` (examples exist in the notebook and demo scripts).

## Files

- `pustu_chatbot.py`: core module implementing data generation, NER, Naive Bayes classifier, Dialog Manager, and chat wrapper.
- `generate_data.py`: script to generate synthetic dataset and save train/test splits and intent distribution plot.
- `data/dictionaries/`: contains dictionaries for symptoms, severity, locations, and stopwords.
- `data/processed/`: generated full_dataset.json, train_data.json, and test_data.json.
- `outputs/figures/`: generated visualizations like `intent_distribution.png`.
- `outputs/models/`: folder where models like `naive_bayes_model.pkl` will be saved.

## Notes
- This implementation avoids using ML libraries like `sklearn`, `spacy`, `nltk`, `tensorflow`, `torch`, and `transformers` per the project guide.
- `pustu_chatbot.py` is organized to be imported by other scripts (e.g., demo, notebook) or executed directly.

## Next steps
- Create notebook `pustu_chatbot_complete.ipynb` and copy the guided cells.
- Implement training and evaluation scripts.
- Add unit tests for NER and Naive Bayes components.
