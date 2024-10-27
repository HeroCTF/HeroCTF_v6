import random
from engine.board import Board
from engine.player import BotEasy, BotMedium, BotPlayer
from engine.ant import Ant
from engine.utils import Position, DIRECTIONS
import time
import copy
import math

MIN_SIZE = 8
MAX_SIZE = 24

class Game:
    def __init__(self, player_bot_code=None, arena=None, champion_code=None):
        self.size = random.randint(MIN_SIZE, MAX_SIZE)
        self.board = Board(self.size)
        self.players = [BotPlayer(player_bot_code), BotPlayer(champion_code) if champion_code else (BotEasy() if arena == 0 else BotMedium())]
        self.max_rounds = self.size ** 3
        self.round = 0
        self.sugar_collected = [0, 0]
        self.max_sugar = 0
        self.ant_cost = 0
        self.round_states = []  # List to store game states for each round
        self.initialize_game()

    def initialize_game(self):
        nb_ants = random.randint(self.size // 4 - 1, self.size // 4 + 1)
        first_ant_index = self.size // 2 - nb_ants // 2

        for i in range(first_ant_index, first_ant_index + nb_ants):
            self.players[0].ants.append(Ant((0, i)))
            self.players[1].ants.append(Ant((self.size - 1, self.size - 1 - i)))

        # Randomly place sugar cubes
        num_sugar_cubes = self.size // 2 if self.size % 2 == 0 else self.size // 2 + 1
        positions = [None]
        for _ in range(num_sugar_cubes):
            if self.size % 2 == 0:
                side = random.choices([0, 1, 2], weights=[5, 5, 1], k=1)[0]
            else:
                side = random.choices([0, 1], weights=[1, 1], k=1)[0]
            pos = None
            while pos in positions:
                if side == 0:
                    pos = (random.randint(2, self.size // 2 - 1), random.randint(1, self.size - 2))
                elif side == 1:
                    pos = (random.randint(self.size // 2 + 1, self.size - 3), random.randint(1, self.size - 2))
                else:
                    pos = (self.size // 2, random.randint(1, self.size - 2))
            positions.append(pos)
        for pos in positions[1:]:
            sugar_amount = 5
            self.board.add_sugar(Position(pos[0], pos[1]), sugar_amount)
        
        self.max_sugar = num_sugar_cubes * sugar_amount
        self.ant_cost = max(1, int(self.max_sugar * 0.1))

        self.round_states.append(self.record_state())

    def adjust_position(self, pos, is_player_two):
        return (self.size - 1 - pos.x, pos.y) if is_player_two else tuple(pos)
    
    def adjust_move(self, move, is_player_two):
        if not is_player_two:
            return move
        # Invert horizontal moves for player 2
        move_map = {"left": "right", "right": "left", "up": "up", "down": "down", "stay": "stay"}
        return move_map[move]
    
    def handle_player(self, player):    
        # Get moves from player
        game_state = self.get_game_state(player)
        move_response = player.make_move(copy.deepcopy(game_state))

        if not move_response:
            return False
        
        # Validate datatype
        if type(move_response["player_data"]) != bytes:
            player.error = "player_data should be bytes."
            return False
        for ant in move_response['your_ants']:
            if type(ant['pos']) != tuple:
                player.error = "pos should be a tuple."
                return False
            if len(ant['pos']) != 2:
                player.error = "pos should have 2 coordinates."
                return False
            if type(ant['carrying']) != bool:
                player.error = "carrying should be a bool."
                return False
            if type(ant['move']) != str:
                player.error = "move should be a string."
                return False
            if ant["move"] not in DIRECTIONS:
                player.error = "move should be in ['stay', 'up', 'down', 'left', 'right']"
                return False

        # Update player data
        player.player_data = move_response["player_data"]
        
        # Determine if this is player 2 for movement inversion
        is_player_two = player == self.players[1]

        # Check for new ants being bought
        ant_amout_difference = len(move_response["your_ants"]) - len(game_state["your_ants"])
        if ant_amout_difference < 0: # Player removed an ant
            return False
        elif ant_amout_difference > 0: # Player bought an ant
            if self.sugar_collected[1 if is_player_two else 0] >= self.ant_cost * ant_amout_difference: # Check sugar balance
                self.sugar_collected[1 if is_player_two else 0] -= self.ant_cost * ant_amout_difference
                # Check if new ants are on the base and a correctly configured
                new_ants = [
                    ant1 for ant1 in move_response["your_ants"]
                    if not any(ant1['pos'] == ant2['pos'] for ant2 in game_state["your_ants"])
                ]
                for ant in new_ants:
                    if ant["pos"][0] != 0 or ant["move"] != "stay" or ant["carrying"] != False:
                        return False
                    x, y = ant["pos"]
                    player.ants.append(Ant(self.adjust_position(Position(x, y), is_player_two)))
            else:
                return False # Player does not have enough sugar to pay for the ant

        # Apply moves
        for ant_data, ant in zip(move_response["your_ants"], player.ants):
            if ant_data['pos'] != self.adjust_position(ant.pos, is_player_two):
                player.error = "You tampered with your ants positions."
                return False
            # Check for carrying changes
            if ant_data["carrying"] != ant.carrying:
                if ant_data["move"] == "stay":
                    # Take sugar
                    if ant_data["carrying"]:
                        # Check if one cube and sugar left
                        cube = self.board.get_cube_at(ant.pos)
                        if cube.sugar > 0:
                            cube.collect_sugar()
                        else :
                            # No sugar left or not a cube, illegal move
                            return False
                    # Drop sugar
                    else:
                        # Check if ant is carrying sugar
                        if ant.carrying:
                            # Check if ant is at base
                            if (ant.pos.x == 0 and player == self.players[0]) or (ant.pos.x == self.size - 1 and player == self.players[1]):
                                self.sugar_collected[self.players.index(player)] += 1
                            else:
                                # Illegal move
                                return False
            
            # Update ant carrying status
            ant.update_carrying(ant_data["carrying"])

            # Move the ant
            move = self.adjust_move(ant_data["move"], is_player_two)
            ant.move(move)
        
        return True

    def play_round(self, time_player1, time_player2):
        # Handle player moves
        start = time.time()
        self.players[0].lost = not self.handle_player(self.players[0])
        time_player1.value += time.time() - start
        start = time.time()
        self.players[1].lost = not self.handle_player(self.players[1])
        time_player2.value += time.time() - start

        # Check for illegal moves for player 1
        if not self.players[0].lost:
            brk = False
            for ant in self.players[0].ants:
                if brk:
                    break
                # Check for out of bounds and stepping on ennemy base
                if ant.pos.x < 0 or ant.pos.x >= self.size - 1 or ant.pos.y < 0 or ant.pos.y >= self.size:
                    self.players[0].lost = True
                    break
                # Check for two ants on the same cell
                for ant2 in self.players[0].ants:
                    if ant != ant2 and ant.pos == ant2.pos:
                        self.players[0].lost = True
                        brk = True
                        break
        # Check for illegal moves for player 2
        if not self.players[1].lost:
            brk = False
            for ant in self.players[1].ants:
                if brk:
                    break
                # Check for out of bounds and stepping on ennemy base
                if ant.pos.x <= 0 or ant.pos.x > self.size - 1 or ant.pos.y < 0 or ant.pos.y >= self.size:
                    self.players[1].lost = True
                    break
                # Check for two ants on the same cell
                for ant2 in self.players[1].ants:
                    if ant != ant2 and ant.pos == ant2.pos:
                        self.players[1].lost = True
                        brk = True
                        break

        # If a player lost, end the game
        if self.players[0].lost or self.players[1].lost:
            self.round_states.append(self.record_state())
            return
        
        # Check for discovered cubes (if ant is on the cube or adjacent to it)
        for cube in self.board.cubes:
            if not cube.discovered:
                for player in self.players:
                    for ant in player.ants:
                        if ant.pos == cube.pos or (abs(ant.pos.x - cube.pos.x) <= 1 and abs(ant.pos.y - cube.pos.y) <= 1):
                            cube.discovered = True


        # Check for ant collisions between players ants
        remove_player1 = []
        remove_player2 = []
        for i in range(len(self.players[0].ants)):
            for j in range(len(self.players[1].ants)):
                if self.players[0].ants[i].pos == self.players[1].ants[j].pos:
                    # If there is a collision, kill one of the ants with a 50% chance
                    if random.random() < 0.5:
                        remove_player1.append(i)
                    else:
                        remove_player2.append(j) 
        # Remove ants that collided
        for i in reversed(remove_player1):
            self.players[0].ants.pop(i)
        for i in reversed(remove_player2):
            self.players[1].ants.pop(i)

        
        # Update the board
        self.board.update_grid(self.players[0].ants + self.players[1].ants)

        # Record the game state for this round
        self.round_states.append(self.record_state())

        self.round += 1


    def get_game_state(self, player):
        # Determine the opponent
        opponent = self.players[1] if player == self.players[0] else self.players[0]

        # Determine if this is player 2 (right-side player)
        is_player_two = player == self.players[1]
        
        # Prepare the game state for the current player
        return {
            "your_ants": [
                {
                    "pos": self.adjust_position(ant.pos, is_player_two),
                    "last_pos": self.adjust_position(ant.last_pos, is_player_two),
                    "carrying": ant.carrying,
                    "last_carrying": ant.last_carrying
                }
                for ant in player.ants
            ],
            "opponent_ants": [
                {
                    "pos": self.adjust_position(ant.pos, is_player_two),
                    "last_pos": self.adjust_position(ant.last_pos, is_player_two),
                    "carrying": ant.carrying,
                    "last_carrying": ant.last_carrying
                }
                for ant in opponent.ants
            ],
            "discovered_cubes": [
                {"pos": self.adjust_position(cube.pos, is_player_two), "sugar": cube.sugar}
                for cube in self.board.cubes if cube.discovered
            ],
            "total_sugar_available": sum(cube.sugar for cube in self.board.cubes),
            "grid_size": self.size,
            "your_score": self.sugar_collected[self.players.index(player)],
            "opponent_score": self.sugar_collected[self.players.index(opponent)],
            "ant_cost": self.ant_cost,
            "player_data": player.player_data
        }


    def record_state(self):
        # Record the state of the board and scores for each round
        return {
            "round": self.round,
            "player1": [
                {"pos": ant.pos, "carrying": ant.carrying}
                for ant in self.players[0].ants
            ],
            "player2": [
                {"pos": ant.pos, "carrying": ant.carrying}
                for ant in self.players[1].ants
            ],
            "cubes": [
                {"pos": cube.pos, "sugar": cube.sugar, "discovered": cube.discovered}
                for cube in self.board.cubes
            ],
            "score": list(self.sugar_collected)
        }
    
    def is_game_over(self):
        return self.round >= self.max_rounds or sum(self.sugar_collected) == self.max_sugar or self.players[0].lost or self.players[1].lost

    def run(self, time_player1, time_player2):
        while not self.is_game_over():
            self.play_round(time_player1, time_player2)

        # If no one lost because of a bad code, check who has most points
        if not self.players[0].lost and not self.players[1].lost:
            if self.sugar_collected[0] > self.sugar_collected[1]:
                self.players[1].lost = True
            elif self.sugar_collected[0] < self.sugar_collected[1]:
                self.players[0].lost = True

        return self.round_states, self.players, self.size
