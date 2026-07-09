class prompts:
    def interview_prompt(resume_text: str, job_description: str) -> str:
        return f"""
    You are an expert technical interviewer and ATS system evaluator.

    Analyze the resume against the job description and return a strict JSON response only.
    No markdown, no explanation, no extra text, no trailing commas — only valid JSON.
    ...

    Output format:
    {{
      "ats_score": <integer 0-100>,
      "ats_feedback": "<2-3 sentence explanation of the score>",
      "mcq": [
        {{
          "question": "<technical question based on JD skills>",
          "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
          "answer": "<correct option letter>"
        }}
      ],
      "coding_questions": [
        {{
          "title": "<short title>",
          "description": "<clear problem statement>",
          "difficulty": "<Easy | Medium | Hard>"
        }}
      ],
      "interview_round": [
        {{
          "question": "<behavioral or technical interview question>",
          "expected_answer": "<key points the candidate should cover>"
        }}
      ]
    }}

    Rules:
    - Generate exactly 5 MCQs based on skills in the job description
    - Generate exactly 3 coding questions relevant to the role
    - Generate exactly 5 interview questions (mix of technical and behavioral)
    - ATS score should reflect keyword match, skills alignment, and experience relevance
    - Be specific to the resume and JD provided, not generic

    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """