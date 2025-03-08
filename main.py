from flask import Flask, request, jsonify
from LLModel import LLModel
from flask_cors import CORS

baseurl="https://bakingo.resoee.com/console2/"
customerID=52
class Chatbot:
    def __init__(self,baseurl=baseurl,customerID=customerID):
        self.bot = LLModel(baseurl,customerID)

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
