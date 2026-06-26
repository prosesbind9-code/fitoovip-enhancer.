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

st.title("🎬 Fitoo VIP - AI Face Animator V5")
st.write("Ubah foto wajah diam menjadi video bergerak (LivePortrait Engine). Jalur API khusus, anti-error 404/space error!")
st.markdown("---")

# Mengambil input foto dari pengguna
uploaded_file = st.file_uploader("Upload Foto Wajah (Format JPG/PNG, Wajah Harus Jelas Menghadap Depan)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Simpan file sementara di server Streamlit untuk dikirim ke API
    temp_img_path = "temp_user_face.jpg"
    image = Image.open(uploaded_file)
    image.save(temp_img_path, format="JPEG")
    
    st.subheader("📸 Preview Foto Kamu")
    st.image(image, width=300)
    st.markdown("---")
    
    if st.button("🚀 Mulai Animasikan Wajah (Jalur API Khusus)"):
        with st.spinner("Menghubungkan ke API Dedicated GPU... AI sedang memproses gerakan struktur wajah (Sekitar 30-60 detik)..."):
            try:
                # Mengaktifkan Client API Gradio langsung ke server LivePortrait yang stabil
                # Jalur ini tidak akan terkena 'Space Error' visual karena bypass tampilan web utama
                client = Client("KwaiVGI/LivePortrait")
                
                # Eksekusi prediksi gerakan (menggunakan template gerakan default berkedip & tersenyum alami)
                result = client.predict(
                    img_input=handle_file(temp_img_path),
                    vid_input=None, # menggunakan default motion template bawaan AI
                    api_name="/predict"
                )
                
                # Hasil dari Gradio API biasanya berupa path file video (.mp4) yang sukses dibuat
                # Kita cari file videonya di dalam struktur data hasil response
                video_output_path = None
                if isinstance(result, tuple) or isinstance(result, list):
                    video_output_path = result[0]
                elif isinstance(result, str):
                    video_output_path = result
                
                if video_output_path and os.path.exists(video_output_path):
                    # Baca file biner videonya
                    with open(video_output_path, "rb") as f:
                        video_bytes = f.read()
                    
                    st.subheader("✨ Hasil Video Wajah Bergerak")
                    st.video(video_bytes)
                    
                    # Sediakan tombol download aman (.mp4 standar Android)
                    st.markdown(" ")
                    st.download_button(
                        label="📥 Download Hasil Video (MP4)",
                        data=video_bytes,
                        file_name="fitoovip_wajah_bergerak.mp4",
                        mime="video/mp4"
                    )
                    st.success("Sukses! AI berhasil menghidupkan foto diammu menjadi bergerak.")
                else:
                    st.error("❌ AI selesai memproses, namun format video gagal diekstrak. Silakan coba sesaat lagi.")
                    
            except Exception as e:
                st.error(f"Terjadi kendala saat mengantre di server AI: {e}")
                st.info("Tips: Jika server sedang penuh antrean global, tunggu 1-2 menit lalu klik tombol proses kembali.")
            
            finally:
                # Bersihkan file sampah foto sementara di server
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Powered by Gradio LivePortrait API Engine")
