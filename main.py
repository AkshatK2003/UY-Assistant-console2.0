from flask import Flask, request, jsonify
from LLModel import LLModel
from flask_cors import CORS

baseurl="http://localhost:3000/console2/"
class Chatbot:
    def __init__(self,baseurl=baseurl):
        self.bot = LLModel(baseurl)

    def generate(self, query):
        res = self.bot.generate(query)
        return res

app = Flask(__name__)
CORS(app)
chatbot_instance = Chatbot(baseurl)

@app.route('/generate', methods=['POST'])
def generate_response():
    data = request.get_json()
    if 'query' not in data:
        return jsonify({'error': 'Missing query parameter'}), 400
    
    query = data['query']
    response = chatbot_instance.generate(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
