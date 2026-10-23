# -*- coding: utf-8 -*-
"""Streamlit chatbot menggunakan Google Gemini API."""

import streamlit as st
from google import genai

st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Gemini Chatbot")
st.caption("Chatbot AI sederhana menggunakan Google Gemini API.")

# Prefer Streamlit Secrets for deployment; allow sidebar entry for local/testing use.
with st.sidebar:
    st.subheader("Pengaturan")
    secret_key = ""
    try:
        secret_key = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        secret_key = ""

    google_api_key = st.text_input(
        "Google AI API Key",
        value=secret_key,
        type="password",
        help="Untuk deployment, lebih aman simpan key di Streamlit Secrets.",
    )
    model_name = st.selectbox(
        "Model Gemini",
        options=["gemini-3.5-flash", "gemini-3.5-flash-lite"],
        index=0,
    )
    system_instruction = st.text_area(
        "Instruksi sistem (opsional)",
        value="Jawab pertanyaan pengguna dengan jelas dan membantu. Gunakan Bahasa Indonesia kecuali pengguna meminta bahasa lain.",
        help="Instruksi ini digunakan saat membuat sesi percakapan baru.",
    )
    reset_button = st.button("Reset Percakapan", use_container_width=True)

if reset_button:
    st.session_state.pop("messages", None)
    st.session_state.pop("chat", None)
    st.session_state.pop("client_key_fingerprint", None)
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Recreate the client/chat if the API key or model changes.
if not google_api_key:
    st.info("Masukkan Google AI API Key di sidebar untuk mulai menggunakan chatbot.")
    st.markdown("Dapatkan API key melalui [Google AI Studio](https://aistudio.google.com/).")
    st.stop()

# Do not store the API key itself in session state; compare a lightweight fingerprint.
import hashlib
key_fingerprint = hashlib.sha256(
    f"{google_api_key}:{model_name}:{system_instruction}".encode("utf-8")
).hexdigest()

if st.session_state.get("client_key_fingerprint") != key_fingerprint:
    try:
        st.session_state.genai_client = genai.Client(api_key=google_api_key)
        st.session_state.chat = st.session_state.genai_client.chats.create(
            model=model_name,
            config={"system_instruction": system_instruction},
        )
        st.session_state.client_key_fingerprint = key_fingerprint
        st.session_state.messages = []
    except Exception as exc:
        st.error(f"Tidak dapat menginisialisasi Gemini. Periksa API key dan konfigurasi. Detail: {exc}")
        st.stop()

# Render saved conversation.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ketik pesan Anda di sini...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Gemini sedang menyiapkan jawaban..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                answer = response.text if getattr(response, "text", None) else str(response)
            except Exception as exc:
                answer = (
                    "Maaf, permintaan belum berhasil diproses. Periksa koneksi, kuota, "
                    "nama model, dan API key Anda.\n\n"
                    f"Detail teknis: `{exc}`"
                )
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

with st.sidebar:
    st.divider()
    st.caption("API key tidak perlu ditulis di source code. Gunakan Streamlit Secrets untuk deployment.")
