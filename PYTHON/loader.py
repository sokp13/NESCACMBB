import pandas as pd

def load_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Convert df to dictionary
    data = df.to_dict('records')
    return data

def load_data_no_dict(file_path):
    df = pd.read_csv(file_path)
    
    return df