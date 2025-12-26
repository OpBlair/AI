from flask import Flask, request, jsonify
from flask_cors import CORS
from chessEngine import ChessEngine

app = Flask(__name__)
#allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def home():
    return "Chess AI backend is running...."

#--- API Route placeholder
@app.route('/api/ai_move', methods=['POST', 'OPTIONS'])
def get_ai_move():
    #Receive full board state object from frontend, calculates AI move and returns it.
    if request.method == 'OPTIONS':
    	return '', 200

    try:
        data = request.get_json()
        board_state = data.get('boardState')
     
        if not board_state:
            return jsonify({
            	"Status": "error", 
            	"message": "Missing boardState in request"
            }), 400

        AI_COLOR = 'b'

        #initialize the Engine
        engine = ChessEngine(board_state)

        #Calculate the Best move using Minimax
        from_sq, to_sq = engine.find_best_move(ai_color=AI_COLOR)
        
        if from_sq and to_sq:
        	#Return the move coordinates to the frontend
        
            white_in_check = engine.is_in_check('w')
            black_in_check = engine.is_in_check('b')
            
            return jsonify({
        		"status": "move_found",
        		"from_square": from_sq,
        		"to_square": to_sq,
        		"piece_code": engine.board.get(from_sq),
                "isWhiteInCheck": white_in_check,
                "isBlackInCheck": black_in_check,
        		"message": f"AI played: {from_sq} to {to_sq}"
        	}), 200

        else:
        	return jsonify({
        		"Status": "game_over",
        		"message": "AI found no legal moves."
        	}), 200

    except Exception as e:   
        app.logger.error(f"Error in get_ai_move: {e}")
        return jsonify({"status": "error", "message": f"server error: {e}"}), 500

if __name__ == '__main__':
        print("Starting Flask Server on http://127.0.0.1:5000")
        app.run(debug=True, port=5000)
