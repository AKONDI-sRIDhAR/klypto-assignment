import pandas as pd
import numpy as np

def safe_rename(df, mapping):
    cols = set(df.columns)
    effective_mapping = {}
    for src, dst in mapping.items():
        if src in cols:
            if dst in cols and src != dst:
                effective_mapping[src] = dst
            else:
                effective_mapping[src] = dst
    
    df = df.rename(columns=effective_mapping)
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def clean_spot_data(df: pd.DataFrame) -> pd.DataFrame:
    print("  > Cleaning Spot Data...")
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]
    
    mapping = {
        'ltp': 'close',
        'vol': 'volume',
        'contracts': 'volume', 
        'shares traded': 'volume',
        'datetime': 'timestamp',
        'date': 'timestamp',
        'time': 'timestamp_time'
    }
    df = safe_rename(df, mapping)
    
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    if 'volume' not in df.columns:
        t_cols = [c for c in df.columns if 'turnover' in c]
        if t_cols:
            df['volume'] = df[t_cols[0]]
        else:
            df['volume'] = 0
            
    req = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    for c in req:
        if c not in df.columns:
            df[c] = 0
            
    df = df[req].sort_values('timestamp').ffill()
    
    numeric = ['open','high','low','close']
    for col in numeric:
        mu = df[col].mean()
        std = df[col].std()
        df[col] = df[col].clip(mu - 3*std, mu + 3*std)
        
    return df

def clean_futures_data(df: pd.DataFrame) -> pd.DataFrame:
    print("  > Cleaning Futures Data...")
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Filter for NIFTY symbol matches
    # Symbols could be 'NIFTY', 'NIFTY 50', 'NIFTY50', etc.
    # We check if 'symbol' col exists
    if 'symbol' in df.columns:
        # Normalize symbol
        df['symbol'] = df['symbol'].str.upper().str.strip()
        # Filter for NIFTY
        # If dataset only has NIFTY files, this is no-op. If mixed, this is CRITICAL.
        target_symbols = ['NIFTY', 'NIFTY 50']
        df = df[df['symbol'].isin(target_symbols)]
        if len(df) == 0:
            print("WARNING: No NIFTY futures found after filtering. Checking available symbols...")
            # If we filtered everything, maybe the symbol is named differently?
            # Revert to all? Or empty?
            # For now, if empty, we might return empty or try relaxation.
            pass
            
    mapping = {
        'expiry_dt': 'expiry', 
        'open interest': 'open_interest', 
        'oi': 'open_interest', 
        'datetime': 'timestamp',
        'open_int': 'open_interest',
        'val_inlakh': 'turnover' 
    }
    df = safe_rename(df, mapping)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    if 'expiry_dt_final' in df.columns:
        df['expiry'] = pd.to_datetime(df['expiry_dt_final'])
    else:
        df['expiry'] = pd.to_datetime(df['expiry'])
        
    df = df.sort_values(['timestamp', 'expiry'])
    
    # Rollover logic
    df = df[df['expiry'] >= df['timestamp']]
    
    df = df.drop_duplicates(subset=['timestamp'], keep='first')
    
    return df

def clean_options_data(df: pd.DataFrame) -> pd.DataFrame:
    print("  > Cleaning Options Data...")
    df = df.copy()
    df.columns = [c.lower().strip() for c in df.columns]
    
    # Filter NIFTY
    if 'symbol' in df.columns:
        df['symbol'] = df['symbol'].str.upper().str.strip()
        df = df[df['symbol'].isin(['NIFTY', 'NIFTY 50'])]
    
    mapping = {
        'expiry_dt': 'expiry', 
        'strike_pr': 'strike', 
        'option_typ': 'option_type', 
        'open interest': 'open_interest',
        'oi': 'open_interest', 
        'datetime': 'timestamp',
        'open_int': 'open_interest',
        'expiry_dt_final': 'expiry'
    }
    df = safe_rename(df, mapping)
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['expiry'] = pd.to_datetime(df['expiry'])
    
    return df.sort_values('timestamp').ffill()
