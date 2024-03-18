RESET = "\033[0m"
BLACK = "\033[30m"
WHITE = "\033[37m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"


def print_colored_pieces(board):
    for row in board:
        for piece in row:
            if piece.isupper():
                color = WHITE if piece.isupper() else YELLOW
                print(f"{color}{piece}{RESET}", end=" ")
            elif piece.islower():
                color = BLACK if piece.islower() else YELLOW
                print(f"{color}{piece}{RESET}", end=" ")
            else:
                print(piece, end=" ")
        print()


# Example usage
board1 = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

print_colored_pieces(board1)

board2 = {
            'a1': 'john', 'b1': 'sara', 'c1': 'bob'
        }

print(board2['d1'])
