# -*- coding: utf-8 -*-
"""EduML — chatbot edukasi pengenalan Machine Learning untuk siswa SMA/SMK."""

import hashlib
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="EduML | AI Learning Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual identity ----------
st.markdown("""
<style>
    :root {
        --edu-ink: #172554;
        --edu-violet: #6d28d9;
        --edu-blue: #2563eb;
        --edu-cyan: #06b6d4;
        --edu-pink: #ec4899;
        --edu-yellow: #fbbf24;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 0% 0%, rgba(191,219,254,.34), transparent 36%),
            radial-gradient(ellipse at 100% 10%, rgba(251,207,232,.32), transparent 32%),
            linear-gradient(180deg, #f8fbff 0%, #f5f3ff 52%, #fdf2f8 100%);
        color: var(--edu-ink);
    }
    .block-container {max-width: 1220px; padding-top: 1.5rem; padding-bottom: 2.2rem;}
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #eef2ff 0%, #ecfeff 55%, #fdf2f8 100%);
        border-right: 1px solid rgba(99,102,241,.18);
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {color: #312e81;}
    .hero {
        position: relative; overflow: hidden;
        padding: 2rem 2.1rem; border-radius: 26px;
        background: linear-gradient(120deg, #4f46e5 0%, #7c3aed 38%, #db2777 72%, #0891b2 115%);
        color: white; margin-bottom: 1.25rem;
        box-shadow: 0 18px 45px rgba(99,102,241,.22);
        border: 1px solid rgba(255,255,255,.45);
    }
    .hero:after {
        content: "✦"; position: absolute; right: 5%; top: -32px;
        font-size: 9rem; color: rgba(255,255,255,.15);
        transform: rotate(12deg); pointer-events: none;
    }
    .hero h1 {font-size: clamp(1.8rem, 3vw, 2.65rem); line-height: 1.12; margin: 0 0 .7rem 0; color: white; letter-spacing: -.035em;}
    .hero p {font-size: 1.05rem; line-height: 1.65; max-width: 780px; margin: 0 0 1rem 0; color: #f5f3ff;}
    .pill {
        display: inline-block; padding: .36rem .75rem; margin: .15rem .3rem .15rem 0;
        background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.45);
        border-radius: 999px; font-size: .8rem; font-weight: 650; color: white;
        backdrop-filter: blur(8px);
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,.84); border: 1px solid #e0e7ff;
        border-radius: 18px; padding: 1rem 1.1rem;
        box-shadow: 0 7px 22px rgba(79,70,229,.06);
    }
    [data-testid="stMetricLabel"] {color: #6366f1 !important; font-weight: 650;}
    [data-testid="stMetricValue"] {color: #312e81 !important;}
    div[data-testid="stChatMessage"] {
        border: 1px solid #e0e7ff; border-radius: 18px; padding: .65rem .8rem;
        background: rgba(255,255,255,.9); box-shadow: 0 5px 18px rgba(79,70,229,.05);
        margin-bottom: .6rem;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left: 4px solid #8b5cf6;
    }
    .stButton > button {
        border-radius: 13px; border: 1px solid #c4b5fd;
        background: linear-gradient(135deg, #ffffff 0%, #eef2ff 100%);
        color: #4338ca; font-weight: 650; min-height: 2.8rem;
        box-shadow: 0 4px 12px rgba(99,102,241,.07);
        transition: transform .15s ease, box-shadow .15s ease;
    }
    .stButton > button:hover {
        border-color: #a78bfa; color: #6d28d9;
        box-shadow: 0 8px 20px rgba(139,92,246,.16); transform: translateY(-1px);
    }
    [data-testid="stChatInput"] {
        border: 1px solid #c4b5fd; border-radius: 18px;
        box-shadow: 0 7px 24px rgba(99,102,241,.09);
    }
    [data-testid="stExpander"] {
        border: 1px solid #ddd6fe; border-radius: 16px; background: rgba(255,255,255,.7);
    }
    .small-note {font-size: .86rem; color: #64748b;}
    hr {border-color: #e0e7ff;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------- Defaults ----------
DEFAULT_SYSTEM_PROMPT = """Kamu adalah EduML, asisten edukasi yang mengajarkan pengenalan Machine Learning
kepada siswa SMA/SMK (STM) di Indonesia.

Prinsip mengajar:
- Gunakan Bahasa Indonesia yang ramah, suportif, jelas, dan tidak menggurui.
- Sesuaikan penjelasan untuk pemula usia sekolah menengah; jelaskan istilah teknis saat pertama muncul.
- Mulai dari intuisi dan contoh sehari-hari, lalu jelaskan konsep, langkah, dan contoh sederhana.
- Gunakan analogi yang relevan dengan sekolah, game, kendaraan, musik, olahraga, atau teknologi.
- Untuk pertanyaan teknis, berikan contoh kecil dan kode Python hanya jika bermanfaat; jelaskan kode secara bertahap.
- Bedakan dengan jelas antara data latihan, data pengujian, prediksi, dan fakta.
- Jangan mengklaim model selalu benar. Jelaskan bias, privasi, etika, dan keterbatasan AI saat relevan.
- Jika siswa meminta jawaban tugas, bantu memahami proses dan berikan langkah penyelesaian, bukan hanya jawaban tanpa penjelasan.
- Jika pertanyaan di luar Machine Learning, jawab singkat bila masih relevan, lalu arahkan kembali ke topik belajar.
- Akhiri dengan satu pertanyaan refleksi atau saran langkah belajar berikutnya jika terasa alami.
"""

TOPICS = {
    "Mulai dari dasar": "Jelaskan apa itu Machine Learning untuk pemula, gunakan analogi sehari-hari dan tiga poin utama.",
    "AI vs Machine Learning": "Apa perbedaan Artificial Intelligence, Machine Learning, dan Deep Learning? Beri analogi sederhana.",
    "Jenis Machine Learning": "Jelaskan supervised learning, unsupervised learning, dan reinforcement learning dengan contoh siswa SMA/SMK.",
    "Contoh proyek sekolah": "Berikan 5 ide proyek Machine Learning sederhana untuk siswa SMA/SMK, termasuk data yang dibutuhkan dan tingkat kesulitan.",
    "Contoh Python": "Ajari saya contoh Machine Learning paling sederhana dengan Python. Jelaskan kode baris demi baris untuk pemula.",
    "Kuis singkat": "Buat kuis pengenalan Machine Learning berisi 5 soal pilihan ganda. Jangan tampilkan kunci jawaban sampai saya menjawab.",
}

with st.sidebar:
    st.markdown("## 🌈 EduML")
    st.caption("✨ Learn • Explore • Create | SMA / SMK")
    st.divider()
    st.subheader("🔑 Koneksi model")
    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="Tempel API key di sini",
        help="API key dimasukkan manual dan tidak ditulis ke file Python.",
    )
    st.markdown("[Dapatkan API key di Google AI Studio](https://aistudio.google.com/apikey)")
    model = st.selectbox(
        "Model LLM",
        ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
        help="Pilih model yang tersedia pada akun/API key Anda.",
    )
    st.divider()
    st.subheader("⚙️ Parameter generasi")
    temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.5, value=0.5, step=0.1,
        help="Lebih rendah = jawaban cenderung konsisten; lebih tinggi = lebih variatif.",
    )
    top_p = st.slider(
        "Top-p", min_value=0.1, max_value=1.0, value=0.9, step=0.05,
        help="Mengatur rentang kandidat token yang dipertimbangkan model.",
    )
    max_tokens = st.slider(
        "Panjang jawaban maksimum (token)", min_value=256, max_value=4096,
        value=1536, step=256,
        help="Batas maksimum panjang respons model; bukan jumlah kata yang pasti.",
    )
    st.divider()
    st.subheader("🧑‍🏫 Gaya mengajar")
    teaching_style = st.selectbox(
        "Gaya bahasa",
        ["Ramah dan sederhana", "Formal dan terstruktur", "Interaktif seperti tutor"],
        index=0,
    )
    student_level = st.selectbox(
        "Tingkat materi",
        ["Pemula (tanpa prasyarat)", "Menengah (dasar Python)", "Lanjutan (matematika/Python dasar)"],
        index=0,
    )
    extra_instruction = st.text_area(
        "Instruksi tambahan (opsional)",
        placeholder="Contoh: gunakan analogi otomotif atau proyek IoT...",
        height=90,
    )
    reset = st.button("🗑️ Reset percakapan", use_container_width=True)
    st.caption("Tips: jangan bagikan API key kepada orang lain.")

if reset:
    for key in ("messages", "chat", "config_fingerprint"):
        st.session_state.pop(key, None)
    st.rerun()

# Build system instruction from visible settings.
style_instruction = {
    "Ramah dan sederhana": "Gunakan bahasa santai, sederhana, dan ramah.",
    "Formal dan terstruktur": "Gunakan bahasa formal dengan heading dan urutan langkah yang rapi.",
    "Interaktif seperti tutor": "Ajukan pertanyaan pemandu, cek pemahaman, dan ajak siswa berpikir aktif.",
}[teaching_style]
level_instruction = {
    "Pemula (tanpa prasyarat)": "Anggap siswa belum memahami pemrograman atau matematika lanjutan.",
    "Menengah (dasar Python)": "Siswa memahami konsep dasar Python; boleh gunakan contoh kode sederhana.",
    "Lanjutan (matematika/Python dasar)": "Boleh membahas fitur, evaluasi model, dan matematika dasar secara bertahap.",
}[student_level]
system_instruction = "\n\n".join([
    DEFAULT_SYSTEM_PROMPT,
    f"Pengaturan gaya: {style_instruction}",
    f"Pengaturan tingkat: {level_instruction}",
    f"Instruksi tambahan dari pengelola: {extra_instruction.strip()}" if extra_instruction.strip() else "",
]).strip()

# ---------- Main page ----------
st.markdown("""
<div class="hero">
  <h1>✨ Masa depan dimulai dari rasa ingin tahu!</h1>
  <p>Selamat datang di EduML — ruang belajar AI yang seru, kreatif, dan futuristik. Kenali Machine Learning, coba ide-ide baru, dan jadilah pencipta teknologi masa depan.</p>
  <span class="pill">🚀 Eksplorasi AI</span><span class="pill">🐍 Python pemula</span>
  <span class="pill">💡 Proyek kreatif</span><span class="pill">🌈 Etika AI</span>
</div>
""", unsafe_allow_html=True)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Fokus", "Machine Learning")
with col_b:
    st.metric("Target", "SMA / SMK")
with col_c:
    st.metric("Mode", "Tutor interaktif")

with st.expander("📚 Pilih topik untuk memulai", expanded=not bool(st.session_state.get("messages"))):
    topic_cols = st.columns(3)
    selected_topic = None
    for idx, (label, prompt_text) in enumerate(TOPICS.items()):
        with topic_cols[idx % 3]:
            if st.button(label, key=f"topic_{idx}", use_container_width=True):
                selected_topic = prompt_text
    if selected_topic:
        st.session_state.pending_prompt = selected_topic
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not api_key:
    st.info("Untuk memulai, masukkan Google Gemini API Key pada panel pengaturan di sebelah kiri.")
    st.markdown(
        '<p class="small-note">API key bisa dibuat melalui Google AI Studio. '
        'Kunci dimasukkan manual dan tidak perlu ditaruh di repository GitHub.</p>',
        unsafe_allow_html=True,
    )
    st.stop()

# Use a fingerprint so changes to key/model/settings start a clean chat context.
fingerprint_source = f"{api_key}|{model}|{temperature}|{top_p}|{max_tokens}|{system_instruction}"
fingerprint = hashlib.sha256(fingerprint_source.encode("utf-8")).hexdigest()
if st.session_state.get("config_fingerprint") != fingerprint:
    try:
        st.session_state.client = genai.Client(api_key=api_key)
        st.session_state.chat = st.session_state.client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=temperature,
                top_p=top_p,
                max_output_tokens=max_tokens,
            ),
        )
        st.session_state.config_fingerprint = fingerprint
        st.session_state.messages = []
        st.session_state.pop("pending_prompt", None)
        st.toast("Konfigurasi diterapkan. Percakapan baru dimulai.", icon="⚙️")
    except Exception as exc:
        st.error("Gagal menginisialisasi model. Periksa API key, nama model, dan koneksi.")
        with st.expander("Detail teknis"):
            st.code(str(exc))
        st.stop()

# Render conversation.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🎓"):
        st.markdown(msg["content"])

typed_prompt = st.chat_input("Tanyakan sesuatu tentang Machine Learning...")
prompt = typed_prompt or st.session_state.pop("pending_prompt", None)

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("EduML sedang menyiapkan penjelasan..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                answer = response.text if getattr(response, "text", None) else str(response)
            except Exception as exc:
                answer = (
                    "Maaf, jawaban belum berhasil dibuat. Periksa API key, kuota, koneksi internet, "
                    "dan ketersediaan model yang dipilih.\n\n"
                    f"**Detail teknis:** `{exc}`"
                )
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
foot1, foot2 = st.columns([3, 1])
with foot1:
    st.caption("🚀 EduML • Berani bertanya, bebas bereksperimen, tumbuh bersama AI.")
with foot2:
    st.caption("Powered by Gemini")
