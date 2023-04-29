# os is needed for clearing the screen dependant on the operating system
import os
# time is needed to keep start and quit screen for some time
import time
# random is needed to set the monster randomly
import random




# game relevant constants
STATES = {
    'startup': '',
    'running': 1,
    'shutdown': 2,
}

SUCCESS = {
    'win': 0,
    'lose': 1,
    'neither': 2,
}

SCENES = {
    'start_scene': 0,
    'game_scene': 1,
    'quit_scene': 2,
    'win_scene': 3,
    'lose_scene': 4,
}

ACTIONS = {
    'go': 'go',
    'get': 'get',
    'quit': 'quit',
}

MAP = {
    'Hall': {
        'display_name': 'Hall',
        'north': 'Garden',
        'east': 'Dining Room',
        'south': 'Kitchen',
        'west': 'Library',
        'items': ['Key'],
        'monster': False,
    },
    'Dining Room': {
        'display_name': 'Dining Room',
        'west': 'Hall',
        'items': ['Potion'],
        'monster': False,
    },
    'Kitchen': {
        'display_name': 'Kitchen',
        'north': 'Hall',
        'west': 'Laboratory',
        'items': [],
        'monster': False,
    },
    'Laboratory': {
        'display_name': 'Laboratory',
        'north': 'Library',
        'east': 'Kitchen',
        'items': ['BeamOMat'],
        'monster': False,
    },
    'Library': {
        'display_name': 'Library',
        'north': 'Office',
        'east': 'Hall',
        'south': 'Laboratory',
        'items': ['BookOfLife'],
        'monster': False,
    },
    'Office': {
        'display_name': 'Office',
        'south': 'Library',
        'items': [],
        'monster': False,
    },
    'Garden': {
        'display_name': 'Garden',
        'directions': ['north', 'east', 'south', 'west'],
        'south': 'Hall',
        'items': [],
        'monster': False,
    },
}




# states
app_state = {
    'current_state': '',
    'current_scene': '',
    'info': '',
    'action': '',
    'target': '',
}

game_state = {
    'success_state': '',
    'current_room': '',
    'inventory': '',
    'current_room': '',
}




# function to get and validate input
def get_input(state, scene):
    user_input = ''

    if state == STATES['running'] and scene == SCENES['game_scene']:
        user_input = input('    > ')

    if user_input != '':
        app_state['action'] = user_input.lower().split(' ')[0]
        if len(user_input.split()) > 1:
            app_state['target'] = user_input.split(' ')[1]




# functions to update states according to input and game logic
def init_app_state():
    app_state['current_state'] = STATES['running']
    app_state['current_scene'] = SCENES['start_scene']
    app_state['info'] = ''
    app_state['action'] = ''
    app_state['target'] = ''

def init_game_state():
    game_state['success_state'] = SUCCESS['neither']
    game_state['current_room'] = MAP['Hall']['display_name']
    game_state['inventory'] = []

    i = random.randint(0, 1)
    if i == 0:
        MAP['Office']['monster'] = True
    if i == 1:
        MAP['Kitchen']['monster'] = True

def move(direction):
    current_room = game_state['current_room']

    if direction in MAP[current_room]:
        game_state['current_room'] = MAP[current_room][direction]

def get_item(item):
    current_room = MAP[game_state['current_room']]

    if item in current_room['items']:
        game_state['inventory'].append(item)
        current_room['items'].remove(item)

def shutdown():
    app_state['current_scene'] = SCENES['quit_scene']
    app_state['current_state'] = STATES['shutdown']

def determine_success():
    if 'Key' in game_state['inventory'] and 'Potion' in game_state['inventory'] and game_state['current_room'] == MAP['Garden']['display_name']:
        game_state['success_state'] = SUCCESS['win']
    if MAP[game_state['current_room']]['monster']:
        game_state['success_state'] = SUCCESS['lose']

def update_state(state, action, target):
    if state == STATES['startup']:
        init_app_state()
        init_game_state()

    if state == STATES['running']:
        app_state['current_scene'] = SCENES['game_scene']

        if action == ACTIONS['go']: move(target)
        elif action == ACTIONS['get']: get_item(target)
        elif action == ACTIONS['quit']: shutdown()

        determine_success()

        if game_state['success_state'] == SUCCESS['win']:
            app_state['current_scene'] = SCENES['win_scene']
            app_state['current_state'] = STATES['shutdown']
        
        if game_state['success_state'] == SUCCESS['lose']:
            app_state['current_scene'] = SCENES['lose_scene']
            app_state['current_state'] = STATES['shutdown']




# functions to render screens according to current_scene in app_state
def clear_screen_wait():
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')

def startup_scene():
    print('\n\n    Welcome!')

def game_scene():
    # print information
    print('''

                            SNOWMANSION
    ============================================================

    You are in an abandoned mansion. You have to find the potion
    they told you about. When you entered the yard the gate
    slammed shut so you have to find a key to open it.
    ''')

    # print status
    print('    You are in the', game_state['current_room'])
    if len(MAP[game_state['current_room']]['items']) > 0:
        print('    You see', ', '.join(MAP[game_state['current_room']]['items']))
    if game_state['inventory']:
        print('    You have:', ', '.join(game_state['inventory']))
    else:
        print()
    print('\n    ------------------------------------------------------------')

    # print controls
    print('''
    Controls:
    - go [direction] ............... move to specified direction
    - get [item] .......................... take an item you see
    - quit ...................................... leave the game
    ''')
    print('    ------------------------------------------------------------\n')

    # print additional information
    if app_state['info'] != '':
        print(app_state['info'])
    else:
        print()

def quit_scene():
    print('\n\n    Goodbye!')

def win_scene():
    print('\n\n    You win!')

def lose_scene():
    print('\n\n    The monster got you!')
    print('    You lose!')

def render_scene(scene):
    os.system('cls' if os.name == 'nt' else 'clear')

    if scene == SCENES['start_scene']: startup_scene()

    if scene == SCENES['game_scene']: game_scene()

    if scene == SCENES['quit_scene']: quit_scene()

    if scene == SCENES['win_scene']: win_scene()

    if scene == SCENES['lose_scene']: lose_scene()

    if scene != SCENES['game_scene']: clear_screen_wait()




# main event loop
while app_state['current_state'] != STATES['shutdown']:
    # get input from the player
    get_input(app_state['current_state'], app_state['current_scene'])
    # update state according to input and game logic
    update_state(app_state['current_state'], app_state['action'], app_state['target'])
    # render user interface
    render_scene(app_state['current_scene'])
