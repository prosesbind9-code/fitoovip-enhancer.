import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import urllib.request

# --- KONFIGURASI HALAMAN UTAMA WEBSITE ---
st.set_page_config(
    page_title="Fitoo VIP - Standalone AI Enhancer", 
    page_icon="📸", 
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button {
        background-image: linear-gradient(to right, #1e40af , #3b82f6);
        color: white; border-radius: 8px; border: none;
        padding: 10px 24px; font-weight: bold; width: 100%;
    }
    h1, h2, h3 { color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Fitoo VIP - AI Standalone Enhancer V3")
st.write("Menggunakan Local EDSR Deep Learning Engine. Proses 100% mandiri di dalam server, bebas error koneksi!")
st.markdown("---")

# Fungsi untuk download model AI EDSR jika belum ada di server
@st.cache_resource
def download_model():
    model_url = "https://github.com/Saafke/EDSR_Tensorflow/raw/master/models/EDSR_x2.pb"
    model_path = "EDSR_x2.pb"
    if not os.path.exists(model_path):
        with st.spinner("Mengunduh Otak AI EDSR ke server (Hanya sekali di awal)..."):
            urllib.request.urlretrieve(model_url, model_path)
    return model_path

try:
    model_file = download_model()
except Exception as e:
    st.error(f"Gagal menyiapkan komponen AI: {e}")

uploaded_file = st.file_uploader("Pilih atau seret foto kamu ke sini", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("🔄 Gambar Asli (Sebelum)")
    st.image(image, use_container_width=True)
    st.markdown("---")
    
    if st.button("🚀 Proses Jernihkan dengan Local AI"):
        with st.spinner("AI sedang merekonstruksi piksel gambar langsung di server... Mohon tunggu 15-30 detik..."):
            try:
                # Konversi PIL Image ke OpenCV format
                img_array = np.array(image.convert('RGB'))
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                # Set up OpenCV Super Resolution menggunakan model EDSR
                sr = cv2.dnn_superres.DnnSuperResImpl_create()
                sr.readModel(model_file)
                sr.setModel("edsr", 2) # Menaikkan resolusi 2x lipat dengan kecerdasan buatan

                # Eksekusi rekonstruksi gambar oleh AI
                result_cv = sr.upsample(img_cv)

                # Kembalikan ke format PIL untuk ditampilkan
                result_rgb = cv2.cvtColor(result_cv, cv2.COLOR_BGR2RGB)
                result_img = Image.fromarray(result_rgb)
                
                st.subheader("✨ Hasil Local AI Super Resolution (Sesudah)")
                st.image(result_img, use_container_width=True, caption="Tekstur dipertajam nyata oleh Model EDSR")
                
                # Persiapan tombol download
                import io
                buf = io.BytesIO()
                result_img.save(buf, format="PNG", quality=100)
                byte_im = buf.getvalue()
                
                st.markdown(" ")
                st.download_button(
                    label="📥 Download Foto Kualitas Terbaik (PNG)",
                    data=byte_im,
                    file_name="FitooVIP_EDSR_LocalHD.png",
                    mime="image/png"
                )
                st.success("Sukses! Gambar berhasil diubah ke HD tanpa meminjam server luar.")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")

st.markdown("---")
st.caption("Aplikasi Web ini berjalan mandiri menggunakan model EDSR Tensorflow x2 | Powered for Fitoo VIP")
