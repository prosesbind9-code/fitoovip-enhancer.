import streamlit as st

# --- KONFIGURASI HALAMAN UTAMA WEBSITE ---
st.set_page_config(
    page_title="Fitoo VIP - AI Face Animator Hub", 
    page_icon="🎬", 
    layout="centered"
)

# Tampilan CSS Premium Cyberpunk
st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .card {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-image: linear-gradient(to right, #1e40af , #3b82f6);
        color: white; border-radius: 8px; border: none;
        padding: 10px 24px; font-weight: bold; width: 100%;
    }
    h1, h2, h3 { color: #3b82f6 !important; }
    a { color: #60a5fa !important; text-decoration: none; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 Fitoo VIP - AI Face Animator Hub")
st.write("Platform khusus untuk mengubah foto wajah diam menjadi video manusia bergerak & hidup.")
st.markdown("---")

st.info("💡 Karena server gratisan membatasi pemrosesan video berat, Fitoo VIP kini terhubung langsung dengan Engine AI Temporal terbaik dunia yang 100% gratis dan stabil.")

# --- OPSI 1: LALUAN LIVEPORTRAIT (TERBAIK) ---
st.markdown("""
<div class="card">
    <h3>🔥 Opsi 1: LivePortrait Engine (Sangat Instan)</h3>
    <p>Teknologi AI terbaik saat ini untuk membuat foto wajah berkedip, tersenyum, dan menoleh dengan sangat mulus mirip manusia asli.</p>
    <ul>
        <li><b>Kelebihan:</b> Tanpa coding, proses instan 5 detik, hasil sangat realistis.</li>
        <li><b>Status Server:</b> Online 24 Jam (Dedicated GPU).</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Menanamkan (Embed) Demo AI LivePortrait langsung di dalam websitemu agar bisa dipakai langsung
st.subheader("🤖 Jalankan LivePortrait Langsung di Sini:")
st.components.v1.iframe(
    src="https://kwai-vgi-liveportrait.hf.space",
    height=600,
    scrolling=True
)

st.markdown("---")

# --- OPSI 2: LALUAN SADTALKER (BISA PAKAI SUARA) ---
st.markdown("""
<div class="card">
    <h3>🗣️ Opsi 2: SadTalker Engine (Foto Berbicara + Suara)</h3>
    <p>Jika kamu ingin membuat foto wajahnya tidak cuma bergerak, tapi juga <b>berbicara mengikuti suara/audio</b> yang kamu upload.</p>
    <ul>
        <li><b>Cara Pakai:</b> Upload foto wajah, upload rekaman suara (MP3), lalu klik Generate.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.subheader("🤖 Jalankan SadTalker Langsung di Sini:")
st.components.v1.iframe(
    src="https://vinthony-sadtalker.hf.space",
    height=600,
    scrolling=True
)

st.markdown("---")
st.caption("Aplikasi Web Resmi Fitoo VIP | Integrasi Dedicated AI Cloud Space")
