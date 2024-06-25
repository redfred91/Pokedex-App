from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import cv2
import numpy as np
import json

app = Flask(__name__)
CORS(app)

def query_card_database(card_name):
    conn = sqlite3.connect('pokemon_cards.db')
    c = conn.cursor()
    query = """
    SELECT cards.id, cards.name, cards.rarity, cards.artist, cards.images, sets.name as set_name
    FROM cards
    JOIN sets ON cards.id LIKE sets.id || '%'
    WHERE cards.name LIKE ?
    """
    c.execute(query, ('%' + card_name + '%',))
    cards = c.fetchall()
    conn.close()
    return cards

@app.route('/')
def index():
    return "Flask server is running. Try accessing /api/cards endpoint."

@app.route('/api/card', methods=['POST'])
def get_card_info():
    file = request.files['image']
    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # Placeholder for image processing logic
    card_name = "Pikachu"  # Replace this with actual image processing result

    cards = query_card_database(card_name)
    if cards:
        return jsonify([{
            "id": card[0],
            "name": card[1],
            "rarity": card[2],
            "artist": card[3],
            "images": json.loads(card[4]),
            "set_name": card[5]
        } for card in cards])
    else:
        return jsonify({"message": "Card not found"}), 404

@app.route('/api/cards', methods=['GET'])
def get_cards():
    name_query = request.args.get('name', '')
    cards = query_card_database(name_query)
    return jsonify([{
        "id": card[0],
        "name": card[1],
        "rarity": card[2],
        "artist": card[3],
        "images": json.loads(card[4]),
        "set_name": card[5]
    } for card in cards])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
