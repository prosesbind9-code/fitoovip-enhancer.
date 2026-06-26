import streamlit as st
import requests
import io
from PIL import Image

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="Fitoo VIP - AI Face Animator Pro", 
    page_icon="🎬", 
    layout="centered"
)

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stButton>button {
        background-image: linear-gradient(to right, #1e40af , #3b82f6);
        color: white; border-radius: 8px; border: none;
        padding: 12px 24px; font-weight: bold; width: 100%;
    }
    h1, h2, h3 { color: #3b82f6 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Fitoo VIP - AI Face Animator V6")
st.write("Ubah foto wajah diam menjadi video bergerak hidup. Menggunakan Jalur Direct HTTP Request (Anti Parameter Error)!")
st.markdown("---")

uploaded_file = st.file_uploader("Upload Foto Wajah (Format JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("📸 Preview Foto")
    st.image(image, width=300)
    st.markdown("---")
    
    if st.button("🚀 Mulai Nyalakan AI"):
        with st.spinner("Mengirim data langsung ke repositori server AI... Mohon tunggu 30-60 detik..."):
            try:
                # Konversi gambar ke format biner untuk ditembak langsung
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_data = img_byte_arr.getvalue()

                # Kita tembak model SadTalker versi API publik murni tanpa library Gradio Client
                # Ini adalah jalur lurus tanpa hambatan parameter
                API_URL = "https://api-inference.huggingface.co/models/vinthony/SadTalker"
                
                # Mengirim header kosong untuk akses tamu publik yang stabil
                headers = {}
                response = requests.post(API_URL, headers=headers, data=img_data)
                
                # Jika server berhasil mengembalikan data video biner (.mp4)
                if response.status_code == 200:
                    video_bytes = response.content
                    
                    st.subheader("✨ Hasil Video Wajah Bergerak")
                    st.video(video_bytes)
                    
                    st.markdown(" ")
                    st.download_button(
                        label="📥 Download Hasil Video (MP4)",
                        data=video_bytes,
                        file_name="fitoovip_bergerak.mp4",
                        mime="video/mp4"
                    )
                    st.success("Sukses! AI berhasil memproses gambar tanpa hambatan kode fungsi.")
                
                elif response.status_code == 503:
                    st.warning("⏳ Server AI sedang memanaskan mesin (loading model). Silakan tunggu 10 detik lalu klik tombolnya lagi.")
                else:
                    st.error(f"Server pusat menolak kiriman data (Status: {response.status_code}). Tampaknya antrean global sedang penuh, coba klik ulang beberapa saat lagi.")
                    
            except Exception as e:
                st.error(f"Gagal terhubung ke pusat data AI: {e}")

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Direct HTTP Stream Engine")
