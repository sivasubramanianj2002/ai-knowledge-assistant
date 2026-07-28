from google import genai

from app.core.config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(context, question):

    prompt = f"""

You are an AI onboarding assistant.

Answer only using the given context.

Context:

{context}


Question:

{question}


If the answer is not available,
say "I don't have information about this."

"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )


    return response.text