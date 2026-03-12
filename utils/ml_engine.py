import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib
import os

os.makedirs("models", exist_ok=True)
MODEL_PATH = "models/rf_model.pkl"

def train_and_evaluate(X, y):
    if len(y.unique()) < 2:
        return False, "Gagal: Dataset hanya menghasilkan 1 kelas label. Ubah threshold pelabelan atau perbaiki data."

    try:
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)       
        y_pred = rf.predict(X)
        
        akurasi = accuracy_score(y, y_pred)
        cm = confusion_matrix(y, y_pred) 
        
        importances = rf.feature_importances_
        fi_df = pd.DataFrame({'Fitur': X.columns, 'Kepentingan': importances})
        fi_df = fi_df.sort_values(by='Kepentingan', ascending=False).reset_index(drop=True)

        joblib.dump(rf, MODEL_PATH)
        metrik = {
            "akurasi": akurasi,
            "confusion_matrix": cm,
            "feature_importance": fi_df
        }
        
        return True, metrik

    except Exception as e:
        return False, f"Terjadi kesalahan fatal saat training: {str(e)}"

def load_model():
    if not os.path.exists(MODEL_PATH):
         return None, "Model belum tersedia. Admin harus melakukan training terlebih dahulu."
    try:
         model = joblib.load(MODEL_PATH)
         return model, "OK"
    except Exception as e:
         return None, f"Gagal memuat model: {str(e)}"