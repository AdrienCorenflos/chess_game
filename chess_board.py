from .settings import Colour
from .chess_piece import *

def takewhile(fun, iterable):
    iterator = iter(iterable)
    while True:
        value = next(iterator)
        if not fun(value):
            yield value
            return
        yield value


class ChessBoard(object):
    def __init__(self):
        board = [[None] * 8 for _ in range(8)]
        board[0] = self.first_line(Colour.black)
        board[1] = self.second_line(Colour.black)

        board[-2] = self.second_line(Colour.white)
        board[-1] = self.first_line(Colour.white)

        self.board = board

        self.whose_turn = Colour.white
        self.finished = False

    @staticmethod
    def first_line(colour):
        if colour == Colour.black:
            x = 0
        else:
            x = 7
        king = King(position=(x, 3), colour=colour)
        queen = Queen(position=(x, 4), colour=colour)
        bishop_king = Bishop(position=(x, 2), colour=colour)
        bishop_queen = Bishop(position=(x, 5), colour=colour)
        knight_king = Knight(position=(x, 1), colour=colour)
        knight_queen = Knight(position=(x, 6), colour=colour)
        tower_king = Tower(position=(x, 0), colour=colour)
        tower_queen = Tower(position=(x, 7), colour=colour)

        return [tower_king, knight_king, bishop_king, king, queen, bishop_queen, knight_queen, tower_queen]

    @staticmethod
    def second_line(colour):
        if colour == Colour.black:
            x = 1

        else:
            x = 6

        return [Pawn(position=(x, y), colour=colour) for y in range(8)]

    # def dump_dead(self):
    #     for line in self.board:
    #         for piece in line:
    #             if piece is not None:
    #                 if not piece.alive:
    #                     piece = None

    def switch_turn(self):
        if self.whose_turn == Colour.white:
            self.whose_turn = Colour.black
        else:
            self.whose_turn = Colour.white

    def display(self):
        print(self.board)

    def get_piece(self, position):
        if not (0 <= position[0] <= 7 and 0 <= position[1] <= 7):
            return "out"
        return self.board[position[0]][position[1]]

    def get_possibilities(self, piece):
        x, y = piece.position

        def stop_at_piece(direction):
            take_move = dict()
            places = [position for position in takewhile(lambda z: self.get_piece(z) is None, direction)]
            last_place = self.get_piece(places[-1])
            if isinstance(last_place, str):
                take_move["take"] = set()
                take_move["move"] = set(places[:-1])
            else:
                if last_place.colour == piece.colour:
                    take_move["take"] = set()
                    take_move["move"] = set(places[:-1])

                else:
                    take_move["take"] = {places[-1]}
                    take_move["move"] = set(places[:-1])
            return take_move

        north = stop_at_piece([(x - i, y) for i in range(1, 9)])

        south = stop_at_piece([(x + i, y) for i in range(1, 9)])

        west = stop_at_piece([(x, y - i) for i in range(1, 9)])

        east = stop_at_piece([(x, y + i) for i in range(1, 9)])

        north_west = stop_at_piece([(x - i, y - i) for i in range(1, 9)])

        north_east = stop_at_piece([(x - i, y + i) for i in range(1, 9)])

        south_west = stop_at_piece([(x + i, y - i) for i in range(1, 9)])

        south_east = stop_at_piece([(x + i, y + i) for i in range(1, 9)])

        final_take_move = {"take": set(),
                           "move": set()}

        for direction in [north, south, west, east, north_west, north_east, south_west, south_east]:
            final_take_move["take"].update(direction["take"])
            final_take_move["move"].update(direction["move"])

        return final_take_move

    def possible_moves_one_piece(self, piece):
        possible_moves = piece.move_rules
        possible_takes = piece.take_rules

        if piece.is_knight:
            for position in possible_moves.copy():
                if self.get_piece(position) is None:
                    possible_takes -= {position}

                elif self.get_piece(position).colour == piece.colour:
                    possible_moves -= {position}
                    possible_takes -= {position}

                else:
                    possible_moves -= {position}

        else:
            possilities = self.get_possibilities(piece)
            possible_moves = possible_moves.intersection(possilities["move"])
            possible_takes = possible_takes.intersection(possilities["take"])

        return {"move": possible_moves,
                "take": possible_takes}

    def play_one_turn(self, piece, position, display=True):
        assert self.whose_turn == piece.colour, "Not your turn to play"
        possibilities = self.possible_moves_one_piece(piece)
        possible_moves = possibilities["move"]
        possible_takes = possibilities["take"]

        if position in possible_moves:
            self.board[piece.position[0]][piece.position[1]] = None
            piece.move(position)
            self.board[position[0]][position[1]] = piece

        elif position in possible_takes:
            self.board[piece.position[0]][piece.position[1]] = None
            opponent_piece = self.get_piece(position)
            piece.take(opponent_piece)
            self.board[position[0]][position[1]] = piece
        #
        # self.dump_dead()
        self.switch_turn()

        if display:
            self.display()



