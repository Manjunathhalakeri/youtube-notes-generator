import streamlit as st
from main import pipeline

st.set_page_config(
    page_title="🎙️ YouTube Hindi → English Notes Generator",
    layout="centered",
    page_icon="🎙️"
)

st.markdown(
    """
    <style>
    .main {background-color: #f5f6fa;}
    .stButton>button {background-color: #4F8BF9; color: white;}
    .stTextInput>div>div>input {background-color: #fffbe7;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📚 YouTube Hindi → English Notes Generator")
st.markdown(
    """
    Welcome! Paste a **YouTube video URL** (in Hindi) below and click **Generate Notes**.<br>
    This app will transcribe, translate, and summarize the video into clear, structured English notes.<br>
    <br>
    <span style="color: #4F8BF9;">Powered by OpenAI Whisper & GPT-4 Turbo</span>
    """,
    unsafe_allow_html=True,
)

url = st.text_input("🔗 Paste a YouTube Video URL (Hindi)", placeholder="e.g. https://youtu.be/yourvideo")

if st.button("🚀 Generate Notes") and url:
    with st.spinner("⏳ Processing your video... Please wait."):
        try:
            notes = pipeline(url)
            st.success("✅ Notes generated!")
            st.markdown("### ✍️ Your Notes:")
            st.markdown(notes)
            st.download_button(
                "📥 Download Notes as Markdown",
                data=notes,
                file_name="notes.md",
                mime="text/markdown"
            )
        except Exception as e:
            st.error(f"❌ Error: {e}")

st.markdown("---")
st.info(
    "🔒 **Your data is processed securely and not stored.**\n\n"
    "💡 *Tip: For best results, use clear audio and shorter videos.*"
)
