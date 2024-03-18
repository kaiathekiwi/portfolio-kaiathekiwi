# Author: Kaia Reichard
# GitHub username: kaiathekiwi
# Date: 3/6/24
# DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS:
# 2. Keeping track of turn order:
#       - Turn order is tracked by self.turn and alternates after each turn
#       - self.turn is updated within either make_move or enter_fairy_piece at the end, unless they return False
#       - Once the move is completed or the fairy piece has entered, the turn order will change
#       - If self.turn is equal to 'WHITE' it will be set equal to 'BLACK'
#       - If self.turn is equal to 'BLACK' it will be set equal to 'WHITE'
# 3. Keeping track of the current board position:
#       - The current position of a piece on the board is tracked by a dictionary in the format
#         {position : 'ChessPiece object name'}
#       - initialize_board will create a dictionary for each spot on the board, where the keys are a letter and number
#       - The values are the ChessPiece object's name. For example, {a8 : 'black_rook1'}
#       - initialize_board will put the correct pieces in each spot for the start of the game and create ChessPiece
#         objects
#       - make_move will update the dictionary whenever a piece is moved by removing the value from the original spot
#         and adding the piece as a value in the new spot
#       - enter_fairy_piece will update the dictionary by putting the new piece as a value at the chosen position
#       - make_move will remove the enemy piece at the position a piece is moving to from the dictionary if a piece
#         is taken
# 4. Determining if a regular move is valid:
#       - Check self.game_state and return False if it's not 'UNFINISHED'
#       - Check if it is the correct player's turn. If not, return False
#       - Check if moved_from is on the board and check if move_to is on the board. If not, return False
#       - Check if the color of the piece being moved matches the turn counter. If not, return False
#       - Check the piece type and come up with which positions are legal moves for that piece (which will vary). If
#         the move_to is not one of those positions, return False
#       - Check if there is a piece of the same color at move_to. If there is, return False
# 5. Determining if a fairy piece entering move is valid:
#       - Check self.game_state and return False if it's not 'UNFINISHED'
#       - Check if move_to is on the board. If not, return False
#       - Check if move_to is in the home ranks. If not, return False
#       - Check if it is the correct player's turn. If not, return False
#       - Check if self.(color)_fairy_count is equal to 2, where (color) is the color of the player's turn. If it's 2,
#         return False
#       - Iterate through self.(color)_lost to check if a queen, rook, bishop, or knight has been lost.
#         If not, return False.
#       - Check if self.(color)_fairy_count is equal to 1. If so, iterate through self.(color)_lost if two pieces that
#         are a queen, rook, bishop, or knight have been lost. If not, return false.

# KEY: Each chess piece is represented by a letter (usually the first letter of their name), a number, and their color
#   which is represented by 'b' or 'w'. Kings are represented with a 'K', whereas knights are represented by 'k'
#   Pawn: p
#   Rook: r
#   Knight: k
#   Bishop: b
#   King: K
#   Queen: q
#   Falcon: f
#   Hunter: h

# Example: bp1 = Pawn('black') is the first black pawn
class ChessVar:
    """A ChessVar object represents a chess game. It is responsible for keeping track of the board, the
        game state, what moves are legal/illegal, which pieces have been lost, and entering the fairy pieces.
        It will need to communicate with the ChessPiece class to keep track of the types of chess pieces and colors."""
    def __init__(self):
        """Initialize a chess game object with a board, a turn string, a list of lost pieces for white and black,
            the game state, and two counters for the number of fairy pieces in play (to maintain maximums).
            It will also have a boolean for each fairy piece, to ensure no duplicates.
            Parameters: None
            Returns: None"""
        self._board = {}
        self._turn = 'WHITE'
        self._white_lost_pieces = []
        self._black_lost_pieces = []
        self._white_fairy_count = 0  # for fairy count in play
        self._black_fairy_count = 0
        self._black_falcon_stored = True  # for fairy pieces not in play
        self._white_falcon_stored = True
        self._black_hunter_stored = True
        self._white_hunter_stored = True
        self._game_state = 'UNFINISHED'
        self.initialize_board()

    def initialize_board(self):
        """Create a board with the columns represented by letters and the rows represented by numbers
            for the start of the game. Each spot on the board has a column and a row. It will also create ChessPiece
            objects and place them at their starting spots.
            Parameters: None
            Returns: None"""

        bp1 = PawnPiece('b')
        bp2 = PawnPiece('b')
        bp3 = PawnPiece('b')
        bp4 = PawnPiece('b')
        bp5 = PawnPiece('b')
        bp6 = PawnPiece('b')
        bp7 = PawnPiece('b')
        bp8 = PawnPiece('b')

        wp1 = PawnPiece('w')
        wp2 = PawnPiece('w')
        wp3 = PawnPiece('w')
        wp4 = PawnPiece('w')
        wp5 = PawnPiece('w')
        wp6 = PawnPiece('w')
        wp7 = PawnPiece('w')
        wp8 = PawnPiece('w')

        br1 = RookPiece('b')
        br2 = RookPiece('b')

        wr1 = RookPiece('w')
        wr2 = RookPiece('w')

        bk1 = KnightPiece('b')
        bk2 = KnightPiece('b')

        wk1 = KnightPiece('w')
        wk2 = KnightPiece('w')

        bb1 = BishopPiece('b')
        bb2 = BishopPiece('b')

        wb1 = BishopPiece('w')
        wb2 = BishopPiece('w')

        bk = KingPiece('b')  # this may be confusing, so for clarity: to maintain naming conventions (lowercase vars),
        wk = KingPiece('w')     # kings have no number to differentiate from knights

        bq = QueenPiece('b')
        wq = QueenPiece('w')

        self._board = {
            'a8': br1, 'b8': bk1, 'c8': bb1, 'd8': bq, 'e8': bk, 'f8': bb2, 'g8': bk2, 'h8': br2,
            'a7': bp1, 'b7': bp2, 'c7': bp3, 'd7': bp4, 'e7': bp5, 'f7': bp6, 'g7': bp7, 'h7': bp8,
            'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None, 'g6': None, 'h6': None,
            'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None, 'g5': None, 'h5': None,
            'a4': None, 'b4': None, 'c4': None, 'd4': None, 'e4': None, 'f4': None, 'g4': None, 'h4': None,
            'a3': None, 'b3': None, 'c3': None, 'd3': None, 'e3': None, 'f3': None, 'g3': None, 'h3': None,
            'a2': wp1, 'b2': wp2, 'c2': wp3, 'd2': wp4, 'e2': wp5, 'f2': wp6, 'g2': wp7, 'h2': wp8,
            'a1': wr1, 'b1': wk1, 'c1': wb1, 'd1': wq, 'e1': wk, 'f1': wb2, 'g1': wk2, 'h1': wr2
        }

    def get_game_state(self):
        """Return unfinished when a game is in progress, or which color won if the game is over.
            Parameters: None
            Returns: 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'"""

        for index in self._white_lost_pieces:
            if index.get_piece_type() == 'K':
                self._game_state = 'BLACK_WON'
        for index in self._black_lost_pieces:
            if index.get_piece_type() == 'K':
                self._game_state = 'WHITE_WON'
        return self._game_state

    # 4. Determining if a regular move is valid:
    #       - Check the piece type and come up with which positions are legal moves for that piece (which will vary). If
    #         the move_to is not one of those positions, return False
    #       - Check that nothing is in the path when validating piece moves
    def make_move(self, moved_from, move_to):
        """Move chess piece from moved_from to move_to and update game state (if a king is taken during the move)
            and player turn (at the end of the move) accordingly. If the move isn't possible, for any reason,
            it will return False. Otherwise, it'll return True.
            Parameters: moved_from and move_to
            Returns: True or False"""
        if self._game_state != 'UNFINISHED':
            return False
        if moved_from not in self._board or move_to not in self._board:
            return False
        if self._board[moved_from] is None:
            return False
        piece = self._board[moved_from]
        piece_type = piece.get_piece_type()
        piece_color = piece.get_color()
        other_piece = self._board[move_to]
        if (piece_color == 'w' and self._turn == 'WHITE') or (piece_color == 'b' and self._turn == 'BLACK'):
            # if the piece being moved matches the person's turn
            possible_moves = []
            start_let = ord(moved_from[0])  # converts to ASCII value for incrementing
            start_num = int(moved_from[1])
            if piece_type == 'p':
                if piece_color == 'w':
                    # if it can move forward 1
                    if (start_num + 1) <= 8 and (self._board[str(chr(start_let) + str(start_num + 1))] is None):
                        possible_moves.append(str(chr(start_let) + str(start_num + 1)))

                        # if it can move forward 2
                        if (piece.get_pawn_move() is True and (start_num + 2) <= 8 and
                                (self._board[str(chr(start_let) + str(start_num + 2))] is None)):
                            possible_moves.append(str(chr(start_let) + str(start_num + 2)))

                    # if it can move diagonal left
                    if ((start_let - 1) >= ord('a') and
                            (self._board[str(chr(start_let - 1) + str(start_num + 1))] is not None)):
                        if self._board[str(chr(start_let - 1) + str(start_num + 1))].get_color() != piece_color:
                            possible_moves.append(str(chr(start_let - 1) + str(start_num + 1)))

                    # if it can move diagonal right
                    if ((start_let + 1) <= ord('h') and
                            (self._board[str(chr(start_let + 1) + str(start_num + 1))] is not None)):
                        if self._board[str(chr(start_let + 1) + str(start_num + 1))].get_color() != piece_color:
                            possible_moves.append(str(chr(start_let + 1) + str(start_num + 1)))
                elif piece_color == 'b':
                    # if it can move forward 1
                    if (start_num - 1) >= 1 and (self._board[str(chr(start_let) + str(start_num - 1))] is None):
                        possible_moves.append(str(chr(start_let) + str(start_num - 1)))

                        # if it can move forward 2
                        if (piece.get_pawn_move() is True and (start_num - 2) >= 1 and
                                (self._board[str(chr(start_let) + str(start_num - 2))] is None)):
                            possible_moves.append(str(chr(start_let) + str(start_num - 2)))

                    # if it can move diagonal left
                    if ((start_let - 1) >= ord('a') and
                            (self._board[str(chr(start_let - 1) + str(start_num - 1))] is not None)):
                        if self._board[str(chr(start_let - 1) + str(start_num - 1))].get_color() != piece_color:
                            possible_moves.append(str(chr(start_let - 1) + str(start_num - 1)))

                    # if it can move diagonal right
                    if ((start_let + 1) <= ord('h') and
                            (self._board[str(chr(start_let + 1) + str(start_num - 1))] is not None)):
                        if self._board[str(chr(start_let + 1) + str(start_num - 1))].get_color() != piece_color:
                            possible_moves.append(str(chr(start_let + 1) + str(start_num - 1)))

                if move_to in possible_moves:
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        else:
                            self._turn = 'WHITE'
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        else:
                            self._turn = 'BLACK'
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    piece.change_pawn_move()
                    return True
                return False

            elif piece_type == 'r':
                # vertical movement
                if moved_from[0] == move_to[0]:
                    for i in range((int(moved_from[1]) + 1), 9):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                    for i in range((int(moved_from[1]) - 1), 0, -1):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                    if move_to in possible_moves:
                        if piece_color == 'b':
                            if other_piece is not None:
                                self._white_lost_pieces.append(other_piece)
                                for index in self._white_lost_pieces:
                                    if index.get_piece_type() == 'K':
                                        self._game_state = 'BLACK_WON'
                                        return True
                            else:
                                self._turn = 'WHITE'
                        if piece_color == 'w':
                            if other_piece is not None:
                                self._black_lost_pieces.append(other_piece)
                                for index in self._black_lost_pieces:
                                    if index.get_piece_type() == 'K':
                                        self._game_state = 'WHITE_WON'
                                        return True
                            else:
                                self._turn = 'BLACK'
                        self._board[move_to] = self._board[moved_from]
                        self._board[moved_from] = None
                        return True

                    return False

                # horizontal movement
                elif moved_from[1] == move_to[1]:
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if self._board[str(chr(i)) + moved_from[1]] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if self._board[str(chr(i)) + moved_from[1]] is None:
                            possible_moves.append(str(chr(i)) + moved_from[1])
                        else:
                            if self._board[str(chr(i)) + moved_from[1]].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + moved_from[1])
                                break

                    if move_to in possible_moves:
                        if piece_color == 'b':
                            if other_piece is not None:
                                self._white_lost_pieces.append(other_piece)
                                for index in self._white_lost_pieces:
                                    if index.get_piece_type() == 'K':
                                        self._game_state = 'BLACK_WON'
                                        return True
                            else:
                                self._turn = 'WHITE'
                        if piece_color == 'w':
                            if other_piece is not None:
                                self._black_lost_pieces.append(other_piece)
                                for index in self._black_lost_pieces:
                                    if index.get_piece_type() == 'K':
                                        self._game_state = 'WHITE_WON'
                                        return True
                            else:
                                self._turn = 'BLACK'
                        self._board[move_to] = self._board[moved_from]
                        self._board[moved_from] = None
                        return True
                    return False
                else:
                    return False
            elif piece_type == 'k':
                pass
            elif piece_type == 'b':
                # right movement
                if ord(move_to[0]) > ord(moved_from[0]):
                    counter = 1
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                            possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                        else:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                break
                        counter += 1

                # left movement
                elif ord(move_to[0]) < ord(moved_from[0]):
                    counter = 1
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                            possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                        else:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                break
                        counter += 1

                if move_to in possible_moves:
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        else:
                            self._turn = 'WHITE'
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        else:
                            self._turn = 'BLACK'
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True
                return False

            elif piece_type == 'K':
                pass
            elif piece_type == 'q':
                pass
            elif piece_type == 'f':
                # right movement
                if ord(move_to[0]) > ord(moved_from[0]) and piece_color == 'w':
                    counter = 1
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                            possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                        else:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                break
                        counter += 1

                # left movement
                if ord(move_to[0]) < ord(moved_from[0]) and piece_color == 'w':
                    counter = 1
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                            possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                        else:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                break
                        counter += 1

                # backward movement
                if moved_from[0] == move_to[0] and piece_color == 'b':
                    for i in range((int(moved_from[1]) + 1), 9):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                if moved_from[0] == move_to[0] and piece_color == 'w':
                    for i in range((int(moved_from[1]) - 1), 0, -1):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                if move_to in possible_moves:
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        else:
                            self._turn = 'WHITE'
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        else:
                            self._turn = 'BLACK'
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                return False

            elif piece_type == 'h':
                # forward movement
                if moved_from[0] == move_to[0] and piece_color == 'w':
                    for i in range((int(moved_from[1]) + 1), 9):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                if moved_from[0] == move_to[0] and piece_color == 'b':
                    for i in range((int(moved_from[1]) - 1), 0, -1):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                if move_to in possible_moves:
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        else:
                            self._turn = 'WHITE'
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        else:
                            self._turn = 'BLACK'
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                return False

            else:
                return False

                # for switching pieces after the move is generally validated
            if other_piece is not None:
                if other_piece.get_color() == piece_color:  # if the same color
                    return False
                else:
                    if piece_color == 'b':
                        self._white_lost_pieces.append(other_piece)
                        self._turn = 'WHITE'
                    if piece_color == 'w':
                        self._black_lost_pieces.append(other_piece)
                        self._turn = 'BLACK'
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

    def enter_fairy_piece(self, piece_type, move_to):
        """Enter a falcon/hunter piece at move_to if it is legal to do so, then update the player turn accordingly.
            If that isn't possible, for any reason, it will return False. Otherwise, it'll return True.
            Parameters: piece_type and move_to
            Returns: True or False"""
        if self._game_state != 'UNFINISHED':
            return False
        if move_to not in self._board:
            return False
        if self._board[move_to] is not None:
            return False

        # white fairy piece
        if (piece_type == 'F' or piece_type == 'H') and self._turn == 'WHITE':
            if self._white_fairy_count == 2:
                return False
            temp_count = 0
            for piece in self._white_lost_pieces:
                if piece.get_piece_type() != 'p' and piece.get_piece_type() != 'h' and piece.get_piece_type() != 'f':
                    temp_count += 1
            if (self._white_fairy_count == 0) and (int(move_to[1]) <= 2) and (temp_count >= 1):
                if piece_type == 'F' and self._white_falcon_stored is True:
                    wf1 = FalconPiece('w')
                    self._board[move_to] = wf1
                    self._white_falcon_stored = False
                elif piece_type == 'H' and self._white_hunter_stored is True:
                    wh1 = HunterPiece('w')
                    self._board[move_to] = wh1
                    self._white_hunter_stored = False
                else:
                    return False
                self._turn = 'BLACK'
                self._white_fairy_count += 1
                return True
            elif (self._white_fairy_count == 1) and (int(move_to[1]) <= 2) and (temp_count >= 2):
                if piece_type == 'F' and self._white_falcon_stored is True:
                    wf1 = FalconPiece('w')
                    self._board[move_to] = wf1
                    self._white_falcon_stored = False
                elif piece_type == 'H' and self._white_hunter_stored is True:
                    wh1 = HunterPiece('w')
                    self._board[move_to] = wh1
                    self._white_hunter_stored = False
                else:
                    return False
                print("White cannot place anymore fairy pieces.")
                self._turn = 'BLACK'
                self._white_fairy_count += 1
                return True
            else:
                return False

        # black fairy piece
        elif (piece_type == 'f' or piece_type == 'h') and self._turn == 'BLACK':
            if self._black_fairy_count == 2:
                return False
            temp_count = 0
            for piece in self._black_lost_pieces:
                if piece.get_piece_type() != 'p' and piece.get_piece_type() != 'h' and piece.get_piece_type() != 'f':
                    temp_count += 1
            if (self._black_fairy_count == 0) and (int(move_to[1]) >= 7) and (temp_count >= 1):
                if piece_type == 'f' and self._black_falcon_stored is True:
                    bf1 = FalconPiece('b')
                    self._board[move_to] = bf1
                    self._black_falcon_stored = False
                elif piece_type == 'h' and self._black_hunter_stored is True:
                    bh1 = HunterPiece('b')
                    self._board[move_to] = bh1
                    self._black_hunter_stored = False
                else:
                    return False
                self._turn = 'WHITE'
                self._black_fairy_count += 1
                return True
            elif (self._black_fairy_count == 1) and (int(move_to[1]) >= 7) and (temp_count >= 2):
                if piece_type == 'f' and self._black_falcon_stored is True:
                    bf1 = FalconPiece('b')
                    self._board[move_to] = bf1
                    self._black_falcon_stored = False
                elif piece_type == 'h' and self._black_hunter_stored is True:
                    bh1 = HunterPiece('b')
                    self._board[move_to] = bh1
                    self._black_hunter_stored = False
                else:
                    return False
                print("Black cannot place anymore fairy pieces.")
                self._turn = 'WHITE'
                self._black_fairy_count += 1
                return True
            else:
                return False
        else:
            return False

    def display_board(self):
        """Print the current board with the pieces in play. It will do so by printing the string representation of each
            object, meaning it does not include a number. Each piece will print in color, with errors (such as two
            pieces on the same spot) will print in bright magenta.
            Parameters: None
            Returns: None
            Note: Since this part isn't required and only for personal checking, I'm not worrying about legibility.
            I did use the internet a bit for this part, but again, since it isn't graded, I wasn't too worried."""
        reset = "\033[0m"
        black = "\033[30m"
        white = "\033[37m"
        error_color = "\033[1;95;38;5;200m"
        count = 0

        for key, value in self._board.items():
            text = str(value)
            if count == 8:
                print("\n")
                count = 0
            if isinstance(value, list):
                print("[", end=" ")
                for index in value:
                    print(f"{error_color}{index}{reset}", end=" ")
                print("]", end=" ")
            elif text[0] == 'b':
                print(f"[{black}{text}{reset}]", end=" ")
            elif text[0] == 'w':
                print(f"[{white}{text}{reset}]", end=" ")
            else:
                print("[  ]", end=" ")
            count += 1
        print(self._turn)


class ChessPiece:
    """A ChessPiece object represents a chess piece. It is responsible for keeping track of the color
        and type of chess piece. It will need to communicate with the ChessVar class in order to check if moves are
        legal/illegal and to display the board."""
    def __init__(self, color, piece_type):
        """Initialize a chess piece with a color and type.
            Parameters: color and piece_type
            Returns: None"""
        self._color = color
        self._piece_type = piece_type

    def __str__(self):
        return str(self._color + self._piece_type)

    def get_piece_type(self):
        """Return the type of piece, being a rook, knight, bishop, queen, king, pawn, hunter, or falcon.
            Parameters: None
            Returns: piece_type"""
        return self._piece_type

    def get_color(self):
        """Return the color of the piece, being black or white.
            Parameters: None
            Returns: color"""
        return self._color


class PawnPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'p')
        self.pawn_move = True

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()

    def get_pawn_move(self):
        return self.pawn_move

    def change_pawn_move(self):
        self.pawn_move = False


class RookPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'r')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


class KnightPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'k')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


class BishopPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'b')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


class KingPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'K')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


class QueenPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'q')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


class FalconPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'f')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


class HunterPiece(ChessPiece):
    def __init__(self, color):
        super().__init__(color, 'h')

    def __str__(self):
        return super().__str__()

    def get_color(self):
        return super().get_color()

    def get_piece_type(self):
        return super().get_piece_type()


game1 = ChessVar()
game1.display_board()
print(game1.get_game_state())
game1.make_move('f1', 'a6')
game1.display_board()
