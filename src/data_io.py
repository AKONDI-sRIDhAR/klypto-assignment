import os
import pandas as pd

# Determine project root dynamically (folder containing data/)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_csv(relative_path: str) -> pd.DataFrame:
    """
    Load CSV using a path relative to project root.
    Example: load_csv('data/raw/nifty_spot_5min.csv')
    """
    full_path = os.path.join(PROJECT_ROOT, relative_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Missing file: {full_path}")

    df = pd.read_csv(full_path)
    print(f"Loaded {len(df)} rows from {full_path}")
    return df


def save_csv(df: pd.DataFrame, relative_path: str):
    """
    Save CSV using a path relative to project root.
    """
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    df.to_csv(full_path, index=False)
    print(f"Saved file: {full_path}")
