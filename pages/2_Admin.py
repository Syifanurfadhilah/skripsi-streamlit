import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_handler import load_and_preprocess_data
from utils.ml_engine import train_and_evaluate
from utils.ui_components import apply_custom_css, render_navbar

st.set_page_config(page_title="Admin Panel", layout="wide", initial_sidebar_state="collapsed")

apply_custom_css()
render_navbar()

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["admin_password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Masukkan Password Admin", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Masukkan Password Admin", type="password", on_change=password_entered, key="password")
        st.error("Password salah.")
        return False
    return True

if not check_password():
    st.stop()

st.title("Admin Panel - Pelatihan Model")

st.markdown("### 1. Ekspor Data Responden")
st.info("Unduh data mentah hasil pengisian kuesioner.")

file_hasil = "hasil_responden.csv"
if os.path.exists(file_hasil):
    try:
        df_hasil = pd.read_csv(file_hasil, sep=';')
        st.success(f"Terdapat **{len(df_hasil)}** observasi baru yang berhasil direkam.")
        
        with open(file_hasil, "rb") as f:
            st.download_button(
                label="Unduh CSV Hasil Responden",
                data=f,
                file_name="hasil_responden_live.csv",
                mime="text/csv",
                type="primary"
            )
            
        with st.expander("Inspeksi Tabel Data Responden"):
            st.dataframe(df_hasil, width="stretch")
            
    except Exception as e:
        st.error(f"Gagal membaca file data responden: {e}")
else:
    st.warning("Belum ada entri data kuesioner dari responden saat ini.")

st.markdown("---")

st.markdown("### 2. Upload Dataset")
st.info("Upload file CSV.")

uploaded_file = st.file_uploader("Pilih file CSV", type=["csv"])

if uploaded_file is not None:
    X, y, df_raw = load_and_preprocess_data(uploaded_file)
    
    if X is None:
        st.error(f"Gagal memproses data: {df_raw}") 
        st.stop()
        
    st.success("Format data valid.")
    
    with st.expander("Inspeksi Data Input (X)"):
        st.dataframe(X.head())
        
    st.markdown("### 3. Eksekusi Training Model")
    st.warning("Menekan tombol ini akan menimpa model `rf_model.pkl` yang lama. Halaman User akan langsung menggunakan model baru ini.")
    
    if st.button("Latih Model Sekarang!", type="primary"):
        with st.spinner("Mengkalibrasi Random Forest..."):
            sukses, hasil = train_and_evaluate(X, y)
            
        if sukses:
            st.session_state['training_results'] = hasil
            st.session_state['df_raw'] = df_raw
            st.success("Model berhasil diperbarui.")
        else:
            st.error(hasil)

if 'training_results' in st.session_state:
    st.markdown("---")
    st.markdown("### 3. Hasil Evaluasi Model")
    
    hasil = st.session_state['training_results']
    df_raw = st.session_state['df_raw']
    
    st.markdown("### 1. Evaluasi Performa Model")
    st.caption("Ringkasan metrik evaluasi algoritma Random Forest berdasarkan dataset uji.")
    
    # --- Tingkat Akurasi ---
    acc_percent = hasil['akurasi'] * 100
    st.metric("Tingkat Akurasi (Accuracy Score)", f"{acc_percent:.2f}%")
    st.success(f"**Interpretasi:** Model berhasil memprediksi label kelas (Impulsif / Tidak Impulsif) dengan tingkat akurasi sebesar {acc_percent:.2f}%. Nilai ini menunjukkan kapabilitas model dalam mereplikasi pola keputusan dari dataset historis.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Feature Importance ---
    st.markdown("#### Feature Importance")
    st.caption("Persentase kontribusi setiap variabel uji terhadap hasil prediksi akhir.")
    
    df_fi = hasil['feature_importance']
    top_feature = df_fi.iloc[0]['Fitur'].replace('X_', '')
    top_score = df_fi.iloc[0]['Kepentingan'] * 100
    
    st.dataframe(df_fi.style.format({'Kepentingan': '{:.2%}'}), width="stretch")
    st.info(f"**Analisis Variabel:** Indikator **{top_feature}** menempati bobot tertinggi ({top_score:.2f}%), menandakan variabel ini memiliki korelasi terkuat dalam memicu perilaku pembelian impulsif responden.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Confusion Matrix ---
    st.markdown("#### Confusion Matrix")
    st.caption("Tabel distribusi frekuensi prediksi model vs data historis (aktual).")
    cm = hasil['confusion_matrix']
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greys', ax=ax, cbar=False,
                xticklabels=['Tidak Impulsif', 'Impulsif'], 
                yticklabels=['Tidak Impulsif', 'Impulsif'])
    ax.set_xlabel('Prediksi Model (Predicted Label)')
    ax.set_ylabel('Data Aktual (True Label)')
    st.pyplot(fig)
    
    benar_tidak_impulsif = cm[0][0]
    benar_impulsif = cm[1][1] if len(cm) > 1 else 0
    total_benar = benar_tidak_impulsif + benar_impulsif
    
    st.markdown(f"**Ringkasan Prediksi:** Dari keseluruhan sampel, sistem mengklasifikasikan **{total_benar} observasi** secara presisi sesuai dengan pelabelan aktual.")

    st.markdown("---")
        
    st.markdown("### 2. Analisis Distribusi Demografi")
    st.caption("Pemetaan proporsi perilaku impulsif dikelompokkan berdasarkan variabel jenis kelamin.")
    
    # Menghitung persentase agar bisa ditampilkan di dalam grafiknya
    df_group = df_raw.groupby(['Gender', 'Label_Impulsif']).size().reset_index(name='Jumlah')
    df_group['Gender'] = df_group['Gender'].map({0: 'Laki-laki (0)', 1: 'Perempuan (1)'})
    df_group['Klasifikasi'] = df_group['Label_Impulsif'].map({0: 'Rasional', 1: 'Impulsif'})
    
    # Hitung total per gender untuk mencari persentase
    total_per_gender = df_group.groupby('Gender')['Jumlah'].transform('sum')
    df_group['Persentase'] = (df_group['Jumlah'] / total_per_gender) * 100
    df_group['Persentase Teks'] = df_group['Persentase'].round(1).astype(str) + '%'

    # Buat grafik bar chart interaktif dengan Plotly Express
    fig2 = px.bar(
        df_group, 
        x='Gender', 
        y='Jumlah', 
        color='Klasifikasi',
        barmode='group',
        text='Persentase Teks', # Memunculkan teks persentase
        color_discrete_map={'Rasional': '#94a3b8', 'Impulsif': '#005b96'},
        hover_data={'Persentase': ':.1f%', 'Gender': False} # Memunculkan info saat hover
    )
    
    fig2.update_traces(textposition='inside', textfont_size=14)
    fig2.update_layout(
        xaxis_title="Kelompok Jenis Kelamin",
        yaxis_title="Frekuensi (Jumlah Sampel)",
        legend_title="Status Klasifikasi",
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    # Menampilkan grafik
    st.plotly_chart(fig2, width="stretch")
    
    # Menambahkan penjelasan hasil demografi
    st.info("**Interpretasi Demografi:** Berdasarkan visualisasi di atas, kita dapat memantau perbandingan sebaran frekuensi kelas impulsif antara kelompok responden. Distribusi ini membantu menganalisis apakah faktor jenis kelamin memberikan pengaruh yang signifikan terhadap perilaku belanja spontan pada kampanye Flash Sale.")