import random
class Board():


    def __init__(self):
        self.red = "r"
        self.black = "b"
        self.redK = "R"
        self.blackK = "B"
        self.empty = "."
        self.board = [
                        [".", "b", ".", "b", ".", "b", ".", "b"],
                        ["b", ".", "b", ".", "b", ".", "b", "."],
                        [".", "b", ".", "b", ".", "b", ".", "b"],
                        [".", ".", ".", ".", ".", ".", ".", "."],
                        [".", ".", ".", ".", ".", ".", ".", "."],
                        ["r", ".", "r", ".", "r", ".", "r", "."],
                        [".", "r", ".", "r", ".", "r", ".", "r"],
                        ["r", ".", "r", ".", "r", ".", "r", "."],
                    ]
    def printBoard(self):
        print("\n")
        for row in range(len(self.board)):
            print(" ")
            for col in range(len(self.board[row])):
                if self.board[row][col] == '.':
                    print("⬜",end = '')
                elif self.board[row][col] == 'b':
                    print("⚫", end = '',)
                elif self.board[row][col] == 'r':
                    print("🔴", end = '',)
    def getPiece(self,position):

    
        return self.board[position[0]][position[1]]

    def movePiece(self, piecePos, movePos):
        piece = self.getPiece(piecePos)

        if piece in ('r', 'R'):
            player = 'r'
        elif piece in ('b', 'B'):
            player = 'b'
        else:
            print("There is no piece there.")
            return

        legalMoves = self.getLegalMoves(player)

        if (piecePos, movePos) not in legalMoves:
            print("not a move")
            return

        # Move the piece
        self.board[piecePos[0]][piecePos[1]] = self.empty

        # If it's a jump, remove the captured piece
        if abs(piecePos[0] - movePos[0]) == 2:
            capturedRow = (piecePos[0] + movePos[0]) // 2
            capturedCol = (piecePos[1] + movePos[1]) // 2

            self.board[capturedRow][capturedCol] = self.empty

        self.board[movePos[0]][movePos[1]] = piece

        self.printBoard()
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
    def randOpp(self,player):
        if player =='b':
            move = self.getLegalMoves('b')
            rand = random.randint(0,len(move))
            piecePos, movePos = move[rand]
            self.movePiece(piecePos,movePos)
    def startGame(self):
        stop =False
        playerColor = input("\nPick Red or Black: ")
        while not stop:

            if playerColor == "Red":
                print("Legal Moves:")
                print(*(self.getLegalMoves('r') + self.getLegalMoves('R')), sep='\n')
                piecePos = tuple(map(int, input("\nPick a Piece: ").split()))
                movePos = tuple(map(int, input("\nTo Where?: ").split()))
                myBoard.movePiece(piecePos, movePos)
                self.randOpp('b')







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