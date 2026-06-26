import streamlit as st
from gradio_client import Client, handle_file
from PIL import Image
import os

# --- KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="Fitoo VIP - AI Face Animator Pro", 
    page_icon="🎬", 
    layout="centered"
)

# Tampilan UI Premium
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

st.title("🎬 Fitoo VIP - AI Face Animator V5.1")
st.write("Ubah foto wajah diam menjadi video bergerak. Menggunakan Smart Client API Auto-Routing!")
st.markdown("---")

uploaded_file = st.file_uploader("Upload Foto Wajah (Format JPG/PNG, Wajah Jelas Menghadap Depan)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Simpan file sementara di server Streamlit
    temp_img_path = "temp_user_face.jpg"
    image = Image.open(uploaded_file)
    image.save(temp_img_path, format="JPEG")
    
    st.subheader("📸 Preview Foto Kamu")
    st.image(image, width=300)
    st.markdown("---")
    
    if st.button("🚀 Mulai Animasikan Wajah"):
        with st.spinner("Mengantre di server GPU... AI sedang memproses gerakan struktur wajah (Sekitar 30-60 detik)..."):
            try:
                # KONEKSI KE SERVER API
                client = Client("KwaiVGI/LivePortrait")
                
                # PERBAIKAN UTAMA: Menggunakan indeks parameter posisi, bukan menggunakan api_name.
                # Ini memaksa Gradio Client untuk langsung menembak fungsi utama aplikasi webnya.
                result = client.predict(
                    handle_file(temp_img_path),  # Parameter 1: Input Foto Wajah
                    None,                         # Parameter 2: Driving Video (Kosongkan untuk default)
                    # Kita hapus baris api_name="/predict" agar sistem otomatis mencari jalurnya sendiri
                )
                
                # Ekstrak hasil file video (.mp4)
                video_output_path = None
                if isinstance(result, tuple) or isinstance(result, list):
                    video_output_path = result[0]
                elif isinstance(result, str):
                    video_output_path = result
                
                if video_output_path and os.path.exists(video_output_path):
                    with open(video_output_path, "rb") as f:
                        video_bytes = f.read()
                    
                    st.subheader("✨ Hasil Video Wajah Bergerak")
                    st.video(video_bytes)
                    
                    st.markdown(" ")
                    st.download_button(
                        label="📥 Download Hasil Video (MP4)",
                        data=video_bytes,
                        file_name="fitoovip_wajah_bergerak.mp4",
                        mime="video/mp4"
                    )
                    st.success("Sukses! AI berhasil menghidupkan foto diammu.")
                else:
                    st.error("❌ Gagal memproses. Server AI mengembalikan respons kosong. Coba klik ulang tombol proses.")
                    
            except Exception as e:
                st.error(f"Terjadi kendala saat mengantre di server AI: {e}")
                st.info("Tips: Jika muncul pesan overload, server Hugging Face sedang penuh antrean global. Tunggu beberapa saat lalu klik ulang tombolnya.")
            
            finally:
                # Bersihkan file sampah
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Powered by Auto-Routing LivePortrait API Engine")
