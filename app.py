import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# 1. Memuat otak AI
vectorizer = joblib.load('kamus_kata.pkl')
model_ai = joblib.load('model_ai.pkl')

# 2. Menyiapkan brankas penyimpanan (File CSV)
file_database = 'database_pengunjung.csv'
if not os.path.exists(file_database):
    # Membuat file kosong jika belum ada
    df_kosong = pd.DataFrame(columns=['Waktu', 'Nama', 'Ulasan', 'Sentimen'])
    df_kosong.to_csv(file_database, index=False)

# 3. Tampilan Website
st.set_page_config(page_title="Ulasan EV", page_icon="⚡")
st.title("⚡ Sentimen Mobil Listrik")
st.write("Coba ketik ulasan Anda. Datanya akan langsung terekam di tabel bawah!")

# Kotak Input
nama_user = st.text_input("Nama Anda:")
ulasan_user = st.text_area("Masukkan Ulasan:")

if st.button("Kirim Ulasan"):
    if nama_user.strip() == "" or ulasan_user.strip() == "":
        st.warning("Nama dan Ulasan tidak boleh kosong!")
    else:
        # AI Memproses
        teks_angka = vectorizer.transform([ulasan_user])
        hasil = model_ai.predict(teks_angka)
        label_sentimen = "Positif 🟢" if hasil[0] == 1 else "Negatif 🔴"
        
        st.success(f"**HASIL DETEKSI:** Ulasan ini bernada **{label_sentimen}**")
        
        # Menyimpan langsung ke file
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_baru = pd.DataFrame([[waktu_sekarang, nama_user, ulasan_user, label_sentimen]])
        data_baru.to_csv(file_database, mode='a', header=False, index=False)
        st.info("✅ Data berhasil masuk ke brankas!")

st.markdown("---")
st.subheader("📁 Tabel Data Pengunjung")

# 4. Menampilkan Tabel dan Tombol Download
if os.path.exists(file_database):
    df_tampil = pd.read_csv(file_database)
    st.dataframe(df_tampil, use_container_width=True) # Menampilkan tabel di web
    
    # Tombol ajaib untuk download ke Excel
    with open(file_database, "rb") as file:
        st.download_button(
            label="📥 Download Data ke Excel (CSV)",
            data=file,
            file_name="Data_Website_Mobil_Listrik.csv",
            mime="text/csv"
        )
