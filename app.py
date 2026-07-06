from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Tame generate kareli Gemini API Key ahi muko
GEMINI_API_KEY = "AQ.Ab8RN6J9HfNYYKActUygVnRBt7Q-a0327CNYTu0ed1Nq1FnzbQ" 
genai.configure(api_key=GEMINI_API_KEY)

# AI Model select karo
model = genai.GenerativeModel('gemini-1.5-flash')

# Aa line thi tamaro chatbot support agent ni jem vartase
system_instruction = "Tame ek helpful Customer Support Assistant chho. User na prashno na javab saral ane polite bhasha ma aapo."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_bot():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "Mane tamaro message na malyo."})
    
    try:
        # AI paase thi response levva mate
        full_prompt = f"{system_instruction}\nUser: {user_message}\nAssistant:"
        response = model.generate_content(full_prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"Error aavi: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)