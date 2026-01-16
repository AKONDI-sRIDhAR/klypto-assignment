import pandas as pd
import numpy as np

def merge_spot_futures_options(spot: pd.DataFrame, futures: pd.DataFrame, options: pd.DataFrame) -> pd.DataFrame:
    """
    Merges Spot (5min) with Futures (nearest) and Options (ATM).
    """
    # 1. Base: Spot
    merged = spot.copy()
    
    # 2. Merge Futures
    # Align on timestamp. Futures should be 5-min aligned ideally.
    # If Futures is daily, we'd need date merge, but previous steps suggest 5-min or we aligned it.
    # Let's assume timestamp merge for strictness.
    merged = pd.merge(merged, futures[['timestamp', 'close', 'open_interest']], 
                      on='timestamp', how='left', suffixes=('', '_fut'))
    
    # 3. ATM Options Logic
    # Calculate Dynamic ATM Strike
    # We do this daily approx for robustness
    merged['date'] = merged['timestamp'].dt.date
    options['date'] = options['timestamp'].dt.date
    
    daily_spot = merged.groupby('date')['close'].mean().reset_index()
    daily_spot['atm'] = round(daily_spot['close'] / 50) * 50
    
    # Merge ATM target into options
    # Handling potential date column name issues
    if 'index' in daily_spot.columns: daily_spot.rename(columns={'index': 'date'}, inplace=True)
    
    # Options usually huge. Filter first.
    options_atm = pd.merge(options, daily_spot[['date', 'atm']], on='date')
    options_atm = options_atm[options_atm['strike'] == options_atm['atm']]
    
    # Separate CE/PE to avoid duplicates
    ce = options_atm[options_atm['option_type'] == 'CE'].groupby('date').first().reset_index()
    pe = options_atm[options_atm['option_type'] == 'PE'].groupby('date').first().reset_index()
    
    # Merge back to 5-min
    merged = pd.merge(merged, ce[['date', 'close', 'open_interest', 'expiry']], 
                      on='date', how='left', suffixes=('', '_ce'))
    merged = pd.merge(merged, pe[['date', 'close', 'open_interest']], 
                      on='date', how='left', suffixes=('', '_pe'))
    
    # Cleanup
    merged = merged.drop(columns=['date'])
    return merged.ffill()
