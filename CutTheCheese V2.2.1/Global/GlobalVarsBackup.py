import random
import AUDIO.musicVars as musVars

totalCheeseCount = 3
cheeseTotal = 0
gameEnd = False
selectedMus = musVars.musCredits

resistance = 0
Health, maxHealth, inventoryLen, cheeseTolerance = 100, 100, 10, 0
gameEnd, expansions, returning, stored = False, False, False, False
equipped, ending, sendToRoom, wearing = '', '', '', ''

addons = [{'Expansions' : {}}, {'Extensions' : {}}]
itemCopies = {}
loadedExpansions = {}
darkRooms = ['CAVES', 'CAVERNS', 'BASEMENT', 'TUNNELS']
craftables = {'Sandwich' : ['Ham', 'Cheese', 'Bread'], 'Slipper' : ['Belt', 'Cannon', 'Stick'], 'Apple Juice' : ['Apple', 'Water Bottle']}
dropables = [{'Storage' : 'Sack', 'Loot' : ['Cheese']}, {'Storage' : 'Box', 'Loot' : []}]
enemies = {'Demon' : {'Health' : 0, 'Room' : '', 'Exists' : False, 'Location' : '', 'Damage' : 10, 'Restrictions' : ['VEHICLE'], 'Defeated' : False, 'Ending' : 'Demon Slayer', 'HRange' : [100, 110, 120, 130, 140, 150], 'Drop' : ''}}

itemProperties = [{'Item' : 'Sack', 'Type' : 'Container', 'Slots' : 3, 'Count' : -1, 'Description' : 'A small bundle of leather shaped like a pouch, particularly useful for carrying a few items.'},
                  {'Item' : 'Sword', 'Type' : 'Weapon', 'Damage' : 30, 'Count' : -1, 'Cutting' : True, 'Description' : 'A peice of steel, molded into the perfect shape resembling that of a longsword. It is clean enough to see your own reflection.'},
                  {'Item' : 'Revolver', 'Type' : 'Weapon', 'Damage' : 30, 'Count' : 6, 'Description' : 'A six-round barrel revolver, capable of dealing moderate damage from a distance. Best used against a moderately powerful enemy.'},
                  {'Item' : 'Slingshot', 'Type' : 'Weapon', 'Damage' : 20, 'Count' : 10, 'Description' : 'A Y-shaped piece of wood, wrapped with a strand of rubber across the gap. Not very powerful, but it can still hurt if used correctly.'},
                  {'Item' : 'Belt', 'Type' : 'Weapon', 'Damage' : 100, 'Count' : -1, 'Description' : 'Father\'s leather belt, a sleek streamlined peice of leather with a sturdy metal buckle. Can be used to strike down foes in a single blow.'},
                  {'Item' : 'Cheese', 'Type' : 'Food', 'Health' : random.randint(0,10)*10, 'Cut' : False, 'Count' : 1, 'Description' : 'A small wedge of swiss cheese, it smells slightly of mold but otherwise looks edible.'},
                  {'Item' : 'Apple', 'Type' : 'Food', 'Health' : 30, 'Cut' : False, 'Count' : 1, 'Description' : 'A fresh granny smith apple, full of vibrant green colour and a crisp texture. If you\'re lucky you might be able to turn it into cider...'},
                  {'Item' : 'Water Bottle', 'Type' : 'Beverage', 'Health' : 10, 'Count' : 1, 'Description' : 'A piece of plastic shaped in a roughly cylindrical shape filled with clean drinking water. Enough to quench both thirst and hunger for a short while.'},
                  {'Item' : 'Ham', 'Type' : 'Food', 'Health' : 15, 'Cut' : False, 'Count' : 1, 'Description' : 'A slice of cured ham, slightly salty but otherwise edible. Could be used to make a sandwich if you had the right ingredients.'},
                  {'Item' : 'Bread', 'Type' : 'Food', 'Health' : 5, 'Cut' : False, 'Count' : 1, 'Description' : 'A slice of white bread, soft and fluffy. Could be used to make a sandwich if you had the right ingredients.'},
                  {'Item' : 'Sandwich', 'Type' : 'Food', 'Health' : 40, 'Cut' : False, 'Count' : 1, 'Description' : 'A delicious ham and cheese sandwich, stacked high with layers of ham, cheese, and bread. Perfect for a quick meal on the go, all while being plenty nutricious.'},
                  {'Item' : 'Potion', 'Type' : 'Effect', 'Effect' : random.choice(['Teleport', 'Strength']), 'Count' : 1, 'Description' : 'A small vial filled with a glowing liquid. Drinking it will grant you a random effect, but be careful... you never know what might happen...'},
                  {'Item' : 'Box', 'Type' : 'Container', 'Slots' : 3, 'Count' : -1, 'Description' : 'A small cardboard box, capable of holding a few items inside. Not very secure, but better than nothing.'},
                  {'Item' : 'Soul Orb', 'Type' : 'Spawner', 'Spawn' : 'Demon', 'Count' : 1, 'Description' : 'A dark orb pulsating with an eerie purple light. It seems to contain a malevolent presence within, capable of summoning a powerful demon when activated.'},
                  {'Item' : 'Recipe', 'Type' : 'Instructions', 'Instructions' : 'Step 1: Cut Cheese\nStep 2: Cut Ham\nStep 3: Cut Bread\nStep 4: Type "craft" in the options menu\nStep 5: Type the item you want to craft and hit ENTER', 'Count' : -1, 'Description' : 'A worn piece of parchment containing instructions on how to craft various items. It seems to be quite old, but the information is still legible.'},
                  {'Item' : 'Cannon', 'Type' : 'Weapon', 'Damage' : 70, 'Count' : 1, 'Description' : 'A small handheld cannon, capable of firing powerful blasts of energy. It looks quite dangerous, so be careful when using it.'},
                  {'Item' : 'Stick', 'Type' : 'Weapon', 'Damage' : 10, 'Count' : -1, 'Description' : 'A sturdy wooden stick, roughly the size of a baseball bat. Not very powerful, but it can still be used to strike down foes.'},
                  {'Item' : 'Slipper', 'Type' : 'Weapon', 'Damage' : 200, 'Count' : 10, 'Description' : 'The fabled slipper, the killer of all behinds. Be weary of the individual who possesses this item. Not to be taken lightly.'},
                  {'Item' : 'Apple Juice', 'Type' : 'Beverage', 'Health' : 30, 'Count' : 1, 'Description' : 'A refreshing bottle of apple cider, perfect for quenching your thirst and satisfying your hunger. Made from fresh apples and a hint of cinnamon, it\'s sure to delight your taste buds.'}]
rooms = [{'Location': 'OUTSIDE', 'Description': 'You stand in a quiet yard, the air crisp and fresh. The mailbox creaks gently in the breeze, leaves rustle softly beneath your feet, and distant birdsong fills the morning. The cracked pathway leads your eyes toward the old house, promising stories waiting inside.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', '7': '7 = load menu', '8': '8 = help'},
        {'Location': 'CORRIDOR', 'Description': 'A dimly lit corridor stretches ahead, its scuffed wooden floor whispering secrets of countless footsteps. Doors to other rooms flank each side, some slightly ajar, revealing glimpses of shadowed interiors. The faint smell of aged wood mingles with dust in the air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'KITCHEN', 'Description': 'The kitchen is cluttered and cozy, filled with forgotten utensils hanging on rusty hooks and mismatched plates stacked high. The fridge hums steadily in the corner, its glow casting eerie shadows over cracked countertops. The scent of stale coffee lingers faintly.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'BEDROOM', 'Description': 'This small bedroom feels lived-in yet neglected. An unmade bed lies crumpled under a thin blanket, and dusty shelves crowd the walls, housing trinkets and old books. A narrow window lets in pale light, illuminating floating dust motes dancing in the air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'UPSTAIRS', 'Description': 'The upstairs landing creaks with every step you take. The air is thick with a mix of old wallpaper scents and faint drafts slipping through cracked windows. Doors open into rooms filled with memories and forgotten tales.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'ATTIC', 'Description': 'Low ceilings and thick cobwebs create a feeling of timeless abandonment. The dusty attic holds forgotten relics — old trunks, faded photographs, and brittle letters. The air is stale but charged with a hint of mystery, as if memories cling stubbornly here.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'BASEMENT', 'Description': 'Dim and damp, the basement holds a chilling silence and old storage. Shadows dance against the cracked walls, and the scent of mildew mingles with the faint echo of dripping water. It feels like a place where secrets hide in the dark.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'GARAGE', 'Description': 'A clean garage with tools neatly arranged and a vehicle sitting in the center of the room. The scent of oil and rubber fills the air, and sunlight filters through the dusty windows, illuminating the workbench scattered with half-finished projects.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'BATHROOM', 'Description': 'A sterile bathroom with a flickering light and a cracked mirror. The faint drip of a leaky faucet echoes softly, while the chipped tiles and worn linoleum floor tell tales of long days and forgotten nights.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'LOUNGE', 'Description': 'A cozy lounge with worn-out furniture and a dusty television. Faded photographs hang crookedly on the walls, and the faint smell of old books and pipe tobacco lingers in the air, inviting quiet reflection.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'DINING ROOM', 'Description': 'A long table dominates the room, set for a meal that never came. Dust-covered plates and tarnished cutlery hint at celebrations frozen in time, while a chandelier overhead flickers weakly, casting dancing shadows.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'TUNNELS', 'Description': 'A narrow TUNNELS, carved roughly through the rock, leads to darker places. The air grows colder and thicker with each step, and the sound of distant dripping water echoes off the uneven walls, hinting at mysteries hidden deeper underground.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'ROOF', 'Description': 'A precarious perch with a sweeping view, the wind whispers secrets as it swirls around you. The sky stretches wide and endless above, dotted with stars even in daylight, while the city hums far below, muffled and distant.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'FOREST', 'Description': 'Tall trees surround you, their branches knitting a thick canopy overhead. The undergrowth is dense with secrets and sounds — rustling leaves, distant animal calls, and the steady pulse of nature alive and watching.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'CAMPSITE', 'Description': 'A quiet clearing with a worn tent and signs of a long-abandoned fire. Scattered ashes and broken logs hint at stories shared beneath the stars, while the scent of pine and earth fills the cool night air.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'CAVES', 'Description': 'Natural caves extend into the darkness, the air cool and still. Stalactites hang like silent sentinels from the ceiling, and the faint sound of dripping water echoes through vast, shadowed chambers.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'},
        {'Location': 'CAVERNS', 'Description': 'A vast underground space with echoes that never seem to fade. The cavern walls glisten faintly with moisture, and the distant rumble of shifting earth reminds you that this place is alive, ancient, and full of untold secrets.', '0': '0 = wait', '1': '1 = enter room', '2': '2 = open storage', '3': '3 = use item', '4': '4 = equip item', '5': '5 = store item', '6': '6 = drop item', 'menu': '7 = load menu', '8': '8 = help'}]
roomAttributes = [{'Location' : 'OUTSIDE', 'Doors' : ['KITCHEN', 'CORRIDOR', 'GARAGE', 'FOREST'], 'Storage' : ['MAILBOX']},
                {'Location' : 'CORRIDOR', 'Doors' : ['KITCHEN', 'BATHROOM', 'UPSTAIRS', 'OUTSIDE', 'BASEMENT'], 'Storage' : ['CABINET']},
                {'Location' : 'KITCHEN', 'Doors' : ['CORRIDOR', 'DINING ROOM', 'ATTIC', 'OUTSIDE'], 'Storage' : ['CABINET','FRIDGE']},
                {'Location' : 'ATTIC', 'Doors' : ['KITCHEN', 'UPSTAIRS', 'ROOF'], 'Storage' : ['CHEST', 'CABINET']},
                {'Location' : 'BASEMENT', 'Doors' : ['CORRIDOR', 'TUNNELS'], 'Storage' : ['FRIDGE', 'CHEST']},
                {'Location' : 'TUNNELS', 'Doors' : ['BASEMENT', 'CAVES'], 'Storage' : ['DECORATED CHEST']},
                {'Location' : 'ROOF', 'Doors' : ['ATTIC'], 'Storage' : []},
                {'Location' : 'UPSTAIRS', 'Doors' : ['ATTIC', 'CORRIDOR', 'LOUNGE', 'BEDROOM'], 'Storage' : ['CABINET', 'CHEST']},
                {'Location' : 'GARAGE', 'Doors' : ['OUTSIDE', 'VEHICLE'], 'Storage' : ['CHEST']},
                {'Location' : 'BEDROOM', 'Doors' : ['UPSTAIRS'], 'Storage' : ['CABINET', 'CHEST']},
                {'Location' : 'DINING ROOM', 'Doors' : ['KITCHEN', 'BATHROOM'], 'Storage' : ['CHEST']},
                {'Location' : 'BATHROOM', 'Doors' : ['DINING ROOM', 'CORRIDOR'], 'Storage' : []},
                {'Location' : 'LOUNGE', 'Doors' : ['UPSTAIRS'], 'Storage' : ['CABINET']},
                {'Location' : 'FOREST', 'Doors' : ['OUTSIDE', 'CAMPSITE', 'CAVES'], 'Storage' : []},
                {'Location' : 'CAMPSITE', 'Doors' : ['FOREST'], 'Storage' : ['TENT']},
                {'Location' : 'CAVES', 'Doors' : ['FOREST', 'CAVERNS', 'TUNNELS'], 'Storage' : []},
                {'Location' : 'CAVERNS', 'Doors' : ['CAVES'], 'Storage' : ['WAR CHEST']}]
lootBoxes = [{'Storage' : 'DECORATED CHEST', 'Loot' : ['Soul Orb']},
            {'Storage' : 'CHEST', 'Loot' : ['Sword', 'Potion', 'Sack', 'Revolver', 'Key', 'Belt']},
            {'Storage' : 'MAILBOX', 'Loot' : ['Box']},
            {'Storage' : 'FRIDGE', 'Loot' : ['Cheese', 'Apple']},
            {'Storage' : 'CABINET', 'Loot' : ['Cheese', 'Slingshot', 'Water Bottle', 'Ham', 'Bread', 'Recipe']},
            {'Storage' : 'WAR CHEST', 'Loot' : ['Cannon']},
            {'Storage' : 'TENT', 'Loot' : ['Stick']}]

inventory, addonLocations = {}, ['HOUSE']
room = 'OUTSIDE'
expansionLoc = 'HOUSE'

tutorialMode = True
failed = False
