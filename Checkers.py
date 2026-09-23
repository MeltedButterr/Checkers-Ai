import random
class Board():


    def __init__(self):
        self.red = "r"
        self.black = "b"
        self.redK = "R"
        self.blackK = "B"
        self.empty = "."
        # self.board = [
        #                 [".", "b", ".", "b", ".", "b", ".", "b"],
        #                 ["b", ".", "b", ".", "b", ".", "b", "."],
        #                 [".", "b", ".", "b", ".", "b", ".", "b"],
        #                 [".", ".", ".", ".", ".", ".", ".", "."],
        #                 [".", ".", ".", ".", ".", ".", ".", "."],
        #                 ["r", ".", "r", ".", "r", ".", "r", "."],
        #                 [".", "r", ".", "r", ".", "r", ".", "r"],
        #                 ["r", ".", "r", ".", "r", ".", "r", "."],
        #             ]
        self.board = [
                                [".", "b", ".", "b", ".", "b", ".", "b"],
                                ["b", ".", "b", ".", "b", ".", "b", "."],
                                [".", "b", ".", "b", ".", "b", ".", "b"],
                                [".", ".", "r", ".", ".", ".", ".", "."],
                                [".", ".", ".", ".", ".", ".", ".", "."],
                                ["r", ".", "r", ".", "r", ".", "r", "."],
                                [".", ".", ".", ".", ".", "r", ".", "r"],
                                ["r", ".", "r", ".", "r", ".", "r", "."],
                            ]
    def printBoard(self):
        print("\n")
        print("  ",end ="")
        for col in range(8):
            print(f" {col}", end="")
        for row in range(len(self.board)):
            print(" ")
            print(f"{row}  ", end="")
            for col in range(len(self.board[row])):
                if self.board[row][col] == '.':
                    print("· ", end="")
                elif self.board[row][col] == 'b':
                    print("○ ", end="")
                elif self.board[row][col] == 'r':
                    print("● ", end="")
                elif self.board[row][col] == 'R':
                    print("R ", end="")
                elif self.board[row][col] == 'B':
                    print("B ", end="")
    def getPiece(self,position):

    
        return self.board[position[0]][position[1]]

    def movePiece(self, piecePos, movePos, legalMoves):
        piece = self.getPiece(piecePos)

        if piece in ('r', 'R'):
            player = 'r'
        elif piece in ('b', 'B'):
            player = 'b'
        else:
            print("There is no piece there.")
            return False

        if (piecePos, movePos) not in legalMoves:
            print("not a move")
            return False

        # Move the piece
        self.board[piecePos[0]][piecePos[1]] = self.empty

        # If it's a jump, remove captured piece
        if abs(piecePos[0] - movePos[0]) == 2:
            capturedRow = (piecePos[0] + movePos[0]) // 2
            capturedCol = (piecePos[1] + movePos[1]) // 2
            self.board[capturedRow][capturedCol] = self.empty

        # Put piece in new position
        self.board[movePos[0]][movePos[1]] = piece

        # Kinging
        kinged = False

        if piece == 'r' and movePos[0] == 0:
            self.board[movePos[0]][movePos[1]] = 'R'
            kinged = True

        elif piece == 'b' and movePos[0] == 7:
            self.board[movePos[0]][movePos[1]] = 'B'
            kinged = True

        self.printBoard()

        return kinged
    def getMovesFrom(self, position):
        piece = self.getPiece(position)
        moves = []

        if piece == 'r':
            left = (position[0] - 1, position[1] - 1)
            right = (position[0] - 1, position[1] + 1)

            if 0 <= left[0] < 8 and 0 <= left[1] < 8:
                if self.getPiece(left) == self.empty:
                    moves.append(left)

            if 0 <= right[0] < 8 and 0 <= right[1] < 8:
                if self.getPiece(right) == self.empty:
                    moves.append(right)

        elif piece == 'b':
            left = (position[0] + 1, position[1] - 1)
            right = (position[0] + 1, position[1] + 1)

            if 0 <= left[0] < 8 and 0 <= left[1] < 8:
                if self.getPiece(left) == self.empty:
                    moves.append(left)

            if 0 <= right[0] < 8 and 0 <= right[1] < 8:
                if self.getPiece(right) == self.empty:
                    moves.append(right)

        elif piece == 'R' or piece == 'B':

            upLeft = (position[0] - 1, position[1] - 1)
            upRight = (position[0] - 1, position[1] + 1)
            downLeft = (position[0] + 1, position[1] - 1)
            downRight = (position[0] + 1, position[1] + 1)

            if 0 <= upLeft[0] < 8 and 0 <= upLeft[1] < 8:
                if self.getPiece(upLeft) == self.empty:
                    moves.append(upLeft)

            if 0 <= upRight[0] < 8 and 0 <= upRight[1] < 8:
                if self.getPiece(upRight) == self.empty:
                    moves.append(upRight)

            if 0 <= downLeft[0] < 8 and 0 <= downLeft[1] < 8:
                if self.getPiece(downLeft) == self.empty:
                    moves.append(downLeft)

            if 0 <= downRight[0] < 8 and 0 <= downRight[1] < 8:
                if self.getPiece(downRight) == self.empty:
                    moves.append(downRight)

        return moves
    def getJumps(self, position):

        jumpMoves = []

        upLeft = (position[0] - 1, position[1] - 1)
        upLeftLeft = (position[0] - 2, position[1] - 2)

        upRight = (position[0] - 1, position[1] + 1)
        upRightRight = (position[0] - 2, position[1] + 2)

        downLeft = (position[0] + 1, position[1] - 1)
        downLeftLeft = (position[0] + 2, position[1] - 2)

        downRight = (position[0] + 1, position[1] + 1)
        downRightRight = (position[0] + 2, position[1] + 2)

        piece = self.getPiece(position)

        # RED
        if piece == 'r':

            # Up-left
            if (0 <= upLeft[0] < 8 and 0 <= upLeft[1] < 8 and
                    0 <= upLeftLeft[0] < 8 and 0 <= upLeftLeft[1] < 8):

                if self.getPiece(upLeft) in ('b', 'B') and self.getPiece(upLeftLeft) == '.':
                    jumpMoves.append(upLeftLeft)

            # Up-right
            if (0 <= upRight[0] < 8 and 0 <= upRight[1] < 8 and
                    0 <= upRightRight[0] < 8 and 0 <= upRightRight[1] < 8):

                if self.getPiece(upRight) in ('b', 'B') and self.getPiece(upRightRight) == '.':
                    jumpMoves.append(upRightRight)

        # BLACK
        elif piece == 'b':

            # Down-left
            if (0 <= downLeft[0] < 8 and 0 <= downLeft[1] < 8 and
                    0 <= downLeftLeft[0] < 8 and 0 <= downLeftLeft[1] < 8):

                if self.getPiece(downLeft) in ('r', 'R') and self.getPiece(downLeftLeft) == '.':
                    jumpMoves.append(downLeftLeft)

            # Down-right
            if (0 <= downRight[0] < 8 and 0 <= downRight[1] < 8 and
                    0 <= downRightRight[0] < 8 and 0 <= downRightRight[1] < 8):

                if self.getPiece(downRight) in ('r', 'R') and self.getPiece(downRightRight) == '.':
                    jumpMoves.append(downRightRight)

        # KINGS
        elif piece == 'R' or piece == 'B':

            # Up-left
            if (0 <= upLeft[0] < 8 and 0 <= upLeft[1] < 8 and
                    0 <= upLeftLeft[0] < 8 and 0 <= upLeftLeft[1] < 8):

                if piece == 'R':
                    opponent = ('b', 'B')
                else:
                    opponent = ('r', 'R')

                if self.getPiece(upLeft) in opponent and self.getPiece(upLeftLeft) == '.':
                    jumpMoves.append(upLeftLeft)

            # Up-right
            if (0 <= upRight[0] < 8 and 0 <= upRight[1] < 8 and
                    0 <= upRightRight[0] < 8 and 0 <= upRightRight[1] < 8):

                if piece == 'R':
                    opponent = ('b', 'B')
                else:
                    opponent = ('r', 'R')

                if self.getPiece(upRight) in opponent and self.getPiece(upRightRight) == '.':
                    jumpMoves.append(upRightRight)

            # Down-left
            if (0 <= downLeft[0] < 8 and 0 <= downLeft[1] < 8 and
                    0 <= downLeftLeft[0] < 8 and 0 <= downLeftLeft[1] < 8):

                if piece == 'R':
                    opponent = ('b', 'B')
                else:
                    opponent = ('r', 'R')

                if self.getPiece(downLeft) in opponent and self.getPiece(downLeftLeft) == '.':
                    jumpMoves.append(downLeftLeft)

            # Down-right
            if (0 <= downRight[0] < 8 and 0 <= downRight[1] < 8 and
                    0 <= downRightRight[0] < 8 and 0 <= downRightRight[1] < 8):

                if piece == 'R':
                    opponent = ('b', 'B')
                else:
                    opponent = ('r', 'R')

                if self.getPiece(downRight) in opponent and self.getPiece(downRightRight) == '.':
                    jumpMoves.append(downRightRight)

        return jumpMoves





    def getAllJumps(self, player):
        jumpMoves = []

        for row in range(8):
            for col in range(8):
                piece = self.getPiece((row, col))

                if player == 'r' and piece in ('r', 'R'):
                    jumps = self.getJumps((row, col))

                    for jump in jumps:
                        jumpMoves.append(((row, col), jump))

                elif player == 'b' and piece in ('b', 'B'):
                    jumps = self.getJumps((row, col))

                    for jump in jumps:
                        jumpMoves.append(((row, col), jump))

        return jumpMoves
    def getLegalMoves(self, player):
        jumps = self.getAllJumps(player)

        if jumps:
            return jumps

        moves = []

        for row in range(8):
            for col in range(8):
                piece = self.getPiece((row, col))

                if player == 'r' and piece in ('r', 'R'):
                    pieceMoves = self.getMovesFrom((row, col))

                    for move in pieceMoves:
                        moves.append(((row, col), move))

                elif player == 'b' and piece in ('b', 'B'):
                    pieceMoves = self.getMovesFrom((row, col))

                    for move in pieceMoves:
                        moves.append(((row, col), move))

        return moves
    def continueJumps(self, movePos, kinged, randomMove=False):

        while True:
            jumps = self.getJumps(movePos)

            # No more jumps
            if not jumps:
                break

            jumpMoves = [(movePos, jump) for jump in jumps]

            if randomMove:
                # Computer randomly chooses the next jump
                newMove = random.choice(jumps)
            else:
                # Human chooses the next jump
                print("\nMore jumps available:")
                print(*jumpMoves, sep="\n")

                while True:
                    try:
                        newMove = tuple(
                            map(int, input("\nJump to Where?: ").split())
                        )
                    except ValueError:
                        print("Not Valid Move")
                        continue

                    if newMove not in jumps:
                        print("Not a valid jump.")
                        continue

                    break

            # Make the jump
            kinged = self.movePiece(movePos, newMove, jumpMoves)

            # Move the piece's current position
            movePos = newMove

            # Your current rules stop the jump sequence if the piece is kinged
            if kinged:
                break

        return
    def randOpp(self, player):
        legal = self.getLegalMoves(player)

        if not legal:
            return False

        # Pick a random legal first move
        piecePos, movePos = random.choice(legal)

        # Check if the first move is a jump
        isJump = abs(piecePos[0] - movePos[0]) == 2

        # Make the first move
        kinged = self.movePiece(piecePos, movePos, legal)

        # If it was a jump, continue jumping
        if isJump:
            self.continueJumps(movePos, kinged, randomMove=True)

        return True
    def makeTurn(self, player):
        self.printBoard()

        legalMoves = self.getLegalMoves(player)

        if not legalMoves:
            print(f"{player} has no legal moves.")
            return False

        print("\nLegal Moves:")
        print(*legalMoves, sep="\n")

        while True:
            try:
                piecePos = tuple(
                    map(int, input("\nPick a Piece: ").split())
                )
                movePos = tuple(
                    map(int, input("To Where?: ").split())
                )

                if (piecePos, movePos) not in legalMoves:
                    print("Not a valid move.")
                    continue

                break

            except ValueError:
                print("Not Valid Move")

        # Check whether the first move is a jump
        isJump = abs(piecePos[0] - movePos[0]) == 2

        # Make the first move
        kinged = self.movePiece(piecePos, movePos, legalMoves)

        # Continue the multiple jump
        if isJump:
            self.continueJumps(movePos, kinged, randomMove=False)

        return True

    def startGame(self):
        stop = False
        playerColor = input("\nPick White, Black or Auto ")
        turns =0
        while not stop:

            if playerColor == "White":
                if not self.makeTurn('r'):
                    print("\nBlack wins!")
                    print(f"turns: {turns}")
                    break

                if not self.randOpp('b'):
                    print("\nRed wins!")
                    print(f"turns: {turns}")
                    break
                turns +=1
            elif playerColor == "Black":
                if not self.makeTurn('b'):
                    print("\nRed wins!")
                    print(f"turns: {turns}")
                    break

                if not self.randOpp('r'):
                    print("\nBlack wins!")
                    print(f"turns: {turns}")
                    break
                turns +=1
            elif playerColor == 'Auto':
                self.printBoard()

                if not self.randOpp('r'):
                    print("\nBlack wins!")
                    print(f"turns: {turns}")
                    break

                if not self.randOpp('b'):
                    print("\nRed wins!")
                    print(f"turns: {turns}")
                    break
                turns +=1
            else:
                print("Please enter White or Black.")
                playerColor = input("\nPick White or Black: ")







# Start of function
myBoard = Board()
Board.printBoard(myBoard)
Board.getPiece(myBoard,(0,0))
# piecePos = tuple(map(int, input("\nPick a Piece: ").split()))
# movePos = tuple(map(int, input("\nTo Where?: ").split()))
# myBoard.movePiece(piecePos, movePos)
myBoard.startGame()
# print(myBoard.getJumps((5,2)))
# print(Board.getMovesFrom(myBoard,(5,0)))
# Board.verifyRules(myBoard,(5,0))