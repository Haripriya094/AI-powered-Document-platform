import requests

API_BASE = "http://127.0.0.1:8015"

def api_login(username, password):
    return requests.post(f"{API_BASE}/login", json={"username": username, "password": password})

def api_register(username, email, password):
    return requests.post(f"{API_BASE}/register", json={"username": username, "email": email, "password": password})

def api_logout(username):
    return requests.post(f"{API_BASE}/logout", json={"username": username})

def api_analyze(resume_file, jd_file, user_id):
    return requests.post(
        f"{API_BASE}/interview_analyze",
        files={
            "resume": (resume_file.name, resume_file.getvalue(), "application/pdf"),
            "job_description": (jd_file.name, jd_file.getvalue(), "application/pdf")
        },
        data={"user_id": user_id}      # ← pass user_id as form field
    )