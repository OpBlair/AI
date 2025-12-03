#from flask import Flask, request, jsonify, send_from_directory
#import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from chess_engine import ChessEngine

# -----------------
# FLASK SETUP
# -----------------
app = Flask(__name__)
# IMPORTANT: Allows your frontend (running on a different port/origin) to talk to this backend
CORS(app) 

# Initialize the Chess Engine
engine = ChessEngine()

# -----------------
# API ENDPOINTS
# -----------------

@app.route('/api/state', methods=['GET'])
def get_initial_state():
    """Returns the current board state and turn."""
    return jsonify({
        'boardState': engine.board_state,
        'currentPlayer': engine.current_player
    })

@app.route('/api/move', methods=['POST'])
def make_move():
    """
    Handles a move request from the frontend (human player).
    Expects JSON: {'from': 'a2', 'to': 'a4'}
    """
    data = request.get_json()
    from_sq = data.get('from')
    to_sq = data.get('to')

    if not from_sq or not to_sq:
        return jsonify({'error': 'Missing move coordinates'}), 400

    try:
        # The frontend does basic validation, but the backend must do the final, authoritative check
        if engine.move(from_sq, to_sq):
            # Check for game end conditions (placeholder for now)
            game_over = False # TODO: Implement check/checkmate/stalemate logic
            
            return jsonify({
                'success': True,
                'boardState': engine.board_state,
                'currentPlayer': engine.current_player,
                'gameOver': game_over
            })
        else:
            return jsonify({'success': False, 'error': 'Illegal move according to backend rules'}), 403

    except Exception as e:
        # Catch any internal errors (e.g., trying to move a non-existent piece)
        return jsonify({'error': str(e)}), 500


# Endpoint for Human vs. Computer mode - this is where the AI logic will be called
@app.route('/api/ai_move', methods=['POST'])
def get_ai_move():
    """
    1. Check if it's the AI's turn.
    2. Calls the AI logic (Minimax/Alpha-Beta).
    3. Executes the best move found.
    """
    # TODO: Implement AI logic (Minimax/Alpha-Beta) here!
    
    if engine.current_player != engine.ai_color:
         return jsonify({'error': "It is not the AI's turn"}), 400

    # --- Minimax Placeholder ---
    # Example: best_move = engine.find_best_move() 
    # For now, let's return a simple placeholder error or a random move once you have move gen.
    
    # For initial testing, just return the current state and a message
    return jsonify({
        'success': False, 
        'message': 'AI logic not yet implemented. This endpoint is a placeholder.',
        'boardState': engine.board_state
    })


if __name__ == '__main__':
    # Use a specific port to avoid conflict with frontend (e.g., React/Vue/Svelte on 3000/5173)
    app.run(debug=True, port=5000)
