from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump

# ensure output directory exists
Path("models").mkdir(parents=True, exist_ok=True)

# load joined pollinator+env table
df = pd.read_csv("data/processed/pollinators_with_env.csv")

# features & target
X = df[["temp", "precip", "nitrogen"]]
y = df["species"]

# split, train, evaluate
Xtr, Xte, ytr, yte = train_test_split(
    X, y, train_size=0.7, stratify=y, random_state=42
)
rf = RandomForestClassifier(n_estimators=400, class_weight="balanced")
rf.fit(Xtr, ytr)
print("Test accuracy:", rf.score(Xte, yte))

# save the model
dump(rf, "models/pollinator_sdm.joblib")
print("Model saved to models/pollinator_sdm.joblib")