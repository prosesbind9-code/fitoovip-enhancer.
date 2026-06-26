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

st.title("🎬 Fitoo VIP - AI Face Animator V5.2")
st.write("Ubah foto wajah diam menjadi video bergerak. Konfigurasi Eksplisit fn_index / Endpoint.")
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
                # KONEKSI KE SERVER API LIVEPORTRAIT
                client = Client("KwaiVGI/LivePortrait")
                
                # SOLUSI: Menggunakan fn_index=0 atau fn_index=1 untuk menargetkan fungsi utama aplikasi.
                # Kita juga melengkapi parameter default bawaan model LivePortrait (seperti pengaturan pemotongan wajah/lip-sync).
                result = client.predict(
                    img_input=handle_file(temp_img_path), # Parameter 1: Gambar Wajah
                    vid_input=None,                        # Parameter 2: Video penggerak (kosong untuk default)
                    flag_lip_zero=True,                    # Parameter 3: Mengunci bibir tetap rapat di awal
                    flag_relative_motion=True,             # Parameter 4: Gerakan relatif alami
                    flag_stitching=True,                   # Parameter 5: Menjahit kembali wajah ke background asli
                    flag_eye_retargeting=False,            # Parameter 6: Retargeting mata otomatis
                    flag_lip_retargeting=False,            # Parameter 7: Retargeting bibir otomatis
                    scale_factor=2.0,                      # Parameter 8: Skala area potong wajah
                    vx_ratio=0.0,                          # Parameter 9: Pergeseran posisi X
                    vy_ratio=-0.1,                         # Parameter 10: Pergeseran posisi Y
                    fn_index=1                             # KUNCI UTAMA: Memaksa masuk ke endpoint pemroses utama (Indeks 1 atau 0)
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
                    st.error("❌ Gagal mengekstrak video hasil pemrosesan. Coba ganti pengaturan atau klik ulang.")
                    
            except Exception as e:
                # Jika fn_index=1 gagal, kita buat sistem fallback otomatis ke fn_index=0 di dalam penanganan error
                try:
                    client = Client("KwaiVGI/LivePortrait")
                    result = client.predict(
                        handle_file(temp_img_path),
                        None,
                        fn_index=0 # Mencoba gerbang alternatif jika indeks 1 ditolak
                    )
                    
                    video_output_path = result[0] if isinstance(result, (tuple, list)) else result
                    if video_output_path and os.path.exists(video_output_path):
                        with open(video_output_path, "rb") as f:
                            video_bytes = f.read()
                        st.subheader("✨ Hasil Video Wajah Bergerak")
                        st.video(video_bytes)
                        st.download_button(label="📥 Download Hasil Video (MP4)", data=video_bytes, file_name="fitoovip_wajah_bergerak.mp4", mime="video/mp4")
                        st.success("Sukses memproses via Jalur Cadangan!")
                    else:
                        st.error(f"Kedua jalur sibuk. Error detail: {e}")
                except Exception as fallback_error:
                    st.error(f"Gagal terhubung ke endpoint utama: {fallback_error}")
                    st.info("Tips: Server Hugging Face sedang melakukan pemeliharaan fungsi API. Silakan dicoba secara berkala.")
            
            finally:
                # Bersihkan file sampah
                if os.path.exists(temp_img_path):
                    os.remove(temp_img_path)

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Explicit Endpoint Allocation Engine")
