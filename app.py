import streamlit as st
import json
import urllib.parse

# ==========================
# APP SETTINGS
# ==========================

APP_URL = "https://bise-grw-result-2026-wbhibjmejwpopvc6mjf9yf.streamlit.app"
st.set_page_config(
    page_title="BISE Gujranwala SSC part II First Annual Result 2026",
    page_icon="🎓",
    layout="centered"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>
.main {
    padding-top: 10px;
}
.stButton>button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
    background-color: #1565C0;
    color: white;
    border: none;
}
.stButton>button:hover {
    background-color: #0D47A1;
    color: white;
}
.stTextInput input {
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
    letter-spacing: 2px;
    font-weight: bold;
}
.result-card {
    background: #F8FAFC;
    border: 2px solid #2196F3;
    border-radius: 15px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0px 8px 24px rgba(0,0,0,0.1);
}
.info-label {
    color: #64748b;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: -10px;
}
.info-value {
    font-size: 22px;
    font-weight: bold;
    color: #1e293b;
    margin-bottom: 15px;
}
.footer {
    text-align: center;
    color: #666;
    margin-top: 40px;
    font-size: 14px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# HEADER & LOGO
# ==========================

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/en/2/23/Board_of_Intermediate_and_Secondary_Education%2C_Gujranwala.png", use_container_width=True)

st.markdown("<h3 style='text-align: center; color: #1e293b; margin-top: -10px;'>SSC First Annual Examination 2025</h3>", unsafe_allow_html=True)

# ==========================
# LOAD INDEX
# ==========================

@st.cache_data(show_spinner=False)
def load_index():
    with open("index.json", "r", encoding="utf-8") as f:
        return json.load(f)

try:
    with st.spinner("Initializing Database..."):
        pages = load_index()
except Exception as e:
    st.error(f"Unable to load index.json\n\n{e}")
    st.stop()

# ==========================
# SEARCH SECTION
# ==========================

st.divider()

roll = st.text_input(
    "🔢 Enter your 6-Digit Roll Number below",
    max_chars=6,
    placeholder="e.g. 531214"
)

search_btn = st.button("🔍 Search Result")

# ==========================
# SEARCH LOGIC
# ==========================

if search_btn:
    roll = roll.strip()

    if not roll:
        st.warning("Please enter your Roll Number.")
        st.stop()

    if not (roll.isdigit() and len(roll) == 6):
        st.error("Invalid input. Please enter exactly 6 digits.")
        st.stop()

    found = False
    student_name = ""
    student_result = ""
    page_number = ""

    with st.spinner("Searching Result..."):
        for page in pages:
            lines = [
                line.strip()
                for line in page["text"].splitlines()
                if line.strip()
            ]

            for i in range(len(lines) - 2):
                if lines[i] == roll:
                    student_name = lines[i + 1]
                    student_result = lines[i + 2]
                    page_number = page['page']
                    found = True
                    break

            if found:
                break

    # ==========================
    # DISPLAY RESULT
    # ==========================
    if found:
        st.success("✅ Result retrieved successfully!")
        st.balloons()

        result_color = "red" if "FAIL" in student_result.upper() else "green"

        # Note: Absolutely NO spaces before the HTML tags here to prevent Markdown code-block rendering
        st.markdown(f"""
<div class="result-card">
<h3 style="text-align:center;color:#1565C0;margin-top:0;">📋 OFFICIAL RESULT</h3>
<hr>
<p class="info-label">Student Name</p>
<p class="info-value">{student_name}</p>
<p class="info-label">Roll Number</p>
<p class="info-value">{roll}</p>
<p class="info-label">Marks / Status</p>
<p class="info-value" style="color:{result_color}; font-size: 28px;">{student_result}</p>
<p class="info-label">Gazette Reference</p>
<p class="info-value" style="font-size: 16px;">Page {page_number}</p>
</div>
""", unsafe_allow_html=True)

        # ==========================
        # SHARE & COPY RESULT
        # ==========================
        st.markdown("<br>", unsafe_allow_html=True)
        share_message = f"""🎓 *BISE Gujranwala SSC First Annual Examination 2025*

👤 *Name:* {student_name}
🎫 *Roll Number:* {roll}
🏆 *Result:* {student_result}

🔍 Check your result online:
{APP_URL}

Developed by M. Farhan Iqbal"""

        whatsapp_url = "https://wa.me/?text=" + urllib.parse.quote(share_message)

        st.link_button(
            "📤 Share on WhatsApp",
            whatsapp_url,
            use_container_width=True
        )

        with st.expander("📋 Copy Result Text"):
            st.code(share_message, language="markdown")

    else:
        st.error("❌ No record found for this Roll Number.")
        st.info("Ensure the roll number is 6 digits long and belongs to the current SSC 2025 examination.")

# ==========================
# FOOTER
# ==========================

st.divider()

st.markdown("""
<div class="footer">
<p><strong>👨‍💻 Developed by M. Farhan Iqbal</strong></p>
<p>We wish every student success in their future endeavors. ❤️</p>
<p style="font-size: 12px; color: #999;">
⚠️ Disclaimer: This is an unofficial result search tool based on the published gazette. 
Please verify your result from the official BISE Gujranwala records if required.
</p>
</div>
""", unsafe_allow_html=True)
