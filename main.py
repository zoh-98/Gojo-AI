from flask import Flask, request, jsonify
from characterai import PyCAI

app = Flask(__name__)

client = PyCAI('bb27dbf32c4d80e8043ff0248bc389212aed808f')

@app.route('/api/send_message', methods=['POST'])
def send_message():
    char_id = request.args.get('char_id')  # Get char_id from the query parameter
    if not char_id:
        return jsonify({"error": "char_id is required in the query parameter"}), 400

    # Use char_id to get chat information
    chat = client.chat.get_chat(char_id)
    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    data = request.json
    message = data['message']

    response = client.chat.send_message(chat['external_id'], tgt, message)

    name = response['src_char']['participant']['name']
    text = response['replies'][0]['text']

    return jsonify({"name": name, "text": text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
