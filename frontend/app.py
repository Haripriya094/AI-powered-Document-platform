import streamlit as st
from auth import api_login, api_register, api_logout, api_analyze

# ── session state ─────────────────────────────────────────────
for key, default in {"token": None, "user": None, "user_id": None, "result": None}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def show_auth():
    st.title("AI Resume Analyzer")
    st.divider()

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True):
            if not username or not password:
                st.warning("Fill in all fields.")
            else:
                resp = api_login(username, password)
                data = resp.json()
                if data["status"] == "success":
                    st.session_state.token = data["data"]["user_id"]
                    st.session_state.user = data["data"]["username"]
                    st.session_state.user_id = data["data"]["user_id"]
                    st.rerun()
                else:
                    st.error(data["message"])

    with tab2:
        st.subheader("Register")
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register", use_container_width=True):
            if not username or not email or not password:
                st.warning("Fill in all fields.")
            else:
                resp = api_register(username, email, password)
                data = resp.json()
                if data["status"] == "success":
                    st.success(f"{data['message']} — Please login.")
                else:
                    st.error(data["message"])


def show_results(result):
    # ATS Score
    st.divider()
    st.subheader("ATS Score")
    st.metric("Score", f"{result['ats_score']} / 100")
    st.info(result["ats_feedback"])

    # MCQ
    st.divider()
    st.subheader("MCQ Questions")
    for i, mcq in enumerate(result["mcq"], 1):
        with st.expander(f"Q{i}: {mcq['question']}"):
            for opt in mcq["options"]:
                st.write(opt)
            user_answer = st.radio(
                "Your Answer:",
                options=["A", "B", "C", "D"],
                index=None,
                key=f"mcq_{i}"
            )
            if user_answer:
                if user_answer == mcq["answer"]:
                    st.success(f"Correct! Answer: {mcq['answer']}")
                else:
                    st.error(f"Wrong! Correct Answer: {mcq['answer']}")

    # Coding Questions
    st.divider()
    st.subheader("Coding Questions")
    for i, cq in enumerate(result["coding_questions"], 1):
        with st.expander(f"Q{i}: {cq['title']} — {cq['difficulty']}"):
            st.write(cq["description"])

    # Interview Round
    st.divider()
    st.subheader("Interview Round")
    for i, iq in enumerate(result["interview_round"], 1):
        with st.expander(f"Q{i}: {iq['question']}"):
            st.write(f"Expected Answer: {iq['expected_answer']}")


def show_dashboard():
    with st.sidebar:
        st.markdown(f"### {st.session_state.user}")
        st.caption(f"ID: {st.session_state.user_id}")
        st.divider()
        if st.button("Logout", use_container_width=True):
            resp = api_logout(st.session_state.user)
            data = resp.json()
            if data["status"] == "success":
                st.session_state.token = None
                st.session_state.user = None
                st.session_state.user_id = None
                st.session_state.result = None
                st.rerun()

    st.title("AI Resume Analyzer")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    with col2:
        jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

    if st.button("Analyze", use_container_width=True):
        if not resume_file or not jd_file:
            st.warning("Upload both Resume and Job Description PDFs.")
        else:
            with st.spinner("Analyzing..."):
                resp = api_analyze(resume_file, jd_file,st.session_state.user_id)
                data = resp.json()
            if data["status"] == "success":
                st.session_state.result = data["data"]
            else:
                st.error(data["message"])

    # ── display persisted results ──
    if st.session_state.result:
        show_results(st.session_state.result)


# ── router ────────────────────────────────────────────────────
if st.session_state.token:
    show_dashboard()
else:
    show_auth()