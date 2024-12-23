from flask import Flask, jsonify, request
from flask_cors import CORS
import random

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow requests from React frontend

# Wrestler class definition
class Wrestlers:
    def __init__(self, name, weight, height, special_move, win_perc, main_title, ic_title, us_title, tag_title, nxt_title, money_in_the_bank, royal_rumble):
        self.name = name
        self.weight = weight
        self.height = height
        self.special_move = special_move
        self.win_perc = win_perc
        self.main_title = main_title
        self.ic_title = ic_title
        self.us_title = us_title
        self.tag_title = tag_title
        self.nxt_title = nxt_title
        self.money_in_the_bank = money_in_the_bank
        self.royal_rumble = royal_rumble
        

    def display_info(self):
        return {
            "name": self.name,
            "weight": self.weight,
            "height": self.height,
            "special_move": self.special_move,
            "win_perc": self.win_perc,
            "main_title": self.main_title,
            "ic_title": self.ic_title,
            "us_title": self.us_title,
            "tag_title": self.tag_title,
            "nxt_title": self.nxt_title,
            "money_in_the_bank": self.money_in_the_bank,
            "royal_rumble": self.royal_rumble,
        }

    def calculate_score(self):
        return (self.height * 0.1 +
                self.weight * 0.2 +
                self.win_perc * 0.5 +
                self.total_championships())

    def total_championships(self):
        return (self.main_title * 0.8 +
                self.ic_title * 0.4 +
                self.us_title * 0.4 +
                self.tag_title * 0.3 +
                self.nxt_title * 0.2 +
                self.money_in_the_bank * 0.6 +
                self.royal_rumble * 0.6)

    def update_record(self, won):
        if won:
            self.wins += 1
        else:
            self.losses += 1

    @staticmethod
    def simulate_match(wrestler1, wrestler2):
        score1 = wrestler1.calculate_score()
        score2 = wrestler2.calculate_score()

        adjusted_score1 = score1 * random.uniform(0.8, 1.2)
        adjusted_score2 = score2 * random.uniform(0.8, 1.2)

        return wrestler1 if adjusted_score1 > adjusted_score2 else wrestler2


# List of wrestlers
wrestlers = [
    Wrestlers("John Cena", 250, 6.1, "Attitude Adjustment", 85, 16, 5, 3, 2, 0, 1, 2),
    Wrestlers("The Rock", 260, 6.4, "Rock Bottom", 80, 10, 2, 0, 3, 0, 0, 1),
    Wrestlers("Stone Cold", 252, 6.2, "Stone Cold Stunner", 88, 6, 2, 1, 2, 0, 0, 3),
    Wrestlers("Undertaker", 309, 6.9, "Tombstone Piledriver", 90, 7, 0, 0, 4, 0, 0, 0),
    Wrestlers("Triple H", 255, 6.4, "Pedigree", 82, 14, 5, 0, 2, 1, 1, 0)
]

# API Endpoints

#Fetch wrestlers
@app.route('/api/wrestlers', methods=['GET'])
def get_wrestlers():
    """Get a list of all wrestlers."""
    return jsonify([wrestler.display_info() for wrestler in wrestlers])

#Fetch wrestler details
@app.route('/api/wrestlers/<int:wrestler_id>', methods=['GET'])
def get_wrestler(wrestler_id):
    """Get details of a specific wrestler."""
    if 0 <= wrestler_id < len(wrestlers):
        return jsonify(wrestlers[wrestler_id].get_info())
    return jsonify({"error": "Wrestler not found"}), 404

#Sim match
@app.route('/api/simulate', methods=['POST'])
def simulate_match():
    """Simulate a match between two wrestlers."""
    data = request.json
    try:
        id1 = int(data.get("wrestler1"))  # Get index
        id2 = int(data.get("wrestler2"))  
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid wrestler IDs"}), 400

    if not (0 <= id1 < len(wrestlers)) or not (0 <= id2 < len(wrestlers)):
        return jsonify({"error": "Wrestler IDs out of range"}), 400

    wrestler1 = wrestlers[id1] # Get wrestler from index
    wrestler2 = wrestlers[id2]

    winner = Wrestlers.simulate_match(wrestler1, wrestler2)
    return jsonify({"winner": winner.display_info()})



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
