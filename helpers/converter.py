import pandas as pd
import io

def to_dataframe(file, ext):
    df = None
    if ext == 'xlsx':
        df = pd.read_excel(io.BytesIO(file), engine="openpyxl")
    elif ext == 'csv':
        df = pd.read_csv(io.BytesIO(file))
    
    return df