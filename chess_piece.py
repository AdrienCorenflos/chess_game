from moves import *


def combine_positions(*positions):
    return set.union(*positions)


class ChessPiece(object):
    def __init__(self, position, colour):
        self.position = position
        self._colour = colour
        self.alive = True
        self.is_knight = False

        self.limited_diagonal = Diagonal(distance=1)
        self.unlimited_diagonal = Diagonal(distance=8)
        self.limited_straight = Straight(distance=1)
        self.unlimited_straight = Straight(distance=8)
        self.forward_straight = ForwardStraight(distance=1, colour=colour)
        self.forward_straight_2 = ForwardStraight(distance=2, colour=colour)
        self.forward_diagonal = ForwardDiagonal(distance=1, colour=colour)
        self.jump = Jump()

    @property
    def move_rules(self):
        raise NotImplementedError

    @property
    def take_rules(self):
        raise NotImplementedError

    @property
    def colour(self):
        return self._colour

    @property
    def name(self):
        return self.__class__.__name__

    def move(self, position):
        self.position = position

    def take(self, piece):
        assert piece.colour != self.colour, TypeError("Pieces are of the same colour")
        self.position = piece.position
        piece.alive = False

    def __str__(self):
        return self.colour.name + ' ' + self.name

    def __repr__(self):
        return self.__str__()


class King(ChessPiece):
    def __init__(self, position, colour):
        super(King, self).__init__(position, colour)
        self.can_rock = True
        self.check = False
        self.check_mate = False

    @property
    def move_rules(self):
        return combine_positions(self.limited_diagonal.allowed_moves(self.position),
                                 self.limited_straight.allowed_moves(self.position))

    @property
    def take_rules(self):
        return self.move_rules

    def move(self, position):
        self.position = position
        self.can_rock = False

    def rock(self, piece):
        assert piece.__class__ == "Tower", TypeError("You're trying to rock with something else but a tower and a king")
        assert piece.can_rock and self.can_rock, TypeError("You're trying to rock with a piece that has already moved")
        assert piece.colour == self.colour, TypeError("You can't rock with the opponents pieces")

        x, y = self.position
        self.position = piece.position
        piece.position = x, y

        piece.can_rock = self.can_rock = False


class Queen(ChessPiece):
    def __init__(self, position, colour):
        super(Queen, self).__init__(position, colour)

    @property
    def move_rules(self):
        return combine_positions(self.unlimited_diagonal.allowed_moves(self.position),
                                 self.unlimited_straight.allowed_moves(self.position))

    @property
    def take_rules(self):
        return self.move_rules


class Knight(ChessPiece):
    def __init__(self, position, colour):
        super(Knight, self).__init__(position, colour)
        self.is_knight = True

    @property
    def move_rules(self):
        return self.jump.allowed_moves(self.position)

    @property
    def take_rules(self):
        return self.move_rules


class Tower(ChessPiece):
    def __init__(self, position, colour):
        super(Tower, self).__init__(position, colour)
        self.can_rock = True

    @property
    def move_rules(self):
        return self.unlimited_straight.allowed_moves(self.position)

    @property
    def take_rules(self):
        return self.move_rules


class Bishop(ChessPiece):
    def __init__(self, position, colour):
        super(Bishop, self).__init__(position, colour)

    @property
    def move_rules(self):
        return self.unlimited_diagonal.allowed_moves(self.position)

    @property
    def take_rules(self):
        return self.move_rules


class Pawn(ChessPiece):
    def __init__(self, position, colour):
        super(Pawn, self).__init__(position, colour)
        self.first_move = True

    @property
    def move_rules(self):
        if self.first_move:
            return self.forward_straight_2.allowed_moves(self.position)
        else:
            return self.forward_straight.allowed_moves(self.position)

    @property
    def take_rules(self):
        return self.forward_diagonal.allowed_moves(self.position)
