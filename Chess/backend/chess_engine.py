#Chess Engine
#===== Constants =====#
piece_values = {
    'p': 100,
    'n': 320,
    'b': 330,
    'r': 500,
    'q': 900,
    'k': 20000
}

columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

search_depth = 3

#=== Utility Functions ===
def square_to_coords(square_id: str) -> tuple[int, int]:
    #convert piece positions to coordinates e.g. 'a1' -> (1,1) where (row, col)
    if not square_id or len(square_id) != 2 or square_id[0] not in columns:
        return 0,0

    col = columns.index(square_id[0]) + 1
    row = int(square_id[1])
    return row, col

def coords_to_square(row: int, col: int) -> str | None:
    #converts coordinates to piece positions e.g. (1,1) -> 'a1'
    if 1 <= row <= 8 and 1 <= col <=8:
        return columns[col - 1] + str(row)
    return None

#Chess Engine class
class ChessEngine:
    def __init__(self, board_state: dict):
        self.board = board_state

    #--- Core Algorithm(Minimax, Find Best move)
    def minimax(self, depth: int, maximizing_player: bool) -> float:
        
        if depth == 0:
            return self.evaluate()

        current_color = 'b' if maximizing_player else 'w'
        legal_moves = self.get_legal_moves(current_color)

        if not legal_moves:
            return self.evaluate()

        if maximizing_player:
            max_eval = float('-inf')
            for from_sq, to_sq in legal_moves:
                captured_piece = self.make_move(from_sq, to_sq)

                eval = self.minimax(depth - 1, False)

                self.undo_move(from_sq, to_sq, captured_piece)
                max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for from_sq, to_sq in legal_moves:
                captured_piece = self.make_move(from_sq, to_sq)

                eval = self.minimax(depth - 1, True)

                self.undo_move(from_sq, to_sq, captured_piece)
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, ai_color: str) -> tuple[str, str]:
        #initiates the minimax search and returns best move
        search_depth = 3
        maximizing_player = ai_color == 'b'
        current_color = ai_color

        best_move = None
        best_eval = float('-inf') if maximizing_player else float('inf')

        ai_legal_moves = self.get_legal_moves(current_color)

        for from_sq, to_sq in ai_legal_moves:
            captured_piece = self.make_move(from_sq, to_sq)

            eval = self.minimax(
                search_depth -1,
                not maximizing_player
            )
            self.undo_move(from_sq, to_sq, captured_piece)

            #check if move is better than current best
            if maximizing_player and eval > best_eval:
                best_eval = eval
                best_move = (from_sq, to_sq)

        if best_move:
            print(f"AI Best move found(Minimax): {best_move} with Eval: {best_eval}")
        return best_move if best_move else (None, None)


    #Game Logic (move execution, evaluation)
    def evaluate(self) -> float:
        score = 0
        for piece_code in self.board.values():
            if piece_code:
                color = 1 if piece_code[0] == 'b' else - 1
                piece_type = piece_code[1]
                score += color * piece_values.get(piece_type, 0)

        return score

    def get_legal_moves(self, color: str) -> list[tuple[str, str]]:
        #All moves that DO NOT leave the King in Check
        all_pseudo_legal_moves = [] #all moves
        final_legal_moves = [] #moves that don't leave the King in Check

        #====== Pseudo-Legal Moves ====
        for sq, piece_code in self.board.items():
            if piece_code and piece_code[0] == color:
                piece_type = piece_code[1]

                # ---- PAWN MOVES -----
                if piece_type == 'p':
                    #extend the list with all valid pawn moves from this square
                    all_pseudo_legal_moves.extend(self.get_pawn_moves(sq, color))

                # ---- KNIGHT MOVES -----

        #Filter for King Safety
        for from_sq, to_sq in all_pseudo_legal_moves:
            captured_piece = self.make_move(from_sq, to_sq)
            if not self.is_in_check(color):
               final_legal_moves.append((from_sq, to_sq))

            self.undo_move(from_sq, to_sq, captured_piece)
            final_legal_moves.append((from_sq, to_sq))
        return final_legal_moves

    def make_move(self, from_sq: str, to_sq: str) -> str | None:
        #executes the move and returns the captured piece.
        captured_piece = self.board.get(to_sq)

        piece_to_move = self.board.get(from_sq)

        if not piece_to_move:
            #raise ValueError(f"Attempted to move piece from empty square: {from_sq}")
            print(f"Warning: Attempted to move piece from empty square: {from_sq}")
            return None

        self.board[to_sq] = piece_to_move

        self.board[from_sq] = None

        return captured_piece

    def undo_move(self, from_sq: str, to_sq: str, captured_piece: str | None) -> None:
        #Reverts the move
        piece_to_move = self.board.get(to_sq)

        self.board[from_sq] = piece_to_move

        self.board[to_sq] = captured_piece

    #def is_in_check(self, color: str) -> bool:
        #determines if the King of 'color' is under attack.
        
    def get_pawn_moves(self, from_sq: str, color: str) -> list[tuple[str, str]]:
        moves = []
        row, col = square_to_coords(from_sq)
        direction = 1 if color == 'w' else -1 #pawns move up for white, down for black

        #One Square Forward
        one_step_row = row + direction
        one_step_sq = coords_to_square(one_step_row, col)

        if one_step_sq and not self.board.get(one_step_sq):
            moves.append((from_sq, one_step_sq))

            #Two Square forward(only when starting)
            start_rank = 2 if color == 'w' else 7
            if row == start_rank:
                two_step_row = row + 2 * direction
                two_step_sq = coords_to_square(two_step_row, col)

                #Is square on board and empty
                if two_step_sq and not self.board.get(two_step_sq):
                    moves.append((from_sq, two_step_sq))

        #Captures (Diagonal moves)
        opponent_color = 'w' if color == 'b' else 'b'

        #check for capture on the left diagonal
        left_col = col - 1
        capture_row = row + direction
        left_capture_sq = coords_to_square(capture_row, left_col)

        if left_capture_sq:
            target_piece = self.board.get(left_capture_sq)
            #check if target square has an oppent piece
            if target_piece and target_piece[0] == opponent_color:
                moves.append((from_sq, left_capture_sq))

        #check for capture on the right diagonal
        right_col = col + 1
        right_capture_sq = coords_to_square(capture_row, right_col)

        if right_capture_sq:
            target_piece = self.board.get(right_capture_sq)
            #check if target square has an oppent piece
            if target_piece and target_piece[0] == opponent_color:
                moves.append((from_sq, right_capture_sq))

        #TODO: En Passant logic

        return moves

    #--Knight moves
    #def get_knight_moves():


