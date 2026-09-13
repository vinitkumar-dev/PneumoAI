import os

import google.generativeai as genai

_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if _GEMINI_API_KEY:
    genai.configure(api_key=_GEMINI_API_KEY)

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = genai.GenerativeModel("gemini-2.5-flash")
    return _model


def ask_ai(prediction, question):

    if not _GEMINI_API_KEY:
        return (
            "The AI assistant is not configured on this server. "
            "Please set the GEMINI_API_KEY environment variable."
        )

    prompt = f"""You are an experienced pulmonologist. Patient Information

    Name:
    {prediction.patient_name}

    Age:
    {prediction.patient_age}

    Gender:
    {prediction.patient_gender}

    Symptoms:
    {prediction.clinical_notes}

    Prediction:
    {prediction.prediction}

    Confidence:
    {prediction.confidence} %

    Model:
    {prediction.model}

    Explanation:
    {prediction.explanation}

    Question:

    {question}

    Rules

    Never invent results.

    Use only given data.

    If unsure say "consult a doctor."

    Maximum 150 words.

    """

    try:
        response = _get_model().generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Unable to reach the AI assistant right now ({e})."
