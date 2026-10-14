# Phishing URL Detection — ML Mini Project

A Random Forest classifier trained on labeled URLs, with a Streamlit demonstration interface.

## Dataset
Download a **labeled URL dataset** as `urls.csv` with these exact column names:
- `url`: complete URL string
- `label`: `1` for phishing, `0` for legitimate

Use a trusted public labeled URL dataset (e.g., a phishing URL dataset from Kaggle or a public research repository). Inspect its license, label meanings and provenance. Do not visit suspicious URLs to gather data. A dataset with both classes and at least several hundred distinct URLs is preferable. Do not use a dataset that contains only extracted numeric features; this project needs raw URL strings.

Example format (illustrative only, **not enough for training**):
```csv
url,label
https://www.wikipedia.org,0
http://example.com/verify-account,1
```

## Run (Windows)
```powershell
py -m pip install -r requirements.txt
py train.py
py -m streamlit run app.py
```

If `py` isn't available, replace it with `python`.

## What to explain
- URL feature engineering (length, symbols, digits, IP address, subdomains, suspicious words)
- Train/test split (80/20, stratified)
- Random Forest classification
- Accuracy, precision, recall and F1 from the held-out test set
- Limitations: HTTPS alone doesn't mean safe; URL-only analysis can miss malicious sites and produce false positives; random URL-level splits can overestimate generalization if related domains appear in both sets.

**Security:** Never enter credentials into a site solely because this demo predicts 'legitimate'. Load `joblib` model files only if created by you or from trusted sources.
