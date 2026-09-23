import random


class Board:
    BOARD_SIZE = 8
    WHITE = "w"
    BLACK = "b"
    WHITE_KING = "W"
    BLACK_KING = "B"
    EMPTY = "."

    def __init__(self, board=None, test_position=True):
        """Create a board.

        Args:
            board: Optional 8x8 board to copy.
            test_position: If True and no board is supplied, use the custom
                multi-jump test position. If False, use the standard setup.
        """
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
        """Return an independent copy of the board."""
        return Board(board=self.board)

    def getPiece(self, position):
        row, col = position
        return self.board[row][col]

    def printBoard(self):
        print("\n")
        print("   ", end="")
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
        """Return ordinary one-step moves from a position."""
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
        """Return all legal single jumps from a position."""
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
        """Apply one legal movement step and return whether it crowned."""
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
        """Return all legal first jumps for a player as (start, landing) pairs."""
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
        """Return every complete multiple-jump sequence starting at start.

        A returned sequence is a tuple of board positions, for example:
            ((5, 2), (3, 4), (1, 6))

        This implementation treats crowning during a capture as the end of
        the turn, matching the checkers ruleset used by this project.
        """
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
        """Return complete legal turns for player.

        If any capture exists, only complete capture sequences are returned.
        Ordinary moves are represented by two positions; multi-jumps are
        represented by three or more positions.
        """
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
        """Alias for getLegalTurns; moves now represent complete turns."""
        return self.getLegalTurns(player)

    def applyTurn(self, turn):
        """Return a new board with a complete turn applied."""
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
        """Return True when player has no legal complete turns."""
        return not self.getLegalTurns(player)

    def getWinner(self, player):
        """Return the opponent if player has lost, otherwise None."""
        if not self.isGameOver(player):
            return None

        return self.BLACK if player == self.WHITE else self.WHITE

    def getState(self):
        """Return an immutable representation of the board."""
        return tuple(
            piece
            for row in self.board
            for piece in row
        )


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


class RandomPlayer:
    def chooseTurn(self, board, player):
        legal_turns = board.getLegalTurns(player)

        if not legal_turns:
            return None

        return random.choice(legal_turns)


class Game:
    DRAW_REPETITIONS = 3

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



def createGame():
    choice = input("\nPick White, Black or Auto: ").strip().lower()

    while choice not in {"white", "black", "auto"}:
        print("Please enter White, Black or Auto.")
        choice = input("\nPick White, Black or Auto: ").strip().lower()

    # Keep the custom position enabled for multi-jump development/testing.
    # Set test_position=False here when you want the standard starting board.
    board = Board(test_position=False)

    human = HumanPlayer()
    random_player = RandomPlayer()

    if choice == "white":
        WHITE_player = human
        black_player = random_player
    elif choice == "black":
        WHITE_player = random_player
        black_player = human
    else:
        WHITE_player = random_player
        black_player = random_player

    return Game(board, WHITE_player, black_player)

def testGame():
    board = Board(test_position=False)
    random_playerW = RandomPlayer()
    random_playerB = RandomPlayer()
    return Game(board, random_playerW, random_playerB)
if __name__ == "__main__":
    # game = createGame()
    game = testGame()
    game.play()
