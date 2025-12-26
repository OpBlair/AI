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
                elif piece_type == 'n':
                    all_pseudo_legal_moves.extend(self.get_knight_moves(sq, color))

                # ---- ROOK MOVES ----
                elif piece_type == 'r':
                    all_pseudo_legal_moves.extend(self.get_rook_moves(sq, color))

                # ---- BISHOP MOVES ----
                elif piece_type == 'b':
                    all_pseudo_legal_moves.extend(self.get_bishop_moves(sq, color))

                # ---- QUEEN MOVES ----
                elif piece_type == 'q':
                    all_pseudo_legal_moves.extend(self.get_queen_moves(sq, color))

                # ---- KING MOVES ----
                elif piece_type == 'k':
                    all_pseudo_legal_moves.extend(self.get_king_moves(sq, color))
                

        #Filter for King Safety
        for from_sq, to_sq in all_pseudo_legal_moves:
            # 1.Execute the move hypothetically
            captured_piece = self.make_move(from_sq, to_sq)

            # 2.Check if the current player is in check after the move
            if not self.is_in_check(color):
               final_legal_moves.append((from_sq, to_sq))

            # 3.Revert the move to explore the next option
            self.undo_move(from_sq, to_sq, captured_piece)
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

    def is_in_check(self, color: str) -> bool:
        #determines if the King of 'color' is under attack.
        king_code = color + 'k'
        king_sq = None
        
        # 1.Find the King's position
        for sq, piece_code in self.board.items():
            if piece_code == king_code:
                king_sq = sq
                break

        if not king_sq:
            # Should only happen in end-game situations like checkmate/stalemate scenarios 
            # where the king might have been captured (though this engine doesn't track game over yet).
            return False
        
        # 2.Check if the King's square is attacked by the opponent
        opponent_color = 'w' if color == 'b' else 'b'
        return self.is_square_attacked(king_sq, opponent_color)
                
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

    #--Knight moves ----
    def get_knight_moves(self, from_sq: str, color: str) -> list[tuple[str, str]]:
        moves = []
        row, col = square_to_coords(from_sq)

        #possible moves(row_change, col_change)
        knight_deltas = [
            (2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        opponent_color = 'w' if color == 'b' else 'b'

        for d_row, d_col in knight_deltas:
            target_row = row + d_row
            target_col = col + d_col
            target_sq = coords_to_square(target_row, target_col)

            if target_sq:
                target_piece = self.board.get(target_sq)

                #move is valid if the square is empty OR contains opponent's piece
                if not target_piece or target_piece[0] == opponent_color:
                    moves.append((from_sq, target_sq))

        return moves

    #=== Rules for sliding pieces like rook, bishop, queen
    def get_directional_moves(self, from_sq: str, color: str, directions: list[tuple[int, int]]) -> list[tuple[str, str]]:
        moves = []
        row, col = square_to_coords(from_sq)
        opponent_color = 'w' if color == 'b' else 'b'

        #loop through each direction defined by piece
        for d_row, d_col in directions:
            current_row = row + d_row
            current_col = col + d_col

            #keep sliding till board edge
            while 1 <= current_row <= 8 and 1 <= current_col <= 8:
                target_sq = coords_to_square(current_row, current_col)
                target_piece = self.board.get(target_sq)

                if not target_piece:
                    #square is empty ? add move and continue sliding
                    moves.append((from_sq, target_sq))
                    current_row += d_row
                    current_col += d_col

                else:
                    #square is occupied: check if its opponents's piece
                    if target_piece[0] == opponent_color:
                        #capture & stop sliding
                        moves.append((from_sq, target_sq))
                    break
        return moves

    #=== Rook moves ====
    def get_rook_moves(self, from_sq: str, color: str) -> list[tuple[str, str]]:
        directions = [
            (0, 1), (0, -1), #horizontal
            (1, 0), (-1, 0) #vertical
        ]
        return self.get_directional_moves(from_sq, color, directions)

    #=== Bishop moves ===
    def get_bishop_moves(self, from_sq: str, color: str) -> list[tuple[str, str]]:
        directions = [
            (1, 1), (1, -1),
            (-1, 1), (-1, -1)
        ]
        return self.get_directional_moves(from_sq, color, directions)

    #=== Queen moves ===
    def get_queen_moves(self, from_sq: str, color: str) -> list[tuple[str, str]]:
        #combines bishoop and rook moves
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0), #Rook moves
            (1, 1), (1, -1), (-1, 1), (-1, -1) #Bishop moves
        ]
        return self.get_directional_moves(from_sq, color, directions)

    def get_king_moves(self, from_sq: str, color: str) -> list[tuple[str, str]]:
        moves = []
        row, col = square_to_coords(from_sq)
        opponent_color = 'w' if color == 'b' else 'b'

        #King moves one step in all 8 directions
        knight_deltas = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in knight_deltas:
            target_row = row + d_row
            target_col = col + d_col
            target_sq = coords_to_square(target_row, target_col)

            if target_sq:
                target_piece = self.board.get(target_sq)

                #move is valid if square is empty or contains an opponent piece
                if not target_piece or target_piece[0] == opponent_color:
                    moves.append((from_sq, target_sq))
        #TODO : CASTLING
        return moves

    def is_square_attacked(self, target_sq: str, by_color: str) -> bool:
        #Determines if 'target_sq' is attacked by any piece of 'by_color'.
        #Check 8 directions for sliding pieces and specific positions for King, Knight, and pawn.
        opponent_king = 'k'
        opponent_queen = 'q'
        opponent_rook = 'r'
        opponent_bishop = 'b'
        opponent_knight = 'n'
        opponent_pawn = 'p'

        #The pieces will have a prefix e.g. 'bk'
        opponent_piece_code_prefix = by_color

        target_row, target_col = square_to_coords(target_sq)

        # 1. Check for sliding pieces
        #Directions: (d_row, d_col, piece_types_to_look_for)
        sliding_checks = [
            # Rook/queen directions (straight)
            (0, 1, [opponent_rook, opponent_queen]), (0, -1, [opponent_rook, opponent_queen]),
            (1, 0, [opponent_rook, opponent_queen]), (-1, 0, [opponent_rook, opponent_queen]),

            # Bishop/Queen directions (diagonal)
            (1, 1, [opponent_bishop, opponent_queen]), (1, -1, [opponent_bishop, opponent_queen]),
            (-1, 1, [opponent_bishop, opponent_queen]), (-1, -1, [opponent_bishop, opponent_queen]),
        ]

        for d_row, d_col, piece_types in sliding_checks:
            current_row = target_row + d_row
            current_col = target_col + d_col

            while 1 <= current_row <= 8 and 1 <= current_col <= 8:
                current_sq = coords_to_square(current_row, current_col)
                piece_code = self.board.get(current_sq)

                if piece_code:
                    # Found a piece! check if it's the attacking type
                    if piece_code[0] == by_color and piece_code[1] in piece_types:
                        return True

                    # Blocked by own piece or non-threathening opponent piece
                    break

                #keep sliding
                current_col += d_col
                current_row += d_row

        # 2. Check for Knight Attacks
        knight_deltas = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for d_row, d_col in knight_deltas:
            check_row = target_row + d_row
            check_col = target_col + d_col
            check_sq = coords_to_square(check_row, check_col)

            if check_sq:
                piece_code = self.board.get(check_sq)
                if piece_code == opponent_piece_code_prefix + opponent_knight:
                    return True

        # 3. Check for Pawn Attacks(Reverse Movement)
        pawn_direction = 1 if by_color == 'w' else -1 #pawns attack 'down for white', 'up' for black

        for d_col in [-1, 1]: #check diagonals
            check_row = target_row + pawn_direction
            check_col = target_col + d_col
            check_sq = coords_to_square(check_row, check_col)

            if check_sq:
                piece_code = self.board.get(check_sq)
                if piece_code == opponent_piece_code_prefix + opponent_pawn:
                    return True

        # 4. Check for King Attacks
        king_deltas = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for d_row, d_col in king_deltas:
            check_row = target_row + d_row
            check_col = target_col + d_col
            check_sq = coords_to_square(check_row, check_col)

            if check_sq:
                piece_code = self.board.get(check_sq)
                if piece_code == opponent_piece_code_prefix + opponent_king:
                    return True

        return False
