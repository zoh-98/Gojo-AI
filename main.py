from flask import Flask, request, jsonify
import os
from characterai import PyCAI

app = Flask(__name__)

client = PyCAI(os.environ['CLIENT'])
char = os.environ['CHAR']
chat = client.chat.get_chat(char)
participants = chat['participants']

if not participants[0]['is_human']:
    tgt = participants[0]['user']['username']
else:
    tgt = participants[1]['user']['username']

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data['message']

    response = client.chat.send_message(chat['external_id'], tgt, message)

    name = response['src_char']['participant']['name']
    text = response['replies'][0]['text']

    return jsonify({"name": name, "text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
