import os
import time
import scenes

inventory = ['Key', 'Potion', 'Book']

os.system('cls')

print(scenes.startup.format(current_room='Hall', inventory=', '.join(inventory)))