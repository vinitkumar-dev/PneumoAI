import os

import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_ai(prediction, question):

    prompt=f"""You are an experienced pulmonologist.Patient Information

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

    response=model.generate_content(prompt)

    return response.text