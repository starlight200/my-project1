from flask import Flask, request, jsonify
from bot import CDPChatbot #replace your_chatbot_file

app = Flask(__name__)
chatbot = CDPChatbot()

@app.route('/ask', methods=['POST'])
def ask_chatbot():
    data = request.get_json()
    question = data.get('question')
    if question:
        answer = chatbot.answer_question(question)
        return jsonify({'answer': answer})
    else:
        return jsonify({'error': 'No question provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)