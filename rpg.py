
import os # necessary to use when clearing the screen
import random # necessary to set the monster in a random room
import time


inventory = []
rooms = {
  'Hall': {
    'north': 'Garden',
    'east': 'Dining Room',
    'south': 'Kitchen',
    'west': 'Library',
    'item': 'Key'
  },
  'Dining Room': {
    'west': 'Hall',
    'item': 'Potion',
  },
  'Kitchen': {
    'north': 'Hall',
    'west': 'Laboratory'
  },
  'Laboratory': {
    'north': 'Library',
    'east': 'Kitchen',
    'item': 'BeamOMat'
  },
  'Library': {
    'north': 'Office',
    'east': 'Hall',
    'south': 'Laboratory',
    'item': 'BookOfLife'
  },
  'Office': {
    'south': 'Library',
  },
  'Garden': {
    'south': 'Hall'
  },
}
currentRoom = 'Hall'


def set_monster():
  i = random.randint(0, 1)
  if i == 0:
    rooms['Office']['item'] = 'monster'
  if i == 1:
    rooms['Kitchen']['item'] = 'monster'

def show_instructions():

  print('''
Welcome to your own RPG Game
============================

Get to the Garden with a key and a potion.
Avoid the monsters!
Maybe you even find... Well just forget that...

Commands:
  go [north, east, south, west]
  get [item]
  exit [leave game]
''')

def show_status():
  print('---------------------------')
  print('You are in the ' + currentRoom)
  print('Inventory : ' + str(inventory))
  if "item" in rooms[currentRoom]:
    print('You see a ' + rooms[currentRoom]['item'])
  print('---------------------------')

# check all possible endings to determine when to leave game loop
def win_or_lose():
  if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item']:
    print('A monster got you... GAME OVER!')
    return 'exit'

  if currentRoom == 'Garden' and 'Key' in inventory and 'Potion' in inventory:
    print('You escaped the house... YOU WIN!')
    return 'exit'
  
  if currentRoom == 'Laboratory' and 'BookOfLife' in inventory and 'BeamOMat' in inventory:
    print('You escaped the house... YOU WIN!')
    return 'exit'


set_monster()
while True:
  os.system('cls' if os.name == 'nt' else 'clear')
  show_instructions()
  show_status()

  event = ''
  while event == '':
    event = input('> ')
  
  # format input for easy input handling
  if ' ' in event:
    action = event.split(' ')[0].lower()
    subject = event.split(' ')[1]
  else:
    action = event.lower()
    

  if action == 'exit':
    break

  if action == 'go':
    if subject in rooms[currentRoom]:
      currentRoom = rooms[currentRoom][subject]
    else:
      print('You can\'t go that way!')
  
  if action == 'get':
    if 'item' in rooms[currentRoom] and subject in rooms[currentRoom]['item']:
      inventory += [subject]
      print(subject + ' got!')
      del rooms[currentRoom]['item']
      time.sleep(1)
    else:
      print('Can\'t get ' + subject + '!')
      time.sleep(1)
  
  if win_or_lose() == 'exit':
    break

os.system('cls' if os.name == 'nt' else 'clear')
