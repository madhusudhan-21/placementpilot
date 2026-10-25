import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    # Detect key from GEMINI_API_KEY or OPENAI_API_KEY
    key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not key or not key.strip():
        raise ValueError(
            "No API key found in .env! Please add GEMINI_API_KEY or OPENAI_API_KEY to your .env file."
        )
    return key.strip()

def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior technical hiring manager and career mentor.

Evaluate the following resume specifically against the candidate's target career goal.

Target Goal: "{user_goal}"

STRICT INSTRUCTIONS:
1. Extract existing skills from the resume that are strictly relevant to the target goal.
2. Identify missing skills / critical skill gaps needed to succeed in this target role.
3. Generate a structured step-by-step roadmap for mastering the missing skills.
4. Generate realistic technical interview questions tailored to this role and candidate background.

You MUST respond strictly with valid JSON using this schema:
{{
  "skills": ["string"],
  "missing_skills": ["string"],
  "roadmap": ["string"],
  "interview_questions": ["string"]
}}

Candidate Resume:
\"\"\"
{resume_text}
\"\"\"
"""
    try:
        api_key = get_api_key()

        # Preferred model list for fast and reliable resume analysis
        configured_model = os.getenv("GEMINI_MODEL")
        candidate_models = [configured_model] if configured_model else ["gemini-flash-lite-latest", "gemini-3.5-flash-lite", "gemini-3.8-flash"]

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        }

        last_error = None
        for model in candidate_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )

                with urllib.request.urlopen(req, timeout=45) as response:
                    result_data = json.loads(response.read().decode("utf-8"))

                parts = result_data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                raw_text = "".join(part.get("text", "") for part in parts if "text" in part).strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                if raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                raw_text = raw_text.strip()
                data = json.loads(raw_text)

                return {
                    "skills": data.get("skills", []),
                    "missing_skills": data.get("missing_skills", []),
                    "roadmap": data.get("roadmap", data.get("Roadmap", [])),
                    "interview_questions": data.get("interview_questions", [])
                }
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8") if e.fp else str(e)
                # If model not found or deprecated, try next candidate model
                if e.code == 404:
                    last_error = e
                    continue
                raise e
            except Exception as e:
                last_error = e
                continue

        if last_error:
            raise last_error

        # Standardize return keys to avoid case mismatch
        return {
            "skills": data.get("skills", []),
            "missing_skills": data.get("missing_skills", []),
            "roadmap": data.get("roadmap", data.get("Roadmap", [])),
            "interview_questions": data.get("interview_questions", [])
        }

    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else str(e)
        if e.code == 400 and ("API_KEY_INVALID" in err_body or "API key not valid" in err_body):
            friendly_err = "Invalid API Key: Please verify the API key in your .env file."
        elif e.code == 429:
            friendly_err = "Gemini Rate Limit: Too many requests. Please wait a moment and try again."
        else:
            friendly_err = f"Gemini API Error (HTTP {e.code}): {err_body}"

        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": friendly_err
        }

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": f"AI Analysis Error: {str(e)}"
        }