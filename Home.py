import streamlit as st
import pandas as pd
import sys
import os
import csv
from datetime import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils.ml_engine import load_model
from utils.ui_components import apply_custom_css, render_navbar

st.set_page_config(page_title="Prediksi Impulsif", layout="wide", initial_sidebar_state="collapsed")

apply_custom_css()
render_navbar()

# Hero Banner
st.markdown("""
    <div style="
        width: 100%;
        height: 280px;
        overflow: hidden;
        border-radius: 16px;
        margin-bottom: 2rem;
    ">
        <img src="app/static/hero_image.png" style="
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center top;
        ">
    </div>
""", unsafe_allow_html=True)

st.title("Kuesioner Prediksi Perilaku Pembelian Impulsif")
st.markdown("Silakan isi kuesioner di bawah ini dengan memilih tingkat persetujuan Anda.")

model, msg = load_model()
if model is None:
    st.warning(msg)
    st.stop()

with st.form("form_kuesioner"):
    st.subheader("Data Demografi")
    usia = st.number_input("Usia", min_value=12, max_value=29, value=20, step=1, help="Pilih usia Anda (12-29 tahun)")
    gender = st.radio("Jenis Kelamin", options=["Laki-laki", "Perempuan"], horizontal=True)
    val_gender = 0 if gender == "Laki-laki" else 1
    
    st.markdown("---")
    
    def create_choice(label):
        options = [
            "Sangat Tidak Setuju",
            "Tidak Setuju",
            "Netral",
            "Setuju",
            "Sangat Setuju"
        ]
        
        mapping = {
            "Sangat Tidak Setuju": 1,
            "Tidak Setuju": 2,
            "Netral": 3,
            "Setuju": 4,
            "Sangat Setuju": 5
        }
        
        st.markdown(f"<div style='font-weight: 500; font-size: 1.1rem; color: var(--text-color); margin-bottom: 10px;'>{label}</div>", unsafe_allow_html=True)
        # horizontal=True lets it use the full width flexibly
        val = st.radio("Pilihan", options=options, index=2, horizontal=True, label_visibility="collapsed", key=label)
        st.markdown("<br>", unsafe_allow_html=True)
        return mapping[val]
        
    st.subheader("1. Diskon")
    d1 = create_choice("Saya tertarik melihat produk Flash Sale karena potongan harganya yang besar")
    d2 = create_choice("Harga produk pada Flash Sale terasa jauh lebih murah dibandingkan harga normal")
    d3 = create_choice("Saya merasa rugi jika melewatkan Flash Sale karena diskonnya sangat menguntungkan")
    
    st.subheader("2. Durasi Waktu")
    w1 = create_choice("Waktu Flash Sale yang singkat membuat saya harus cepat mengambil keputusan")
    w2 = create_choice("Adanya hitungan waktu mundur mendorong saya segera melakukan transaksi")
    w3 = create_choice("Saya terburu-buru saat membeli produk Flash Sale karena takut promo berakhir")
    
    st.subheader("3. Visual/Notifikasi")
    v1 = create_choice("Notifikasi Flash Sale dari Shopee membuat saya langsung membuka aplikasi")
    v2 = create_choice("Tampilan label Flash Sale menarik perhatian saya saat sedang scrolling produk")
    v3 = create_choice("Saya lebih tertarik membeli produk bertanda Flash Sale dibanding produk biasa")

    st.subheader("4. Stok Terbatas")
    s1 = create_choice("Saya khawatir kehabisan produk jika tidak segera membeli saat Flash Sale")
    s2 = create_choice("Informasi 'stok terbatas' membuat saya ingin segera melakukan pembayaran")
    s3 = create_choice("Saya cenderung membeli produk Flash Sale meski belum tentu butuh karena stok terbatas")

    submitted = st.form_submit_button("Analisis Perilaku", type="primary")

if submitted:
    x_diskon = (d1 + d2 + d3) / 3.0
    x_durasi = (w1 + w2 + w3) / 3.0
    x_visual = (v1 + v2 + v3) / 3.0
    x_stok = (s1 + s2 + s3) / 3.0
    
    input_data = pd.DataFrame([[usia, val_gender, x_diskon, x_durasi, x_visual, x_stok]], 
                              columns=['Usia', 'Gender', 'X_Diskon', 'X_Durasi', 'X_Visual', 'X_Stok'])
    
    with st.spinner("Memproses prediksi..."):
        prediksi = model.predict(input_data)[0]
        probabilitas = model.predict_proba(input_data)[0]
    
    st.markdown("---")
    st.subheader("Hasil Prediksi Model")
    
    prob_persen = round(max(probabilitas) * 100, 2)
    file_hasil = "hasil_responden.csv"
    file_exist = os.path.isfile(file_hasil)
    
    with open(file_hasil, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';') 
        if not file_exist:
            header = [
                "Timestamp", "Jenis Kelamin", "Tahun Lahir", "Usia",
                "Diskon_1", "Diskon_2", "Diskon_3",
                "Durasi_1", "Durasi_2", "Durasi_3",
                "Visual_1", "Visual_2", "Visual_3",
                "Stok_1", "Stok_2", "Stok_3",
                "Impulsif_1", "Impulsif_2", "Impulsif_3", "Impulsif_4", "Impulsif_5", "Impulsif_6",
                "Prediksi_Sistem", "Probabilitas_Persen"
            ]
            writer.writerow(header)
        
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
        tahun_lahir = now.year - int(usia)
        
        row_data = [
            timestamp_str,
            val_gender,
            tahun_lahir,
            usia,
            d1, d2, d3,
            w1, w2, w3,
            v1, v2, v3,
            s1, s2, s3,
            "", "", "", "", "", "",
            "Impulsif" if prediksi == 1 else "Tidak Impulsif", 
            f"{prob_persen}%"
        ]
        writer.writerow(row_data)
        
    if prediksi == 1:
        st.error(f"**Kecenderungan: IMPULSIF (Probabilitas: {prob_persen}%)**")
        st.markdown(f"**Analisis:** Sistem mendeteksi probabilitas sebesar **{prob_persen}%** bahwa responden memiliki kecenderungan pembelian impulsif. Skor kuesioner menunjukkan bahwa elemen kampanye Flash Sale memiliki pengaruh signifikan terhadap keputusan transaksi.")
    else:
        st.success(f"**Kecenderungan: RASIONAL / TIDAK IMPULSIF (Probabilitas: {prob_persen}%)**")
        st.markdown(f"**Analisis:** Sistem memprediksi dengan probabilitas **{prob_persen}%** bahwa responden tergolong pembeli yang rasional (tidak impulsif). Keputusan belanja cenderung didasarkan pada kebutuhan objektif dan tidak mudah dipengaruhi oleh taktik urgensi Flash Sale.")
