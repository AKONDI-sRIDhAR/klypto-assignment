import pandas as pd
from py_vollib.black_scholes.greeks.analytical import delta, gamma, theta, vega, rho

def add_greeks(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Defaults
    r = 0.06
    
    # Ensure inputs
    # We require: spot_close (usually close), strike, expiry
    # And we need IV. Since offline, we simulate/default if missing.
    
    if 'iv' not in df.columns:
        df['call_iv'] = 0.2
        df['put_iv'] = 0.2
    
    # Time to expiry
    if 'expiry' in df.columns:
        # Avoid div by zero
        df['time_to_expiry'] = (pd.to_datetime(df['expiry']) - pd.to_datetime(df['timestamp'])).dt.total_seconds() / (365*24*3600)
        df['time_to_expiry'] = df['time_to_expiry'].clip(lower=0.0001)
        
    # We use 'close' as spot price
    # We use 'strike' from merged ATM columns
    
    # Only calculate if we have ATM data
    if 'strike' not in df.columns:
        print("Warning: No strike column found. Skipping Greeks.")
        return df
        
    # Apply
    # Using simple iteration for clarity/robustness over vectorization in this specific requirements set
    # (py_vollib is scalar). Vectorize with apply.
    
    T = df['time_to_expiry']
    S = df['close']
    K = df['strike']
    
    df['call_delta'] = df.apply(lambda x: delta('c', x['close'], x['strike'], x['time_to_expiry'], r, x['call_iv']), axis=1)
    df['call_gamma'] = df.apply(lambda x: gamma('c', x['close'], x['strike'], x['time_to_expiry'], r, x['call_iv']), axis=1)
    df['call_theta'] = df.apply(lambda x: theta('c', x['close'], x['strike'], x['time_to_expiry'], r, x['call_iv']), axis=1)
    df['call_vega'] = df.apply(lambda x: vega('c', x['close'], x['strike'], x['time_to_expiry'], r, x['call_iv']), axis=1)
    
    df['put_delta'] = df.apply(lambda x: delta('p', x['close'], x['strike'], x['time_to_expiry'], r, x['put_iv']), axis=1)
    df['put_gamma'] = df.apply(lambda x: gamma('p', x['close'], x['strike'], x['time_to_expiry'], r, x['put_iv']), axis=1)
    
    return df
