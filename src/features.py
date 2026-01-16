import pandas as pd
import numpy as np

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['ema_5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['ema_15'] = df['close'].ewm(span=15, adjust=False).mean()
    
    df['returns'] = df['close'].pct_change()
    
    if 'close_fut' in df.columns:
        df['futures_basis'] = df['close_fut'] - df['close']
        
    return df

def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # PCR OI: Put OI / Call OI
    # Assuming columns 'open_interest_pe', 'open_interest_ce' from merge
    if 'open_interest_pe' in df.columns and 'open_interest_ce' in df.columns:
        df['pcr_oi'] = df['open_interest_pe'] / df['open_interest_ce'].replace(0, np.nan)
        
    # PCR Vol: Assuming 'volume_pe', 'volume_ce' (if available, else skip)
    
    # IV Spread: call_iv - put_iv
    if 'call_iv' in df.columns and 'put_iv' in df.columns:
        df['iv_spread'] = df['call_iv'] - df['put_iv']
        df['avg_iv'] = (df['call_iv'] + df['put_iv']) / 2
        
    return df
