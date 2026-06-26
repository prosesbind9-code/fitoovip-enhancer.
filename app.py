import streamlit as st
import requests
from PIL import Image
import io

# --- KONFIGURASI HALAMAN UTAMA WEBSITE ---
st.set_page_config(
    page_title="Fitoo VIP - True AI Photo Enhancer", 
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

st.title("📸 Fitoo VIP - AI Photo Enhancer V2")
st.write("Menggunakan teknologi SwinIR / Real-ESRGAN Cloud Gratis. Hasil tajam maksimal tanpa akun Pro!")
st.markdown("---")

uploaded_file = st.file_uploader("Pilih atau seret foto kamu ke sini", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("🔄 Gambar Asli (Sebelum)")
    st.image(image, use_container_width=True)
    st.markdown("---")
    
    if st.button("🚀 Proses Jernihkan dengan Cloud AI Gratis"):
        with st.spinner("Mengirim gambar ke Server AI Gratisan... Mohon tunggu sekira 10-20 detik (tergantung antrean server)..."):
            try:
                # Konversi gambar ke biner
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='JPEG')
                img_data = img_byte_arr.getvalue()

                # Menggunakan API Publik Gratis Hugging Face untuk model SwinIR (salah satu AI upscaler terbaik)
                API_URL = "https://api-inference.huggingface.co/models/caidas/swinir-lightweight-image-super-resolution-x4"
                
                response = requests.post(API_URL, data=img_data)
                
                # Jika response berupa data gambar (sukses)
                if response.status_code == 200:
                    result_img = Image.open(io.BytesIO(response.content))
                    
                    st.subheader("✨ Hasil AI Ultra HD (Sesudah)")
                    st.image(result_img, use_container_width=True, caption="Detail berhasil dipulihkan oleh AI SwinIR")
                    
                    # Persiapan tombol download
                    buf = io.BytesIO()
                    result_img.save(buf, format="PNG", quality=100)
                    byte_im = buf.getvalue()
                    
                    st.markdown(" ")
                    st.download_button(
                        label="📥 Download Foto Kualitas Terbaik (PNG)",
                        data=byte_im,
                        file_name="FitooVIP_SwinIR_HD.png",
                        mime="image/png"
                    )
                    st.success("Sukses! AI selesai merekonstruksi detail foto kamu.")
                
                elif response.status_code == 503:
                    st.warning("⏳ Server AI sedang bersiap (loading model). Mohon klik ulang tombol proses dalam 10 detik lagi.")
                else:
                    st.error(f"Gagal memproses. Server memberikan respon kode: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan koneksi ke server AI: {e}")

st.markdown("---")
st.caption("Aplikasi Web ini menggunakan Ruang Inference Hugging Face | Bebas Biaya & Tanpa Login")
