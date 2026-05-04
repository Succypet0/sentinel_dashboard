import streamlit as st
import requests

# --- CONFIGURATION ---
# Your actual n8n Webhook Test URL
WEBHOOK_URL = "https://succypet09.app.n8n.cloud/webhook/sentinel-alert"

# --- UI DESIGN ---
st.set_page_config(page_title="Professor's Dashboard", page_icon="📝", layout="centered")

st.title("📝 Sentinel: Professor's Pad")

# --- INTRODUCTORY SECTION ---
st.markdown("""
### The Problem
Every year, universities lose countless students because early warning signs—like a missed assignment, a failed quiz, or sudden absences—are caught too late. Traditional intervention is reactive, slow, and often lacks human empathy. **Sentinel changes this.** It is a proactive orchestration engine that detects at-risk students in real-time and immediately deploys a personalised, empathetic AI adviser to help them get back on track before they fail.

### The Professor's Pad
This dashboard acts as the 'eyes and ears' of the Sentinel system. It symbolises a university's existing Learning Management System (LMS) or gradebook. When a professor logs raw academic data here, it is instantly routed to Sentinel's hidden AI brain, which calculates a proprietary Risk Score and autonomously triggers the appropriate intervention.
""")

# --- TELEGRAM SETUP INSTRUCTIONS ---
st.info("""
**🚨 CRITICAL: READ BEFORE TESTING 🚨**

To experience the live AI intervention, you must connect your Telegram account to the Sentinel system before submitting any data below.

1. Open **Telegram** on your phone or computer.
2. Click the button below to go directly to the bot, OR go to the search bar and type the username: **`@Sentinel_0027_bot`**
3. Hit the **Start** button at the bottom of the chat.
4. Send a quick message introducing yourself to the bot (e.g., *'Hi, my name is Alex'*). Sentinel's onboarding agent will save your profile.
5. **Return to this page** and enter that *exact same name* in the 'Student Name' box below to trigger the live intervention test.
""")

# --- NEW TELEGRAM BUTTON ---
st.link_button("📱 Open Sentinel Telegram Bot", "https://t.me/Sentinel_0027_bot", type="secondary")

st.divider()

# --- INPUT FORM ---
st.subheader("Student Data Entry")
st.write("Log student performance metrics below. Sentinel's central rules engine will autonomously evaluate if an intervention is required.")

# Text inputs with placeholders and NO default values
student_name = st.text_input("Student Name", value="", placeholder="e.g., Amina Bello")
subject = st.text_input("Course/Subject", value="", placeholder="e.g., PHY101 - Mechanics")

# Number inputs laid out in columns for a professional dashboard look
col1, col2, col3 = st.columns(3)
with col1:
    exam_score = st.number_input("Latest Exam Score (%)", min_value=0, max_value=100, value=None, placeholder="e.g., 45")
with col2:
    absences = st.number_input("Consecutive Absences", min_value=0, value=None, placeholder="e.g., 3")
with col3:
    missing_assignments = st.number_input("Missing Assignments", min_value=0, value=None, placeholder="e.g., 2")

teacher_observation = st.text_area("Teacher's Observation", value="", placeholder="e.g., Amina has been looking exhausted in class and failing to participate.")

# --- THE TRIGGER BUTTON ---
if st.button("Submit to Sentinel Database", type="primary"):

    # Basic safety check to ensure the teacher at least typed a name
    if not student_name:
        st.warning("⚠️ Please enter a Student Name before submitting.")
    else:
        st.info("Transmitting data to n8n Orchestration Engine...")

        # Package the data for n8n. If a number box is left empty, we safely default it to passing metrics so n8n maths does not break.
        payload = {
            "name": student_name,
            "subject": subject,
            "exam_score": exam_score if exam_score is not None else 100,
            "absences": absences if absences is not None else 0,
            "missing_assignments": missing_assignments if missing_assignments is not None else 0,
            "teacher_observation": teacher_observation
        }

        # Send the HTTP POST request to the n8n Webhook
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                # --- MODIFIED SECTION: Outputs the direct reply from n8n ---
                try:
                    # Attempt to display the webhook response as a formatted JSON block
                    st.json(response.json())
                except ValueError:
                    # Fallback to plain text if the webhook doesn't send JSON back
                    st.write(response.text)
            else:
                st.warning(f"Connection failed. n8n status code: {response.status_code}")
        except Exception as e:
            st.warning(f"Could not reach n8n. Error: {e}")