import os

def check_environment():
    print("Checking environment...")
    
    # 1. Check Data
    raw_files = [
        "data/raw/nifty_spot_5min.csv",
        "data/raw/nifty_futures_raw.csv",
        "data/raw/nifty_options_raw.csv"
    ]
    
    missing = [f for f in raw_files if not os.path.exists(f)]
    
    if missing:
        print("ERROR: Missing raw files:")
        for m in missing: print(f" - {m}")
        print("\nPlease ensure Step 1 (Standardization) was run correctly or place files manually.")
        return
        
    print("Raw data found.")
    
    # 2. Check Dirs
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    print("\nEnvironment Ready.")
    print("Run notebooks 01 -> 08 in order.")

if __name__ == "__main__":
    check_environment()
