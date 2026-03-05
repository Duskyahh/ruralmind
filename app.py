from flask import Flask, render_template, request, jsonify
from groq import Groq
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

client = Groq(api_key="GROQ_API_KEY")

SYSTEM_PROMPT = """
You are RuralMind, a helpful assistant for rural Indian users.
IMPORTANT: Always reply in English only, regardless of what language the question is in.
You only answer questions about:
1. Indian government schemes (PM Kisan, Ayushman Bharat, MGNREGA etc.)
2. Basic health symptoms and when to see a doctor
3. Farming advice and crop problems

Rules:
- Keep answers under 5 sentences
- Use very simple language
- Always be helpful and kind
- If question is unrelated, politely say you can only help with schemes, health and farming
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_question = data.get('question', '')

    if not user_question:
        return jsonify({'english': 'Please ask a question!', 'hindi': 'कृपया एक प्रश्न पूछें!'})

    # Get AI answer in English
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question}
        ]
    )
    english_answer = response.choices[0].message.content

    # Translate to Hindi
    hindi_answer = GoogleTranslator(source='auto', target='hi').translate(english_answer)

    return jsonify({
        'english': english_answer,
        'hindi': hindi_answer
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)