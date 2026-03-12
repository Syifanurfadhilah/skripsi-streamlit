import pandas as pd
import numpy as np

def load_and_preprocess_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, skiprows=1, header=None, sep=None, engine='python')
        
        if df.shape[1] > 21:
            df = df.iloc[:, :21]
        
        if df.shape[1] != 21:
            raise ValueError(f"Format CSV salah! Diharapkan 21 kolom, tapi mendapat {df.shape[1]} kolom.")

        columns = [
            "Gender", "Tahun_Lahir", "Usia",
            "Diskon_1", "Diskon_2", "Diskon_3",
            "Durasi_1", "Durasi_2", "Durasi_3",
            "Visual_1", "Visual_2", "Visual_3",
            "Stok_1", "Stok_2", "Stok_3",
            "Impulsif_1", "Impulsif_2", "Impulsif_3", "Impulsif_4", "Impulsif_5", "Impulsif_6"
        ]
        df.columns = columns
        
        df['X_Diskon'] = df[['Diskon_1', 'Diskon_2', 'Diskon_3']].mean(axis=1)
        df['X_Durasi'] = df[['Durasi_1', 'Durasi_2', 'Durasi_3']].mean(axis=1)
        df['X_Visual'] = df[['Visual_1', 'Visual_2', 'Visual_3']].mean(axis=1)
        df['X_Stok'] = df[['Stok_1', 'Stok_2', 'Stok_3']].mean(axis=1)
        
        df['Y_Score_Total'] = df[['Impulsif_1', 'Impulsif_2', 'Impulsif_3', 
                                 'Impulsif_4', 'Impulsif_5', 'Impulsif_6']].sum(axis=1)
        
        df['Label_Impulsif'] = np.where(df['Y_Score_Total'] >= 18, 1, 0)
        
        fitur_final = ['Usia', 'Gender', 'X_Diskon', 'X_Durasi', 'X_Visual', 'X_Stok']
        X = df[fitur_final]
        y = df['Label_Impulsif']
        
        return X, y, df
        
    except Exception as e:
        return None, None, str(e)