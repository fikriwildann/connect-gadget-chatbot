import streamlit as st
import google.generativeai as genai

# ================================
# 1. API KEY GEMINI
# ===============================
genai.configure(api_key=st.secrets["API_KEY"])

# ================================
# 2. MODEL
# ================================
model = genai.GenerativeModel("gemini-2.5-flash")

# ===========================
# STYLE CUSTOM (iMessage)
# ===========================
st.markdown("""
<style>

body {
    background-color: #ffffff;
}

.chat-container {
    max-width: 600px;
    margin: auto;
}

.user-bubble {
    background-color: #007AFF;
    color: white;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px;
    max-width: 80%;
    width: fit-content;
    text-align: right;
    margin-left: auto;
    font-size: 16px;
    line-height: 1.4;
}

.bot-bubble {
    background-color: #E5E5EA;
    color: black;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 8px;
    max-width: 80%;
    width: fit-content;
    text-align: left;
    margin-right: auto;
    font-size: 16px;
    line-height: 1.4;
}

</style>
""", unsafe_allow_html=True)

# ================================
# 3. LOAD STORE INFO DARI FILE TXT
# ================================
with open("store_info.txt", "r", encoding="utf-8") as f:
    STORE_INFO = f.read()

# ================================
# 4. FUNGSI CHAT
# ================================
def ask_gemini(user_message):
    prompt = f"""
Kamu adalah chatbot resmi toko CONNECT.GADGET.

Gunakan informasi toko berikut untuk menjawab semua pertanyaan:
{STORE_INFO}

Tugas kamu:
- Jawab dengan bahasa Indonesia yang ramah dan lengkap.
- Jawab dengan profesional.
- Informasikan harga, stok, warna, varian, diskon, dan detail produk jika diminta.
- Jika ditanya rekomendasi, berikan jawaban yang membantu.
- Jika diminta alamat, jam buka, gunakan data di atas.
- Jika produk tidak ada di daftar, jawab bahwa produk tersebut tidak tersedia.
- Jangan gunakan tanda bintang (*), bold (** **)
- Jangan gunakan format Markdown.

Pertanyaan pengguna:
{user_message}
"""

    response = model.generate_content(prompt)
    return response.text

# ===========================
# HISTORY CHAT
# ===========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ===========================
# HEADER
# ===========================
st.title("📱 CONNECT.GADGET Chatbot")
st.write("Halo! Saya siap bantu cari iPhone, iPad, atau MacBook 😊")

# ===========================
# QUICK REPLY
# ===========================
st.write("Rekomendasi cepat:")
col1, col2, col3 = st.columns(3)

if col1.button("📱 iPhone Terlaris"):
    st.session_state.quick_msg = "iPhone terlaris saat ini apa?"

if col2.button("💻 MacBook"):
    st.session_state.quick_msg = "MacBook yang tersedia apa saja?"

if col3.button("📍 Alamat Toko"):
    st.session_state.quick_msg = "Alamat toko CONNECT.GADGET di mana?"

# ===========================
# TAMPILKAN CHAT HISTORY
# ===========================
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{chat['msg']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{chat['msg']}</div>", unsafe_allow_html=True)

# ===========================
# INPUT CHAT
# ===========================
user_input = st.chat_input("Ketik pesan...")

if "quick_msg" in st.session_state:
    user_input = st.session_state.quick_msg
    del st.session_state.quick_msg

# ===========================
# CHAT PROCESS
# ===========================
if user_input:
    # Simpan pesan user
    st.session_state.chat_history.append({"role": "user", "msg": user_input})

    # Typing indicator
    with st.spinner("CONNECT.GADGET sedang mengetik..."):
        reply = ask_gemini(user_input)

    # Balasan chatbot
    st.session_state.chat_history.append({"role": "bot", "msg": reply})

    st.rerun()