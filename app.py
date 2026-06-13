import streamlit as st
import joblib

vectorizer = joblib.load('kamus_kata.pkl')
model_ai = joblib.load('model_ai.pkl')

st.set_page_config(page_title="Ulasan EV Indonesia", page_icon="⚡")
st.title("⚡ Sentimen Mobil Listrik Indonesia")
st.write("Ketik ulasan Anda tentang mobil listrik di bawah ini, dan AI kami akan mendeteksi apakah itu pujian atau kritikan!")

ulasan = st.text_area("Masukkan Ulasan:")

if st.button("Kirim Ulasan"):
    if ulasan.strip() == "":
        st.warning("Ulasan tidak boleh kosong!")
    else:
        teks_angka = vectorizer.transform([ulasan])
        hasil = model_ai.predict(teks_angka)
        
        st.markdown("---")
        if hasil[0] == 1:
            st.success("🟢 **HASIL: POSITIF** (Ulasan Mendukung)")
        else:
            st.error("🔴 **HASIL: NEGATIF** (Ulasan Kritis)")
