import os
import shutil
import pandas as pd

# Define authoritative paths relative to this file (src/data_utils.py)
# src is one level deep. Project root is one level up.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

def get_processed_path(filename: str) -> str:
    """Returns the absolute path for a file in data/processed."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    return os.path.join(PROCESSED_DIR, filename)

def get_raw_path(filename: str) -> str:
    """Returns the absolute path for a file in data/raw."""
    os.makedirs(RAW_DIR, exist_ok=True)
    return os.path.join(RAW_DIR, filename)

def ensure_raw_data_standardized():
    """
    Moves raw files from project root to data/raw.
    """
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Standard mappings
    mapping = {
        "nifty50.csv": "nifty_spot_5min.csv",
        "niftyfuture.csv": "nifty_futures_raw.csv",
        "niftyoptions.csv": "nifty_options_raw.csv",
    }

    # Move from Root -> Raw
    for src, dst in mapping.items():
        src_path = os.path.join(PROJECT_ROOT, src)
        dst_path = os.path.join(RAW_DIR, dst)
        if os.path.exists(src_path) and not os.path.exists(dst_path):
            os.rename(src_path, dst_path)

    # Cleanup: If any 'clean' or 'processed' files ended up in root by mistake, move them.
    for filename in os.listdir(PROJECT_ROOT):
        if filename.endswith(".csv"):
            if "clean" in filename or "merged" in filename or "features" in filename or "regime" in filename:
                src = os.path.join(PROJECT_ROOT, filename)
                dst = os.path.join(PROCESSED_DIR, filename)
                if not os.path.exists(dst):
                    os.rename(src, dst)
                    print(f"Moved stray processed file {filename} to data/processed/")
            elif "raw" in filename:
                src = os.path.join(PROJECT_ROOT, filename)
                dst = os.path.join(RAW_DIR, filename)
                if not os.path.exists(dst):
                    os.rename(src, dst)

def load_data(path: str) -> pd.DataFrame:
    """
    Robust loader. If path is just a filename, attempts to find it in processed, then raw.
    Otherwise handles absolute/relative path.
    """
    if not os.path.exists(path):
        # Fallback logic: check processed dir then raw dir
        p_path = os.path.join(PROCESSED_DIR, os.path.basename(path))
        r_path = os.path.join(RAW_DIR, os.path.basename(path))
        if os.path.exists(p_path):
            path = p_path
        elif os.path.exists(r_path):
            path = r_path
        else:
            raise FileNotFoundError(f"Could not find {path} in local path, data/processed, or data/raw")
            
    return pd.read_csv(path)

def save_data(df: pd.DataFrame, path: str):
    """
    Saves data. If path is a filename, defaults to PROCESSED_DIR.
    """
    # If it's just a filename (no separators), assume processed dir
    if os.sep not in path and "/" not in path:
        path = os.path.join(PROCESSED_DIR, path)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
