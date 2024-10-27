#!/usr/bin/python3

import base64
import requests
import random
import string
from engine.game import Game
import os
import json
from dotenv import load_dotenv
from math import ceil
import signal
import multiprocessing
import uuid
import time
from random import randint
from collections import defaultdict
from tabulate import tabulate
from datetime import datetime

load_dotenv()

CTFD = os.environ.get('CTFD')
API = f"{CTFD}/api/v1"
CHALLENGES = [os.environ.get('CHALLENGE1'), os.environ.get('CHALLENGE2')]
FLAGS = [os.environ.get('FLAG1'), os.environ.get('FLAG2')]
PLATEFORM = os.environ.get('PLATEFORM')

def timeout_handler(signum, frame):
    raise Exception("TIMEOUT")

def welcome():
    """Print welcome message with basic information"""
    print('            ,')
    print('     _,-\'\   /|   .    .    /`.')
    print(' _,-\'     \_/_|_  |\   |`. /   `._,--===--.__')
    print('^       _/"/  " \ : \__|_ /.   ,\'    :.  :. .`-._')
    print('       // ^   /7 t\'""    "`-._/ ,\'\   :   :  :  .`.')
    print('       Y      L/ )\         ]],\'   \  :   :  :   : `.         Welcome to antwarz!')
    print('       |        /  `.n_n_n,\',\'\_    \ ;   ;  ;   ;  _>')
    print('       |__    ,\'     |  \`-\'    `-.__\_______.==---\'')
    print('      //  `""\\      |   \            \ ')
    print('      \|     |/      /    \            \ ')
    print('                    /     |             `. ')
    print('                   /      |               ^')
    print('                  ^       |')
    print('                      ^ (original production Ghizmo x ChatGPT)')
    print(f'You can find the full documentation here: {PLATEFORM}')
    print()
    print("[*] Here is a function template")
    print()
    print("""def make_move(game_state):
    return {
        "your_ants": [
            {"pos": ant["pos"], "carrying": False, "move": "stay"}
            for ant in game_state["your_ants"]
        ],
        "player_data": b""
    }
""")

def generate_random_endpoint(length=32):
    """Generate a random endpoint name."""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def create_random_endpoint(endpoint_name, game_data, code, grid_size):
    filename = os.path.join("/var/www/html", f"{endpoint_name}.html")
    template = open('/app/review.html', 'r').read()
    template = template.replace('REPLACE_ME_WITH_GAME_DATA', json.dumps(game_data, indent = 4))
    template = template.replace('REPLACE_ME_WITH_CODE', code)
    template = template.replace('REPLACE_ME_WITH_GRID_SIZE', str(grid_size))
    try:
        with open(filename, "w") as file:
            file.write(template)
        print(f"[+] Access it at: {PLATEFORM}/{endpoint_name}.html")
    except PermissionError:
        print("[-] Permission denied: ensure the script has write access to /var/www/html")
    except Exception as e:
        print(f"[-] Error while saving the file: {e}")

def log(msg):
    formatted = f'{datetime.now().strftime("%m/%d/%Y-%H:%M:%S")}:{msg}'
    open('/var/log/antwarz.log', 'a').write(f"{formatted}\n")

def check_team_exists(token):
    """Check if a team exists on the CTFd instance."""
    response = requests.get(f"{API}/users/me", headers={"Authorization": f"Token {token}", "Content-Type": "application/json"})
    if response.status_code == 200:
        username = response.json()['data']['name']
        team_id = response.json()['data']['team_id']
        if not team_id:
            print('[-] Error: You must be part of a team to play.')
            exit()

        return (username, team_id)
    return False

def fetch_team_names():
    url = f"{API}/teams"
    response = requests.get(url)
    response_data = response.json()
    
    # Map each team ID to its name
    team_id_to_name = {
        team["id"]: team["name"]
        for team in response_data["data"]
    }
    return team_id_to_name

def fetch_team_ids():
    url = f"{API}/teams"
    response = requests.get(url)
    response_data = response.json()
    
    # Map each team ID to its name
    team_name_to_id = {
        team["name"]: team["id"]
        for team in response_data["data"]
    }
    return team_name_to_id

def check_current_step(token):
    """Check at wich step the player is"""
    response = requests.get(f"{API}/challenges", headers={"Authorization": f"Token {token}", "Content-Type": "application/json"})
    solved = []
    if response.status_code == 200:
        f1, f2 = False, False
        for ctfd_challenge in response.json()['data']:
                if ctfd_challenge['name'] == CHALLENGES[0]:
                    if ctfd_challenge['solved_by_me']:
                        f1 = True
                if ctfd_challenge['name'] == CHALLENGES[1]:
                    if ctfd_challenge['solved_by_me']:
                        f2 = True
    if f2:
        return 2
    elif f1:
        return 1
    return 0

def check_if_won(players):
    """Given to players objects, checks if player[0] won"""
    if players[0].lost and not players[1].lost:
        return 0
    elif players[1].lost and not players[0].lost:
        return 1
    return -1

def new_champion(team_id, code):
    bot_id = uuid.uuid4()
    a = open('/app/names/adjectives.txt').readlines()
    n = open('/app/names/nouns.txt').readlines()
    random_name = f"{a[randint(0, 50)].strip()} {n[randint(0, 50)].strip()}"
    open(os.path.join("/app/champions", f"{team_id}_{bot_id}.py"), 'w').write(code)
    open('/app/champions.txt', 'a').write(f'{int(time.time())},{bot_id},{random_name},{team_id}\n')
    log(f"Added new champion {int(time.time())},{bot_id},{random_name},{team_id}")


def run_single_game(team, code, arena):
    """Run a single game"""
    champion_code = None
    print(arena)
    if arena == 2:
        since, bot_id, name, team_id = open('/app/champions.txt').readlines()[-1].strip().split(",")
        if int(team_id) == int(team):
            log(f"{int(team_id)} tried to submit while being champion")
            print('[-] Error: You are not allowed to submit while you are the champion of the arena...')
            exit()
        champion_code = open(f'/app/champions/{team_id}_{bot_id}.py').read()
    
    print(champion_code)

    game = Game(player_bot_code=code, arena=arena, champion_code=champion_code)
    timeout = ceil(game.max_rounds * 0.005)
    t1 = multiprocessing.Value('d', 0)
    t2 = multiprocessing.Value('d', 0)

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    log(f"Running game for {team}. Arena: {arena}")
    game_states, players, size = game.run(t1, t2)
    signal.alarm(0)
    
    if "TIMEOUT" in players[0].error or "TIMEOUT" in players[1].error:
        t1 = t1.value
        t2 = t2.value
        if t1 > t2:
            players[0].error = "Your bot timed out. Make sure you don't have an infinite loop in your code. If not, your code is probably taking to long to execute."
            players[0].lost = True
            players[1].lost = False
        elif t1 < t2:
            players[1].error = "Your bot timed out. Make sure you don't have an infinite loop in your code. If not, your code is probably taking to long to execute."
            players[1].lost = True
            players[0].lost = False

    if players[0].error:
        print(f'[!] Error: {players[0].error}')

    won = check_if_won(players)
    log(f"Finished processing game for {team}. Arena: {arena} / won: {won} / player1: {players[0].error} / player2: {players[1].error}")
    return game_states, players, size

def run_multiple_games(team, code, arena, rounds):
    """Run multiple games to get a flag"""
    champion_code=None
    if arena == 2:
        since, bot_id, name, team_id = open('/app/champions.txt').readlines()[-1].strip().split(",")
        if int(team_id) == int(team):
            print('[-] Error: You are not allowed to submit while you are the champion of the arena...')
            exit()
        champion_code = open(f'/app/champions/{team_id}_{bot_id}.py').read()
        print(champion_code)

    games = [Game(player_bot_code=code, arena=arena, champion_code=None) for _ in range(rounds)]
    looses = 0
    log(f"Running game submission for {team}. Arena: {arena}")
    for i, game in enumerate(games):
        timeout = ceil(game.max_rounds * 0.005)
        t1 = multiprocessing.Value('d', 0)
        t2 = multiprocessing.Value('d', 0)

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        log(f"Running game for {team}. Arena: {arena} {i+1}/15")
        game_states, players, size = game.run(t1, t2)
        signal.alarm(0)
        
        if "TIMEOUT" in players[0].error or "TIMEOUT" in players[1].error:
            t1 = t1.value
            t2 = t2.value
            if t1 > t2:
                players[0].error = "Your bot timed out. Make sure you don't have an infinite loop in your code. If not, your code is probably taking to long to execute."
                players[0].lost = True
                players[1].lost = False
            elif t1 < t2:
                players[1].error = "Your bot timed out. Make sure you don't have an infinite loop in your code. If not, your code is probably taking to long to execute."
                players[1].lost = True
                players[0].lost = False
        
        won = check_if_won(players)
        looses += 1 if won == 0 else 0
        print(f'[*] Processed game {i+1}/{rounds} {"(won)" if won == 1 else ""}', flush=True)
        log(f"Finished processing game for {team}. Arena: {arena} / won: {won} / player1: {players[0].error} / player2: {players[1].error}")

    return looses

def get_scoreboard():
    # Fetch team names from API
    team_id_to_name = fetch_team_names()

    # Load champions data from file
    champions = [c.strip().split(',') for c in open('/app/champions.txt').readlines()]
    current_bot_id = champions[-1][1]

    initial_timestamp = int(champions[0][0])  # Start time of the first champion
    current_timestamp = int(time.time())

    # Initialize parameters
    bot_times = {}
    team_points = defaultdict(int)
    M = 1

    for i in range(initial_timestamp, current_timestamp, 300):
        n = initial_timestamp + i - initial_timestamp
        multiplier = ((n - initial_timestamp) // 1800) + 1
        for j in range(len(champions)):
            if j < len(champions)-1 and n >= int(champions[j][0]) and n < int(champions[j+1][-1]):
                team_points[champions[j][-1]] += M * multiplier
            elif j == len(champions)-1 and n >= int(champions[j][0]):
                team_points[champions[j][-1]] += M * multiplier

    print(team_points)

    # Prepare team scoreboard with team names
    team_scoreboard = []
    for team_id, points in sorted(team_points.items(), key=lambda x: x[1], reverse=True):
        team_name = team_id_to_name[int(team_id)]  # Use name if available, else ID
        team_scoreboard.append([team_name, points])

    print(team_scoreboard)
    for i in range(len(champions)-1):
        bot_times[champions[i][1]] = (champions[i][2], int(champions[i+1][0])- int(champions[i][0]), champions[i][3])
    bot_times[champions[-1][1]] = (champions[-1][2], current_timestamp - int(champions[-1][0]), champions[-1][3])
    
    # Prepare bot scoreboard with "(current)" for the active bot
    bot_scoreboard = []
    for i, (bot_id, (name, total_time, team_id)) in enumerate(sorted(bot_times.items(), key=lambda x: x[1][1], reverse=True)):
        team_name = team_id_to_name[int(team_id)]  # Fetch team name
        if bot_id == current_bot_id:  # The last bot in the sorted list is the current one
            name += " (current)"
        bot_scoreboard.append([name, team_name, str(total_time)])
    print(bot_scoreboard)
    return bot_scoreboard, team_scoreboard


def main():
    welcome()


    # Ask for the CTFd token
    ctfd_token = input("Enter your CTFd token: ")

    # Check if the team exists
    exists = check_team_exists(ctfd_token)
    username, team_id = None, None
    if exists:
        username, team_id = exists
        print(f"[*] Welcome {username}")
    else:
        exit()
    log(f"User {username} from {team_id} logged in.")

    if time.time() >= 1730061000:
        bot_scoreboard, team_scoreboard = get_scoreboard()
        team_name_to_ids = fetch_team_ids()
        if int(team_name_to_ids[team_scoreboard[0][0]]) == int(team_id):
            log(f'{team_scoreboard[0][0]} got the final flag')
            print(f'[+] WOW! Your the lucky (talented?) winner! {FLAGS[2]}')
            exit()
        else:
            print('[!] Submission are closed... Thanks for playing!')
            exit()

    
    # Check what step the team is
    step = check_current_step(ctfd_token)
    if step == None:
        print('[-] Error: could not retrieve current advancement.')
    if step == 2:
        print('[+] You flagged everything, congratz!')
        exit()
    current_challenge = CHALLENGES[step]
    print(f'[*] You are currently in the "{current_challenge}" arena.')


    # Ask for base64 Python code
    print("[?] Enter your base64-encoded Python code: ", flush=True, end="")
    base64_code = ""
    buffer = input()
    while buffer != "EOF":
        base64_code += buffer
        buffer = input()

    print()
    decoded_code = None
    try:
        # Decode the base64 code
        decoded_code = base64.b64decode(base64_code).decode('utf-8')
    except Exception as e:
        print(f"[-] Error while decoding your base64: {e}")
        return
    

    # Ask if this is a test submission
    is_test_raw = input('[?] Would you like to submit this as a test ? In this case only one reviewable game will be ran. (Y/n) ').lower().strip()
    is_test = None
    if is_test_raw in ["y", ""]:
        is_test = True
    elif is_test_raw == "n":
        is_test = False
    else:
        print('[-] Error: invalid choice')


    # Run game
    print(f'[*] Running game in "{current_challenge}" arena', flush=True)
    if is_test:
        players = None
        try:
            result, players, size = run_single_game(team_id, decoded_code, step)
        except Exception as e:
            print(f"[!] An error occured during the game.")
            exit()
        
        won = check_if_won(players)
        if won == 1:
            print('[*] Congratz, you won!')
        elif won == 0:
            print('[*] Sorry, you have to do better than this...')
        elif won == -1:
            print("[*] It's a tie!")

        # Generate endpoint
        endpoint_name = generate_random_endpoint()
        create_random_endpoint(endpoint_name, result, decoded_code, size)
    else:
        try:
            looses = run_multiple_games(team_id, decoded_code, step, 15)
            if looses <= 3:
                print(f"[+] Congratz ! Here is your flag for {current_challenge}: {FLAGS[step]}")
            else:
                print(f'[*] Sorry you failed {looses}/15 games.')
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()