# Author: Kaia Reichard
# GitHub username: kaiathekiwi
# Date: 3/6/24
# Description: A standard chess game with falcon and hunter pieces. It does not take user input. It utilizes a ChessVar
#              class for each chess game, a ChessPiece class for chess pieces in the game, and a PawnPiece subclass of
#              ChessPiece for pawn pieces. There is no check or checkmate, and there is no castling, en passant, or
#              pawn promotion, but all other rules are the same.

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

        # initialize all chess pieces
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

        br1 = ChessPiece('b', 'r')
        br2 = ChessPiece('b', 'r')

        wr1 = ChessPiece('w', 'r')
        wr2 = ChessPiece('w', 'r')

        bk1 = ChessPiece('b', 'k')
        bk2 = ChessPiece('b', 'k')

        wk1 = ChessPiece('w', 'k')
        wk2 = ChessPiece('w', 'k')

        bb1 = ChessPiece('b', 'b')
        bb2 = ChessPiece('b', 'b')

        wb1 = ChessPiece('w', 'b')
        wb2 = ChessPiece('w', 'b')

        bk = ChessPiece('b', 'K')  # for clarity: to maintain naming conventions (lowercase vars),
        wk = ChessPiece('w', 'K')  # kings have no number to differentiate from knights

        bq = ChessPiece('b', 'q')
        wq = ChessPiece('w', 'q')

        # build the board using a dictionary
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

        # double-check if anyone has won yet--likely unnecessary if other code works 100% properly
        for index in self._white_lost_pieces:
            if index.get_piece_type() == 'K':
                self._game_state = 'BLACK_WON'

        for index in self._black_lost_pieces:
            if index.get_piece_type() == 'K':
                self._game_state = 'WHITE_WON'

        return self._game_state

    def make_move(self, moved_from, move_to):
        """Move chess piece from moved_from to move_to and update game state (if a king is taken during the move)
            and player turn (at the end of the move) accordingly. If the move isn't possible, for any reason,
            it will return False. Otherwise, it'll return True.
            Parameters: moved_from and move_to
            Returns: True or False"""
        # check for basics: if game has ended, if anything isn't on the board, if there's no piece being moved, etc.
        if self._game_state != 'UNFINISHED':
            return False
        if moved_from not in self._board or move_to not in self._board:
            return False
        if self._board[moved_from] is None:
            return False
        # this is an additional check for the piece being on the board--likely unnecessary
        if ((ord(move_to[0]) > ord('h')) or (ord(move_to[0]) < ord('a'))
                or (int(move_to[1]) > 8) or (int(move_to[1]) < 1)):
            return False

        # initialize variables used for movements
        piece = self._board[moved_from]
        piece_type = piece.get_piece_type()
        piece_color = piece.get_color()
        other_piece = self._board[move_to]

        # if the piece being moved matches the person's turn
        if (piece_color == 'w' and self._turn == 'WHITE') or (piece_color == 'b' and self._turn == 'BLACK'):
            possible_moves = []
            start_let = ord(moved_from[0])  # converts to ASCII value for incrementing
            start_num = int(moved_from[1])  # converts to int for arithmetic

            # PAWN MOVEMENT
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

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    piece.change_pawn_move()
                    return True

                # if not possible
                return False

            # ROOK MOVEMENT
            elif piece_type == 'r':

                # vertical movement
                if moved_from[0] == move_to[0]:

                    # moving up
                    for i in range((int(moved_from[1]) + 1), 9):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                    # moving down
                    for i in range((int(moved_from[1]) - 1), 0, -1):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                # horizontal movement
                elif moved_from[1] == move_to[1]:
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if self._board[str(chr(i)) + moved_from[1]] is None:
                            possible_moves.append(str(chr(i)) + moved_from[1])
                        else:
                            if self._board[(str(chr(i)) + moved_from[1])].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + moved_from[1])
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

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # KNIGHT MOVEMENT
            elif piece_type == 'k':
                # possible moves are hard-coded, although more efficient methods definitely exist.
                # and yes, I'm aware of how gross this looks.

                # for the spot that's right one and up two
                if (chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) + 2)) in self._board:
                    if self._board[chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) + 2)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) + 2))
                    elif (self._board[chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) + 2)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) + 2))

                # for the spot that's two right and up one
                if (chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) + 1)) in self._board:
                    if self._board[chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) + 1)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) + 1))
                    elif (self._board[chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) + 1)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) + 1))

                # for the spot that's two right and down one
                if (chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) - 1)) in self._board:
                    if self._board[chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) - 1)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) - 1))
                    elif (self._board[chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) - 1)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) + 2) + str(int(moved_from[1]) - 1))

                # for the spot that's one right and down two
                if (chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) - 2)) in self._board:
                    if self._board[chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) - 2)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) - 2))
                    elif (self._board[chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) - 2)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) + 1) + str(int(moved_from[1]) - 2))

                # for the spot that's one left and down two
                if (chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) - 2)) in self._board:
                    if self._board[chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) - 2)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) - 2))
                    elif (self._board[chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) - 2)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) - 2))

                # for the spot that's two left and down one
                if (chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) - 1)) in self._board:
                    if self._board[chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) - 1)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) - 1))
                    elif (self._board[chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) - 1)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) - 1))

                # for the spot that's two left and up one
                if (chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) + 1)) in self._board:
                    if self._board[chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) + 1)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) + 1))
                    elif (self._board[chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) + 1)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) - 2) + str(int(moved_from[1]) + 1))

                # for the spot that's one left and up two
                if (chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) + 2)) in self._board:
                    if self._board[chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) + 2)] is None:
                        possible_moves.append(chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) + 2))
                    elif (self._board[chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) + 2)].get_color()
                          != piece_color):
                        possible_moves.append(chr(ord(moved_from[0]) - 1) + str(int(moved_from[1]) + 2))

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # BISHOP MOVEMENT
            elif piece_type == 'b':

                # right movement
                if ord(move_to[0]) > ord(moved_from[0]):

                    # forward
                    counter = 1
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if (int(moved_from[1]) + counter) <= 8:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                    break
                            counter += 1

                    # backward
                    counter = 1
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if (int(moved_from[1]) - counter) >= 1:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                    break
                            counter += 1

                # left movement
                elif ord(move_to[0]) < ord(moved_from[0]):

                    # forward
                    counter = 1
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if (int(moved_from[1]) + counter) <= 8:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                    break
                            counter += 1

                    # backward
                    counter = 1
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if (int(moved_from[1]) - counter) >= 1:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                    break
                            counter += 1

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # KING MOVEMENT
            elif piece_type == 'K':

                # if move_to is not adjacent to moved_from
                if ((ord(move_to[0]) > (ord(moved_from[0]) + 1)) or (ord(move_to[0]) < (ord(moved_from[0]) - 1))
                        or (int(move_to[1]) > (int(moved_from[1]) + 1))
                        or (int(move_to[1]) < (int(moved_from[1]) - 1))):
                    return False

                else:

                    # if move_to is empty
                    if other_piece is None:
                        possible_moves.append(move_to)

                    # if move_to has an enemy
                    elif other_piece.get_color() != piece_color:
                        possible_moves.append(move_to)

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # QUEEN MOVEMENT
            elif piece_type == 'q':

                # vertical straight movement
                if moved_from[0] == move_to[0]:

                    # upwards movement
                    for i in range((int(moved_from[1]) + 1), 9):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                    # downwards movement
                    for i in range((int(moved_from[1]) - 1), 0, -1):
                        if self._board[moved_from[0] + str(i)] is None:
                            possible_moves.append(moved_from[0] + str(i))
                        else:
                            if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(moved_from[0] + str(i))
                                break

                # horizontal straight movement
                elif moved_from[1] == move_to[1]:

                    # right movement
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if self._board[str(chr(i)) + moved_from[1]] is None:
                            possible_moves.append(str(chr(i)) + moved_from[1])
                        else:
                            if self._board[(str(chr(i)) + moved_from[1])].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + moved_from[1])
                                break

                    # left movement
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if self._board[str(chr(i)) + moved_from[1]] is None:
                            possible_moves.append(str(chr(i)) + moved_from[1])
                        else:
                            if self._board[str(chr(i)) + moved_from[1]].get_color() == piece_color:
                                break
                            else:
                                possible_moves.append(str(chr(i)) + moved_from[1])
                                break

                # right diagonal movement
                elif ord(move_to[0]) > ord(moved_from[0]):

                    # upwards movement
                    counter = 1
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if (int(moved_from[1]) + counter) <= 8:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                    break
                            counter += 1

                    # downwards movement
                    counter = 1
                    for i in range((ord(moved_from[0]) + 1), ord('i')):
                        if (int(moved_from[1]) - counter) >= 1:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                    break
                            counter += 1

                # left movement
                elif ord(move_to[0]) < ord(moved_from[0]):

                    # upwards movement
                    counter = 1
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if (int(moved_from[1]) + counter) <= 8:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                    break
                            counter += 1

                    # downwards movement
                    counter = 1
                    for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                        if (int(moved_from[1]) - counter) >= 1:
                            if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                            else:
                                if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                        == piece_color):
                                    break
                                else:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                    break
                            counter += 1

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # FALCON MOVEMENT (forward bishop, backward rook)
            elif piece_type == 'f':

                # right movement
                if ord(move_to[0]) > ord(moved_from[0]):

                    # white forward / upwards movement
                    if piece_color == 'w':
                        counter = 1
                        for i in range((ord(moved_from[0]) + 1), ord('i')):
                            if (int(moved_from[1]) + counter) <= 8:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                        break
                                counter += 1

                    # black forward / downwards movement
                    if piece_color == 'b':
                        counter = 1
                        for i in range((ord(moved_from[0]) + 1), ord('i')):
                            if (int(moved_from[1]) - counter) >= 1:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                        break
                                counter += 1

                # left movement
                elif ord(move_to[0]) < ord(moved_from[0]):

                    # white forward / upwards movement
                    if piece_color == 'w':
                        counter = 1
                        for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                            if (int(moved_from[1]) + counter) <= 8:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                        break
                                counter += 1

                    # black forward / downwards movement
                    if piece_color == 'b':
                        counter = 1
                        for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                            if (int(moved_from[1]) - counter) >= 1:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                        break
                                counter += 1

                # straight vertical / backwards movement
                if moved_from[0] == move_to[0]:

                    # black backwards / upwards movement
                    if piece_color == 'b':
                        for i in range((int(moved_from[1]) + 1), 9):
                            if self._board[moved_from[0] + str(i)] is None:
                                possible_moves.append(moved_from[0] + str(i))
                            else:
                                if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                    break
                                else:
                                    possible_moves.append(moved_from[0] + str(i))
                                    break

                    # white backwards / downwards movement
                    if piece_color == 'w':
                        for i in range((int(moved_from[1]) - 1), 0, -1):
                            if self._board[moved_from[0] + str(i)] is None:
                                possible_moves.append(moved_from[0] + str(i))
                            else:
                                if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                    break
                                else:
                                    possible_moves.append(moved_from[0] + str(i))
                                    break

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # HUNTER MOVEMENT (forward rook, backward bishop)
            elif piece_type == 'h':

                # right movement
                if ord(move_to[0]) > ord(moved_from[0]):

                    # black backwards / upward movement
                    if piece_color == 'b':
                        counter = 1
                        for i in range((ord(moved_from[0]) + 1), ord('i')):
                            if (int(moved_from[1]) + counter) <= 8:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                        break
                                counter += 1

                    # white backwards / downwards movement
                    if piece_color == 'w':
                        counter = 1
                        for i in range((ord(moved_from[0]) + 1), ord('i')):
                            if (int(moved_from[1]) - counter) >= 1:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                        break
                                counter += 1

                # left movement
                elif ord(move_to[0]) < ord(moved_from[0]):

                    # black backwards / upward movement
                    if piece_color == 'b':
                        counter = 1
                        for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                            if (int(moved_from[1]) + counter) <= 8:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) + counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) + counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) + counter))
                                        break
                                counter += 1

                    # white backwards / downwards movement
                    if piece_color == 'w':
                        counter = 1
                        for i in range((ord(moved_from[0]) - 1), (ord('a') - 1), -1):
                            if (int(moved_from[1]) - counter) >= 1:
                                if self._board[str(chr(i)) + str(int(moved_from[1]) - counter)] is None:
                                    possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                else:
                                    if (self._board[str(chr(i)) + str(int(moved_from[1]) - counter)].get_color()
                                            == piece_color):
                                        break
                                    else:
                                        possible_moves.append(str(chr(i)) + str(int(moved_from[1]) - counter))
                                        break
                                counter += 1

                # vertical movement
                if moved_from[0] == move_to[0]:

                    # white forwards / upwards movement
                    if piece_color == 'w':
                        for i in range((int(moved_from[1]) + 1), 9):
                            if self._board[moved_from[0] + str(i)] is None:
                                possible_moves.append(moved_from[0] + str(i))
                            else:
                                if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                    break
                                else:
                                    possible_moves.append(moved_from[0] + str(i))
                                    break

                    # black forwards / downwards movement
                    if piece_color == 'b':
                        for i in range((int(moved_from[1]) - 1), 0, -1):
                            if self._board[moved_from[0] + str(i)] is None:
                                possible_moves.append(moved_from[0] + str(i))
                            else:
                                if self._board[moved_from[0] + str(i)].get_color() == piece_color:
                                    break
                                else:
                                    possible_moves.append(moved_from[0] + str(i))
                                    break

                # if the desired move is possible
                if move_to in possible_moves:

                    # check if the game ended and switch turns if black
                    if piece_color == 'b':
                        if other_piece is not None:
                            self._white_lost_pieces.append(other_piece)
                            for index in self._white_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'BLACK_WON'
                                    return True
                        self._turn = 'WHITE'

                    # check if the game ended and switch turns if white
                    if piece_color == 'w':
                        if other_piece is not None:
                            self._black_lost_pieces.append(other_piece)
                            for index in self._black_lost_pieces:
                                if index.get_piece_type() == 'K':
                                    self._game_state = 'WHITE_WON'
                                    return True
                        self._turn = 'BLACK'

                    # move piece
                    self._board[move_to] = self._board[moved_from]
                    self._board[moved_from] = None
                    return True

                # if not possible
                return False

            # if the piece isn't a type that works in the game
            else:
                return False

    def enter_fairy_piece(self, piece_type, move_to):
        """Enter a falcon/hunter piece at move_to if it is legal to do so, then update the player turn accordingly
            and return True. If that isn't possible, for any reason, it will return False.
            Parameters: piece_type and move_to
            Returns: True or False"""

        # check for basics: if game has ended, if anything isn't on the board, if the spot isn't empty, etc.
        if self._game_state != 'UNFINISHED':
            return False
        if move_to not in self._board:
            return False
        if self._board[move_to] is not None:
            return False

        # white fairy piece
        if (piece_type == 'F' or piece_type == 'H') and self._turn == 'WHITE':

            # if the max fairies have already been placed
            if self._white_fairy_count == 2:
                return False

            # counts how many special pieces have already been lost
            temp_count = 0
            for piece in self._white_lost_pieces:
                if piece.get_piece_type() != 'p' and piece.get_piece_type() != 'h' and piece.get_piece_type() != 'f':
                    temp_count += 1

            # if it's the first fairy, placed in home ranks, and at least one special piece has been lost
            if (self._white_fairy_count == 0) and (int(move_to[1]) <= 2) and (temp_count >= 1):

                # if a falcon piece is available and has been picked
                if piece_type == 'F' and self._white_falcon_stored is True:
                    wf1 = ChessPiece('w', 'f')
                    self._board[move_to] = wf1
                    self._white_falcon_stored = False

                # if a hunter piece is available and has been picked
                elif piece_type == 'H' and self._white_hunter_stored is True:
                    wh1 = ChessPiece('w', 'h')
                    self._board[move_to] = wh1
                    self._white_hunter_stored = False

                else:
                    return False

                # change turn and add to fairy count
                self._turn = 'BLACK'
                self._white_fairy_count += 1
                return True

            # if it's the second fairy, placed in home ranks, and at least two special pieces have been lost
            elif (self._white_fairy_count == 1) and (int(move_to[1]) <= 2) and (temp_count >= 2):

                # if a falcon piece is available and has been picked
                if piece_type == 'F' and self._white_falcon_stored is True:
                    wf1 = ChessPiece('w', 'f')
                    self._board[move_to] = wf1
                    self._white_falcon_stored = False

                # if a hunter piece is available and has been picked
                elif piece_type == 'H' and self._white_hunter_stored is True:
                    wh1 = ChessPiece('w', 'h')
                    self._board[move_to] = wh1
                    self._white_hunter_stored = False

                else:
                    return False

                # notify the user of reaching limit, change turn, and add to fairy count
                print("White cannot place anymore fairy pieces.")
                self._turn = 'BLACK'
                self._white_fairy_count += 1
                return True

            else:
                return False

        # black fairy piece
        elif (piece_type == 'f' or piece_type == 'h') and self._turn == 'BLACK':

            # if the max fairies have already been placed
            if self._black_fairy_count == 2:
                return False

            # counts how many special pieces have already been lost
            temp_count = 0
            for piece in self._black_lost_pieces:
                if piece.get_piece_type() != 'p' and piece.get_piece_type() != 'h' and piece.get_piece_type() != 'f':
                    temp_count += 1

            # if it's the first fairy, placed in home ranks, and at least one special piece has been lost
            if (self._black_fairy_count == 0) and (int(move_to[1]) >= 7) and (temp_count >= 1):

                # if a falcon piece is available and has been picked
                if piece_type == 'f' and self._black_falcon_stored is True:
                    bf1 = ChessPiece('b', 'f')
                    self._board[move_to] = bf1
                    self._black_falcon_stored = False

                # if a hunter piece is available and has been picked
                elif piece_type == 'h' and self._black_hunter_stored is True:
                    bh1 = ChessPiece('b', 'h')
                    self._board[move_to] = bh1
                    self._black_hunter_stored = False

                else:
                    return False

                # change turn and add to fairy count
                self._turn = 'WHITE'
                self._black_fairy_count += 1
                return True

            # if it's the second fairy, placed in home ranks, and at least two special pieces have been lost
            elif (self._black_fairy_count == 1) and (int(move_to[1]) >= 7) and (temp_count >= 2):

                # if a falcon piece is available and has been picked
                if piece_type == 'f' and self._black_falcon_stored is True:
                    bf1 = ChessPiece('b', 'f')
                    self._board[move_to] = bf1
                    self._black_falcon_stored = False

                # if a hunter piece is available and has been picked
                elif piece_type == 'h' and self._black_hunter_stored is True:
                    bh1 = ChessPiece('b', 'h')
                    self._board[move_to] = bh1
                    self._black_hunter_stored = False

                else:
                    return False

                # notify the user of reaching limit, change turn, and add to fairy count
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
            I did use the internet a bit for this part (to make it prettier for myself), since it isn't graded,
            I wasn't too worried."""

        # initialize colors and count vars
        reset = "\033[0m"
        black = "\033[30m"
        white = "\033[37m"
        error_color = "\033[1;95;38;5;200m"
        count = 0

        # for each spot in the dictionary, print it out pretty!!
        for key, value in self._board.items():
            text = str(value)

            # start new line every 8 spots
            if count == 8:
                print("\n")
                count = 0

            # if the value is a list rather than one thing
            if isinstance(value, list):
                print("[", end=" ")
                for index in value:
                    print(f"{error_color}{index}{reset}", end=" ")
                print("]", end=" ")

            # if it's a black piece
            elif text[0] == 'b':
                print(f"[{black}{text}{reset}]", end=" ")

            # if it's a white piece
            elif text[0] == 'w':
                print(f"[{white}{text}{reset}]", end=" ")

            # if it's None
            else:
                print("[  ]", end=" ")

            # count each thing being printed
            count += 1

        # print the turn
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
        """Return the string representation of a chess piece with its color and piece type.
            Parameters: None
            Returns: str(self._color + self._piece_type)"""
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
    """A PawnPiece object represents a pawn piece, which is a subclass of ChessPiece. It is responsible for
    everything a ChessPiece object can do and keeping track of/changing pawn_move. It will need to communicate with
    the ChessVar class in order to check if moves are legal/illegal and to display the board."""

    def __init__(self, color):
        """Initialize a pawn piece with a color and type. Utilizes superclass init method.
            Parameters: color
            Returns: None"""
        super().__init__(color, 'p')
        self.pawn_move = True

    def __str__(self):
        """Return the string representation of a chess piece with its color and piece type.
            Utilizes superclass str method.
            Parameters: None
            Returns: None"""
        return super().__str__()

    def get_color(self):
        """Return the color of the piece, being black or white.
            Utilizes superclass get_color method.
            Parameters: None
            Returns: color"""
        return super().get_color()

    def get_piece_type(self):
        """Return the type of piece, being a rook, knight, bishop, queen, king, pawn, hunter, or falcon.
            Utilizes superclass get_piece_type method.
            Parameters: None
            Returns: piece_type"""
        return super().get_piece_type()

    def get_pawn_move(self):
        """Return the pawn move, such as if it can move forward twice.
            Parameters: None
            Returns: self._pawn_move"""
        return self.pawn_move

    def change_pawn_move(self):
        """Change the pawn move to false.
            Parameters: None
            Returns: None"""
        self.pawn_move = False
