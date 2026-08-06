# ==========================
# SEARCH LOGIC (Clean & Fixed)
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
    student_name = "Not Specified"
    student_result = "Result Data Found"
    page_number = ""

    with st.spinner("Searching Student Record..."):
        for page in pages:
            text = page["text"]
            if roll in text:
                page_number = page['page']
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                
                for i in range(len(lines)):
                    if roll in lines[i]:
                        found = True
                        # Agli lines ko dhoond kar name aur result alag karne ka smart tareeqa
                        collected_lines = []
                        for j in range(i + 1, min(i + 5, len(lines))):
                            next_line = lines[j]
                            # Agar agli line mein koi aur 6-digit roll number ya page header aa jaye toh rok dein
                            if next_line.isdigit() and len(next_line) == 6:
                                break
                            collected_lines.append(next_line)
                        
                        if collected_lines:
                            # Pehli valid text line ko name maan lein jo digits par mushtamil na ho
                            for l in collected_lines:
                                if not any(char.isdigit() for char in l) and "PII" not in l and "PS" not in l:
                                    student_name = l
                                    break
                            
                            # Aakhri ya marks wali line ko result maan lein
                            student_result = " ".join(collected_lines[-2:]) if len(collected_lines) >= 2 else collected_lines[0]
                        break
                if found:
                    break

    # ==========================
    # DISPLAY SINGLE STUDENT RESULT
    # ==========================
    if found:
        st.success("✅ Student Record Found!")
        st.balloons()

        result_color = "red" if "FAIL" in student_result.upper() else "green"

        st.markdown(f"""
<div class="result-card">
<h3 style="text-align:center;color:#1565C0;margin-top:0;">📋 STUDENT RESULT CARD</h3>
<hr>
<p class="info-label">Roll Number</p>
<p class="info-value">{roll}</p>
<p class="info-label">Student Name</p>
<p class="info-value">{student_name}</p>
<p class="info-label">Marks / Status</p>
<p class="info-value" style="color:{result_color}; font-size: 26px;">{student_result}</p>
<p class="info-label">Gazette Reference</p>
<p class="info-value" style="font-size: 16px;">Page {page_number}</p>
</div>
""", unsafe_allow_html=True)

        share_message = f"""🎓 *BISE Gujranwala SSC part II First Annual Examination 2026*

👤 *Name:* {student_name}
🎫 *Roll Number:* {roll}
🏆 *Result / Marks:* {student_result}

🔍 Check result online:
{APP_URL}

Developed by Sir M. Farhan Iqbal"""

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
        st.info("Ensure the roll number is 6 digits long and belongs to the current SSC 2026 examination.")
