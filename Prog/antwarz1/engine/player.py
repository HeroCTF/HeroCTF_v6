import traceback

class Player:
    def __init__(self):
        self.ants = []
        self.lost = False
        self.player_data = b""
        self.error = ""

class BotEasy(Player):
    """
    Limitations of this bot:
        - It's completely random
    """
    def __init__(self):
        super().__init__()

    def make_move(self, game_state):
        try:
            def random(seed):
                n = hash(str(seed))
                return 0 if n < 0 else 1, n

            def get_possible_moves(ant_positions, position):
                possible = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                # Check if there is an ant on a legal cell adjacent to us
                for p in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    np = (p[0] + position[0], p[1] + position[1])
                    if (np in ant_positions or np[0] < 0 or np[0] >= grid_size - 1 or np[1] < 0 or np[1] >= grid_size - 1)  and p in possible:
                        possible.remove(p)

                # Check if there is an ant 1 cell away from us that could walk on the same cell as us
                for np, p in zip([(-2, 0), (2, 0), (0, -2), (0, 2)], [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                    np = (np[0] + position[0], np[1] + position[1])
                    if np in ant_positions and p in possible:
                        possible.remove(p)
                
                # Check if there is an ant in a corner cell from us, that could walk on the same cell as us
                for p in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    np = (p[0] + position[0], p[1] + position[1])
                    if np in ant_positions:
                        for f in [(0, p[1]), (p[0], 0)]:
                            if f in possible:
                                possible.remove(f)
                
                return possible
            

            player_data = game_state["player_data"]
            ants = game_state["your_ants"]
            ennemy_ants = game_state["opponent_ants"]
            grid_size = game_state["grid_size"]
            cubes = game_state["discovered_cubes"]
            score, price = game_state["your_score"], game_state["ant_cost"]

            relative_moves = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right", (0, 0): "stay"}
            moves = ["" for _ in range(len(ants))]
            carrying = [ant["carrying"] for ant in ants]

            seed = grid_size * len(ants)
            if player_data:
                seed = int(player_data)

            # Check if any ant on a cube with sugar
            for i in range(len(ants)):
                for cube in cubes:
                    if ants[i]["pos"] == cube["pos"] and not carrying[i] and cube["sugar"] > 0:
                        moves[i] = "stay"
                        carrying[i] = True

            # Check if on base to drop off sugar
            for i in range(len(ants)):
                if ants[i]["pos"][0] == 0 and carrying[i]: # It's ok to use carrying variable because sugar cubes cannot be on bases
                    moves[i] = "stay"
                    carrying[i] = False

            # Map positions to ants to optimize the next loop from O(n^2) to O(n)
            ant_positions = [ant["pos"] for ant in ants + ennemy_ants]

            for index in range(len(ants)):
                if moves[index] != "":
                    continue
                

                # Determine possible moves
                position = ants[index]["pos"]
                possible = get_possible_moves(ant_positions, position)

                # If the ant is carrying
                if carrying[index]:
                    # Go straight back to base if possible
                    if (-1, 0) in possible:
                        moves[index] = "left"
                        continue
                    else:
                        # Make sure it does not go further from base
                        if (1, 0) in possible:
                            possible.remove((1, 0))
                
                # "Random" choice within the possible range
                if len(possible) == 0:
                    move = "stay"
                elif len(possible) == 1:
                    move = relative_moves[possible[0]]
                else:
                    p = None
                    n1, seed = random(seed)
                    n2, seed = random(seed)
                    player_data = str(seed).encode()

                    h1 = possible[:len(possible)//2]
                    h2 = possible[len(possible)//2:]

                    h = h1 if n1 else h2
                    if len(h) > 1:
                        p = h[n2]
                    else:
                        p = h[0]
                    move = relative_moves[p]

                moves[index] = move

            return {
                "your_ants": [
                    {"pos": ant["pos"], "carrying": carrying[i], "move": moves[i]}
                    for i, ant in enumerate(game_state["your_ants"])
                ],
                "player_data": player_data
            }
        
        except:
            import traceback
            self.error = traceback.format_exc()
            return False
        
class BotMedium(Player):
    """
    Limitations of this bot:
        - Only the first ant in the list can be the searcher
        - Only one searcher
        - Avoids battle
            - No defense mechanism
            - No offense mechanism
        - The previous point makes it easy to stop the colonny by stepping on the path they take to empty a sugar cube
    """
    def __init__(self):
        super().__init__()
    
    def make_move(self, game_state):
        try:
            def get_possible_relative_positions(ant_positions, position):
                    possible = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                    # Check if there is an ant on a legal cell adjacent to us
                    for p in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        np = (p[0] + position[0], p[1] + position[1])
                        if (np in ant_positions or np[0] < 0 or np[0] >= grid_size - 1 or np[1] < 0 or np[1] >= grid_size - 1)  and p in possible:
                            possible.remove(p)

                    # Check if there is an ant 1 cell away from us that could walk on the same cell as us
                    for np, p in zip([(-2, 0), (2, 0), (0, -2), (0, 2)], [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                        np = (np[0] + position[0], np[1] + position[1])
                        if np in ant_positions and p in possible:
                            possible.remove(p)
                    
                    # Check if there is an ant in a corner cell from us, that could walk on the same cell as us
                    for p in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        np = (p[0] + position[0], p[1] + position[1])
                        if np in ant_positions:
                            for f in [(0, p[1]), (p[0], 0)]:
                                if f in possible:
                                    possible.remove(f)
                    
                    return possible

            def bfs(start: tuple, goal: tuple, grid: list):
                # Define possible movements: right, down, left, up
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                # Get grid dimensions
                rows, cols = len(grid), len(grid[0])
                # Helper function to check if a position is within bounds and walkable
                def is_valid(x, y):
                    return 0 <= x < rows and 0 <= y < cols and grid[y][x] == 0
                # Initialize the queue with the start position and step count (0)
                queue = [(start[0], start[1])]
                # Dictionary to store the path (previous node for each visited node)
                predecessors = {start: None}
                while queue:
                    x, y = queue.pop(0)
                    # If we've reached the goal, reconstruct the path
                    if (x, y) == goal:
                        path = []
                        p = (x, y)
                        while p is not None:
                            path.append(p)
                            p = predecessors[p]
                        return path[::-1]  # Reverse the path to start from the beginning
                    # Explore all four possible directions
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if is_valid(nx, ny) and (nx, ny) not in predecessors:
                            predecessors[(nx, ny)] = (x, y)  # Record where we came from
                            queue.append((nx, ny))
                # If there's no valid path, return an empty list
                return []
            
            def get_round_path(cube_pos):
                x, y = cube_pos
                round_path = []
                for i in range(x+1):
                    round_path.insert(i, (i, y))
                    if y > 0 - 1:
                        round_path.insert(i+1, (i, y-1))
                    else:
                        round_path.insert(i+1, (i, y+1))
                return round_path
            
            def handle_ant_on_path(ant, i, round_path, active_sugar_cube, moves, carrying, dont_pick_up=False):
                x, y = ant['pos']
                
                # Check if carrying and on base
                if ant['carrying'] and x == 0:
                    # Drop cube and stay
                    moves[i] = "stay"
                    carrying[i] = False
                
                # Check it not carrying and on active cube
                elif not ant['carrying'] and (x, y) == active_sugar_cube and not dont_pick_up:
                    # Pick up cube and stay
                    moves[i] = "stay"
                    carrying[i] = True
                
                # Else move along the round path if not obstructed
                else:
                    # Get next cell on round path
                    index_in_path = round_path.index((x, y))
                    next = round_path[index_in_path+1] if index_in_path < len(round_path) - 1 else round_path[0]
                    if next not in [a['pos'] for a in ants+ennemy_ants]:
                        moves[i] = get_move_from_coord(get_relative_move((x, y), next))
                        carrying[i] = ants[i]['carrying']

            def handle_ant_not_on_path(ant, i, moves, carrying):
                x, y = ant['pos']
                found_move = False
                round_path_m = sorted([(manhattan((x, y), r), r) for r in round_path], key=lambda t: t[0])
                possible_moves = [get_real_position((x, y), p) for p in get_possible_relative_positions([a['pos'] for a in ants + ennemy_ants], (x, y))]

                # Check each cell of the path, from the closest to the furthest
                for cell_round_path_by_manhattan in round_path_m:
                    _, cell_round_path = cell_round_path_by_manhattan
                    path = bfs((x, y), cell_round_path, maze)
                    # If there is an accessible path move closer to it
                    if path and len(path) > 1 and path[1] in possible_moves:
                        next_cell = path[1]
                        move = get_move_from_coord(get_relative_move((x, y), next_cell))
                        moves[i] = move
                        found_move = True
                        break
                
                # If there is no move possible, wait
                if not found_move:
                    moves[i] = "stay"
                
                # We do not alter the carrying state
                carrying[i] = ant["carrying"]

                    
            def parse_player_data(player_data):
                decoded = player_data.decode().split(":")
                searching = int(decoded[0])
                last_visited = tuple(map(int, decoded[1].split(",")))
                active_sugar_cube = tuple(map(int, decoded[2].split(",")))

                return searching, last_visited, active_sugar_cube
            
            def encode_player_data(searching, last_visited, active_sugar_cube):
                return f"{searching}:{last_visited[0]},{last_visited[1]}:{active_sugar_cube[0]},{active_sugar_cube[1]}".encode()

            def get_relative_move(end, goal):
                return (goal[0] - end[0], goal[1] - end[1])

            def get_real_position(position, relative_move):
                return (position[0] + relative_move[0], position[1] + relative_move[1])
                
            def get_move_from_coord(coord):
                return {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right", (0, 0): "stay"}[coord]
            
            def manhattan(a, b):
                return sum(abs(val1-val2) for val1, val2 in zip(a,b))
            
            # Get game data
            player_data = game_state["player_data"]
            ants = game_state["your_ants"]
            ennemy_ants = game_state["opponent_ants"]
            grid_size = game_state["grid_size"]
            cubes = game_state["discovered_cubes"]

            # Init moves and carrying states
            moves = [None for _ in range(len(ants))]
            carrying = [None for ant in ants]
            
            # Create maze of the current state of the grid
            maze = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
            for i in range(grid_size): # Add walls for ennemy base
                maze[i][grid_size - 1] = 1
            for ant in ennemy_ants + ants: # Add ennemy ants as obstacles. Friendly ants will be handled at the end to avoid bugs where nobody moves
                maze[ant["pos"][1]][ant["pos"][0]] = 1

            # Init player data if necessary
            if not player_data:
                player_data = b"1:-1,-1:-1,-1"

            # Parse player data
            searching, last_visited, active_sugar_cube = parse_player_data(player_data)
            player_data = None
            searched_all = searching == -1
            
            
            # Check if we had active sugar that is now empty
            if not searching:
                cube = [c for c in cubes if c['pos'] == active_sugar_cube][0]
                if cube['sugar'] == 0:
                    searching = 1

            # Determine round path
            round_path = get_round_path(active_sugar_cube)

            # If in searcher mode (no active sugar)
            if searching:
                # If no ant is still carying, switch of the active cube
                if not any([a['carrying'] for a in ants]):
                    active_sugar_cube = (-1, -1)
                # Other wise keep following the path to avoid blocking carrying ants
                else:
                    for i, ant in enumerate(ants):
                        if ant['pos'] in round_path:
                            handle_ant_on_path(ant, i, round_path, active_sugar_cube, moves, carrying, dont_pick_up=True)

                # Check if we discovered a new cube last round, stop searching if we did
                for cube in cubes:
                    for ant in ants:
                        for offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]:
                            ant_pos = ant["pos"]
                            cube_pos = cube["pos"]
                            if (ant_pos[0]+offset[0], ant_pos[1]+offset[1]) == cube["pos"] and cube['sugar'] > 0 and active_sugar_cube == (-1, -1):
                                active_sugar_cube = cube_pos
                                searching = 0
                                player_data = encode_player_data(searching, last_visited, active_sugar_cube) # DEBUG, REMOVE LATER
                
                # For the searcher ant, determine it's next position (if searcher ant not already moved)
                # Determine the next cell to visit
                if moves[0] == None:
                    target_cell = None
                    if last_visited == (-1, -1):
                        target_cell = (1, 0)
                    else:
                        if last_visited[0] % 2 == 0:
                            target_cell = (last_visited[0], last_visited[1] - 1)
                            if target_cell[1] == -1:
                                target_cell = (target_cell[0] + 1, 0)
                        else:
                            target_cell = (last_visited[0], last_visited[1] + 1)
                            if target_cell[1] == grid_size:
                                target_cell = (target_cell[0] + 1, grid_size-1)

                    # Determine the best route to the next cell to visit
                    next_cell = None
                    start = ants[0]["pos"]
                    path = bfs(start, target_cell, maze)

                    # We don't check for possible moves because friendly ants are not moving (and we are not affraid of ennemies)
                    if path and len(path) > 1 and path[1]: # If we found a path and can walk it
                        next_cell = path[1]

                        if (next_cell == target_cell):
                            player_data = encode_player_data(searching, target_cell, active_sugar_cube)

                        # Move on the next cell on the determined route
                        move = get_move_from_coord(get_relative_move(ants[0]["pos"], next_cell))
                        moves[0] = move
                    else: # No path found (probably a friendly ant on the target cell, move to the next)
                        player_data = encode_player_data(searching, target_cell, active_sugar_cube)

            # If we are not searching (a sugar cube is active)
            else:
                for i, ant in enumerate(ants):
                    if moves[i] != None:
                        continue
                    # If on the round path
                    if ant['pos'] in round_path:
                        handle_ant_on_path(ant, i, round_path, active_sugar_cube, moves, carrying)
                    else:
                        handle_ant_not_on_path(ant, i, moves, carrying)

            if player_data == None:
                player_data = encode_player_data(searching, last_visited, active_sugar_cube)

            # Handle inactive ants
            for i in range(len(ants)):
                if moves[i] == None:
                    moves[i] = "stay"
                if carrying[i] == None:
                    carrying[i] = ants[i]["carrying"]

            return {
                "your_ants": [
                    {"pos": ant["pos"], "carrying": carrying[i], "move": moves[i]}
                    for i, ant in enumerate(game_state["your_ants"])
                ],
                "player_data": player_data
            }
        
        except:
            import traceback
            self.error = traceback.format_exc()
            return False

from engine.utils import Position
import builtins

# Custom import function that raises an exception when trying to import a module
def restricted_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'traceback':
        return builtins.__import__(name, globals, locals, fromlist, level)
    raise ImportError(f"Imports are not allowed in this sandbox.")

def forbidden_function(*arg, **karg):
    raise Exception(f"This function is not allowed.")

class BotPlayer(Player):
    def __init__(self, user_code):
        self.user_code = user_code
        self.format_user_code()

        super().__init__()

    def format_user_code(self):
        lines = self.user_code.split("\n")
        formatted_code = "\n".join([" " + line.replace("    ", " ").replace("\t", " ") for line in lines])
        self.user_code = formatted_code
    
    def make_move(self, game_state):
        # Copy the built-ins to preserve original state
        safe_builtins = {**builtins.__dict__}
        
        # Override the __import__ function to prevent imports
        safe_builtins['__import__'] = restricted_import

        allowed_builtins = {
            'len': len,
            'range': range,
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'all': all,
            'any': any,
            'enumerate': enumerate,
            'sorted': sorted,
            'reversed': reversed,
            'zip': zip,
            'map': map,
            'filter': filter,
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict,
            'set': set,
            'tuple': tuple,
            'str': str,
                'format': str.format,
                'startswith': str.startswith,
                'endswith': str.endswith,
                'lower': str.lower,
                'upper': str.upper
        }

        forbidden_builtins = {
            'print': forbidden_function,
            'exit': forbidden_function
        }

        safe_builtins.update(allowed_builtins)
        safe_builtins.update(forbidden_builtins)

        sandbox_globals = {
            '__builtins__': safe_builtins,  # Use our restricted built-ins
            '__name__': 'sandbox',           # Arbitrary name for the sandbox
            'Position': Position
        }
    
        sandbox_locals = {}

        try:
            exec(f'''try:
{self.user_code}
 result = make_move({game_state!r})
except Exception as e:
    import traceback
    error = traceback.format_exc()
''', sandbox_globals, sandbox_locals)

            if "error" in sandbox_locals.keys():
                self.error = sandbox_locals["error"]
                return False
            
            return sandbox_locals['result']
    
        except Exception as e:
            self.error = "".join(traceback.format_exception_only(type(e), e))
            return False
