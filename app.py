import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import io

# --- 1. KONFIGURASI HALAMAN UTAMA WEBSITE ---
st.set_page_config(
    page_title="Fitoo VIP - AI Photo Enhancer", 
    page_icon="📸", 
    layout="centered"
)

# Gaya Tampilan Premium (CSS Custom)
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button {
        background-image: linear-gradient(to right, #1e40af , #3b82f6);
        color: white; border-radius: 8px; border: none;
        padding: 10px 24px; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-image: linear-gradient(to right, #2563eb , #60a5fa); color: white; }
    h1, h2, h3 { color: #3b82f6 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📸 Fitoo VIP - AI Photo Enhancer")
st.write("Ubah foto buram menjadi kualitas terbaik secara instan melalui browser, tanpa modul tambahan.")
st.markdown("---")

# --- 2. FITUR UPLOAD GAMBAR ---
uploaded_file = st.file_uploader("Pilih atau seret foto kamu ke sini (PNG, JPG, JPEG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Membaca file gambar yang diunggah
    image = Image.open(uploaded_file)
    
    # Menampilkan Preview Gambar Sebelum Diolah
    st.subheader("🔄 Gambar Asli (Sebelum)")
    st.image(image, use_container_width=True, caption="Foto Beresolusi Rendah / Buram")
    
    st.markdown("---")
    
    # --- 3. PROSES EKSEKUSI PENGOPTIMAL GAMBAR ---
    if st.button("🚀 Proses Menjadi Kualitas Terbaik"):
        with st.spinner("Sistem sedang memetakan piksel & menajamkan detail gambar..."):
            
            # A. Konversi gambar ke format Array (OpenCV) untuk memperbesar resolusi
            img_array = np.array(image)
            height, width = img_array.shape[:2]
            
            # Menggunakan interpolasi Kubik untuk menaikkan resolusi 2x lipat tanpa pecah kotak-kotak
            hd_array = cv2.resize(img_array, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
            
            # Kembalikan ke format PIL Image untuk penyelarasan filter visual
            pil_hd = Image.fromarray(hd_array)
            
            # B. Optimasi Ketajaman Detil (Auto-Sharpness 2.0x)
            sharpness_engine = ImageEnhance.Sharpness(pil_hd)
            pil_hd = sharpness_engine.enhance(2.2)
            
            # C. Penyesuaian Keseimbangan Kontras (Auto-Contrast 1.2x)
            contrast_engine = ImageEnhance.Contrast(pil_hd)
            pil_hd = contrast_engine.enhance(1.2)
            
            # D. Koreksi Pencahayaan Otomatis (Auto-Brightness)
            brightness_engine = ImageEnhance.Brightness(pil_hd)
            pil_hd = brightness_engine.enhance(1.05)
            
            # Menampilkan Hasil Akhir di Halaman Web
            st.subheader("✨ Hasil Kualitas Terbaik (Sesudah)")
            st.image(pil_hd, use_container_width=True, caption="Resolusi Berhasil Ditingkatkan & Dipertajam")
            
            # --- 4. ENGINE UNDUHAN (DOWNLOAD BUTTON) ---
            buf = io.BytesIO()
            pil_hd.save(buf, format="PNG", quality=100) # Simpan dengan format PNG kualitas tertinggi
            byte_im = buf.getvalue()
            
            st.markdown(" ")
            st.download_button(
                label="📥 Download Foto Kualitas Terbaik (PNG)",
                data=byte_im,
                file_name="FitooVIP_Enhanced_Photo.png",
                mime="image/png"
            )
            st.success("Sukses! Klik tombol di atas untuk menyimpan ke galeri perangkat Anda.")

st.markdown("---")
st.caption("Aplikasi Web ini dibuat khusus untuk Fitoo VIP | Didukung oleh Python & Streamlit Engine")
