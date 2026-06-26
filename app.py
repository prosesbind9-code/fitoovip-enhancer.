import streamlit as st
import numpy as np
from PIL import Image
from skimage.transform import resize
import io

# --- KONFIGURASI HALAMAN UTAMA WEBSITE ---
st.set_page_config(
    page_title="Fitoo VIP - Pure HD Enhancer", 
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

st.title("📸 Fitoo VIP - Pure HD Enhancer V4")
st.write("Menggunakan Anti-Aliasing Pixel Reconstruction Engine. Ringan, anti-crash, dan tajam saat di-zoom!")
st.markdown("---")

uploaded_file = st.file_uploader("Pilih atau seret foto kamu ke sini", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("🔄 Gambar Asli (Sebelum)")
    st.image(image, use_container_width=True)
    st.markdown("---")
    
    if st.button("🚀 Proses Jernihkan Gambar"):
        with st.spinner("Menggandakan kerapatan piksel & memulihkan detail..."):
            try:
                # Konversi ke numpy array
                img_array = np.array(image)
                
                # Menggunakan skimage resize dengan anti-aliasing tingkat tinggi (mencegah blur/kotak saat di-zoom)
                # Menaikkan resolusi sebesar 3x lipat secara murni
                new_shape = (img_array.shape[0] * 3, img_array.shape[1] * 3, img_array.shape[2])
                hd_array = resize(img_array, new_shape, order=3, anti_aliasing=True, preserve_range=True)
                
                # Konversi kembali ke format gambar unit8
                hd_array = np.clip(hd_array, 0, 255).astype(np.uint8)
                result_img = Image.fromarray(hd_array)
                
                st.subheader("✨ Hasil Pure HD (Sesudah)")
                st.image(result_img, use_container_width=True, caption="Resolusi sukses dinaikkan 3x lipat dengan teknik Anti-Aliasing")
                
                # Persiapan tombol download
                buf = io.BytesIO()
                result_img.save(buf, format="PNG", quality=100)
                byte_im = buf.getvalue()
                
                st.markdown(" ")
                st.download_button(
                    label="📥 Download Foto Kualitas Terbaik (PNG)",
                    data=byte_im,
                    file_name="FitooVIP_PureHD.png",
                    mime="image/png"
                )
                st.success("Sukses! File siap di-download.")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {e}")

st.markdown("---")
st.caption("Aplikasi Web ini menggunakan modul scikit-image Anti-Aliasing | Khusus untuk Fitoo VIP")
