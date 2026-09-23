import random
import math

class Board:
    BOARD_SIZE = 8
    WHITE = "w"
    BLACK = "b"
    WHITE_KING = "W"
    BLACK_KING = "B"
    EMPTY = "."

    def __init__(self, board=None, test_position=True):
        # Create a board.

        # Args:
        #     board: Optional 8x8 board to copy.
        #     test_position: If True and no board is supplied, use the custom
        #         multi-jump test position. If False, use the standard setup.
        
        if board is not None:
            self.board = [row[:] for row in board]
        elif test_position:
            # Custom position intentionally kept for testing multi-jumps.
            self.board = [
                [".", "b", ".", "b", ".", "b", ".", "b"],
                ["b", ".", "b", ".", "b", ".", "b", "."],
                [".", "b", ".", "b", ".", "b", ".", "b"],
                [".", ".", "w", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["w", ".", "w", ".", "w", ".", "w", "."],
                [".", ".", ".", ".", ".", "w", ".", "w"],
                ["w", ".", "w", ".", "w", ".", "w", "."],
            ]
        else:
            self.board = [
                [".", "b", ".", "b", ".", "b", ".", "b"],
                ["b", ".", "b", ".", "b", ".", "b", "."],
                [".", "b", ".", "b", ".", "b", ".", "b"],
                [".", ".", ".", ".", ".", ".", ".", "."],
                [".", ".", ".", ".", ".", ".", ".", "."],
                ["w", ".", "w", ".", "w", ".", "w", "."],
                [".", "w", ".", "w", ".", "w", ".", "w"],
                ["w", ".", "w", ".", "w", ".", "w", "."],
            ]

    def copy(self):
        # Return an independent copy of the board.
        return Board(board=self.board)

    def getPiece(self, position):
        row, col = position
        return self.board[row][col]

    def printBoard(self):
        print("\n")
        print("  ", end="")
        for col in range(self.BOARD_SIZE):

            print(f" {col}", end="")

        for row in range(self.BOARD_SIZE):
            print(" ")
            print(f"{row}  ", end="")
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                symbols = {
                    self.EMPTY: "·",
                    self.BLACK: "○",
                    self.WHITE: "●",
                    self.WHITE_KING: "W",
                    self.BLACK_KING: "B",
                }
                print(f"{symbols.get(piece, piece)} ", end="")
        print()

    def _in_bounds(self, position):
        return (
            0 <= position[0] < self.BOARD_SIZE
            and 0 <= position[1] < self.BOARD_SIZE
        )

    def _directions_for(self, piece):
        if piece == self.WHITE:
            return [(-1, -1), (-1, 1)]
        if piece == self.BLACK:
            return [(1, -1), (1, 1)]
        if piece in (self.WHITE_KING, self.BLACK_KING):
            return [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ]
        return []

    def _opponents_for(self, piece):
        if piece in (self.WHITE, self.WHITE_KING):
            return (self.BLACK, self.BLACK_KING)
        if piece in (self.BLACK, self.BLACK_KING):
            return (self.WHITE, self.WHITE_KING)
        return ()

    def _player_for_piece(self, piece):
        if piece in (self.WHITE, self.WHITE_KING):
            return self.WHITE
        if piece in (self.BLACK, self.BLACK_KING):
            return self.BLACK
        return None

    def getMovesFrom(self, position):
        # Return ordinary one-step moves from a position.
        piece = self.getPiece(position)
        moves = []

        for row_delta, col_delta in self._directions_for(piece):
            destination = (
                position[0] + row_delta,
                position[1] + col_delta,
            )

            if (
                self._in_bounds(destination)
                and self.getPiece(destination) == self.EMPTY
            ):
                moves.append(destination)

        return moves

    def getJumps(self, position):
        # Return all legal single jumps from a position.
        piece = self.getPiece(position)
        opponent = self._opponents_for(piece)
        jump_moves = []

        for row_delta, col_delta in self._directions_for(piece):
            jumped = (
                position[0] + row_delta,
                position[1] + col_delta,
            )
            landing = (
                position[0] + 2 * row_delta,
                position[1] + 2 * col_delta,
            )

            if not self._in_bounds(jumped) or not self._in_bounds(landing):
                continue

            if (
                self.getPiece(jumped) in opponent
                and self.getPiece(landing) == self.EMPTY
            ):
                jump_moves.append(landing)

        return jump_moves

    def applyStep(self, piecePos, movePos):
        # Apply one legal movement step and return whether it crowned.
        piece = self.getPiece(piecePos)

        if piece not in (
            self.WHITE,
            self.BLACK,
            self.WHITE_KING,
            self.BLACK_KING,
        ):
            raise ValueError("There is no playable piece at piecePos.")

        if not self._in_bounds(movePos):
            raise ValueError("movePos is outside the board.")

        normal_move = movePos in self.getMovesFrom(piecePos)
        jump_move = movePos in self.getJumps(piecePos)

        if not normal_move and not jump_move:
            raise ValueError("The requested step is not legal.")

        self.board[piecePos[0]][piecePos[1]] = self.EMPTY

        if jump_move:
            captured_row = (piecePos[0] + movePos[0]) // 2
            captured_col = (piecePos[1] + movePos[1]) // 2
            self.board[captured_row][captured_col] = self.EMPTY

        self.board[movePos[0]][movePos[1]] = piece

        kinged = False

        if piece == self.WHITE and movePos[0] == 0:
            self.board[movePos[0]][movePos[1]] = self.WHITE_KING
            kinged = True
        elif piece == self.BLACK and movePos[0] == self.BOARD_SIZE - 1:
            self.board[movePos[0]][movePos[1]] = self.BLACK_KING
            kinged = True

        return kinged

    def getAllJumps(self, player):
        # Return all legal first jumps for a player as (start, landing) pairs.
        jumps = []

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                position = (row, col)
                piece = self.getPiece(position)

                if self._player_for_piece(piece) != player:
                    continue

                for landing in self.getJumps(position):
                    jumps.append((position, landing))

        return jumps

    def getJumpSequences(self, start):
        # Return every complete multiple-jump sequence starting at start.

        # A returned sequence is a tuple of board positions, for example:
        #     ((5, 2), (3, 4), (1, 6))

        # 
        piece = self.getPiece(start)
        if self._player_for_piece(piece) is None:
            return []

        sequences = []

        def search(position_board, current_position, path):
            jumps = position_board.getJumps(current_position)

            if not jumps:
                if len(path) > 1:
                    sequences.append(tuple(path))
                return

            for next_position in jumps:
                child = position_board.copy()
                kinged = child.applyStep(current_position, next_position)
                new_path = path + [next_position]

                if kinged:
                    sequences.append(tuple(new_path))
                else:
                    search(child, next_position, new_path)

        search(self, start, [start])
        return sequences

    def getLegalTurns(self, player):
        # Return complete legal turns for player.

        # If any capture exists, only complete capture sequences are returned.
        # Ordinary moves are represented by two positions; multi-jumps are
        # represented by three or more positions.
        
        jump_turns = []

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                position = (row, col)
                piece = self.getPiece(position)

                if self._player_for_piece(piece) != player:
                    continue

                if self.getJumps(position):
                    jump_turns.extend(self.getJumpSequences(position))

        if jump_turns:
            return jump_turns

        normal_turns = []

        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                position = (row, col)
                piece = self.getPiece(position)

                if self._player_for_piece(piece) != player:
                    continue

                for destination in self.getMovesFrom(position):
                    normal_turns.append((position, destination))

        return normal_turns

    def getLegalMoves(self, player):
        #Alias for getLegalTurns; moves now represent complete turns.
        return self.getLegalTurns(player)

    def applyTurn(self, turn):
        # Return a new board with a complete turn applied.
        if not turn or len(turn) < 2:
            raise ValueError("A turn must contain at least a start and destination.")

        new_board = self.copy()

        for start, destination in zip(turn, turn[1:]):
            new_board.applyStep(start, destination)

        return new_board

    def countPieces(self, player):
        pieces = (
            (self.WHITE, self.WHITE_KING)
            if player == self.WHITE
            else (self.BLACK, self.BLACK_KING)
        )

        return sum(
            1
            for row in self.board
            for piece in row
            if piece in pieces
        )

    def countKings(self, player):
        king = self.WHITE_KING if player == self.WHITE else self.BLACK_KING
        return sum(
            1
            for row in self.board
            for piece in row
            if piece == king
        )

    def isGameOver(self, player):
        # Return True when player has no legal complete turns.
        return not self.getLegalTurns(player)

    def getWinner(self, player):
        # Return the opponent if player has lost, otherwise None.
        if not self.isGameOver(player):
            return None

        return self.BLACK if player == self.WHITE else self.WHITE

    def getState(self):
        # Return an immutable representation of the board.
        return tuple(
            piece
            for row in self.board
            for piece in row
        )

# Human Player Chooses Moves
class HumanPlayer:
    def chooseTurn(self, board, player):
        legal_turns = board.getLegalTurns(player)

        if not legal_turns:
            return None

        print("\nLegal Turns:")
        for index, turn in enumerate(legal_turns, start=1):
            formatted = " -> ".join(str(position) for position in turn)
            print(f"{index}: {formatted}")

        while True:
            try:
                choice = int(input("\nChoose a move number: "))
                if 1 <= choice <= len(legal_turns):
                    return legal_turns[choice - 1]
                print("Not a valid move number.")
            except ValueError:
                print("Please enter a number.")

# Choose Moves at Random
class RandomPlayer:
    def chooseTurn(self, board, player):
        legal_turns = board.getLegalTurns(player)

        if not legal_turns:
            return None

        return random.choice(legal_turns)


class Game:
    DRAW_REPETITIONS = 10 #how many times can something be repeated before a draw

    def __init__(self, board, WHITE_player, black_player, display=True):
        self.board = board
        self.players = {
            Board.WHITE: WHITE_player,
            Board.BLACK: black_player,
        }
        self.current_player = Board.WHITE
        self.display = display
        self.turns = 0
        self.history = {}

        self._record_position()

    def _record_position(self):
        key = (self.current_player, self.board.getState())
        self.history[key] = self.history.get(key, 0) + 1

    def isDraw(self):
        key = (self.current_player, self.board.getState())
        return self.history.get(key, 0) >= self.DRAW_REPETITIONS

    def switchPlayer(self):
        self.current_player = (
            Board.BLACK
            if self.current_player == Board.WHITE
            else Board.WHITE
        )

    def playTurn(self):
        player = self.current_player
        player_object = self.players[player]

        if self.display:
            self.board.printBoard()
            print(f"\n{'WHITE' if player == Board.WHITE else 'Black'} to move.")

        if self.board.isGameOver(player):
            winner = self.board.getWinner(player)
            if self.display:
                print(
                    f"{'Black' if winner == Board.BLACK else 'WHITE'} wins!"
                )
            return False

        if self.isDraw():
            if self.display:
                print("Draw by repetition.")
            return False

        turn = player_object.chooseTurn(self.board, player)

        if turn is None:
            return False

        self.board = self.board.applyTurn(turn)
        self.turns += 1
        self.switchPlayer()
        self._record_position()

        return True

    def play(self):
        while True:
            if not self.playTurn():
                break


# Minimax Decides best move
class MinimaxPlayer:
    def __init__(self, depth=6):
        self.depth = depth

    def evaluate(self, board, root_player):
        PIECE_VAL = 100
        KING_VAL = 175
        CENTER_VAL = 15
        BACK_ROW_VAL = 25
        
        score = 0
        my_home_row = 7 if root_player == Board.WHITE else 0
        opp_home_row = 0 if root_player == Board.WHITE else 7

        my_pieces = []
        opp_pieces = []

        for row in range(Board.BOARD_SIZE):
            for col in range(Board.BOARD_SIZE):
                piece = board.board[row][col]
                if piece == Board.EMPTY:
                    continue
                
                is_mine = (piece in (Board.WHITE, Board.WHITE_KING)) if root_player == Board.WHITE else (piece in (Board.BLACK, Board.BLACK_KING))
                is_king = piece in (Board.WHITE_KING, Board.BLACK_KING)
                multiplier = 1 if is_mine else -1

                if is_mine:
                    my_pieces.append((row, col, is_king))
                else:
                    opp_pieces.append((row, col, is_king))
                
                # Material Value
                score += (KING_VAL if is_king else PIECE_VAL) * multiplier
                
                # Center Control
                if 2 <= col <= 5:
                    score += CENTER_VAL * multiplier
                    
                # Back Row Protection
                if not is_king:
                    if is_mine and row == my_home_row:
                        score += BACK_ROW_VAL
                    elif not is_mine and row == opp_home_row:
                        score -= BACK_ROW_VAL
                        
                # Promotion Progress
                if not is_king:
                    progress = (7 - row) * 5 if root_player == Board.WHITE else row * 5
                    score += progress * multiplier

        # Endgame King Convergence: Encourage Kings to close distance on enemy pieces
        if opp_pieces:
            for r, c, is_king in my_pieces:
                if is_king:
                    min_dist = min(abs(r - orow) + abs(c - ocol) for orow, ocol, _ in opp_pieces)
                    score -= min_dist * 4  # Deduct points for being far away

        return score

    def minimax(self, board, depth, alpha, beta, maximizing, player, root_player, history_counts):
        state_key = (player, board.getState())
        
        # 1. Detect state repetitions (penalize shuffling)
        if history_counts.get(state_key, 0) >= 2:
            return 0, None  # Treat repeated state as a 0-value draw

        # 2. Terminal Game Over check
        if board.isGameOver(player):
            winner = board.getWinner(player)
            if winner == root_player:
                return 100000 + depth, None
            elif winner is not None:
                return -100000 - depth, None
            else:
                return 0, None

        if depth == 0:
            return self.evaluate(board, root_player), None

        legal_turns = board.getLegalTurns(player)
        if not legal_turns:
            return self.evaluate(board, root_player), None

        best_turn = legal_turns[0]
        opponent = Board.BLACK if player == Board.WHITE else Board.WHITE

        if maximizing: #maximazing
            max_eval = -math.inf
            for turn in legal_turns:
                next_board = board.applyTurn(turn)
                next_state = (opponent, next_board.getState())
                
                history_counts[next_state] = history_counts.get(next_state, 0) + 1
                eval_score, _ = self.minimax(next_board, depth - 1, alpha, beta, False, opponent, root_player, history_counts)
                history_counts[next_state] -= 1
                if history_counts[next_state] == 0:
                    del history_counts[next_state]

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_turn = turn
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_turn
        else: #minimizing
            min_eval = math.inf
            for turn in legal_turns:
                next_board = board.applyTurn(turn)
                next_state = (opponent, next_board.getState())
                
                history_counts[next_state] = history_counts.get(next_state, 0) + 1
                eval_score, _ = self.minimax(next_board, depth - 1, alpha, beta, True, opponent, root_player, history_counts)
                history_counts[next_state] -= 1
                if history_counts[next_state] == 0:
                    del history_counts[next_state]

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_turn = turn
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_turn
    def chooseTurn(self, board, player, game_history=None):
        history_counts = dict(game_history) if game_history else {}
        legal_turns = board.getLegalTurns(player)
        
        if not legal_turns:
            return None

        best_turns = []
        max_eval = -math.inf
        alpha = -math.inf
        beta = math.inf
        opponent = Board.BLACK if player == Board.WHITE else Board.WHITE

        for turn in legal_turns:
            next_board = board.applyTurn(turn)
            next_state = (opponent, next_board.getState())
            
            history_counts[next_state] = history_counts.get(next_state, 0) + 1
            
            # Pass active alpha and beta bounds to preserve pruning
            eval_score, _ = self.minimax(
                next_board, self.depth - 1, alpha, beta, False, opponent, player, history_counts
            )
            
            history_counts[next_state] -= 1
            if history_counts[next_state] == 0:
                del history_counts[next_state]

            if eval_score > max_eval:
                max_eval = eval_score
                best_turns = [turn]
                alpha = max(alpha, eval_score)  # Update alpha to maintain pruning speed
            elif eval_score == max_eval:
                best_turns.append(turn)

        return random.choice(best_turns) # Randomly Selects the 'best' move if scores are equal



def createGame():
    choice = input("\nPick White, Black, Auto-Random or Auto-Minimax: ").strip().lower()
    level = 0
    while choice not in {"white", "black", "auto-random","auto-minimax"}:
        choice = input("\nPick White, Black, Auto-Random or Auto-Minimax: ").strip().lower()
    if choice == "white" or choice == "black" or choice == "auto-minimax":
        level = int(input("\nWhat level of minimax? (1 is low 6 is high): "))

    
    board = Board(test_position=False)

    human = HumanPlayer()
    random_player = RandomPlayer()
    minimax_player = MinimaxPlayer(level)
    if choice == "white":
        WHITE_player = human
        black_player = minimax_player
    elif choice == "black":
        WHITE_player = minimax_player
        black_player = human
    elif choice == "auto-random":
        WHITE_player = random_player
        black_player = random_player
    elif choice == "auto-minimax":
        WHITE_player = minimax_player
        black_player = minimax_player
    return Game(board, WHITE_player, black_player)

def testGame():
    board = Board(test_position=False)
    random_playerW = MinimaxPlayer(1)
    random_playerB = MinimaxPlayer(3)
    return Game(board, random_playerW, random_playerB)
if __name__ == "__main__":
    game = createGame()
    game.play()
