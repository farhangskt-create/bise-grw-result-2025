import streamlit as st
import json
import fitz  # PyMuPDF
from PIL import Image
import io
import urllib.parse

st.set_page_config(page_title="BISE Gujranwala SSC part II First Annual Result 2026", page_icon="🎓", layout="centered")

st.markdown("""
<style>
.main { padding-top: 10px; }
.stButton>button { width: 100%; height: 50px; border-radius: 12px; font-size: 18px; font-weight: bold; background-color: #1565C0; color: white; border: none; }
.stButton>button:hover { background-color: #0D47A1; color: white; }
.stTextInput input { border-radius: 10px; text-align: center; font-size: 20px; letter-spacing: 2px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 BISE Gujranwala Result Portal")
st.markdown("Enter your Roll Number to instantly check your board result details.")

@st.cache_data
def load_data():
    with open("gazette_index.json", "r", encoding="utf-8") as f:
        return json.load(f)

records = load_data()

roll_input = st.text_input("Enter Roll Number:")

if st.button("Search Result"):
    match = next((r for r in records if r["roll_num"] == roll_input.strip()), None)
    
    if match:
        st.success("Result Found Successfully!")
        
        st.markdown("### 📋 Student Result Details")
        st.markdown(f"**Roll Number:** {match['roll_num']}")
        st.markdown(f"**Student Name:** {match['name']}")
        
        # Render the exact row snippet image directly from the PDF page
        doc = fitz.open("gazette.pdf")
        page = doc[match["page"]]
        rect = fitz.Rect(match["bbox"])
        
        pix = page.get_pixmap(clip=rect, dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        
        st.markdown("#### 📄 Official Gazette Row Snippet:")
        st.image(img, use_container_width=True)
        
        # WhatsApp Share Button
        whatsapp_text = f"BISE Gujranwala Result 2026\nRoll Number: {match['roll_num']}\nName: {match['name']}"
        encoded_text = urllib.parse.quote(whatsapp_text)
        whatsapp_url = f"https://api.whatsapp.com/send?text={encoded_text}"
        
        st.markdown(
            f'<br><a href="{whatsapp_url}" target="_blank"><button style="width: 100%; height: 50px; background-color: #25D366; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer;">Share on WhatsApp 📱</button></a>',
            unsafe_allow_html=True
        )
    else:
        st.error("No record found for this roll number. Please double check.")
