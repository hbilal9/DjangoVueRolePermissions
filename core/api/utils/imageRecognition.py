import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def gemini_detect_labels(image: Image):
    prompt = (
        "Here is product picture you have to analyze it and extract product name from it"
        "only return product name in string form"
    )

    response = model.generate_content([prompt, image])
    return response.text