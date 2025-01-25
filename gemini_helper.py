import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_image(image_path):
    prompt = """
    Analyze this image in detail. Describe:
    1. Main elements and their relationships
    2. Colors and mood conveyed
    3. Potential story themes
    4. Unusual or interesting details
    5. Cultural/historical context if any
    
    Be descriptive yet concise. Focus on elements that could inspire children's stories.
    """
    # Upload image to Gemini
    image = genai.upload_file(image_path)
    response = model.generate_content([prompt, image])
    return response.text



def generate_story(image_description, genre):
    prompt = f"""
    Based on this image analysis: {image_description}
    
    Create a {genre} children's story (~200 words) with:
    1. Playful language suitable for ages 5-8
    2. A positive moral lesson
    3. Magical/fantasy elements (if applicable to the genre)
    4. Opportunities for parent-child interaction through fun narration
    
    Format the story with short paragraphs and emoji illustrations. Do not include any choices or questions for the reader. The story should flow smoothly without interruptions.
    """
    response = model.generate_content(prompt)
    return response.text
