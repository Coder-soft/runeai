
import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyDFMewub97IEuO9wSRVzkPSsWlHM4r5tkk")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)