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

# 893d297d-03a7-4996-a09c-d33e4c698e0a
# GANTI teks di bawah ini dengan API Key yang kamu dapatkan dari website DeepAI
DEEPAI_API_KEY = "MASUKKAN_API_KEY_KAMU_DI_SINI"

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

st.title("📸 Fitoo VIP - True AI Photo Enhancer")
st.write("Menggunakan teknologi Deep Learning Cloud untuk merekonstruksi piksel. Hasil dijamin tajam saat di-zoom!")
st.markdown("---")

uploaded_file = st.file_uploader("Pilih atau seret foto kamu ke sini", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("🔄 Gambar Asli (Sebelum)")
    st.image(image, use_container_width=True)
    st.markdown("---")
    
    if st.button("🚀 Proses Jernihkan dengan Cloud AI"):
        if DEEPAI_API_KEY == "MASUKKAN_API_KEY_KAMU_DI_SINI":
            st.error("❌ Kamu belum memasukkan API Key DeepAI di dalam kode script GitHub!")
        else:
            with st.spinner("Mengirim gambar ke Server AI... Mohon tunggu sekira 5-10 detik..."):
                try:
                    # Konversi file gambar ke format biner untuk dikirim via API
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format=image.format if image.format else 'JPEG')
                    img_byte_arr = img_byte_arr.getvalue()

                    # Eksekusi request ke Server AI DeepAI (Waifu2x / TorchSR Engine)
                    r = requests.post(
                        "https://api.deepai.org/api/waifu2x",
                        files={'image': img_byte_arr},
                        headers={'api-key': DEEPAI_API_KEY}
                    )
                    
                    response_json = r.json()
                    
                    # Jika server berhasil memproses dan memberikan link hasil gambar HD
                    if 'output_url' in response_json:
                        output_url = response_json['output_url']
                        
                        # Ambil gambar hasil dari url luar tersebut
                        result_img = Image.open(requests.get(output_url, stream=True).raw)
                        
                        st.subheader("✨ Hasil Cloud AI Ultra HD (Sesudah)")
                        st.image(result_img, use_container_width=True, caption="Piksel berhasil digambar ulang oleh AI")
                        
                        # Persiapan Tombol Download Kualitas Maksimal
                        buf = io.BytesIO()
                        result_img.save(buf, format="PNG", quality=100)
                        byte_im = buf.getvalue()
                        
                        st.markdown(" ")
                        st.download_button(
                            label="📥 Download Foto Kualitas Terbaik (PNG)",
                            data=byte_im,
                            file_name="FitooVIP_True_AI_HD.png",
                            mime="image/png"
                        )
                        st.success("Sukses! AI telah selesai merekonstruksi detail foto kamu.")
                    else:
                        st.error(f"Gagal memproses gambar. Detail: {response_json.get('status', 'Error tidak diketahui')}")
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan koneksi ke server AI: {e}")

st.markdown("---")
st.caption("Aplikasi Web ini menggunakan API DeepAI Cloud | Khusus untuk Fitoo VIP")
