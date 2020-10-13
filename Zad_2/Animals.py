import math
import random
from scipy.spatial import distance


class Animal:
    def __init__(self, move_dist):
        self.move_dist: float = move_dist
        self.position: [float] = [0.0, 0.0]

    def move(self):
        pass

    def get_x_pos(self):
        return self.position[0]

    def get_y_pos(self):
        return self.position[1]

    def set_x_pos(self, x: float):
        self.position[0] = x

    def set_y_pos(self, y: float):
        self.position[1] = y


class Sheep(Animal):
    def __init__(self, init_pos_limit, move_dist):
        super().__init__(move_dist)
        self.init_pos_limit: float = init_pos_limit
        self.init_position()
        self.is_alive = True

    def init_position(self):
        self.position[0]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)
        self.position[1]: float = random.uniform(-self.init_pos_limit, self.init_pos_limit)

    def select_move(self) -> str:
        moves: [str] = ["east", "west", "north", "south"]
        return random.choice(moves)

    def move(self):
        if self.is_alive:
            selected_move: str = self.select_move()
            if selected_move == "east":
                self.position[0] += self.move_dist
                return
            elif selected_move == "west":
                self.position[0] -= self.move_dist
                return
            elif selected_move == "north":
                self.position[1] += self.move_dist
                return
            elif selected_move == "south":
                self.position[1] -= self.move_dist
                return

    def die(self):
        self.is_alive = False


class Wolf(Animal):
    def __init__(self, move_dist, game_sheep):
        super().__init__(move_dist)
        # todo fix (check if type is list of type?)
        if type(game_sheep[0]) is Sheep:
            self.game_sheep: [Sheep] = game_sheep

    def calculate_distance(self, one_game_sheep: Sheep):
        return distance.euclidean([self.position], [one_game_sheep.position])
        # return math.sqrt((int(one_game_sheep.position[0] - self.position[0])) ^ 2 + (int(
        #     one_game_sheep.position[1] - self.position[1])) ^ 2)

    # todo: coś mi się zdaje że ten wilk to się nie porusza tylko w jednym kierunku a może się poruszać po przekątnej
    def move(self):
        """
        Finds closest sheep to the wolf.
        If the sheep is closer than wolf's move distance the sheep dies.
        If it's further the wolf moves in a straight line to the closest sheep.
        :return: None
        """
        distance_to_sheep = -1
        sheep_index = -1

        for s in range(len(self.game_sheep)):
            if self.game_sheep[s].is_alive:
                if sheep_index == -1:
                    sheep_index = s
                    distance_to_sheep = self.calculate_distance(self.game_sheep[s])
                current_dist = self.calculate_distance(self.game_sheep[s])
                if current_dist < distance_to_sheep:
                    distance_to_sheep = current_dist
                    sheep_index = s

        if distance_to_sheep < self.move_dist:
            self.game_sheep[sheep_index].die()
            return

        x_pos_sheep = self.game_sheep[sheep_index].get_x_pos()
        y_pos_sheep = self.game_sheep[sheep_index].get_y_pos()

        # calculate coefficients for x and y pos change
        norm: float = math.sqrt((x_pos_sheep - self.get_x_pos()) ** 2 + (y_pos_sheep - self.get_y_pos()) ** 2)
        dir_x = (x_pos_sheep - self.get_x_pos()) / norm
        dir_y = (y_pos_sheep - self.get_y_pos()) / norm

        # change x and y position of the wolf
        self.set_x_pos(self.get_x_pos() + self.move_dist * dir_x)
        self.set_y_pos(self.get_y_pos() + self.move_dist * dir_y)

