"""
AI Scoring Module

- Trains/uses ML model (e.g., LogisticRegression/sklearn)
- Inputs: enriched_leads.csv with columns: Urgency Score, AI Relevance, Conversion (binary)
- Outputs: model.pkl, and adjusted pitches
"""

import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression

def train_model(csv_path="enriched_leads.csv"):
    df = pd.read_csv(csv_path)
    if "Conversion" not in df.columns:
        print("No Conversion data available, skipping.")
        return
    X = df[["Urgency Score", "AI Relevance Score"]]
    y = df["Conversion"]
    model = LogisticRegression().fit(X, y)
    with open("ai_lead_model.pkl","wb") as f:
        pickle.dump(model,f)
    print("Model trained: ai_lead_model.pkl")

def predict(csv_path="enriched_leads.csv"):
    with open("ai_lead_model.pkl","rb") as f:
        model = pickle.load(f)
    df = pd.read_csv(csv_path)
    X = df[["Urgency Score", "AI Relevance Score"]]
    preds = model.predict_proba(X)[:,1]
    # Adjust Tier for high prob leads
    df['Optimized Tier'] = (preds > .7).astype(int) + 1
    df.to_csv("optimized_leads.csv", index=False)
    print("Lead priorities updated.")

if __name__ == "__main__":
    train_model()
