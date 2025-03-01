from google import genai

client = genai.Client(api_key="AIzaSyBP1BPnpQtA60YJ1dbVYC7RGfQv2_LmPz8")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works"
)
print(response.text)