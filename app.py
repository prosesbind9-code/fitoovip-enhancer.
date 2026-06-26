import streamlit as st

# --- 1. KONFIGURASI HALAMAN UTAMA ---
st.set_page_config(
    page_title="Fitoo VIP - AI Face Animator Hub", 
    page_icon="🎬", 
    layout="centered"
)

# --- 2. GAYA MODERASI VISUAL (THEME CYBERPUNK PREMIUM) ---
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .card {
        background-color: #1e293b;
        padding: 22px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    h1 { color: #3b82f6 !important; font-weight: 800; }
    h3 { color: #60a5fa !important; margin-top: 0; }
    p { color: #cbd5e1; font-size: 15px; }
    li { color: #94a3b8; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER WEBSITE ---
st.title("🎬 Fitoo VIP - AI Face Animator Hub")
st.write("Selamat datang di pusat komputasi gerakan wajah. Di sini kamu bisa mengubah foto portrait diam menjadi video bergerak hidup mirip manusia asli.")
st.markdown("---")

st.info("💡 **Info Kinerja:** Proses animasi video membutuhkan GPU kelas berat. Hub ini menghubungkan kamu langsung ke klaster server kecerdasan buatan (AI Space) secara gratis tanpa membebani memori hosting Streamlit kamu.")

# --- 4. SEKSI MODEL 1: LIVEPORTRAIT (GERAKAN WAJAH INSTAN) ---
st.markdown("""
<div class="card">
    <h3>🔥 Opsi 1: LivePortrait Engine (Realisme Tinggi)</h3>
    <p>Model AI terbaik untuk mengekstrak ekspresi mikro. Foto wajahmu akan berkedip, melirik, dan tersenyum dengan transisi piksel yang sangat halus.</p>
    <ul>
        <li><b>Cara Pakai:</b> Taruh foto wajah (menghadap ke depan) pada kotak 'Source Image' di bawah, lalu klik <b>Animate</b>.</li>
        <li><b>Format Output:</b> MP4 Video HD.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Menanamkan sistem aplikasi LivePortrait menggunakan iframe
st.components.v1.iframe(
    src="https://kwai-vgi-liveportrait.hf.space",
    height=650,
    scrolling=True
)

st.markdown("---")

# --- 5. SEKSI MODEL 2: SADTALKER (FOTO BERBICARA + AUDIO) ---
st.markdown("""
<div class="card">
    <h3>🗣️ Opsi 2: SadTalker Engine (Talking Photo)</h3>
    <p>Gunakan opsi ini jika kamu ingin foto diam tersebut bergerak sembari <b>mengucapkan kalimat tertentu</b> sesuai dengan rekaman suara yang kamu masukkan.</p>
    <ul>
        <li><b>Cara Pakai:</b> Upload foto wajah, upload file rekaman suara (.mp3/.wav), lalu klik tombol generate di dalam panel.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Menanamkan alternatif space SadTalker yang memiliki tingkat kestabilan tinggi
st.components.v1.iframe(
    src="https://as61-sadtalker.hf.space", 
    height=650,
    scrolling=True
)

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Dikembangkan oleh fitzz developer © 2026")
