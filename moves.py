class Moves(object):
    def __init__(self, distance):
        self.distance = distance + 1
        self.is_rock = False

    def allowed_moves(self, distance):
        raise NotImplementedError

    @staticmethod
    def is_in_board(position):
        return (0 <= position[0] < 8) & (0 <= position[1] < 8)


class Diagonal(Moves):
    def __init__(self, distance):
        super(Diagonal, self).__init__(distance)

    def allowed_moves(self, position):
        x = position[0]
        y = position[1]

        distance = self.distance

        positions = [(x + i, y + i) for i in range(-distance, distance)] + [(x + i, y - i) for i in
                                                                            range(-distance, distance)]
        positions = [position for position in positions if self.is_in_board(position)]

        return set(positions) - {position}


class Straight(Moves):
    def __init__(self, distance):
        super(Straight, self).__init__(distance)

    def allowed_moves(self, position):
        x = position[0]
        y = position[1]

        distance = self.distance

        positions = [(x + i, y) for i in range(-distance, distance)] + [(x, y + i) for i in range(-distance, distance)]
        positions = [position for position in positions if self.is_in_board(position)]

        return set(positions) - {position}


class ForwardStraight(Moves):
    def __init__(self, distance, colour):
        super(ForwardStraight, self).__init__(distance)
        self.colour = colour

    def allowed_moves(self, position):
        x = position[0]
        y = position[1]

        distance = self.distance

        positions = [(x + self.colour * i, y) for i in range(0, distance)]
        positions = [position for position in positions if self.is_in_board(position)]

        return set(positions) - {position}


class ForwardDiagonal(Moves):
    def __init__(self, distance, colour):
        super(ForwardDiagonal, self).__init__(distance)
        self.colour = colour

    def allowed_moves(self, position):
        x = position[0]
        y = position[1]

        distance = self.distance
        positions = [(x + self.colour * i,
                      y + self.colour * i) for i in range(0, distance)] + \
                    [(x + self.colour * i,
                      y - self.colour * i) for i in range(0, distance)]

        positions = [position for position in positions if self.is_in_board(position)]

        return set(positions) - {position}


class Jump(Moves):
    def __init__(self):
        super(Jump, self).__init__(-1)

    @staticmethod
    def rotation(position, end_point, angle):
        x = position[0]
        y = position[1]

        a = end_point[0]
        b = end_point[1]

        z_x = a - x
        z_y = b - y

        rot_x = angle[0]
        rot_y = angle[1]

        res_x = x + z_x * rot_x - z_y * rot_y
        res_y = y + z_y * rot_x + z_x * rot_y

        return res_x, res_y

    @staticmethod
    def symmetry(position, end_point, axis):
        x = position[0]
        y = position[1]

        a = end_point[0]
        b = end_point[1]

        z_x = a - x
        z_y = b - y

        sym_x = -axis[0]
        sym_y = -axis[1]

        res_x = x + z_x * (1 + 2 * sym_x)
        res_y = y + z_y * (1 + 2 * sym_y)

        return res_x, res_y

    def allowed_moves(self, position):
        x = position[0]
        y = position[1]

        initial_position = (x - 2, y - 1)
        dual_position = self.symmetry(position, initial_position, (0, 1))

        angles = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        positions = [self.rotation(position, initial_position, angle) for angle in angles]
        positions += [self.rotation(position, dual_position, angle) for angle in angles]

        positions = [position for position in positions if self.is_in_board(position)]

        return set(positions) - {position}


# class Rock(Moves):
#     def __init__(self, distance):
#         super(Rock, self).__init__(dis)
#         self.is_rock = True
#
#     def allowed_moves(self, position):
#         x = position[0]
#         y = position[1]
#
#         distance = self.distance
#
#         if 0 < y < 7:
#             positions = [(x, 0), (x, 7)]
#         else:
#             positions = [(x, 3)]
#         return set(positions) - {position}


# class Double(Moves):
#     def __init__(self, distance):
#         super(Rock, self).__init__()
#         self.is_rock = True
#
#     def allowed_moves(self, position):
#         x = position[0]
#         y = position[1]
#
#         distance = self.distance
#
#         if 0 < y < 7:
#             positions = [(x, 0), (x, 7)]
#         else:
#             positions = [(x, 3)]
#         return set(positions) - {position}
