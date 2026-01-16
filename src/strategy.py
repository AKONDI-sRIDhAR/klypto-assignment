import pandas as pd
import numpy as np

def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    
    # Logic:
    # Long: EMA5 > EMA15 AND Regime == 1
    # Short: EMA5 < EMA15 AND Regime == -1
    
    df['signal'] = 0
    
    long_cond = (df['ema_5'] > df['ema_15']) & (df['regime'] == 1)
    short_cond = (df['ema_5'] < df['ema_15']) & (df['regime'] == -1)
    
    df.loc[long_cond, 'signal'] = 1
    df.loc[short_cond, 'signal'] = -1
    
    # Enter next candle
    df['position'] = df['signal'].shift(1).fillna(0)
    
    return df

def calculate_metrics(df: pd.DataFrame) -> dict:
    # Strategy Return
    df['strategy_return'] = df['position'] * df['returns']
    returns = df['strategy_return'].dropna()
    
    if len(returns) == 0: return {}
    
    ann_factor = 252 * 75
    
    sharpe = np.sqrt(ann_factor) * returns.mean() / returns.std()
    
    wins = len(returns[returns > 0])
    total = len(returns[returns != 0])
    win_rate = wins/total if total > 0 else 0
    
    cum_ret = (1 + returns).cumprod()
    dd = (cum_ret - cum_ret.cummax()) / cum_ret.cummax()
    mdd = dd.min()
    
    total_ret = cum_ret.iloc[-1] - 1
    
    calmar = total_ret / abs(mdd) if mdd != 0 else 0
    
    return {
        'Sharpe': round(sharpe, 2),
        'Win Rate': round(win_rate, 2),
        'Max Drawdown': round(mdd, 2),
        'Calmar': round(calmar, 2),
        'Total Return': round(total_ret, 2)
    }
