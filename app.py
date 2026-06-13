import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
import pytz  # Alat baru untuk zona waktu

# 1. Memuat otak AI
vectorizer = joblib.load('kamus_kata.pkl')
model_ai = joblib.load('model_ai.pkl')

# 2. Menyiapkan brankas penyimpanan (File CSV)
file_database = 'database_pengunjung.csv'
if not os.path.exists(file_database):
    df_kosong = pd.DataFrame(columns=['Waktu (WITA)', 'Nama', 'Ulasan', 'Sentimen'])
    df_kosong.to_csv(file_database, index=False)

# 3. Tampilan Website (Untuk Publik)
st.set_page_config(page_title="Ulasan EV", page_icon="⚡")
st.title("⚡ Sentimen Mobil Listrik")

st.markdown("""
**Selamat datang!** Website ini menggunakan AI untuk menganalisis opini publik tentang kendaraan listrik di Indonesia. 
Ketikkan nama dan pendapat Anda untuk membantu kami mengklasifikasikan sentimennya!
""")
st.markdown("---")

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
        
        # Menyimpan dengan waktu WITA
        wita = pytz.timezone('Asia/Makassar')
        waktu_wita = datetime.now(wita).strftime("%Y-%m-%d %H:%M:%S")
        
        data_baru = pd.DataFrame([[waktu_wita, nama_user, ulasan_user, label_sentimen]])
        data_baru.to_csv(file_database, mode='a', header=False, index=False)
        st.info("✅ Data berhasil tersimpan dengan stempel waktu WITA!")

st.markdown("---")

# 4. PINTU RAHASIA (Mode Admin)
with st.expander("🔒 Mode Admin"):
    pin_rahasia = st.text_input("Masukkan PIN Admin:", type="password")
    
    if pin_rahasia == "12345": # Ganti PIN di sini jika perlu
        st.success("Akses Dibuka!")
        if os.path.exists(file_database):
            df_tampil = pd.read_csv(file_database)
            st.dataframe(df_tampil, use_container_width=True)
            
            with open(file_database, "rb") as file:
                st.download_button(
                    label="📥 Download Data ke Excel (CSV)",
                    data=file,
                    file_name="Data_Mobil_Listrik_WITA.csv",
                    mime="text/csv"
                )
    elif pin_rahasia != "":
        st.error("PIN Salah!")
