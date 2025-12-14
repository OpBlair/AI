from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
#allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "Chess AI backend is running...."

#--- API Route placeholder
@app.route('/api/test_connection', methods=['POST'])
def test_connection():
    #Receive full board state object from frontend.
    try:
        data = request.get_json()
        board_state = data.get('boardState')
        current_player = data.get('currentPlayer')

        if not board_state:
            return jsonify({
            	"Status": "error", 
            	"message": "Missing boardState in request"
            }), 400

        print(f"\n--- Received Data from Frontend ---")
        print(f"Current Player: {current_player}")
        print(f"Board State Keys (Sample): {list(board_state.keys())[:4]}...")
        print(f"--- End Received Data --- \n")

    except Exception as e:   
        app.logger.error(f"Error in test_coonection: {e}")
        return jsonify({"status": "error", "message": f"server error: {e}"}), 500

if __name__ == '__main__':
        print("Starting Flask Server on http://127.0.0.1:5000")
        app.run(debug=True, port=5000)
