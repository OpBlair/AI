# Constants used by the frontend (piece codes and starting state)
INITIAL_BOARD_STATE = {
    'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br',
    'a7': 'bp', 'b7': 'bp', 'c7': 'bp', 'd7': 'bp', 'e7': 'bp', 'f7': 'bp', 'g7': 'bp', 'h7': 'bp',
    'a2': 'wp', 'b2': 'wp', 'c2': 'wp', 'd2': 'wp', 'e2': 'wp', 'f2': 'wp', 'g2': 'wp', 'h2': 'wp',
    'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
}

class ChessEngine:
    """
    Manages the core state and rules of the chess game.
    """
    def __init__(self):
        # The board state is a dictionary mapping square ID ('a1') to piece code ('wk') or None
        self.board_state = dict(INITIAL_BOARD_STATE)
        self.current_player = 'w'  # 'w' for White, 'b' for Black
        self.ai_color = 'b'       # Color for the AI player (can be toggled)
        # TODO: Add game state flags here: 'can_castle_w', 'can_castle_b', 'en_passant_target', etc.

    def _is_legal_move(self, from_sq: str, to_sq: str) -> bool:
        """
        PLACEHOLDER: This is where ALL chess rules validation must be implemented.
        The current version only checks for color.
        """
        piece = self.board_state.get(from_sq)
        if not piece:
            return False

        moving_color = piece[0]
        
        # 1. Check if it's the correct player's turn
        if moving_color != self.current_player:
            return False

        # 2. Check if the destination is occupied by own piece
        target_piece = self.board_state.get(to_sq)
        if target_piece and target_piece[0] == moving_color:
            return False

        # 3. TODO: Implement actual piece movement validation (rook, knight, etc.)
        # The frontend has basic move validation, but the backend must be the source of truth.
        # This includes path clearance, castling, en passant, and, most importantly:
        # 4. TODO: Implement Check/Checkmate logic: A move is illegal if it leaves the king in check.
        
        # For now, we rely on the frontend's basic validation for human moves
        # but in a real game, this must be robust.
        
        # TEMPORARY: Allow any move that passes basic color/turn checks
        return True

    def move(self, from_sq: str, to_sq: str) -> bool:
        """
        Attempts to execute a move and update the board state.
        Returns True on success, False on illegal move.
        """
        piece = self.board_state.get(from_sq)
        if not piece:
            raise ValueError(f"No piece found at {from_sq}")

        if not self._is_legal_move(from_sq, to_sq):
            return False

        # --- EXECUTE MOVE ---
        self.board_state[to_sq] = piece
        self.board_state[from_sq] = None

        # --- UPDATE STATE ---
        self._switch_turn()
        
        # TODO: Handle special moves (castling, en passant, promotion) and update flags
        
        return True

    def _switch_turn(self):
        """Switches the current player."""
        self.current_player = 'b' if self.current_player == 'w' else 'w'


    # --------------------------------
    # --- YOUR AI DEVELOPMENT AREA ---
    # --------------------------------
    
    # 1. Move Generation (REQUIRED for Minimax)
    def get_all_legal_moves(self, player_color: str) -> list[tuple[str, str]]:
        """
        TODO: Generate a list of all legal moves for the given player.
        e.g., [('e2', 'e4'), ('b1', 'c3'), ...]
        """
        # 
        # This will be the most complex part of your engine!
        return [] # Placeholder

    # 2. Evaluation Function (REQUIRED for Minimax)
    def evaluate_board(self) -> float:
        """
        TODO: Assign a numerical score to the current board state.
        Positive score favors 'w', negative score favors 'b'.
        """
        # Common factors: Material advantage, piece activity, king safety, pawn structure.
        return 0.0 # Placeholder

    # 3. Minimax Algorithm
    def minimax(self, depth: int, is_maximizing_player: bool) -> float:
        """
        TODO: Implement the Minimax algorithm here.
        This function recursively searches the game tree to find the best outcome.
        """
        # Recursive base case: if depth is 0 or game is over, return evaluation.
        if depth == 0:
            return self.evaluate_board()
        
        # ... your recursive logic here ...
        
        return 0.0 # Placeholder

    # 4. Alpha-Beta Pruning (Optimization)
    def alpha_beta_minimax(self, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> float:
        """
        TODO: Implement the Alpha-Beta optimization for the Minimax algorithm.
        """
        # ... your optimized recursive logic here ...
        return 0.0 # Placeholder

    # 5. Best Move Finder
    def find_best_move(self) -> tuple[str, str] | None:
        """
        Iterates over all legal moves and uses the Minimax/Alpha-Beta function 
        to determine the best one.
        """
        # Call self.alpha_beta_minimax() for each possible move
        return None # Placeholder
