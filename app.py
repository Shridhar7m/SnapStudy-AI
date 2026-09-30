import streamlit as st
import fitz
import time
from google import genai

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="SnapStudy AI",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.hero {
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    text-align: center;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

.hero p {
    font-size: 18px;
}

.card {
    padding: 22px;
    border-radius: 16px;
    background: white;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <h1>📚 SnapStudy AI</h1>
    <p>Your smart AI learning assistant</p>
    <div>Upload → Understand → Learn</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Gemini client
# -----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    client = None


# -----------------------------
# AI response function
# -----------------------------
def generate_ai_response(prompt):

    # Try models one by one
    models = [
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.6-flash"
    ]

    last_error = None

    for model in models:

        # Retry each model
        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    return response.text

            except Exception as e:

                last_error = e
                error_text = str(e)

                # Retry temporary server errors
                if "503" in error_text or "UNAVAILABLE" in error_text:

                    if attempt < 2:

                        wait_time = 2 ** attempt

                        time.sleep(wait_time)

                        continue

                    else:
                        break

                else:

                    raise e

    raise Exception(
        f"Gemini is temporarily unavailable. Please try again later. "
        f"Last error: {last_error}"
    )


# -----------------------------
# Upload section
# -----------------------------
st.markdown("### 📄 Upload Your Study Material")

uploaded_file = st.file_uploader(
    "Upload a PDF containing your study material",
    type=["pdf"]
)

if uploaded_file:

    # -------------------------
    # Extract PDF text
    # -------------------------
    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    page_count = len(pdf)

    pdf.close()

    # -------------------------
    # Check PDF
    # -------------------------
    if not text.strip():

        st.warning(
            "⚠️ No readable text was found in this PDF."
        )

    else:

        st.success(
            "✅ PDF uploaded successfully!"
        )

        st.session_state["pdf_text"] = text

        # ---------------------
        # Document information
        # ---------------------
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Pages",
                page_count
            )

        with col2:

            st.metric(
                "Characters",
                len(text)
            )

        with col3:

            st.metric(
                "Status",
                "Ready"
            )

        # ---------------------
        # AI tools
        # ---------------------
        st.markdown("### 🤖 AI Study Tools")

        col1, col2, col3 = st.columns(3)

        # =================================================
        # SUMMARY
        # =================================================
        with col1:

            if st.button(
                "📝 Summarize PDF",
                use_container_width=True
            ):

                if client is None:

                    st.error(
                        "Gemini API is not configured."
                    )

                else:

                    with st.spinner(
                        "Creating your summary..."
                    ):

                        prompt = f"""
You are an AI study assistant.

Summarize the following study material
in simple and easy English.

Use:

- Important concepts
- Short explanations
- Bullet points
- Key takeaways

Do not add information that is not
present in the study material.

Study material:

{text[:30000]}
"""

                        try:

                            summary = generate_ai_response(
                                prompt
                            )

                            st.session_state[
                                "summary"
                            ] = summary

                        except Exception as e:

                            st.error(
                                f"AI Error: {e}"
                            )

        # =================================================
        # QUIZ
        # =================================================
        with col2:

            if st.button(
                "🧠 Generate Quiz",
                use_container_width=True
            ):

                if client is None:

                    st.error(
                        "Gemini API is not configured."
                    )

                else:

                    with st.spinner(
                        "Generating quiz..."
                    ):

                        prompt = f"""
Create 5 multiple-choice questions
from the following study material.

For each question provide:

1. Question
2. Four options: A, B, C, D
3. Correct answer
4. Short explanation

Use only information from the
study material.

Study material:

{text[:30000]}
"""

                        try:

                            quiz = generate_ai_response(
                                prompt
                            )

                            st.session_state[
                                "quiz"
                            ] = quiz

                        except Exception as e:

                            st.error(
                                f"AI Error: {e}"
                            )

        # =================================================
        # ASK AI
        # =================================================
        with col3:

            if st.button(
                "💬 Ask AI",
                use_container_width=True
            ):

                st.session_state[
                    "show_chat"
                ] = True

        # =================================================
        # SUMMARY OUTPUT
        # =================================================
        if "summary" in st.session_state:

            st.markdown(
                "### 📝 AI Summary"
            )

            st.success(
                st.session_state["summary"]
            )

        # =================================================
        # QUIZ OUTPUT
        # =================================================
        if "quiz" in st.session_state:

            st.markdown(
                "### 🧠 AI Generated Quiz"
            )

            st.info(
                st.session_state["quiz"]
            )

        # =================================================
        # ASK AI SECTION
        # =================================================
        if st.session_state.get(
            "show_chat",
            False
        ):

            st.markdown(
                "### 💬 Ask SnapStudy AI"
            )

            question = st.text_input(
                "Ask a question about your PDF"
            )

            if st.button(
                "Get answer",
                use_container_width=True
            ):

                if not question:

                    st.warning(
                        "Please enter a question."
                    )

                elif client is None:

                    st.error(
                        "Gemini API is not configured."
                    )

                else:

                    with st.spinner(
                        "Thinking..."
                    ):

                        prompt = f"""
You are a helpful study assistant.

Answer the user's question using
only the information in the study material.

If the answer is not available,
say:

"I could not find this information
in the uploaded PDF."

Study material:

{text[:30000]}

Question:

{question}
"""

                        try:

                            answer = generate_ai_response(
                                prompt
                            )

                            st.markdown(
                                "### 🤖 Answer"
                            )

                            st.success(
                                answer
                            )

                        except Exception as e:

                            st.error(
                                f"AI Error: {e}"
                            )

        # =================================================
        # ORIGINAL DOCUMENT
        # =================================================
        with st.expander(
            "📖 View Extracted PDF Text"
        ):

            st.text_area(
                "Document content",
                text,
                height=400
            )

else:

    # -------------------------
    # Welcome section
    # -------------------------

    st.markdown(
        "### 🚀 What can SnapStudy AI do?"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            "📄 Upload Study Material\n\n"
            "Upload your PDF notes or textbook."
        )

        st.info(
            "📝 AI Summarization\n\n"
            "Get simple explanations and important points."
        )

    with col2:

        st.info(
            "💬 Ask Questions\n\n"
            "Ask questions directly from your PDF."
        )

        st.info(
            "🧠 Generate Quizzes\n\n"
            "Practice your knowledge with AI-generated questions."
        )

    st.success(
        "💡 Upload a PDF above to start learning with SnapStudy AI."
    )