import logging
import os
import sys
import pandas as pd

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV data from a given file path.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(file_path)


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """
    Save DataFrame to CSV.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)

def setup_logger(name=__name__, log_file=None, level=logging.INFO):
    """Function to setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Console handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

def get_project_root():
    """Returns the root directory of the project."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
