import google.generativeai as genai
import os

# Configure your API key
genai.configure(api_key=os.environ["AIzaSyCoIPZ4KX8FgI5sw1EP-I-HIiXzQ3_r8jI"])

# Define the generation configuration
generation_config = {
  "temperature": 0.5,  # Adjust this value based on your needs
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024,
  "response_mime_type": "application/json", # Highly recommended for quiz apps
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

response = model.generate_content("Generate 5 multiple choice questions about history.")
print(response.text)
