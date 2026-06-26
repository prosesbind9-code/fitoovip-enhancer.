import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import io

# --- KONFIGURASI HALAMAN UTAMA WEBSITE ---
st.set_page_config(
    page_title="Fitoo VIP - Photo to Video Converter", 
    page_icon="🎬", 
    layout="centered"
)

st.title("🎬 Fitoo VIP - Photo to Video Converter")
st.write("Ubah kumpulan foto kamu menjadi sebuah video MP4 berkualitas tinggi secara instan.")
st.markdown("---")

# --- INPUT PENGATURAN VIDEO ---
st.sidebar.header("⚙️ Pengaturan Video")
fps = st.sidebar.slider("Durasi Kecepatan (Frame Per Second)", min_value=1, max_value=5, value=1, help="Semakin kecil angkanya, semakin lama foto tampil di video (misal: 1 FPS = 1 foto tampil selama 1 detik).")
video_name = st.sidebar.text_input("Nama File Hasil Video", value="fitoovip_video")

# --- FITUR UPLOAD MULTIPLE FOTO ---
uploaded_files = st.file_uploader(
    "Upload 2 atau lebih foto kamu di sini (PNG, JPG, JPEG)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"📂 **{len(uploaded_files)} foto berhasil dipilih.**")
    
    # Menampilkan grid preview foto yang diupload
    cols = st.columns(4)
    for idx, file in enumerate(uploaded_files):
        with cols[idx % 4]:
            img = Image.open(file)
            st.image(img, use_container_width=True)

    st.markdown("---")

    # --- TOMBOL PROSES EKSEKUSI ---
    if st.button("🚀 Mulai Ubah Menjadi Video"):
        if len(uploaded_files) < 2:
            st.error("❌ Minimal upload 2 foto atau lebih untuk membuat video!")
        else:
            with st.spinner("Sedang menyelaraskan ukuran gambar dan merakit video..."):
                try:
                    # 1. Menentukan ukuran (resolusi) standar video berdasarkan foto pertama
                    first_img = Image.open(uploaded_files[0])
                    first_array = np.array(first_img.convert('RGB'))
                    height, width, layers = first_array.shape
                    size = (width, height)

                    # 2. Inisialisasi Video Writer OpenCV
                    # Menggunakan codec 'mp4v' agar menghasilkan output .mp4 yang kompatibel di Android/PC
                    temp_video_path = "temp_output.mp4"
                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    video = cv2.VideoWriter(temp_video_path, fourcc, fps, size)

                    # 3. Proses penggabungan foto ke dalam video
                    for uploaded_file in uploaded_files:
                        img = Image.open(uploaded_file)
                        # Pastikan semua format gambar diubah ke RGB dan disamakan ukurannya dengan foto pertama
                        img_resized = img.convert('RGB').resize((width, height))
                        
                        # Konversi ke format array OpenCV (BGR)
                        img_array = np.array(img_resized)
                        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                        
                        # Tulis gambar ke dalam frame video
                        video.write(img_cv)

                    # Tutup/selesaikan pembuatan video
                    video.release()

                    # 4. Membaca file video biner untuk tombol download
                    with open(temp_video_path, "rb") as f:
                        video_bytes = f.read()

                    st.success("✨ Sukses! Video kamu berhasil dirakit.")
                    
                    # Tampilkan preview video langsung di website
                    st.video(video_bytes)

                    # 5. TOMBOL DOWNLOAD VIDEO
                    st.markdown(" ")
                    st.download_button(
                        label="📥 Download Hasil Video (MP4)",
                        data=video_bytes,
                        file_name=f"{video_name}.mp4",
                        mime="video/mp4"
                    )

                    # Hapus file sampah sementara di server
                    if os.path.exists(temp_video_path):
                        os.remove(temp_video_path)

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat merakit video: {e}")

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Didukung oleh OpenCV Video Engine")
