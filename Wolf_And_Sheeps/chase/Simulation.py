import csv
import json
import msvcrt
from typing import Union, List

from . import Animals, LoggingUtil, Config


class Simulation:
    def __init__(self, rounds: int, number_of_sheep: int,
                 init_pos_limit: float, sheep_move_dist: float,
                 wolf_move_dist: float):
        self.number_of_sheep: int = number_of_sheep
        self.sheep: [Animals.Sheep] = []
        self.initialize_sheep(number_of_sheep, init_pos_limit, sheep_move_dist)
        self.wolf: Animals.Wolf = Animals.Wolf(wolf_move_dist, self.sheep)
        self.dead_sheep_index: Union[int, None] = None
        self.rounds = rounds
        self.list_to_write_json_file = []
        self.list_to_write_csv_file = []
        self.round_num = 0
        self.living_sheep_count = self.number_of_sheep

    @LoggingUtil.debug_logging
    def initialize_sheep(self, number_of_sheep: int, init_pos_limit: float,
                         sheep_move_dist: float):
        for i in range(number_of_sheep):
            self.sheep.append(Animals.Sheep(init_pos_limit, sheep_move_dist))

    @LoggingUtil.debug_logging
    def perform_simulation(self):
        self.display_and_store_simulation_information(self.living_sheep_count)

        while self.round_num < self.rounds and self.living_sheep_count > 0:
            self.simulation_round()

        self.save_to_json_file()
        self.save_to_csv_file()

    def simulation_round(self):
        [x.move() for x in self.sheep]

        self.dead_sheep_index = self.wolf.move()

        if self.dead_sheep_index is not None:
            self.living_sheep_count -= 1

        self.round_num += 1
        self.display_and_store_simulation_information(self.living_sheep_count)
        if Config.WAIT and (
                self.round_num < self.rounds and self.living_sheep_count > 0):
            print("Press any key to continue...")
            msvcrt.getch()

    def get_sheep(self) -> List[Animals.Sheep]:
        return self.sheep

    def get_wolf(self) -> Animals.Wolf:
        return self.wolf

    @LoggingUtil.debug_logging
    def display_and_store_simulation_information(self, living_sheep_count):
        self.show_information()
        self.append_to_json_list()
        self.append_to_csv_list(living_sheep_count)

    @LoggingUtil.debug_logging
    def show_information(self, ):
        print("Round number: ", self.round_num)
        print("Wolf position: (", round(self.wolf.get_x_pos(), 3), ", ",
              round(self.wolf.get_y_pos(), 3), ")")
        print("Number of alive sheep: ", self.living_sheep_count)
        print("Index of the eaten sheep: ", self.dead_sheep_index, "\n")

    @LoggingUtil.debug_logging
    def append_to_json_list(self):
        sheep_position: [[int, int]] = []
        for s in self.sheep:
            if s.is_alive:
                sheep_position.append([s.get_x_pos(), s.get_y_pos()])
            else:
                sheep_position.append(None)
        self.list_to_write_json_file.append({
            "round_no": self.round_num,
            "wolf_pos": [self.wolf.get_x_pos(), self.wolf.get_y_pos()],
            "sheep_pos": sheep_position,
        })

    @LoggingUtil.debug_logging
    def save_to_json_file(self):
        json_object = json.dumps(self.list_to_write_json_file, indent=3)
        with open(Config.SAVE_DIR + 'pos.json', 'w') as json_file:
            json_file.write(json_object)

    @LoggingUtil.debug_logging
    def append_to_csv_list(self, number_of_alive_sheep: int):
        self.list_to_write_csv_file.append(
            [self.round_num, number_of_alive_sheep])

    @LoggingUtil.debug_logging
    def save_to_csv_file(self):
        with open(Config.SAVE_DIR + 'alive.csv', mode='w',
                  newline='') as alive_file:
            csv_writer = csv.writer(alive_file, delimiter=',', quotechar='"',
                                    quoting=csv.QUOTE_NONE)

            for round_number in range(self.round_num):
                csv_writer.writerow(self.list_to_write_csv_file[round_number])
